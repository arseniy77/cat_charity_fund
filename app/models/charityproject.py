# app/models/meeting_room.py

# Импортируем из Алхимии нужные классы.
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

# Импортируем базовый класс для моделей.
from app.core.db import Base, DonationMixin


class CharityProject(Base, DonationMixin):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
