from langchain.tools import tool
from demo_fast_api.services.file_service import FileService
from langchain_tavily import TavilySearch, TavilyResearch

@tool
def search_documents(query : str):
    """Search the vector database for documents relevant
    to the user's question.

    Use this tool when answering requires information from
    uploaded documents or the application's knowledge base.
    The query should be a focused semantic search query.
    """
    return FileService.search_vectors(query=query)

@tool
def search_transport(query: str) -> str:
    """Search the web for transport information in India.

    Include origin, destination, travel date, and transport mode
    in the query when relevant. Results are not confirmed schedules.
    """
    search = TavilySearch(max_results=5)
    results = search.invoke({"query": query})
    return str(results)