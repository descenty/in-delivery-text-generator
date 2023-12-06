from json import loads
from faststream.rabbit.fastapi import RabbitRouter
from os import getenv

from httpx import AsyncClient

from schemas import GenerateSubcategoriesRequest, category_fields

rabbit_router = RabbitRouter(getenv("RABBITMQ_HOST"))


@rabbit_router.subscriber("generate-subcategories")
async def generate_subcategories(message: GenerateSubcategoriesRequest):
    async with AsyncClient() as client:
        response = await client.post(
            f"{getenv('OPENAI_BASE_URL')}/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            data={
                "messages": [
                    {
                        "role": "system",
                        "content": f"generate as json array of objects with fields: {', '.join(category_fields)}",
                    },
                    {
                        "role": "user",
                        "content": f"{message.count} subcategories for '{message.category_title}' category",
                    },
                ],
                "temperature": 0.7,
                "max_tokens": -1,
                "stream": False,
            },
        )
        print(response)
        # print(loads((await response.json())["choices"][0]["message"]["content"]))
