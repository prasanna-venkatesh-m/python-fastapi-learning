from langchain.tools import tool
from demo_fast_api.services.file_service import FileService

@tool
def search_documents(query : str):
    """Search documents relevant to the user's question.
    It is using the Vector Db for similarity search"""
    return FileService.search_vectors(query=query)