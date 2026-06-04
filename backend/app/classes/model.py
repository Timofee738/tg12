from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey, DateTime

from datetime import datetime



class Classes(Base):
    __tablename__ = 'classes'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    lesson_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    
    reserved: Mapped[bool] = mapped_column(default=False)
    
    user_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey('users.tg_id'), nullable=True)
    
    