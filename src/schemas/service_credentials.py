from backend.database import BaseSchema


class ServiceCredentials(BaseSchema):
    username: str
    password: str
