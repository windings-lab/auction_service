# Use this file to define your models
# So for example alembic would discover them
# By default import this when you are creating lifespan of the fastapi

from app.db import Base
from app.auction.models import Lot, Bid
