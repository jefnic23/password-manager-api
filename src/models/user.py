from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.refresh_token import RefreshToken
    from models.service import Service


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    email: str = Field(unique=True)
    password: str

    refresh_token: Optional["RefreshToken"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"uselist": False}
    )
    services: list["Service"] = Relationship(back_populates="user")
