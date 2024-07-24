from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
import asyncio

router = APIRouter()

UPLOAD_DIR = os.path.abspath(os.path.join("public", "uploads"))


@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_name = file.filename.replace(" ", "_")
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return JSONResponse(content={"success": True, "fileName": file_name})
