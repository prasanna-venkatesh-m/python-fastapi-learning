import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


class LangChainClient:
    def __init__(self):
        model_kwargs = {
            "model": os.getenv("LLM_MODEL", "openai/gpt-oss-120b"),
            "api_key": os.getenv("OPENAI_API_KEY"),
            "temperature": 0,
        }

        base_url = os.getenv("OPENAI_BASE_URL")
        if base_url:
            model_kwargs["base_url"] = base_url

        self.llm = ChatOpenAI(**model_kwargs)

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