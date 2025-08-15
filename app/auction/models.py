import datetime
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, func, ForeignKey, Enum as SAEnum, UniqueConstraint

from app import model
import app.account.models


class LotStatus(str, Enum):
    running = "running"
    finished = "finished"

class Lot(model.Base):
    __tablename__ = "lots"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1024))
    starting_price: Mapped[float] = mapped_column(Float)
    highest_price: Mapped[float] = mapped_column(Float, nullable=False, server_default="0")
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    status: Mapped[LotStatus] = mapped_column(
        SAEnum(LotStatus, native_enum=False),
        nullable=False,
        server_default=LotStatus.running
    )

    bids: Mapped[list["Bid"]] = relationship(
        "Bid",
        back_populates="lot",
        cascade="all, delete-orphan"
    )


class Bid(model.Base):
    __tablename__ = "bids"

    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    amount: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    lot: Mapped["Lot"] = relationship(
        "Lot",
        back_populates="bids",
    )
    user: Mapped["app.account.models.User"] = relationship("User")

    __table_args__ = (
        UniqueConstraint('lot_id', 'user_id', name='uq_lot_user_bid'),
    )
