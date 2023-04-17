"""Add Location Types table

Revision ID: 42adae38ad8b
Revises:
Create Date: 2023-04-17 12:52:38.838007

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42adae38ad8b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('locations_type',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('storage_provider', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('storage_provider')
                    )


def downgrade() -> None:
    op.drop_table('locations_type')
