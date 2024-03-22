from sqlalchemy import select, insert

from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id = model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()


    @classmethod
    async def find_one_or_none(cls,**kwargs):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**kwargs)
            result = await session.execute(query)
            return result.mappings().one_or_none()


    @classmethod
    async def find_all(cls,**kwargs):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**kwargs)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **date):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**date)
            await session.execute(query)
            await session.commit()
