from fastapi import File
from demo_fast_api.dto.enums.file_type_enum import FileType

class FileService:
    def upload_files(self, fileType : FileType, file : File):
        update_files_list = {FileType.FAQ, FileType.INFORMATION}
        if(fileType in update_files_list):
            return True
        return False