from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import pandas as pd
import numpy as np
import os
import asyncio

from utils.na_values import na_values

router = APIRouter()

chunk_size = 100

UPLOAD_DIR = os.path.abspath(os.path.join("public", "uploads"))


@router.get("/fetch-data-chunks")
async def fetch_data_chunks(request: Request):
    try:
        index = int(request.query_params.get("index", 0))
        file_name = request.query_params.get("file-name", "")
        file_path = os.path.join(UPLOAD_DIR, file_name)

        if not file_path:
            raise HTTPException(status_code=400, detail="Path parameter is required")

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Read the CSV file using pandas
        chunk_size = 100
        start_line = index * chunk_size + 1

        df = pd.read_csv(
            file_path,
            skiprows=range(1, start_line),
            nrows=chunk_size,
            parse_dates=True,
            na_values=na_values,
        )

        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.fillna(0, inplace=True)

        int_columns = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

        object_columns = df.select_dtypes(include="object").columns.tolist()

        csv_data = df.to_dict(orient="records")

        with open(file_path, "r") as file:
            row_count = sum(1 for line in file) - 1

        total_pages = (row_count + chunk_size - 1) // chunk_size

        return JSONResponse(
            content={
                "totalPages": total_pages,
                "data": csv_data,
                "numericalColumns": int_columns,
                "stringColumns": object_columns,
            }
        )
    except Exception as e:
        print("Error:", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
