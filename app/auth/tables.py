from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Table,
    ForeignKey,
    Boolean,
    FetchedValue,
    MetaData,
)

metadata = MetaData()

user_table = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, server_default=FetchedValue()),
    Column("first_name", String(length=64), nullable=False),
    Column("last_name", String(length=64), nullable=False),
    Column("user_name", String(length=64), nullable=False),
    Column("text", String(length=512)),
    Column("hashed_password", String(length=1024), nullable=False),
    Column("role", Integer, ForeignKey("role.id"), nullable=False, onupdate="CASCADE"),
    Column(
        "is_active",
        Boolean,
        default=True,
        nullable=True,
        server_default=FetchedValue(),
    ),
    Column(
        "is_superuser",
        Boolean,
        default=False,
        nullable=True,
        server_default=FetchedValue(),
    ),
)


role_table = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True, server_default=FetchedValue()),
    Column("name", String(length=64), nullable=False),
)
