# app/schemas/meeting_room.py

from typing import Optional

from pydantic import BaseModel, Field, validator

from datetime import datetime

from app.services.converters import (
    convert_datetime_to_iso_8601_with_z_suffix as datetime_converter
)

class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(...)
    full_amount: int = Field(gt=0)


# Новый класс для обновления объектов.
class CharityProjectUpdate(CharityProjectBase):
    full_amount: Optional[int] = Field(None, ge=0)

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError(
                'Имя проекта не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectBase):
    id: int

    class Config:
        orm_mode = True


class CharityProjectResponse(CharityProjectBase):

    full_amount: int
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: datetime_converter
        }