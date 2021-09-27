from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Methods(BaseModel):
    date: datetime
    name: str
    comment: Optional[str] = None
    media: str
    surfactant: Optional[str] = None
    conc: Optional[str] = None
    volume: Optional[int] = None
    apparatus: Optional[str] = None
    speed: int
    N: int


class Batches(BaseModel):
    batchNumber: str
    values: list[list[int]]


class MethodsUpdate(BaseModel):
    date: Optional[datetime]
    name: Optional[str]
    comment: Optional[str]
    media: Optional[str]
    surfactant: Optional[str]
    conc: Optional[str]
    volume: Optional[int]
    apparatus: Optional[str]
    speed: Optional[int]
    N: Optional[int]



