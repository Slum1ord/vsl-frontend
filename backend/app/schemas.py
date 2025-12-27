from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    token: str
    token_type: str = "bearer"


class UserProfile(BaseModel):
    id: int
    email: str
    tier: str
    usage: Dict[str, int]
    voice_profile: Optional[Dict] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CheckoutRequest(BaseModel):
    price_id: str


class CheckoutResponse(BaseModel):
    url: str


class SpyRequest(BaseModel):
    url: str


class SpyResponse(BaseModel):
    headline: Optional[str]
    prices: List[str]
    ai_analysis: str
    domino_statement: str


class VSLRequest(BaseModel):
    product: str
    audience: str
    pain: str
    result: str


class VSLResponse(BaseModel):
    script: str


class VoiceRequest(BaseModel):
    answers: List[str]


class VoiceResponse(BaseModel):
    profile: str


class FunnelRequest(BaseModel):
    product: str
    benefit: str


class FunnelResponse(BaseModel):
    html: str


class TesterRequest(BaseModel):
    vsl: str
    page: str


class TesterResponse(BaseModel):
    score: int
    predicted_conversion: float
    revenue_projection: str
    drop_off_points: List[Dict]
    objections: List[Dict]
