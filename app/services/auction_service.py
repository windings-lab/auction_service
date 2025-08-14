from typing import Sequence

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db import get_db
from app.models import Lot, Bid, LotStatus
from app.schemas import LotCreate, BidCreate


class AuctionService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_lots(self) -> Sequence[Lot]:
        result = await self.db.execute(select(Lot))
        return result.scalars().all()

    async def get_lot(self, lot_id: int) -> Lot:
        result = await self.db.execute(select(Lot).where(Lot.id == lot_id))
        lot = result.scalar_one_or_none()
        if not lot:
            raise HTTPException(status_code=404, detail="Lot not found")
        return lot

    async def update_status(self, lot_id: int, status: LotStatus):
        lot = await self.get_lot(lot_id)
        lot.status = status

        await self.db.commit()
        await self.db.refresh(lot)

    async def create_lot(self, lot_data: LotCreate) -> Lot:
        lot = Lot(
            title=lot_data.title,
            description=lot_data.description,
            starting_price=float(lot_data.starting_price),
        )
        self.db.add(lot)
        await self.db.commit()
        await self.db.refresh(lot)
        return lot

    async def create_bid(self, lot_id: int, bid_data: BidCreate) -> Bid:
        # Load lot with all bids
        result = await self.db.execute(
            select(Lot).options(joinedload(Lot.bids)).where(Lot.id == lot_id)
        )
        lot = result.unique().scalar_one_or_none()
        if not lot:
            raise HTTPException(status_code=404, detail="Lot not found")

        # Prevent bids on finished lots
        if lot.status == LotStatus.finished:
            raise HTTPException(
                status_code=400,
                detail="Cannot create a bid on a finished lot"
            )

        # Enforce bid > highest bid
        if bid_data.amount <= lot.highest_bid:
            raise HTTPException(
                status_code=400,
                detail=f"Bid must be higher than current highest bid ({lot.highest_bid})",
            )

        # Create the bid
        bid = Bid(lot_id=lot.id, amount=float(bid_data.amount))
        self.db.add(bid)
        await self.db.commit()
        await self.db.refresh(bid)
        return bid