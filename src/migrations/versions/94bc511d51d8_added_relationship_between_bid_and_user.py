"""Added relationship between bid and user

Revision ID: 94bc511d51d8
Revises: 00c0fd1ac574
Create Date: 2025-08-15 20:53:57.910520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94bc511d51d8'
down_revision: Union[str, Sequence[str], None] = '00c0fd1ac574'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("bids", recreate="always") as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=False, server_default="1"))
        batch_op.create_foreign_key(
            "fk_bids_user_id_users",
            "users",
            ["user_id"],
            ["id"],
            ondelete="CASCADE"
        )

    with op.batch_alter_table("bids") as batch_op:
        batch_op.alter_column("user_id", server_default=None)



def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("bids", recreate="always") as batch_op:
        batch_op.drop_constraint("fk_bids_user_id_users", type_="foreignkey")
        batch_op.drop_column("user_id")
