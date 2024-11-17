from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, BigInteger, func, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_chat: Mapped[int] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(10))
    last_name: Mapped[str] = mapped_column(String(10))
    id_room: Mapped[int] = mapped_column(ForeignKey(column="rooms.id", ondelete="CASCADE"))

    room: Mapped["Rooms"] = relationship(backref="users")


class Schedule(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False, unique=True)
    id_room: Mapped[int] = mapped_column(ForeignKey(column="rooms.id", ondelete="CASCADE"), nullable=False)

    room: Mapped["Rooms"] = relationship(backref="schedule")