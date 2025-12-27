from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class UserTier(str, enum.Enum):
    STANDARD = "STANDARD"
    INSURANCE = "INSURANCE"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    tier = Column(String, default="STANDARD")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Usage tracking
    usage = Column(JSON, default={
        "funnel": 0,
        "vsl": 0,
        "spy": 0,
        "tester": 0
    })

    # Voice profile
    voice_profile = Column(JSON, nullable=True)

    # Stripe customer ID
    stripe_customer_id = Column(String, nullable=True)
