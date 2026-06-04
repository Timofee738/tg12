from app.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, Boolean



class Users(Base):
    __tablename__ = 'users'
    
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tg_usname: Mapped[str] = mapped_column(nullable=False, unique=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    
    is_tutor: Mapped[bool] = mapped_column(default=False)
    accepted: Mapped[bool] = mapped_column(default=False)
    
    