"""LIBITD-2254. Add storage_providers table

Revision ID: 2e9547b223ac
Revises: 7da0ed6568f0
Create Date: 2023-04-19 15:51:38.883636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e9547b223ac'
down_revision = '7da0ed6568f0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('storage_providers',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('storage_provider', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_storage_providers')),
                    sa.UniqueConstraint('storage_provider', name=op.f('uq_storage_providers_storage_provider'))
                    )


def downgrade() -> None:
    op.drop_table('storage_providers')
