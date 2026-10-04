import os
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

class LLMClient:

    async def generate(self,
        model : str, 
        system_prompt: str, 
        user_query: str, 
        context: str, 
        histories : list[dict]):

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            *histories,
            {
                "role": "user",
                "content": f"""
                Context : 
                {context}

                User Question:
                {user_query}
                """
            }
        ]

        response = await groq_client.chat.completions.create(
            model = model,
            messages=messages
        )

        return response
    