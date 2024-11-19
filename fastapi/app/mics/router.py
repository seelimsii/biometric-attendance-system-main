import os
from http import HTTPStatus as status

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from loguru import logger

from app.config import API_CONFIG_TEMPLATE_FOLDER_PATH

router = APIRouter()


@router.get("/bulk-user-upload-template")
async def bulk_user_upload_template():
    file_path = f"{API_CONFIG_TEMPLATE_FOLDER_PATH}/bulk_user_upload.csv"
    root_path = os.path.abspath(file_path)
    logger.info(f"Template file path: {root_path}")

    if not os.path.exists(root_path):
        raise HTTPException(
            status_code=status.NOT_FOUND,
            detail="Template file not found",
        )

    return FileResponse(
        path=os.path.abspath(root_path),
        filename=os.path.basename(root_path),
        media_type="application/octet-stream",
    )
