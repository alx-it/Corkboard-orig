from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Table,
    ForeignKey,
    Boolean,
    func,
    FetchedValue,
    MetaData
)

metadata = MetaData()

ticket_table = Table(
    "ticket",
    metadata,
    Column("id", Integer, primary_key=True, server_default=FetchedValue()),
    Column("header", String(length=128), nullable=False),
    Column("text", String(length=512)),
    Column(
        "location",
        Integer,
        ForeignKey("location.id"),
        nullable=False,
        onupdate="CASCADE",
    ),
    Column(
        "regularity",
        Integer,
        ForeignKey("regularity.id"),
        nullable=False,
        onupdate="CASCADE",
    ),
    Column(
        "manager", Integer, ForeignKey("user.id"), nullable=False, onupdate="CASCADE"
    ),
    Column(
        "updated",
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    ),
    Column("complaint", Boolean, default=False, server_default=FetchedValue()),
)

location_table = Table(
    "location",
    metadata,
    Column("id", Integer, primary_key=True, server_default=FetchedValue()),
    Column("name", String(length=64), nullable=False),
    Column("address", String(length=128), nullable=False),
    Column("slug", String(length=64), unique=True, nullable=False),
)


regularity_table = Table(
    "regularity",
    metadata,
    Column("id", Integer, primary_key=True, server_default=FetchedValue()),
    Column("name", String(length=64), unique=True, nullable=False),
)
