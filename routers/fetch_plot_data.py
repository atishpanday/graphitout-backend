from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import pandas as pd
import numpy as np
import os

from utils.na_values import na_values

router = APIRouter()

UPLOAD_DIR = os.path.abspath(os.path.join("public", "uploads"))


@router.get("/fetch-plot-data")
def fetch_plot_data(request: Request):
    try:
        file_name = request.query_params.get("file-name", "")
        x = request.query_params.get("x", "")
        y = request.query_params.get("y", "")
        chart_type = request.query_params.get("chart-type", "")

        file_path = os.path.join(UPLOAD_DIR, file_name)

        df = pd.read_csv(
            file_path,
            parse_dates=True,
            na_values=na_values,
        )

        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.fillna(0, inplace=True)

        if chart_type == "Scatter":
            df_avg = pd.concat([df[[x]], df[[y]]], axis=1)
        else:
            df_avg = df.groupby(x)[y].mean().reset_index()

        plot_data = df_avg.to_dict(orient="records")

        return JSONResponse(content={"data": plot_data})

    except Exception as e:
        print("Error:", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
