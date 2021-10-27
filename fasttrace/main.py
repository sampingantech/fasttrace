import random
import asyncio
import os

from fastapi import FastAPI, Depends
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from sqlmodel import create_engine, SQLModel, Session, select as select_sync
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm.session import sessionmaker
from databases import Database
from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor

from . import tracing
from .models import Hero, HeroAsync

hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

#  async sqlite
engine = create_async_engine("sqlite+aiosqlite:///database.db")
engine_sync = create_engine("sqlite:///database.db")
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# asyncpg databases
# directly see endpoint implementation


# Dependable
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


# instrument asyncpg
AsyncPGInstrumentor().instrument()

# instrument sql alchemy
# uncomment either for async or sync sqlalchemy engine
SQLAlchemyInstrumentor().instrument(
    engine=engine_sync,
)
# SQLAlchemyInstrumentor().instrument(
#     engine=engine.sync_engine,
# )


create_rows = False

if create_rows:
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.commit()


# uncomment this to create sqlite table
# SQLModel.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@tracing.instrument("calling get_name")
async def get_name():
    return "your name"


@tracing.instrument_sync("calling get_name_sync")
def get_name_sync():
    return "your name sync"


@tracing.instrument("calling process csv file")
async def process_csv():
    await asyncio.sleep(0.01)


@app.get("/name")
async def name():
    for i in range(0, random.randint(1, 5)):
        name = await get_name()
    name2 = get_name_sync()
    return {"name": name, "name2": name2}


@app.get("/hero")
async def get_hero():
    with Session(engine_sync) as session:
        statement = select_sync(Hero).where(Hero.name == "Spider-Boy")
        hero = session.exec(statement).first()
        return hero


@app.get("/hero-sqlalchemy")
async def get_hero(
    session: AsyncSession = Depends(get_session),
):
    await get_name()
    await process_csv()
    statement = select(HeroAsync).where(HeroAsync.name == "Spider-Boy")
    result = await session.execute(statement)
    hero = result.scalars().one()
    return hero


@app.get("/hero-asyncpg")
async def get_hero_asyncpg():
    async with Database(os.environ["DATABASE_URL"]) as db:
        query = select(HeroAsync).where(HeroAsync.name == "Spider-Boy")
        data = await db.fetch_one(query)
        return data


# auto instrument api
FastAPIInstrumentor.instrument_app(app)
