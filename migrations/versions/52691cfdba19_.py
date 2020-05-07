"""empty message

Revision ID: 52691cfdba19
Revises: f9fe02c70c89
Create Date: 2020-04-05 19:10:54.818051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52691cfdba19'
down_revision = 'f9fe02c70c89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    op.drop_column('users', 'is_seller')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'users',
        sa.Column(
            'is_seller',
            sa.BOOLEAN(),
            autoincrement=False,
            nullable=True))
    op.add_column(
        'users',
        sa.Column(
            'password',
            sa.VARCHAR(),
            autoincrement=False,
            nullable=False))
    # ### end Alembic commands ###
