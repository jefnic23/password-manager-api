from backend.database import BaseSchema


class CreateServiceRequest(BaseSchema):
    name: str
