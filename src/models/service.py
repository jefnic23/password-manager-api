from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.user import User


class Service(SQLModel, table=True):
    __tablename__ = "services"

    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    password: str

    user_id: int = Field(foreign_key="users.id")
    user: "User" = Relationship(back_populates="services")
