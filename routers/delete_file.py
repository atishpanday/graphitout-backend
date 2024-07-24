from fastapi import APIRouter, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import os

router = APIRouter()

UPLOAD_DIR = os.path.abspath(os.path.join("public", "uploads"))


@router.delete("/delete-file")
async def delete_file(request: Request):
    try:
        file_name = request.query_params.get("file-name")
        file_name = os.path.basename(file_name)
        file_path = os.path.join(UPLOAD_DIR, file_name)

        if not file_name:
            raise HTTPException(status_code=400, detail="Path parameter is required")

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        os.remove(file_path)
        return JSONResponse(content={"success": True})
    except Exception as e:
        return JSONResponse(content={"err": str(e)}, status_code=500)
