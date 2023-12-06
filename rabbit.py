from json import loads
from faststream.rabbit.fastapi import RabbitRouter
from os import getenv

from httpx import AsyncClient

from schemas import GenerateSubcategoriesRequest, category_fields

rabbit_router = RabbitRouter(getenv("RABBITMQ_HOST"))


@rabbit_router.subscriber("generate-subcategories")
async def generate_subcategories(message: GenerateSubcategoriesRequest):
    data = {
        "messages": [
            {
                "role": "system",
                "content": f"generate as json array of objects with fields: {', '.join(category_fields)}\nyou need to generate only what the user needs in json format",
            },
            {
                "role": "user",
                "content": f"generate only {message.count} subcategory objects for '{message.category_title}' category",
            },
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False,
    }
    print(data)
    async with AsyncClient() as client:
        response = await client.post(
            f"{getenv('OPENAI_BASE_URL')}/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json=data,
            timeout=1000,
        )
        return loads(response.json()["choices"][0]["message"]["content"])
