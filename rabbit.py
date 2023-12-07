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
                "content": 'you are a json-generator, generate response as json array of objects\njson schema: {"slug": string, "title": string}, for example {"slug": "fruits-vegetables", "title": "Fruits and Vegetables"}\ndo not write any other words or introduction\ndo not use any escape-sequences like \\n newline character, just raw json format\n',
            },
            {
                "role": "user",
                "content": f"generate only {message.count} subcategory objects for '{message.category_title}' category",
            },
        ],
        "temperature": 0.3,
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
