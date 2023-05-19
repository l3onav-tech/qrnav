from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Uuid, DateTime
from sqlalchemy.sql import func as function
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.settings.database import Base
import uuid

class TapModel(Base):
    __tablename__ = "tap"
    
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name = Column(String)
    qr_url = Column(String, unique=True)
    note = Column(String)
    created_at = Column(DateTime, server_default=function.now())
    updated_at = Column(DateTime, onupdate=function.now())

    user: Mapped["User"] = relationship(back_populates="taps")
