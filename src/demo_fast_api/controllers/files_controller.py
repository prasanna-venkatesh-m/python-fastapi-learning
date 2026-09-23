from fastapi import APIRouter, File, Form, UploadFile

router = APIRouter(prefix="/files", tags=["Files"])


@router.post(path="/upload-file")
def upload_files(
    fileType: int = Form(...), file: UploadFile = File(...)
) -> bool:
  return True