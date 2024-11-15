from typing import Annotated
from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, BigInteger, func, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


id = Annotated(Mapped[int], mapped_column(primary_key=True, autoincrement=True))


class Rooms(Base):
    __tablename__ = "rooms"

    id = id
    number_room:  Mapped[str] = mapped_column(String(10), nullable=False, unique=True)


class Users(Base):
    __tablename__ = "users"

    id = id
    first_name: Mapped[str] = mapped_column(String(10))
    last_name: Mapped[str] = mapped_column(String(10))
    id_number_room: Mapped[int] = mapped_column(ForeignKey(column="room.id", ondelete="CASCADE"), nullable=False)

    number_room: Mapped["Rooms"] = relationship(backref="users")


class Schedule(Base):
    __tablename__ = "schedule"

    id = id
    time: Mapped[DateTime] = mapped_column(nullable=False)
    date: Mapped[Date] = mapped_column(nullable=False, unique=True)
    id_room: Mapped[int] = mapped_column(ForeignKey(column="room.id", ondelete="CASCADE"), nullable=False)

    number_room: Mapped["Rooms"] = relationship(backref="rooms")