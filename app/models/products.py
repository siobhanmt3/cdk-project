from pydantic import BaseModel


class CreateProduct(BaseModel):
    user_token: str
    name: str
    description: str
    category: str


class UpdateProduct(BaseModel):
    name: str
    description: str
    category: str
