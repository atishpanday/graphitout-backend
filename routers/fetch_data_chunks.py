from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import pandas as pd
import numpy as np
import os
import asyncio

router = APIRouter()

na_values = [
    "NA",
    "N/A",
    "NaN",
    "nan",
    "NULL",
    "null",
    "None",
    "none",
    "Nil",
    "nil",
    "Na",
    "na",
    "",
    " ",
    "?",
    "--",
    "---",
    "n/a",
    "NIL",
    "NONE",
    "NULL",
    ".",
    "..",
    "...",
    "unknown",
    "Unknown",
    "UNDEFINED",
    "undefined",
    "UNDEFINED",
    "missing",
    "Missing",
    "MISSING",
]

chunk_size = 100

UPLOAD_DIR = os.path.abspath(os.path.join("public", "uploads"))


@router.get("/fetch-data-chunks")
async def fetch_data_chunks(request: Request):
    try:
        index = int(request.query_params.get("index", 0))
        file_name = request.query_params.get("file-name", "")
        file_path = os.path.join(UPLOAD_DIR, file_name)

        root, ext = os.path.splitext(file_path)

        if not file_path:
            raise HTTPException(status_code=400, detail="Path parameter is required")

        full_path = os.path.join(UPLOAD_DIR, file_path)
        if not os.path.exists(full_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Read the CSV file using pandas
        chunk_size = 100
        start_line = index * chunk_size + 1

        if ext.lower() == ".csv" or ext.lower() == ".txt":
            df = pd.read_csv(
                full_path,
                skiprows=range(1, start_line),
                nrows=chunk_size,
                parse_dates=True,
                na_values=na_values,
            )
        elif ext.lower() == ".xlsx":
            df = pd.read_excel(
                full_path,
                skiprows=range(1, start_line),
                nrows=chunk_size,
                parse_dates=True,
                na_values=na_values,
                engine="openpyxl",
            )
        else:
            return JSONResponse(content={"error": "File extension not supported"})

        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.fillna(0, inplace=True)
        csv_data = df.to_dict(orient="records")
        total_pages = (len(pd.read_csv(full_path)) + chunk_size - 1) // chunk_size

        return JSONResponse(content={"totalPages": total_pages, "data": csv_data})
    except Exception as e:
        print("Error:", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
