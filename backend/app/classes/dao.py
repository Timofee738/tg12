from app.classes.model import Classes
from app.dao.base import BaseDao

from app.database import async_session

from datetime import time, datetime
from sqlalchemy import select

class ClassesDao(BaseDao):
    model = Classes
    
    @classmethod
    async def get_busy_slots_for_day(cls, target_date: datetime.date):
        async with async_session() as session:
            start_datetime = datetime.combine(target_date, time.min)
            end_datetime = datetime.combine(target_date, time.max)

            query = select(Classes).where(
                Classes.lesson_timestamp >= start_datetime,
                Classes.lesson_timestamp <= end_datetime,
                Classes.reserved == True
            )

            result = await session.execute(query)
            lessons = result.scalars().all()
            return [
                {
                    "time": lesson.lesson_timestamp.strftime("%H:%M"),
                    "user_id": lesson.user_id
                }
                for lesson in lessons
            ]
            
    @classmethod
    async def check_slot_busy(cls, timestamp: datetime) -> bool:
        async with async_session() as session:
            query = (
                select(Classes).where(
                    Classes.lesson_timestamp==timestamp,
                    Classes.reserved==True
                )
            )
            result = await session.execute(query)
            return result.scalar_one_or_none() is not None