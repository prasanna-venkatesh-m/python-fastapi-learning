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
        histories : list[dict],
        response_format = None,
        ):

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

        kwargs = {
        "model": model,
        "messages": messages,
        }

        if response_format is not None:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "evaluation_result",
                    "schema": response_format.model_json_schema(),
                    "strict": False,
                },
            }

        response = await groq_client.chat.completions.create(**kwargs)

        return response
    