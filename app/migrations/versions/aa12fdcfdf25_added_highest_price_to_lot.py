"""Added highest price to lot

Revision ID: aa12fdcfdf25
Revises: 9ee1ad08f03e
Create Date: 2025-08-15 21:52:57.324897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

from app.auction.models import Lot

# revision identifiers, used by Alembic.
revision: str = 'aa12fdcfdf25'
down_revision: Union[str, Sequence[str], None] = '9ee1ad08f03e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'lots',
        sa.Column('highest_price', sa.Float(), nullable=False, server_default="0")
    )

    bind = op.get_bind()
    session = Session(bind=bind)

    try:
        # Load all lots
        lots = session.query(Lot).all()
        for lot in lots:
            if not lot.bids:
                lot.highest_price = lot.starting_price
                continue
            lot.highest_price = max(b.amount for b in lot.bids)
        session.commit()
    finally:
        session.close()

    # 3. Remove the server_default after initialization
    with op.batch_alter_table("lots") as batch_op:
        batch_op.alter_column("highest_price", server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('lots', 'highest_price')
