from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str
