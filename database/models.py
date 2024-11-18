from sqlalchemy import DateTime, ForeignKey, String, func, Date, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_chat: Mapped[int] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(10))
    last_name: Mapped[str] = mapped_column(String(10))
    id_room: Mapped[int] = mapped_column(ForeignKey(column="rooms.id", ondelete="CASCADE"))

    number: Mapped["Rooms"] = relationship(backref="users")


class Schedule(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time: Mapped[Time] = mapped_column(Time, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    id_room: Mapped[int] = mapped_column(ForeignKey(column="rooms.id", ondelete="CASCADE"), nullable=False)

    number: Mapped["Rooms"] = relationship(backref="schedule")