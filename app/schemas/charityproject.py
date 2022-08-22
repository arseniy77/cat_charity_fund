# app/schemas/meeting_room.py

from typing import Optional

from pydantic import BaseModel, Field, validator

TIME = '2022-04-24T11:00'

class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(...)
    full_amount: int = Field(gt=0)


# Новый класс для обновления объектов.
class CharityProjectUpdate(CharityProjectBase):

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError(
                'Имя переговорки не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectBase):
    id: int

    class Config:
        orm_mode = True