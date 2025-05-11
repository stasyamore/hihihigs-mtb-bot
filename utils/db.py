import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = 'sqlite+aiosqlite:///users.db'

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    userid = sa.Column(sa.BigInteger, unique=True, nullable=False)  # Telegram user id
    username = sa.Column(sa.String, nullable=False) # Telegram username
    tutrocode = sa.Column(sa.String, nullable=True)  # Код преподавателя
    subscribe = sa.Column(sa.String, nullable=True)  # Имя преподавателя, на которого подписан слушатель
    extra = sa.Column(sa.String, nullable=True)      # Доп. колонка
    role = sa.Column(sa.String, nullable=False)      # "teacher" или "student"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 