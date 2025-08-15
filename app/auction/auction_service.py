from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.db_service import DBService

from . import models
from . import schemas


class AuctionService(DBService):
    async def get_lots(self) -> Sequence[models.Lot]:
        result = await self.db.execute(select(models.Lot))
        return result.scalars().all()

    async def get_lot(self, lot_id: int) -> models.Lot:
        result = await self.db.execute(select(models.Lot).where(models.Lot.id == lot_id))
        lot = result.scalar_one_or_none()
        if not lot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lot not found")
        return lot

    async def update_status(self, lot_id: int, lot_status: models.LotStatus):
        lot = await self.get_lot(lot_id)
        lot.status = lot_status

        await self.db.commit()
        await self.db.refresh(lot)

    async def create_lot(self, lot_data: schemas.LotCreate) -> models.Lot:
        lot = models.Lot(
            title=lot_data.title,
            description=lot_data.description,
            starting_price=float(lot_data.starting_price),
        )
        self.db.add(lot)
        await self.db.commit()
        await self.db.refresh(lot)
        return lot

    async def create_bid(self, lot_id: int, bid_data: schemas.BidCreate) -> models.Bid:
        # Load lot with all bids
        result = await self.db.execute(
            select(models.Lot).options(joinedload(models.Lot.bids)).where(models.Lot.id == lot_id)
        )
        lot = result.unique().scalar_one_or_none()
        if not lot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lot not found")

        # Prevent bids on finished lots
        if lot.status == models.LotStatus.finished:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot create a bid on a finished lot"
            )

        # Enforce bid > highest bid
        if bid_data.amount <= lot.highest_bid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Bid must be higher than current highest bid ({lot.highest_bid})",
            )

        # Create the bid
        bid = models.Bid(lot_id=lot.id, amount=float(bid_data.amount))
        self.db.add(bid)
        await self.db.commit()
        await self.db.refresh(bid)
        return bid