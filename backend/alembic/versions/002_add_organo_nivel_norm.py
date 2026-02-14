"""add nivel_norm columns to organo

Revision ID: 002_nivel_norm
Revises: 001_initial
Create Date: 2026-02-11

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002_nivel_norm'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Añadir columnas nivel*_norm a organo para búsqueda normalizada."""
    op.add_column('organo', sa.Column('nivel1_norm', sa.String(), nullable=True), schema='bdns')
    op.add_column('organo', sa.Column('nivel2_norm', sa.String(), nullable=True), schema='bdns')
    op.add_column('organo', sa.Column('nivel3_norm', sa.String(), nullable=True), schema='bdns')

    op.create_index(
        'ix_organo_niveles',
        'organo',
        ['nivel1_norm', 'nivel2_norm', 'nivel3_norm'],
        unique=False,
        schema='bdns',
    )


def downgrade() -> None:
    """Eliminar columnas nivel*_norm de organo."""
    op.drop_index('ix_organo_niveles', table_name='organo', schema='bdns')
    op.drop_column('organo', 'nivel3_norm', schema='bdns')
    op.drop_column('organo', 'nivel2_norm', schema='bdns')
    op.drop_column('organo', 'nivel1_norm', schema='bdns')
