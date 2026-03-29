from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.user import User


class RefreshToken(SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    id: int = Field(primary_key=True)
    token: str
    expiry_time: datetime = Field(sa_column=Column(DateTime(timezone=True)))

    user_id: int = Field(foreign_key="users.id", unique=True)
    user: "User" = Relationship(back_populates="refresh_token")
