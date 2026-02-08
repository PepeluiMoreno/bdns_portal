"""desdoblar_importe_concesion

Revision ID: fc5db4ea92bd
Revises: 0593883f1a85
Create Date: 2026-02-08 11:20:22.243143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc5db4ea92bd'
down_revision: Union[str, None] = '0593883f1a85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Agregar nuevas columnas importe_nominal e importe_equivalente (nullable)
    op.add_column('concesion', sa.Column('importe_nominal', sa.Float(), nullable=True))
    op.add_column('concesion', sa.Column('importe_equivalente', sa.Float(), nullable=True))

    # 2. Copiar datos de importe a importe_nominal (si existen registros)
    op.execute("""
        UPDATE concesion
        SET importe_nominal = importe
        WHERE importe IS NOT NULL
    """)

    # 3. Eliminar columna importe antigua
    op.drop_column('concesion', 'importe')


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Restaurar columna importe
    op.add_column('concesion', sa.Column('importe', sa.Float(), nullable=True))

    # 2. Copiar datos de importe_nominal a importe
    op.execute("""
        UPDATE concesion
        SET importe = importe_nominal
        WHERE importe_nominal IS NOT NULL
    """)

    # 3. Eliminar nuevas columnas
    op.drop_column('concesion', 'importe_equivalente')
    op.drop_column('concesion', 'importe_nominal')
