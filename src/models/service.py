from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.user import User


class Service(SQLModel, table=True):
    __tablename__ = "services"
    __table_args__ = (UniqueConstraint("name", "user_id", name="uq_service_name_user"),)

    id: int = Field(primary_key=True)
    name: str
    password: str

    user_id: int = Field(foreign_key="users.id")
    user: "User" = Relationship(back_populates="services")
