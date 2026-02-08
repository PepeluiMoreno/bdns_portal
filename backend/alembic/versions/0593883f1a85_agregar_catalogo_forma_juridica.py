"""agregar_catalogo_forma_juridica

Revision ID: 0593883f1a85
Revises: bd5f8e7d7313
Create Date: 2026-02-08 10:52:12.087167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0593883f1a85'
down_revision: Union[str, None] = 'bd5f8e7d7313'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Crear tabla forma_juridica
    op.create_table(
        'forma_juridica',
        sa.Column('id', sa.Uuid(), nullable=False, server_default=sa.text('uuid_generate_v7()')),
        sa.Column('codigo', sa.String(), nullable=False),
        sa.Column('codigo_natural', sa.String(length=1), nullable=False),
        sa.Column('descripcion', sa.String(), nullable=False),
        sa.Column('descripcion_norm', sa.String(), nullable=False),
        sa.Column('tipo', sa.String(), nullable=False),
        sa.Column('es_persona_fisica', sa.Boolean(), nullable=False, server_default='false'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('codigo')
    )
    op.create_index('ix_forma_juridica_codigo', 'forma_juridica', ['codigo'])
    op.create_index('ix_forma_juridica_codigo_natural', 'forma_juridica', ['codigo_natural'])
    op.create_index('ix_forma_juridica_descripcion_norm', 'forma_juridica', ['descripcion_norm'])

    # 2. Agregar columna forma_juridica_id a beneficiario (nullable para migración)
    op.add_column('beneficiario', sa.Column('forma_juridica_id', sa.Uuid(), nullable=True))

    # 3. Crear FK de beneficiario.forma_juridica_id a forma_juridica.id
    op.create_foreign_key(
        'fk_beneficiario_forma_juridica',
        'beneficiario', 'forma_juridica',
        ['forma_juridica_id'], ['id']
    )

    # 4. Eliminar la columna forma_juridica (String) antigua
    op.drop_column('beneficiario', 'forma_juridica')


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Restaurar columna forma_juridica (String) en beneficiario
    op.add_column('beneficiario', sa.Column('forma_juridica', sa.String(), nullable=True))

    # 2. Eliminar FK
    op.drop_constraint('fk_beneficiario_forma_juridica', 'beneficiario', type_='foreignkey')

    # 3. Eliminar columna forma_juridica_id
    op.drop_column('beneficiario', 'forma_juridica_id')

    # 4. Eliminar tabla forma_juridica
    op.drop_index('ix_forma_juridica_descripcion_norm', 'forma_juridica')
    op.drop_index('ix_forma_juridica_codigo_natural', 'forma_juridica')
    op.drop_index('ix_forma_juridica_codigo', 'forma_juridica')
    op.drop_table('forma_juridica')
