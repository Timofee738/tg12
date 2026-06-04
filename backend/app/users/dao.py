from app.dao.base import BaseDao
from app.users.model import Users

from sqlalchemy import update

from app.database import async_session


class UsersDao(BaseDao):
    model = Users
    
    @classmethod
    async def edit_acception(cls, tg_id, new_status):
        async with async_session() as session:
            query = update(Users).where(Users.tg_id == tg_id).values(accepted=new_status)
            
            await session.execute(query)
            await session.commit()
    