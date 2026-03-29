from src.database import BaseSchema


class ServiceCredentials(BaseSchema):
    username: str
    password: str
