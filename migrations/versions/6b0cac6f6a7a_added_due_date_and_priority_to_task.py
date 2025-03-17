"""Added due_date and priority to Task

Revision ID: 6b0cac6f6a7a
Revises: 20f7786387ce
Create Date: 2025-02-24 13:37:28.795462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b0cac6f6a7a'
down_revision = '20f7786387ce'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns
    with op.batch_alter_table("task") as batch_op:
        batch_op.add_column(sa.Column("due_date", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("priority", sa.String(length=10), nullable=False, server_default="Medium"))

def downgrade():
    with op.batch_alter_table("task") as batch_op:
        batch_op.drop_column("due_date")
        batch_op.drop_column("priority")


    # ### end Alembic commands ###
