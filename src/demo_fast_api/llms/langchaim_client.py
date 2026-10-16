import os

from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class LangChainClient:
    def __init__(self):
        self.llm = ChatGroq(
            model=os.getenv("LLM_MODEL", "openai/gpt-oss-120b"),
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0,
        )

    def build_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "{system_prompt}\n\n"
                "Use the following retrieved context to answer "
                "the user's question:\n\n{context}"
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{user_query}"),
        ])

        return prompt | self.llm | StrOutputParser()

    async def generate(
        self,
        system_prompt: str,
        user_query: str,
        context: str,
        histories: list[BaseMessage] | None = None,
    ) -> str:
        chain = self.build_chain()

        return await chain.ainvoke({
            "system_prompt": system_prompt,
            "user_query": user_query,
            "context": context,
            "history": histories or [],
        })
