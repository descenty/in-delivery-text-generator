from json import dumps, loads
# from aiohttp import ClientSession
from fastapi import FastAPI
from rabbit import rabbit_router
from os import getenv
from dotenv import load_dotenv

from schemas import GenerateProductsRequest, GenerateSubcategoriesRequest

load_dotenv()

product_fields = [
    "title (str)",
    "description (str)",
    "price (in rubles, float)",
    "weight (in grams, int)",
    "days_to_eat (recommended to eat after opening, in days, int)"
    "nutrition: {energy (float), protein (float), fat (float), carbohydrates (float)}",
]


app = FastAPI(lifespan=rabbit_router.lifespan_context)


@app.post("/generate-subcategories")
async def generate_subcategories(request: GenerateSubcategoriesRequest):
    pass


@app.post("/generate-products")
async def generate_products(request: GenerateProductsRequest):
    async with ClientSession() as session:
        async with session.post(
            f"{getenv('OPENAI_BASE_URL')}/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            data=dumps(
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": f"generate as json array of objects with fields: {', '.join(product_fields)}",
                        },
                        {
                            "role": "user",
                            "content": f"{request.count} products for '{request.category_title}' category",
                        },
                    ],
                    "temperature": 0.7,
                    "max_tokens": -1,
                    "stream": False,
                }
            ),
        ) as response:
            return loads((await response.json())["choices"][0]["message"]["content"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", reload=True)
