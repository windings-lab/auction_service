"""Added unique constraint for bid on lot and user

Revision ID: 9ee1ad08f03e
Revises: 94bc511d51d8
Create Date: 2025-08-15 21:00:01.742721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

from src.auction.models import Bid

# revision identifiers, used by Alembic.
revision: str = '9ee1ad08f03e'
down_revision: Union[str, Sequence[str], None] = '94bc511d51d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    session = Session(bind=bind)

    try:
        # 1. Find duplicates per (lot_id, user_id), keep only highest amount
        all_bids = session.query(Bid).all()
        keep = {}

        for bid in all_bids:
            key = (bid.lot_id, bid.user_id)
            if key not in keep or bid.amount > keep[key].amount:
                keep[key] = bid

        # Delete bids not in `keep`
        delete_ids = [bid.id for bid in all_bids if bid not in keep.values()]
        if delete_ids:
            session.query(Bid).filter(Bid.id.in_(delete_ids)).delete(synchronize_session=False)

        session.commit()

        with op.batch_alter_table("bids") as batch_op:
            batch_op.create_unique_constraint(
                "uq_lot_user_bid", ["lot_id", "user_id"]
            )
    finally:
        session.close()


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("bids") as batch_op:
        batch_op.drop_constraint("uq_lot_user_bid", type_="unique")
