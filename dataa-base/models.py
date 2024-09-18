
# Создание таблиц в базе с помощью python


from datetime import datetime
from sqlalchemy import DateTime, Float, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    date_insert: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now().date())
    # updated: Mapped[DateTime] = mapped_column(DateTime, 
    #                                           default=datetime.now().date(), 
    #                                           onupdate=datetime.now().date())

    
class Product(Base):
    __tablename__ = 'test_tele'

    order_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)


