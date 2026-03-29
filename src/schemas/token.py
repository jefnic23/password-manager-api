from src.database import BaseSchema


class Token(BaseSchema):
    access_token: str
    token_type: str
    refresh_token: str
