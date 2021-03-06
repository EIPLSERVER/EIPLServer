"""adding names

Revision ID: a74250816b0f
Revises: 
Create Date: 2022-06-02 22:40:42.012696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a74250816b0f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin', sa.Column('name', sa.String(), nullable=True))
    op.add_column('subadmin', sa.Column('name', sa.String(), nullable=True))
    op.add_column('user', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'name')
    op.drop_column('subadmin', 'name')
    op.drop_column('admin', 'name')
    # ### end Alembic commands ###
