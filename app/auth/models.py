from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    MetaData,
    FetchedValue,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = MetaData()


class Role(Base):
    __tablename__ = "role"

    id: int = Column(Integer, primary_key=True, server_default=FetchedValue())
    name: str = Column(String(length=64), nullable=False)

    class Config:
        from_attributes = True


class User(Base):
    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True, server_default=FetchedValue())
    first_name: str = Column(String(length=64))
    last_name: str = Column(String(length=64))
    user_name: str = Column(String(length=64))
    hashed_password: str = Column(String(length=1024), nullable=False)
    role: int = Column(
        Integer, ForeignKey("role.id"), nullable=False, onupdate="CASCADE"
    )
    is_active: bool = Column(
        Boolean, default=True, nullable=False, server_default=FetchedValue()
    )
    is_superuser: bool = Column(
        Boolean, default=False, nullable=False, server_default=FetchedValue()
    )

    class Config:
        from_attributes = True
