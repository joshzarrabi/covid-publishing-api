"""Add totalTestResults states columns

Revision ID: db050f46440f
Revises: b5c0630efcf2
Create Date: 2020-08-27 15:40:48.413634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db050f46440f'
down_revision = 'b5c0630efcf2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('states', sa.Column('totalTestResultsColumns', sa.String(), nullable=True))
    op.add_column('states', sa.Column('totalTestResultsUnits', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('states', 'totalTestResultsUnits')
    op.drop_column('states', 'totalTestResultsColumns')
    # ### end Alembic commands ###
