from sqlite3 import Timestamp
import string
from typing import Text
from sqlalchemy import Boolean, Column, Date, Integer, String, Time, column, ForeignKey, BigInteger
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base


class admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String,  nullable=False)
    phone = Column(BigInteger, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class subadmin(Base):
    __tablename__ = "subadmin"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String,  nullable=False)
    phone = Column(BigInteger,  nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey(
        "admin.id", ondelete="CASCADE"), nullable=False)
    access = Column(String,  nullable=False, server_default="1")
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class user(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String,  nullable=False)
    phone = Column(BigInteger,  nullable=False, unique=True)
    password = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey(
        "clients.id", ondelete="CASCADE"), nullable=False)
    created_by = Column(Integer, ForeignKey(
        "admin.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))


class bay(Base):
    __tablename__ = "bay"

    id = Column(Integer, primary_key=True, nullable=False)
    bay_name = Column(String, nullable=False, unique=True)
    product_id = Column(Integer, ForeignKey(
        "products.id", ondelete="CASCADE"), nullable=False)
    #no_of_slots = Column(Integer , nullable= False)


class slots(Base):
    __tablename__ = "slots"
    id = Column(Integer, primary_key=True, nullable=False)
    truck = Column(String,  nullable=False)
    phone = Column(BigInteger, ForeignKey(
        "user.phone", ondelete="CASCADE"), nullable=False)
    bay_id = Column(Integer, ForeignKey(
        "bay.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey(
        "products.id", ondelete="CASCADE"), nullable=False)
    client_id = Column(Integer, ForeignKey(
        "clients.id", ondelete="CASCADE"), nullable=False)
    slot_date = Column(Date, nullable=False)
    slot_time = Column(Time, nullable=False)
    status = Column(Boolean, nullable=False, server_default=Text(True))
    booked_at = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=text("now()"))


class products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, nullable=False)
    product = Column(String, nullable=False)
    minutes = Column(Integer, nullable=False, server_default=Text(60))


class clients(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, nullable=False)
    client = Column(String, nullable=False)


class clients_products(Base):
    __tablename__ = "clients_products"
    id = Column(Integer, primary_key=True, nullable=False)
    client_id = Column(Integer, ForeignKey(
        "clients.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey(
        "products.id", ondelete="CASCADE"), nullable=False)


class slot_60(Base):
    __tablename__ = "slot_60"

    id = Column(Integer, primary_key=True, nullable=False)
    slot = Column(Time, nullable=False, unique=True)
    booked = Column(Boolean, nullable=False, server_default=Text(False))


class slot_30(Base):
    __tablename__ = "slot_30"

    id = Column(Integer, primary_key=True, nullable=False)
    slot = Column(Time, unique=True, nullable=False)
    booked = Column(Boolean, nullable=False, server_default=Text(False))


class month(Base):
    __tablename__ = "month"

    id = Column(Integer, primary_key=True, nullable=False)
    working = Column(Boolean, nullable=False)
    date = Column(Date, unique=True, nullable=False)
    E = Column(Boolean, nullable=False, server_default=Text(False))


class days_10(Base):
    __tablename__ = "days_10"

    id = Column(Integer, primary_key=True, nullable=False)
    bay_id = Column(Integer, ForeignKey(
        "bay.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, ForeignKey(
        "month.date", ondelete="CASCADE"), nullable=False)
    slot = Column(Time, nullable=False)
    booked = Column(Boolean, nullable=False, server_default=Text(False))
