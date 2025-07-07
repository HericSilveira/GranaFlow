from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from Core.database import Base

class users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255), unique=True)