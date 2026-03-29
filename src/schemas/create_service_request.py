from src.database import BaseSchema


class CreateServiceRequest(BaseSchema):
    name: str
