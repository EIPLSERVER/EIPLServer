"""update2

Revision ID: 641f2dfb13b0
Revises: 6d7ddb0b5c2a
Create Date: 2022-03-18 12:48:48.476727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '641f2dfb13b0'
down_revision = '6d7ddb0b5c2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('slots', sa.Column('bay_id', sa.Integer(), nullable=False))
    op.drop_constraint('slots_bay_name_fkey', 'slots', type_='foreignkey')
    op.create_foreign_key(None, 'slots', 'bay', ['bay_id'], ['id'], ondelete='CASCADE')
    op.drop_column('slots', 'bay_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('slots', sa.Column('bay_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'slots', type_='foreignkey')
    op.create_foreign_key('slots_bay_name_fkey', 'slots', 'bay', ['bay_name'], ['bay_name'], ondelete='CASCADE')
    op.drop_column('slots', 'bay_id')
    # ### end Alembic commands ###