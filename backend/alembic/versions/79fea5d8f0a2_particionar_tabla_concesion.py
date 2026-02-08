"""particionar_tabla_concesion

Revision ID: 79fea5d8f0a2
Revises: fc5db4ea92bd
Create Date: 2026-02-08 11:28:53.411007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79fea5d8f0a2'
down_revision: Union[str, None] = 'fc5db4ea92bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Convierte la tabla concesion en particionada jerárquica (RANGE + LIST).

    PARTICIONADO JERÁRQUICO:
    ========================
    Nivel 1: RANGE por fecha_concesion (anual: 2015, 2016, 2017, ...)
    Nivel 2: LIST por regimen_tipo ('minimis', 'ayuda_estado', 'ordinaria', etc.)

    Beneficios:
    - Partition pruning en dos dimensiones (año + régimen)
    - Queries como "minimis de 2024" escanean solo 1 subpartición
    - Permite borrar/analizar por ejercicio y régimen

    IMPORTANTE: Esta migración asume que la tabla está vacía.
    """

    # 1. Dropar tabla concesion existente (y sus FKs)
    op.drop_table('concesion')

    # 2. Crear tabla concesion particionada (Nivel 1: RANGE por fecha)
    # NOTA: regimen_tipo es campo denormalizado para permitir LIST partitioning
    # PK compuesto: (id, fecha_concesion, regimen_tipo) para soportar ambos niveles
    op.execute("""
        CREATE TABLE concesion (
            id UUID DEFAULT uuid_generate_v7(),
            beneficiario_id UUID NOT NULL,
            convocatoria_id UUID NOT NULL,
            fecha_concesion DATE NOT NULL,
            id_concesion VARCHAR NOT NULL,
            importe_equivalente DOUBLE PRECISION,
            importe_nominal DOUBLE PRECISION,
            regimen_ayuda_id UUID,
            regimen_tipo VARCHAR(20) NOT NULL DEFAULT 'desconocido',
            created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
            created_by VARCHAR(50),
            updated_at TIMESTAMP WITHOUT TIME ZONE,
            updated_by VARCHAR(50),
            PRIMARY KEY (id, fecha_concesion, regimen_tipo),
            UNIQUE (id_concesion, fecha_concesion, regimen_tipo)
        ) PARTITION BY RANGE (fecha_concesion);
    """)

    # 3. Crear índices globales
    op.create_index('ix_concesion_id_concesion', 'concesion', ['id_concesion', 'fecha_concesion'])
    op.create_index('ix_concesion_regimen_fecha', 'concesion', ['regimen_tipo', 'fecha_concesion'])
    op.create_index('ix_concesion_created_at', 'concesion', ['created_at'])

    # 4. Crear particiones jerárquicas por año (2015-2026)
    # Cada partición anual se subparticiona por regimen_tipo (LIST)
    for year in range(2015, 2027):
        partition_name = f'concesion_{year}'
        start_date = f'{year}-01-01'
        end_date = f'{year + 1}-01-01'

        # Nivel 1: Partición anual (RANGE)
        # Esta partición NO almacena datos, solo enruta a las subparticiones
        op.execute(f"""
            CREATE TABLE {partition_name} PARTITION OF concesion
            FOR VALUES FROM ('{start_date}') TO ('{end_date}')
            PARTITION BY LIST (regimen_tipo);
        """)

        # Nivel 2: Subparticiones por régimen (LIST)
        # Estas SÍ almacenan datos

        # Subpartición: De minimis
        op.execute(f"""
            CREATE TABLE {partition_name}_minimis
            PARTITION OF {partition_name}
            FOR VALUES IN ('minimis');
        """)

        # Subpartición: Ayuda de estado (RGEC)
        op.execute(f"""
            CREATE TABLE {partition_name}_ayuda_estado
            PARTITION OF {partition_name}
            FOR VALUES IN ('ayuda_estado');
        """)

        # Subpartición: Ordinaria (no ayuda de estado)
        op.execute(f"""
            CREATE TABLE {partition_name}_ordinaria
            PARTITION OF {partition_name}
            FOR VALUES IN ('ordinaria');
        """)

        # Subpartición: Notificada
        op.execute(f"""
            CREATE TABLE {partition_name}_notificada
            PARTITION OF {partition_name}
            FOR VALUES IN ('notificada');
        """)

        # Subpartición: DEFAULT (captura valores no especificados)
        op.execute(f"""
            CREATE TABLE {partition_name}_otros
            PARTITION OF {partition_name}
            DEFAULT;
        """)

        # Índices locales en cada subpartición (para queries sin regimen_tipo)
        for subpartition in ['minimis', 'ayuda_estado', 'ordinaria', 'notificada', 'otros']:
            op.execute(f"""
                CREATE INDEX ix_{partition_name}_{subpartition}_regimen_ayuda
                ON {partition_name}_{subpartition} (regimen_ayuda_id);
            """)

    # 5. Crear FKs
    op.execute("""
        ALTER TABLE concesion
        ADD CONSTRAINT fk_concesion_beneficiario
        FOREIGN KEY (beneficiario_id) REFERENCES beneficiario(id);
    """)

    op.execute("""
        ALTER TABLE concesion
        ADD CONSTRAINT fk_concesion_convocatoria
        FOREIGN KEY (convocatoria_id) REFERENCES convocatoria(id);
    """)

    op.execute("""
        ALTER TABLE concesion
        ADD CONSTRAINT fk_concesion_regimen_ayuda
        FOREIGN KEY (regimen_ayuda_id) REFERENCES regimen_ayuda(id);
    """)


def downgrade() -> None:
    """Revierte el particionamiento convirtiendo concesion en tabla normal."""

    # 1. Crear tabla temporal con datos
    op.execute("CREATE TABLE concesion_temp AS SELECT * FROM concesion;")

    # 2. Dropar tabla particionada
    op.drop_table('concesion')

    # 3. Recrear tabla normal (sin regimen_tipo)
    op.create_table(
        'concesion',
        sa.Column('id', sa.Uuid(), nullable=False, server_default=sa.text('uuid_generate_v7()')),
        sa.Column('beneficiario_id', sa.Uuid(), nullable=False),
        sa.Column('convocatoria_id', sa.Uuid(), nullable=False),
        sa.Column('fecha_concesion', sa.Date(), nullable=False),
        sa.Column('id_concesion', sa.String(), nullable=False),
        sa.Column('importe_equivalente', sa.Float(), nullable=True),
        sa.Column('importe_nominal', sa.Float(), nullable=True),
        sa.Column('regimen_ayuda_id', sa.Uuid(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('created_by', sa.String(50), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('updated_by', sa.String(50), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # 4. Restaurar datos (sin regimen_tipo)
    op.execute("""
        INSERT INTO concesion
        (id, beneficiario_id, convocatoria_id, fecha_concesion, id_concesion,
         importe_equivalente, importe_nominal, regimen_ayuda_id,
         created_at, created_by, updated_at, updated_by)
        SELECT id, beneficiario_id, convocatoria_id, fecha_concesion, id_concesion,
               importe_equivalente, importe_nominal, regimen_ayuda_id,
               created_at, created_by, updated_at, updated_by
        FROM concesion_temp;
    """)
    op.drop_table('concesion_temp')

    # 5. Recrear constraints
    op.create_unique_constraint('uq_concesion_id_fecha', 'concesion', ['id_concesion', 'fecha_concesion'])
    op.create_index('ix_concesion_id_concesion', 'concesion', ['id_concesion'])
    op.create_index('ix_concesion_regimen_fecha', 'concesion', ['regimen_ayuda_id', 'fecha_concesion'])
    op.create_index('ix_concesion_created_at', 'concesion', ['created_at'])

    # 6. Recrear FKs
    op.create_foreign_key('fk_concesion_beneficiario', 'concesion', 'beneficiario', ['beneficiario_id'], ['id'])
    op.create_foreign_key('fk_concesion_convocatoria', 'concesion', 'convocatoria', ['convocatoria_id'], ['id'])
    op.create_foreign_key('fk_concesion_regimen_ayuda', 'concesion', 'regimen_ayuda', ['regimen_ayuda_id'], ['id'])
