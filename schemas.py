from pydantic import BaseModel


class GenerateSubcategoriesRequest(BaseModel):
    category_title: str
    count: int


class GenerateProductsRequest(BaseModel):
    category_title: str
    count: int


product_fields: list[str] = [
    "title (str)",
    "description (str)",
    "price (in rubles, float)",
    "weight (in grams, int)",
    "days_to_eat (recommended to eat after opening, in days, int)"
    "nutrition: {energy (float), protein (float), fat (float), carbohydrates (float)}",
]

category_fields: list[str] = [
    "slug (e.g. fruits-vegetables)",
    "title (e.g. 'Vegetables, fruits, nuts')"
]
