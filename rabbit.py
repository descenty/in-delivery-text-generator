from dotenv import load_dotenv
from faststream.rabbit import RabbitBroker
from os import getenv
from llama.generator import generate_json_response

from schemas import (
    Category,
    GenerateProductsRequest,
    GenerateSubcategoriesRequest,
    ModelGenerationPrompt,
    Product,
)

load_dotenv()

broker = RabbitBroker(getenv("RABBITMQ_HOST"))


@broker.subscriber("generate-subcategories")
async def generate_subcategories(message: GenerateSubcategoriesRequest):
    json_response = generate_json_response(
        ModelGenerationPrompt(
            object_type=Category,
            object_description=f"subcategories for '{message.category_title}' category",
            additional_prompt=f"Write in English. For a grocery store. {message.additional_prompt}",
            example=Category(slug="fruits-vegetables", title="Fruits and Vegetables"),
            count=message.count,
        )
    )
    for entry in json_response:
        entry["slug"] = entry["slug"].replace("_", "-").lower()
        entry["title"] = entry["title"].capitalize()
    print(json_response)
    return json_response


@broker.subscriber("generate-products")
async def generate_products(message: GenerateProductsRequest):
    additional_prompt = f"Write in English. For a grocery store. \
        Write the price in Russian rubles. Weight in grams. Best before in days. \
            {message.additional_prompt}"
    json_response = generate_json_response(
        ModelGenerationPrompt(
            object_type=Product,
            object_description=f"products for '{message.category_title}' category",
            additional_prompt=additional_prompt,
            count=message.count,
        )
    )
    for entry in json_response:
        entry["title"] = entry["title"].capitalize()
        entry["description"] = entry["description"].capitalize()
    print(json_response)
    return json_response
