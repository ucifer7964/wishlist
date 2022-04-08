"""added user and order foreign key

Revision ID: 9f98c9a63364
Revises: ac6d0e0feaa5
Create Date: 2022-04-09 01:31:39.408508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f98c9a63364'
down_revision = 'ac6d0e0feaa5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'orders', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_column('orders', 'user_id')
    # ### end Alembic commands ###
