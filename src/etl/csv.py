import io

import pandas as pd
from fastapi import UploadFile, HTTPException, status


async def read(csv_file: UploadFile, filter_column: str):
    try:
        content = await csv_file.read()
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to read CSV: {e}")

    if filter_column not in df.columns:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CSV missing required column")

    filter_values = df[filter_column].dropna().unique().tolist()
    if not filter_values:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No values to filter")

    return filter_values