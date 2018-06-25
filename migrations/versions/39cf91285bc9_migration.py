"""migration

Revision ID: 39cf91285bc9
Revises: 16ec0d6b85f3
Create Date: 2018-06-24 10:00:08.150993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39cf91285bc9'
down_revision = '16ec0d6b85f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_hash', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_hash')
    # ### end Alembic commands ###