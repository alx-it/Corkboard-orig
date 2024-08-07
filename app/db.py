import databases
from sqlalchemy import create_engine
from app.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"


database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
