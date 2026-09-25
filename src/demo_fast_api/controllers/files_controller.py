from fastapi import APIRouter, File, Form, UploadFile, Depends
from demo_fast_api.services.file_service import FileService
from demo_fast_api.dto.enums.file_type_enum import FileType
from demo_fast_api.utils.dependencies import authenticate, authorize

router = APIRouter(prefix="/files", tags=["Files"], dependencies=[Depends(authenticate)])

@router.post(path="/upload-file", dependencies=[Depends(authorize(["ADMIN"]))])
async def upload_files(
    fileType: FileType = Form(...), file: UploadFile = File(...),
    fileService : FileService = Depends(FileService)
) -> bool:
  return await fileService.upload_files(fileType, file)