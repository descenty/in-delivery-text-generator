from dotenv import load_dotenv
from faststream.rabbit import RabbitBroker
from os import getenv
from llama.generator import generate_json_response

from schemas import Category, GenerateSubcategoriesRequest, ModelGenerationPrompt

load_dotenv()

broker = RabbitBroker(getenv("RABBITMQ_HOST"))


@broker.subscriber("generate-subcategories")
async def generate_subcategories(message: GenerateSubcategoriesRequest):
    json_response = generate_json_response(
        ModelGenerationPrompt(
            object_type=Category,
            object_description=f"subcategories for '{message.category_title}' category",
            additional_prompt=message.additional_prompt,
            example=Category(slug="fruits-vegetables", title="Fruits and Vegetables"),
            count=message.count,
        )
    )
    for entry in json_response:
        entry["slug"] = entry["slug"].replace("_", "-")
        entry["title"] = entry["title"].capitalize()

    return json_response


# @rabbit_router.subscriber("generate-subcategories")
# async def generate_subcategories(message: GenerateSubcategoriesRequest):
#     data = {
#         "messages": [
#             {
#                 "role": "system",
#                 "content": 'you are a json-generator, generate response as json array of objects\njson schema: {"slug": string, "title": string}, for example {"slug": "fruits-vegetables", "title": "Fruits and Vegetables"}\ndo not write any other words or introduction\ndo not use any escape-sequences like \\n newline character, just raw json format\n',
#             },
#             {
#                 "role": "user",
#                 "content": f"generate only {message.count} subcategory objects for '{message.category_title}' category",
#             },
#         ],
#         "temperature": 0.3,
#         "max_tokens": -1,
#         "stream": False,
#     }
#     print(data)
#     async with AsyncClient() as client:
#         response = await client.post(
#             f"{getenv('OPENAI_BASE_URL')}/v1/chat/completions",
#             headers={"Content-Type": "application/json"},
#             json=data,
#             timeout=1000,
#         )
#         return loads(response.json()["choices"][0]["message"]["content"])
