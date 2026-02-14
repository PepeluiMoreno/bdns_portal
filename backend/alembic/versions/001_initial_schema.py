"""initial_schema

Revision ID: 001_initial
Revises: None
Create Date: 2026-02-10 14:30:00

Migración inicial del schema bdns (datos del dominio):
- Extensiones PostgreSQL (uuid-ossp, pg_trgm, unaccent, postgis)
- Schema 'bdns'
- Todas las tablas del dominio (convocatorias, concesiones, beneficiarios, catálogos)
- Tabla de usuarios (autenticación compartida)
- Índices y constraints

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Creación inicial completa."""

    # ============================================================
    # 1. HABILITAR EXTENSIONES
    # ============================================================

    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
    op.execute("CREATE EXTENSION IF NOT EXISTS \"pg_trgm\"")
    op.execute("CREATE EXTENSION IF NOT EXISTS \"unaccent\"")
    # op.execute("CREATE EXTENSION IF NOT EXISTS \"postgis\"")  # No necesario para este proyecto

    # ============================================================
    # 2. SCHEMA BDNS (ya creado por init_db.sh)
    # ============================================================

    # El esquema ya fue creado por init_db.sh antes de ejecutar migraciones
    op.execute("COMMENT ON SCHEMA bdns IS 'Datos del dominio BDNS: convocatorias, concesiones, beneficiarios y catálogos'")

    # ============================================================
    # 3. TABLAS DE CATÁLOGOS (schema bdns)
    # ============================================================

    # Finalidad
    op.create_table(
        'finalidad',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('api_id', sa.Integer(), nullable=True),
        sa.Column('descripcion', sa.String(), nullable=True),
        sa.Column('descripcion_norm', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='bdns'
    )
    op.create_index('ix_finalidad_api_id', 'finalidad', ['api_id'], unique=True, schema='bdns')

    # Fondo
    op.create_table(
        'fondo',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('api_id', sa.Integer(), nullable=True),
        sa.Column('descripcion', sa.String(), nullable=True),
        sa.Column('descripcion_norm', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='bdns'
    )
    op.create_index('ix_fondo_api_id', 'fondo', ['api_id'], unique=True, schema='bdns')

    # Instrumento
    op.create_table(
        'instrumento',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('api_id', sa.Integer(), nullable=True),
        sa.Column('descripcion', sa.String(), nullable=True),
        sa.Column('descripcion_norm', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='bdns'
    )
    op.create_index('ix_instrumento_api_id', 'instrumento', ['api_id'], unique=True, schema='bdns')

    # Objetivo
    op.create_table(
        'objetivo',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('api_id', sa.Integer(), nullable=True),
        sa.Column('descripcion', sa.String(), nullable=True),
        sa.Column('descripcion_norm', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='bdns'
    )
    op.create_index('ix_objetivo_api_id', 'objetivo', ['api_id'], unique=True, schema='bdns')

    # Órgano (jerárquico)
    op.create_table(
        'organo',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('codigo', sa.String(), nullable=False),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('tipo', sa.String(), nullable=False),
        sa.Column('id_padre', sa.Uuid(), nullable=True),
        sa.Column('nivel1', sa.String(), nullable=True),
        sa.Column('nivel2', sa.String(), nullable=True),
        sa.Column('nivel3', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['id_padre'], ['bdns.organo.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('codigo'),
        schema='bdns'
    )
    op.create_index('ix_organo_tipo', 'organo', ['tipo'], unique=False, schema='bdns')
    op.create_index('ix_organo_id_padre', 'organo', ['id_padre'], unique=False, schema='bdns')

    # Programa
    op.create_table(
        'programa',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('api_id', sa.Integer(), nullable=True),
        sa.Column('descripcion', sa.String(), nullable=True),
        sa.Column('descripcion_norm', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='bdns'
    )
    op.create_index('ix_programa_api_id', 'programa', ['api_id'], unique=True, schema='bdns')

    # Régimen de Ayuda
    op.create_table(
        'regimen_ayuda',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('api_id', sa.Integer(), nullable=True),
        sa.Column('descripcion', sa.String(), nullable=True),
        sa.Column('descripcion_norm', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='bdns'
    )
    op.create_index('ix_regimen_ayuda_api_id', 'regimen_ayuda', ['api_id'], unique=True, schema='bdns')

    # Sector
    op.create_table(
        'sector',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('api_id', sa.Integer(), nullable=True),
        sa.Column('descripcion', sa.String(), nullable=True),
        sa.Column('descripcion_norm', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='bdns'
    )
    op.create_index('ix_sector_api_id', 'sector', ['api_id'], unique=True, schema='bdns')

    # Tipo de Beneficiario
    op.create_table(
        'tipo_beneficiario',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('api_id', sa.Integer(), nullable=True),
        sa.Column('descripcion', sa.String(), nullable=True),
        sa.Column('descripcion_norm', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='bdns'
    )
    op.create_index('ix_tipo_beneficiario_api_id', 'tipo_beneficiario', ['api_id'], unique=True, schema='bdns')

    # Forma Jurídica
    op.create_table(
        'forma_juridica',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('api_id', sa.Integer(), nullable=True),
        sa.Column('descripcion', sa.String(), nullable=True),
        sa.Column('descripcion_norm', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='bdns'
    )
    op.create_index('ix_forma_juridica_api_id', 'forma_juridica', ['api_id'], unique=True, schema='bdns')

    # ============================================================
    # 4. TABLA CONVOCATORIA (schema public)
    # ============================================================

    op.create_table(
        'convocatoria',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('id_bdns', sa.String(), nullable=False),
        sa.Column('titulo', sa.String(), nullable=True),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('fecha_publicacion', sa.Date(), nullable=True),
        sa.Column('fecha_inicio', sa.Date(), nullable=True),
        sa.Column('fecha_fin', sa.Date(), nullable=True),
        sa.Column('importe_total', sa.Float(), nullable=True),
        sa.Column('url_convocatoria', sa.String(), nullable=True),
        sa.Column('organo_id', sa.Uuid(), nullable=True),
        sa.Column('finalidad_id', sa.Uuid(), nullable=True),
        sa.Column('fondo_id', sa.Uuid(), nullable=True),
        sa.Column('instrumento_id', sa.Uuid(), nullable=True),
        sa.Column('objetivo_id', sa.Uuid(), nullable=True),
        sa.Column('programa_id', sa.Uuid(), nullable=True),
        sa.Column('regimen_ayuda_id', sa.Uuid(), nullable=True),
        sa.Column('sector_id', sa.Uuid(), nullable=True),
        sa.Column('tipo_beneficiario_id', sa.Uuid(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.String(length=50), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('updated_by', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['finalidad_id'], ['bdns.finalidad.id'], ),
        sa.ForeignKeyConstraint(['fondo_id'], ['bdns.fondo.id'], ),
        sa.ForeignKeyConstraint(['instrumento_id'], ['bdns.instrumento.id'], ),
        sa.ForeignKeyConstraint(['objetivo_id'], ['bdns.objetivo.id'], ),
        sa.ForeignKeyConstraint(['organo_id'], ['bdns.organo.id'], ),
        sa.ForeignKeyConstraint(['programa_id'], ['bdns.programa.id'], ),
        sa.ForeignKeyConstraint(['regimen_ayuda_id'], ['bdns.regimen_ayuda.id'], ),
        sa.ForeignKeyConstraint(['sector_id'], ['bdns.sector.id'], ),
        sa.ForeignKeyConstraint(['tipo_beneficiario_id'], ['bdns.tipo_beneficiario.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id_bdns'),
        schema='bdns'
    )
    op.create_index('ix_convocatoria_fecha_publicacion', 'convocatoria', ['fecha_publicacion'], unique=False, schema='bdns')
    op.create_index('ix_convocatoria_organo_id', 'convocatoria', ['organo_id'], unique=False, schema='bdns')

    # ============================================================
    # 5. TABLA BENEFICIARIO (schema public)
    # ============================================================

    op.create_table(
        'beneficiario',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('nif', sa.String(length=20), nullable=False),
        sa.Column('nombre', sa.String(), nullable=True),
        sa.Column('tipo_nif', sa.String(length=1), nullable=True),
        sa.Column('provincia', sa.String(), nullable=True),
        sa.Column('municipio', sa.String(), nullable=True),
        sa.Column('codigo_postal', sa.String(length=10), nullable=True),
        sa.Column('forma_juridica_id', sa.Uuid(), nullable=True),
        sa.Column('tipo_beneficiario_id', sa.Uuid(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.String(length=50), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('updated_by', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['forma_juridica_id'], ['bdns.forma_juridica.id'], ),
        sa.ForeignKeyConstraint(['tipo_beneficiario_id'], ['bdns.tipo_beneficiario.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nif'),
        schema='bdns'
    )
    op.create_index('ix_beneficiario_nif', 'beneficiario', ['nif'], unique=False, schema='bdns')
    op.create_index('ix_beneficiario_provincia', 'beneficiario', ['provincia'], unique=False, schema='bdns')

    # ============================================================
    # 6. TABLA CONCESION (schema public) - PARTICIONADA
    # ============================================================

    # Nota: La tabla concesion será particionada jerárquicamente
    # RANGE por fecha_concesion (año) + LIST por regimen_tipo
    # Las particiones se crearán dinámicamente según se necesiten

    op.create_table(
        'concesion',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('fecha_concesion', sa.Date(), nullable=False),
        sa.Column('regimen_tipo', sa.String(length=20), nullable=False, server_default='desconocido'),
        sa.Column('id_concesion', sa.String(), nullable=False),
        sa.Column('beneficiario_id', sa.Uuid(), nullable=False),
        sa.Column('convocatoria_id', sa.Uuid(), nullable=False),
        sa.Column('regimen_ayuda_id', sa.Uuid(), nullable=True),
        sa.Column('importe_nominal', sa.Float(), nullable=True),
        sa.Column('importe_equivalente', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.String(length=50), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('updated_by', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['beneficiario_id'], ['bdns.beneficiario.id'], ),
        sa.ForeignKeyConstraint(['convocatoria_id'], ['bdns.convocatoria.id'], ),
        sa.ForeignKeyConstraint(['regimen_ayuda_id'], ['bdns.regimen_ayuda.id'], ),
        sa.PrimaryKeyConstraint('id', 'fecha_concesion', 'regimen_tipo'),
        sa.UniqueConstraint('id_concesion', 'fecha_concesion', 'regimen_tipo', name='uq_concesion_id_fecha'),
        schema='bdns',
        postgresql_partition_by='RANGE (fecha_concesion)'
    )
    op.create_index('ix_concesion_id_concesion', 'concesion', ['id_concesion', 'fecha_concesion'], unique=False, schema='bdns')
    op.create_index('ix_concesion_regimen_fecha', 'concesion', ['regimen_tipo', 'fecha_concesion'], unique=False, schema='bdns')

    # ============================================================
    # 7. TABLA USUARIO (schema public) - Autenticación compartida
    # ============================================================

    op.create_table(
        'usuario',
        sa.Column('id', sa.Uuid(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('nombre', sa.String(length=255), nullable=True),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='user'),
        sa.Column('activo', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('telegram_chat_id', sa.String(length=50), nullable=True),
        sa.Column('telegram_username', sa.String(length=100), nullable=True),
        sa.Column('telegram_verificado', sa.Boolean(), server_default='false'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.String(length=50), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('updated_by', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('telegram_chat_id'),
        schema='bdns'
    )
    op.create_index('idx_usuario_username_activo', 'usuario', ['username', 'activo'], unique=False, schema='bdns')
    op.create_index('idx_usuario_email_activo', 'usuario', ['email', 'activo'], unique=False, schema='bdns')
    op.create_index('idx_usuario_role_activo', 'usuario', ['role', 'activo'], unique=False, schema='bdns')

    # ============================================================
    # 8. COMENTARIOS
    # ============================================================

    op.execute("""
        -- Comentarios en tablas principales
        COMMENT ON TABLE bdns.convocatoria IS 'Convocatorias de ayudas y subvenciones';
        COMMENT ON TABLE bdns.concesion IS 'Concesiones de ayudas (particionada por fecha y régimen)';
        COMMENT ON TABLE bdns.beneficiario IS 'Beneficiarios de ayudas';
        COMMENT ON TABLE bdns.usuario IS 'Usuarios del sistema para autenticación compartida (Portal + ETL Admin)';

        -- Comentarios en catálogos
        COMMENT ON TABLE bdns.organo IS 'Órganos concedentes (estructura jerárquica)';
        COMMENT ON TABLE bdns.regimen_ayuda IS 'Regímenes de ayuda (minimis, ayuda de estado, etc.)';

        -- Comentarios en columnas especiales
        COMMENT ON COLUMN bdns.usuario.role IS 'Roles: admin (acceso completo), user (acceso limitado), viewer (solo lectura)';
        COMMENT ON COLUMN bdns.concesion.regimen_tipo IS 'Tipo de régimen para particionamiento: minimis, ayuda_estado, ordinaria, partidos_politicos';
    """)


def downgrade() -> None:
    """Downgrade schema - Eliminar schema bdns."""

    # Eliminar tablas en orden inverso de dependencias
    op.drop_table('usuario', schema='bdns')
    op.drop_table('concesion', schema='bdns')
    op.drop_table('beneficiario', schema='bdns')
    op.drop_table('convocatoria', schema='bdns')
    op.drop_table('forma_juridica', schema='bdns')
    op.drop_table('tipo_beneficiario', schema='bdns')
    op.drop_table('sector', schema='bdns')
    op.drop_table('regimen_ayuda', schema='bdns')
    op.drop_table('programa', schema='bdns')
    op.drop_table('organo', schema='bdns')
    op.drop_table('objetivo', schema='bdns')
    op.drop_table('instrumento', schema='bdns')
    op.drop_table('fondo', schema='bdns')
    op.drop_table('finalidad', schema='bdns')

    # Eliminar schema
    op.execute("DROP SCHEMA IF EXISTS bdns CASCADE")

    # Eliminar extensiones
    # op.execute("DROP EXTENSION IF EXISTS \"postgis\"")  # No se creó
    op.execute("DROP EXTENSION IF EXISTS \"unaccent\"")
    op.execute("DROP EXTENSION IF EXISTS \"pg_trgm\"")
    op.execute("DROP EXTENSION IF EXISTS \"uuid-ossp\"")
