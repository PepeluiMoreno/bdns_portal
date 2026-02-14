"""add ETL columns to convocatoria

Añade columnas necesarias para el pipeline ETL de convocatorias:
- codigo_bdns: código alternativo de la convocatoria
- fecha_recepcion: fecha de recepción en BDNS
- presupuesto_total: presupuesto total de la convocatoria
- reglamento_id: FK al catálogo de reglamentos

Revision ID: 003_conv_etl
Revises: 002_nivel_norm
Create Date: 2026-02-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003_conv_etl'
down_revision: Union[str, None] = '002_nivel_norm'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Añadir columnas ETL a convocatoria."""
    op.add_column(
        'convocatoria',
        sa.Column('codigo_bdns', sa.String(), nullable=True),
        schema='bdns'
    )
    op.add_column(
        'convocatoria',
        sa.Column('fecha_recepcion', sa.Date(), nullable=True),
        schema='bdns'
    )
    op.add_column(
        'convocatoria',
        sa.Column('presupuesto_total', sa.Float(), nullable=True),
        schema='bdns'
    )
    op.add_column(
        'convocatoria',
        sa.Column('reglamento_id', sa.Uuid(), nullable=True),
        schema='bdns'
    )

    # Índice en codigo_bdns para búsquedas
    op.create_index(
        'ix_convocatoria_codigo_bdns',
        'convocatoria',
        ['codigo_bdns'],
        unique=False,
        schema='bdns'
    )

    # FK a reglamento (la tabla ya existe, poblada por catálogos)
    op.create_foreign_key(
        'fk_convocatoria_reglamento',
        'convocatoria',
        'reglamento',
        ['reglamento_id'],
        ['id'],
        source_schema='bdns',
        referent_schema='bdns'
    )


def downgrade() -> None:
    """Eliminar columnas ETL de convocatoria."""
    op.drop_constraint('fk_convocatoria_reglamento', 'convocatoria', schema='bdns', type_='foreignkey')
    op.drop_index('ix_convocatoria_codigo_bdns', table_name='convocatoria', schema='bdns')
    op.drop_column('convocatoria', 'reglamento_id', schema='bdns')
    op.drop_column('convocatoria', 'presupuesto_total', schema='bdns')
    op.drop_column('convocatoria', 'fecha_recepcion', schema='bdns')
    op.drop_column('convocatoria', 'codigo_bdns', schema='bdns')
