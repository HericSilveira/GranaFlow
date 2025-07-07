from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
import os

engine = create_engine(f"postgresql://{os.getenv('USER', "")}:{os.getenv('PASSWORD', "")}@{os.getenv('HOST', "")}:{os.getenv('PORT', "")}/{os.getenv('DATABASE', "")}")

class Base(DeclarativeBase):
    pass
