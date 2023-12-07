from pydantic import BaseModel


class GenerateSubcategoriesRequest(BaseModel):
    category_title: str
    count: int


class GenerateProductsRequest(BaseModel):
    category_title: str
    count: int


class ModelGenerationPrompt(BaseModel):
    object_type: type[BaseModel]
    object_description: str
    example: BaseModel
    count: int


class Category(BaseModel):
    slug: str
    title: str


product_fields: list[str] = [
    "title (str)",
    "description (str)",
    "price (in rubles, float)",
    "weight (in grams, int)",
    "days_to_eat (recommended to eat after opening, in days, int)"
    "nutrition: {energy (float), protein (float), fat (float), carbohydrates (float)}",
]

category_fields: list[str] = [
    "slug (e.g. apples, if need to use two words use '-' as divider)",
    "title (e.g. 'Apples')",
]
