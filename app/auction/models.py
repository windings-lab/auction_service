import datetime
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, func, ForeignKey, Enum as SAEnum

from ..db import Base


class LotStatus(str, Enum):
    running = "running"
    finished = "finished"

class Lot(Base):
    __tablename__ = "lots"

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1024))
    starting_price: Mapped[float] = mapped_column(Float)
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

    @property
    def highest_bid(self) -> float:
        """Return the highest bid or starting_price if no bids yet"""
        if not self.bids:
            return self.starting_price
        return max(b.amount for b in self.bids)

class Bid(Base):
    __tablename__ = "bids"

    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id", ondelete="CASCADE"))
    amount: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    lot: Mapped["Lot"] = relationship(
        "Lot",
        back_populates="bids",
    )
