from typing import Annotated

from fastapi import APIRouter, Request, Form, UploadFile, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.inspection import inspect

from ..db import get_db_session
from ..model import Base
from .csv import read as csv_read

router = APIRouter(prefix="/etl", tags=["ETL"])
templates = Jinja2Templates(directory="templates")

BATCH_SIZE = 1000

def get_tables_and_columns() -> dict[str, list[str]]:
    tables_info = {}
    for table_class in Base.__subclasses__():
        table_name = table_class.__tablename__
        columns = [
            col.name
            for col in table_class.__table__.columns
            if not col.foreign_keys
        ]
        tables_info[table_name] = columns
    return tables_info

def model_to_dict(obj):
    """Convert SQLAlchemy model instance to a dictionary."""
    if hasattr(obj, '__table__'):
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}
    return obj

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    tables_info = get_tables_and_columns()
    return templates.TemplateResponse("etl.html", {"request": request, "tables_info": tables_info})


@router.post("/extract")
async def extract_data(
    table_name: Annotated[str, Form(...)],
    filter_column: Annotated[str, Form(...)],
    csv_file: Annotated[UploadFile, Form(...)],
    db: Annotated[AsyncSession, Depends(get_db_session)]
):
    tables_info = get_tables_and_columns()
    if table_name not in tables_info or filter_column not in tables_info[table_name]:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid table or column")

    filter_values = await csv_read(csv_file, filter_column)

    # Отримуємо модель таблиці
    table_class = next((cls for cls in Base.__subclasses__() if cls.__tablename__ == table_name), None)
    if table_class is None:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Table not found")

    # Виконання SELECT батчами
    results = []
    for i in range(0, len(filter_values), BATCH_SIZE):
        batch = filter_values[i:i + BATCH_SIZE]
        stmt = select(table_class).where(getattr(table_class, filter_column).in_(batch))
        rows = await db.execute(stmt)
        query_results = rows.fetchall()
        results.extend([model_to_dict(r[0]) for r in query_results])

    return JSONResponse(content=results)