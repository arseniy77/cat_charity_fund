# app/models/meeting_room.py

# Импортируем из Алхимии нужные классы.
from sqlalchemy import Column, ForeignKey, String, Text, Integer
from sqlalchemy.orm import relationship

# Импортируем базовый класс для моделей.
from app.core.db import Base, DonationMixin


class Donation(Base, DonationMixin):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
