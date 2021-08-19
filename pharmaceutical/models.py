from sqlalchemy import Column, Integer, String, DATE, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Methods(Base):
    __tablename__ = "Methods"

    id = Column(Integer, primary_key=True)
    date = Column(DATE)
    name = Column(String)
    comment = Column(String, nullable=True)
    media = Column(String)
    surfactant = Column(String, nullable=True)
    conc = Column(String, nullable=True)
    volume = Column(Numeric(12, 2), nullable=True)
    apparatus = Column(String, nullable=True)
    speed = Column(Integer)
    N = Column(Integer)

    batches = relationship(
        "Batches", cascade='all,delete', back_populates="method")


class Batches(Base):
    __tablename__ = "Batches"

    id = Column(Integer, primary_key=True)
    batchNumber = Column(String)
    timeIntervals = Column(String)
    measurement = Column(String)
    methodId = Column(Integer, ForeignKey(
        "Methods.id", ondelete='CASCADE'), nullable=False)

    method = relationship(
        "Methods", back_populates="batches", passive_deletes=True)
