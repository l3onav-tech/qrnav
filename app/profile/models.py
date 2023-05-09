from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.settings.database import Base

class (Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", back_populates="profile")
