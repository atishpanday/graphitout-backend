from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
import asyncio

router = APIRouter()

UPLOAD_DIR = os.path.abspath(os.path.join("public", "uploads"))


def delete_files_in_directory(directory_path):
    try:
        files = os.listdir(directory_path)
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("All files deleted successfully.")
    except OSError:
        print("Error occurred while deleting files.")


@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    delete_files_in_directory(UPLOAD_DIR)

    file_name = file.filename.replace(" ", "_")
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return JSONResponse(content={"success": True, "fileName": file_name})
