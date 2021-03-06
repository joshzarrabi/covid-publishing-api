"""Renaming states tab 2 columns

Revision ID: cc91b057d1ee
Revises: 2321b5cbc876
Create Date: 2020-09-02 11:20:53.430606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc91b057d1ee'
down_revision = '2321b5cbc876'
branch_labels = None
depends_on = None


# Manually written to do a rename instead of the Alembic-autogenerated drop/add
def upgrade():
    op.alter_column('states', 'totalTestResultsColumns', new_column_name='covidTrackingProjectPreferredTotalTestField')
    op.alter_column('states', 'totalTestResultsUnits', new_column_name='covidTrackingProjectPreferredTotalTestUnits')

def downgrade():
    op.alter_column('states', 'covidTrackingProjectPreferredTotalTestField', new_column_name='totalTestResultsColumns')
    op.alter_column('states', 'covidTrackingProjectPreferredTotalTestUnits', new_column_name='totalTestResultsUnits')
