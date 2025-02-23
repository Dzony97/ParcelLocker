"""Make latitude and longitude nullable

Revision ID: 754788c6fec0
Revises: 876f9a3dcbae
Create Date: 2025-02-23 13:40:49.638270

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '754788c6fec0'
down_revision = '876f9a3dcbae'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.alter_column('latitude',
               existing_type=mysql.FLOAT(),
               nullable=True)
        batch_op.alter_column('longitude',
               existing_type=mysql.FLOAT(),
               nullable=True)


def downgrade():
    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.alter_column('longitude',
               existing_type=mysql.FLOAT(),
               nullable=False)
        batch_op.alter_column('latitude',
               existing_type=mysql.FLOAT(),
               nullable=False)

