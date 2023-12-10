from decimal import Decimal
from pydantic import BaseModel


class GenerateSubcategoriesRequest(BaseModel):
    category_title: str
    count: int
    additional_prompt: str = ""


class GenerateProductsRequest(BaseModel):
    category_title: str
    count: int
    additional_prompt: str


class ModelGenerationPrompt(BaseModel):
    object_type: type[BaseModel]
    object_description: str
    example: BaseModel | None = None
    count: int
    additional_prompt: str = ""
    # TODO add already existing objects as examples


class Category(BaseModel):
    slug: str
    title: str


class Nutrition(BaseModel):
    proteins: float
    fats: float
    carbohydrates: float
    energy: int


class Product(BaseModel):
    title: str
    description: str
    price: Decimal
    best_before: int
    nutrition: Nutrition
    weight: int


product_fields: list[str] = [
    "title (str)",
    "description (str)",
    "price (in rubles, float)",
    "weight (in grams, int)",
    "best_before (recommended to eat after opening, in days, int)"
    "nutrition: {energy (float), protein (float), fat (float), carbohydrates (float)}",
]

category_fields: list[str] = [
    "slug (e.g. apples, if need to use two words use '-' as divider)",
    "title (e.g. 'Apples')",
]
