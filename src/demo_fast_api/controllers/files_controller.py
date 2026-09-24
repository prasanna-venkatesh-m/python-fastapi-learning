from fastapi import APIRouter, File, Form, UploadFile, Depends
from demo_fast_api.services.file_service import FileService
from demo_fast_api.dto.enums.file_type_enum import FileType

router = APIRouter(prefix="/files", tags=["Files"])

@router.post(path="/upload-file" )
async def upload_files(
    fileType: FileType = Form(...), file: UploadFile = File(...),
    fileService : FileService = Depends(FileService)
) -> bool:
  return await fileService.upload_files(fileType, file)