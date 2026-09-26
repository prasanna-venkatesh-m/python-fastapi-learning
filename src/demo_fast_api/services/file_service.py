from uuid import uuid4

from fastapi import File, UploadFile
from demo_fast_api.dto.enums.file_type_enum import FileType
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from docx import Document
from pathlib import Path
import io
from demo_fast_api.vectordb.vector_db import VectorDB

class FileService:
    def __init__(self):
        self.vector_db = VectorDB()
        self.embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        
    async def upload_files(self, fileType : FileType, file : UploadFile):
        update_files_list = {FileType.FAQ, FileType.INFORMATION}

        file_bytes = await file.read()
        
        text = self._extract_text(
            file_bytes=file_bytes, filename=file.filename
        )

        if not text.strip():
            raise ValueError("No text could be extracted from file")

        chunks = self._chunk_text(text)

        if not chunks:
            raise ValueError("No chunks generated from file")

        embeddings = self.embedding_model.encode(
            chunks,
            normalize_embeddings=True
        )

        file_id = str(uuid4())
        vectors = []

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            vectors.append({
                "id": f"{file_id}-{index}",
                "values": embedding.tolist(),
                "metadata":{
                    "file_id": file_id,
                    "file_name": file.filename,
                    "file_type": fileType.name,
                    "chunk_index": index,
                    "text": chunk
                }
            })
        
        if(fileType in update_files_list):
            self.vector_db.insert_vectors(vectors=vectors)
            return True

        self.vector_db.delete_namespace()
        self.vector_db.insert_vectors(vectors=vectors)
        return True

    async def search_vectors(self, query: str):
        embeddings = self.embedding_model.encode(
                    query,
                    normalize_embeddings=True
                ).tolist()
        return self.vector_db.search_vectors(embeddings, 10)

    def _extract_text(self, file_bytes : bytes, filename : str):
        extension = Path(filename).suffix.lower()
    
        if extension == '.txt':
            return file_bytes.decode("utf-8")

        if extension == ".pdf":
            return self._extract_pdf(file_bytes)

        if extension == ".docx":
            return self._extract_docx(file_bytes)

        raise ValueError("Unsupported file type")


    def _extract_pdf(self, file_bytes : bytes) -> str:
        reader = PdfReader(io.BytesIO(file_bytes))

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return "\n".join(text)

    def _extract_docx(self, file_bytes : bytes) -> str:
        document = Document(
            io.BytesIO(file_bytes)
        )

        text = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)

        return "\n".join(text)

    def _chunk_text(self, text : str, chunk_size : int = 800, chunk_overlap : int = 100) -> list[str] :
        text = " ".join(text.split())
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += chunk_size - chunk_overlap

        return chunks