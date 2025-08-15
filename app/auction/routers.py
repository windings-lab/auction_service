from typing import Annotated

from fastapi import status, APIRouter, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session

from . import models
from . import schemas
from .auction_service import AuctionService
import app.account.schemas
import app.account.routers

router = APIRouter(prefix="/lots", tags=["Auctions"])

def get_auction_service(db: Annotated[AsyncSession, Depends(get_db_session)]):
    return AuctionService(db)


@router.patch("/{lot_id}/status", status_code=status.HTTP_200_OK)
async def update_lot_status(
    lot_id: int,
    lot_status: models.LotStatus,
    auction_service: Annotated[AuctionService, Depends(get_auction_service)],
):
    await auction_service.update_status(lot_id, lot_status)
    return {"message": f"Lot {lot_id} status updated to {lot_status}"}

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.LotRead)
async def create_lot(
    lot: Annotated[schemas.LotCreate, Form()],
    auction_service: Annotated[AuctionService, Depends(get_auction_service)],
):
    return await auction_service.create_lot(lot)

@router.post("/{lot_id}/bids", status_code=status.HTTP_201_CREATED, response_model=schemas.BidRead)
async def create_bid(
    lot_id: int,
    bid: Annotated[schemas.BidCreate, Form()],
    current_user: Annotated[app.account.schemas.UserOut, Depends(app.account.routers.get_current_user)],
    auction_service: Annotated[AuctionService, Depends(get_auction_service)],
):
    return await auction_service.create_bid(lot_id, bid, current_user)

@router.patch("/{lot_id}/bids", status_code=status.HTTP_200_OK, response_model=schemas.BidRead)
async def update_bid(
    lot_id: int,
    bid: Annotated[schemas.BidCreate, Form()],
    current_user: Annotated[app.account.schemas.UserOut, Depends(app.account.routers.get_current_user)],
    auction_service: Annotated[AuctionService, Depends(get_auction_service)],
):
    return await auction_service.update_bid(lot_id, bid, current_user)

@router.get("", status_code=status.HTTP_200_OK, response_model=list[schemas.LotRead])
async def get_lots(auction_service: Annotated[AuctionService, Depends(get_auction_service)]):
    return await auction_service.get_lots()