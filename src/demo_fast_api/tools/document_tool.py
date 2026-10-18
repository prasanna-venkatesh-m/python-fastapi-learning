from langchain.tools import tool
from demo_fast_api.services.file_service import FileService

@tool
def search_documents(query : str):
    """Search the vector database for documents relevant
    to the user's question.

    Use this tool when answering requires information from
    uploaded documents or the application's knowledge base.
    The query should be a focused semantic search query.
    """
    return FileService.search_vectors(query=query)