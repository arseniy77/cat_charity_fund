# app/models/meeting_room.py

# Импортируем из Алхимии нужные классы.
from sqlalchemy import Column, ForeignKey, String, Text, Integer
from sqlalchemy.orm import relationship

# Импортируем базовый класс для моделей.
from app.core.db import Base, DonationMixin


class Donation(Base, DonationMixin):
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    comment = Column(Text)
    # Установите связь между моделями через функцию relationship.
    invested_amount = Column(Integer, default=0)
    charityproject_id = Column(Integer, ForeignKey('charityproject.id'))
