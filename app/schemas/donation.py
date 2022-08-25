from datetime import datetime, timedelta

from pydantic import BaseModel, Extra, Field, root_validator, validator
from typing import Optional

from app.services.converters import (
    convert_datetime_to_iso_8601_with_z_suffix as datetime_converter
)


FROM_TIME = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class DonationBase(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]



class DonationCreate(DonationBase):

    class Config:
        extra = Extra.forbid


class DonationDB(DonationBase):
    id: int
    # Добавьте опциональное поле user_id.
    # user_id: Optional[int]
    create_date: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: datetime_converter
        }

