from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select, exc
from sqlalchemy.orm import joinedload

from src.db_service import DBService

from . import models
from . import schemas
import src.account.schemas


class AuctionService(DBService):
    async def get_lots(self) -> Sequence[models.Lot]:
        result = await self.db.execute(select(models.Lot))
        return result.scalars().all()

    async def get_lot(self, lot_id: int) -> models.Lot:
        result = await self.db.execute(
            select(models.Lot).options(joinedload(models.Lot.bids)).where(models.Lot.id == lot_id)
        )
        lot: models.Lot = result.unique().scalar_one_or_none()
        if not lot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lot not found")

        return lot

    async def get_bid(self, lot_id: int, user_data: src.account.schemas.UserOut) -> models.Bid:
        result = await self.db.execute(
            select(models.Bid)
            .where(models.Bid.lot_id == lot_id, models.Bid.user_id == user_data.id)
        )
        bid: models.Bid = result.scalar_one_or_none()
        if not bid:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bid not found for this user and lot"
            )

        return bid

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
            highest_price=float(lot_data.starting_price),
        )
        self.db.add(lot)
        await self.db.commit()
        await self.db.refresh(lot)
        return lot

    def _check_lot_finished(self, lot: models.Lot):
        """Prevent creating bids on finished lots"""
        if lot.status == models.LotStatus.finished:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot create a bid on a finished lot"
            )

    def _check_highest_bid(self, bid_data: schemas.BidCreate, lot: models.Lot):
        """Enforce bid > highest bid"""
        if bid_data.amount <= lot.highest_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Bid must be higher than current highest bid ({lot.highest_price})",
            )

    async def create_bid(self, lot_id: int, bid_data: schemas.BidCreate, user_data: src.account.schemas.UserOut) -> models.Bid:
        lot = await self.get_lot(lot_id)
        self._check_lot_finished(lot)
        self._check_highest_bid(bid_data, lot)

        # Create the bid
        bid = models.Bid(
            lot_id=lot.id,
            amount=float(bid_data.amount),
            user_id=user_data.id,
        )

        # Update highest price
        lot.highest_price = bid.amount

        self.db.add(bid)
        self.db.add(lot)
        try:
            await self.db.commit()
        except exc.IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already created a bid for this lot. Please update your bid instead."
            )
        await self.db.refresh(bid)
        return bid

    async def update_bid(self, lot_id: int, bid_data: schemas.BidCreate, user_data: src.account.schemas.UserOut):
        bid = await self.get_bid(lot_id, user_data)

        await self.db.refresh(bid, attribute_names=["lot"])
        self._check_lot_finished(bid.lot)
        self._check_highest_bid(bid_data, bid.lot)

        # Update the bid amount and lot highest price
        bid.amount = float(bid_data.amount)
        bid.lot.highest_price = bid.amount

        self.db.add(bid.lot)
        self.db.add(bid)
        await self.db.commit()
        await self.db.refresh(bid)
        return bid