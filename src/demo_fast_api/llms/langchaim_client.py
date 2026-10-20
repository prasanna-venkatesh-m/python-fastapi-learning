import os

from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage
from langchain.agents import create_agent

from demo_fast_api.tools.document_tool import (
    search_documents,
    search_transport,
)


class LangChainClient:
    def __init__(self):
        self.llm = ChatGroq(
            model=os.getenv("LLM_MODEL", "openai/gpt-oss-120b"),
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0,
        )   

        self.tools = [
            search_documents,
            search_transport,
        ]

    def build_chain(self, system_prompt: str):
        return create_agent(
            model=self.llm,
            tools=[search_documents, search_transport],
            system_prompt=system_prompt,
        )

    async def generate(
        self,
        system_prompt: str,
        user_query: str,
        context: str = "",
        histories=None,
    ):
        agent = self.build_chain(system_prompt)

        message = user_query
        if context:
            message = f"Context:\n{context}\n\nQuestion:\n{user_query}"

        result = await agent.ainvoke({
            "messages": [
                *(histories or []),
                {"role": "user", "content": message},
            ]
        })

        return result["messages"][-1].content