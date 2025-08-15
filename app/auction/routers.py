from fastapi import Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db
from .services import AuctionService
from .models import LotStatus
from .schemas import LotCreate, LotRead, BidCreate, BidRead

router = APIRouter(prefix="/lots", tags=["Auctions"])

def get_auction_service(db: AsyncSession = Depends(get_db)) -> AuctionService:
    return AuctionService(db)


@router.patch("/{lot_id}/status", status_code=status.HTTP_200_OK)
async def update_lot_status(
    lot_id: int,
    lot_status: LotStatus,
    svc: AuctionService = Depends()
):
    await svc.update_status(lot_id, lot_status)
    return {"message": f"Lot {lot_id} status updated to {lot_status}"}

@router.post("", response_model=LotRead)
async def create_lot(lot: LotCreate, svc: AuctionService = Depends(get_auction_service)):
    return await svc.create_lot(lot)

@router.post("/{lot_id}/bids", response_model=BidRead)
async def create_bid(lot_id: int, bid: BidCreate, svc: AuctionService = Depends(get_auction_service)):
    return await svc.create_bid(lot_id, bid)

@router.get("", response_model=list[LotRead])
async def get_lots(svc: AuctionService = Depends(get_auction_service)):
    return await svc.get_lots()