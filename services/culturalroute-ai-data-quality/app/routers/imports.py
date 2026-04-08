from fastapi import APIRouter, UploadFile, File
from app.application.import_service import ImportService

router = APIRouter(prefix="/imports", tags=["Imports"])

service = ImportService()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    return await service.process_file(file)
