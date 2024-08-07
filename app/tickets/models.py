from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    func,
    DateTime,
    FetchedValue,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Location(Base):
    __tablename__ = "location"

    id: int = Column(Integer, primary_key=True, server_default=FetchedValue())
    name: str = Column(String(length=64), unique=True)
    address: str = Column(String(length=128))
    slug: str = Column(String(length=64), unique=True)

    class Config:
        from_attributes = True


class Regularity(Base):
    __tablename__ = "regularity"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=64), unique=True)

    class Config:
        from_attributes = True


class Ticket(Base):
    __tablename__ = "ticket"

    id: int = Column(Integer, primary_key=True, server_default=FetchedValue())
    header: str = Column(String(length=128), nullable=False)
    text: str = Column(String(length=512))
    location: int = Column(
        Integer, ForeignKey("location.id"), nullable=False, onupdate="CASCADE"
    )
    regularity: int = Column(
        Integer, ForeignKey("regularity.id"), nullable=False, onupdate="CASCADE"
    )
    manager: int = Column(
        Integer, ForeignKey("user.id"), nullable=False, onupdate="CASCADE"
    )
    updated: int = Column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )
    complaint: bool = Column(Boolean, default=False, server_default=FetchedValue())

    class Config:
        from_attributes = True
