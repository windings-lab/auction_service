"""Added unique constraint for bid on lot and user

Revision ID: 9ee1ad08f03e
Revises: 94bc511d51d8
Create Date: 2025-08-15 21:00:01.742721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ee1ad08f03e'
down_revision: Union[str, Sequence[str], None] = '94bc511d51d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("bids", recreate="always") as batch_op:
        batch_op.create_unique_constraint(
            "uq_lot_user_bid", ["lot_id", "user_id"]
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("bids", recreate="always") as batch_op:
        batch_op.drop_constraint("uq_lot_user_bid", type_="unique")
