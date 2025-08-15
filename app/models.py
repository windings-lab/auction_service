import datetime
from enum import Enum

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Float, func, ForeignKey, Enum as SAEnum


class Base(DeclarativeBase):
    pass

class LotStatus(str, Enum):
    running = "running"
    finished = "finished"

class Lot(Base):
    __tablename__ = "lots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lot_id: Mapped[int] = mapped_column(ForeignKey("lots.id", ondelete="CASCADE"))
    amount: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    lot: Mapped["Lot"] = relationship(
        "Lot",
        back_populates="bids",
    )
