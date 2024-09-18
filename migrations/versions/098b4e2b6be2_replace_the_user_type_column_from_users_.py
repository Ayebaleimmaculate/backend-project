""" replace the user_type column from users  model

Revision ID: 098b4e2b6be2
Revises: 5f6bf001aeb2
Create Date: 2024-06-27 12:23:08.703278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '098b4e2b6be2'
down_revision = '5f6bf001aeb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_type', sa.String(length=50), nullable=False))
        batch_op.create_unique_constraint(None, ['user_type'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('user_type')

    # ### end Alembic commands ###
