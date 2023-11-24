from pydantic import BaseModel


class GenerateProductsRequest(BaseModel):
    category_title: str
    count: int
