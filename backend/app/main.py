from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from .database import get_db, engine
from .models import Base, User
from .schemas import (
    UserCreate, UserLogin, Token, UserProfile,
    CheckoutRequest, CheckoutResponse,
    SpyRequest, SpyResponse,
    VSLRequest, VSLResponse,
    VoiceRequest, VoiceResponse,
    FunnelRequest, FunnelResponse,
    TesterRequest, TesterResponse
)
from .auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)
from .services import (
    spy_service,
    vsl_service,
    voice_service,
    funnel_service,
    tester_service,
    stripe_service
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="VSL Overlord PRO API",
    description="Backend API for VSL Overlord PRO",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"status": "ok", "message": "VSL Overlord PRO API is running"}


@app.post("/signup", status_code=status.HTTP_200_OK)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        tier="STANDARD",
        usage={"funnel": 0, "vsl": 0, "spy": 0, "tester": 0}
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


@app.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create access token
    access_token = create_access_token(data={"user_id": user.id, "email": user.email})

    return {"token": access_token, "token_type": "bearer"}


@app.get("/user/profile", response_model=UserProfile)
def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile."""
    return current_user


@app.post("/subscribe", response_model=CheckoutResponse)
def create_subscription(
    checkout_data: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a Stripe checkout session."""
    checkout_url = stripe_service.create_checkout_session(
        user=current_user,
        price_id=checkout_data.price_id,
        db=db
    )
    return {"url": checkout_url}


@app.post("/spy", response_model=SpyResponse)
def spy_competitor(
    spy_data: SpyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze competitor website."""
    result = spy_service.analyze_competitor(spy_data.url, current_user, db)
    return result


@app.post("/vsl/generate", response_model=VSLResponse)
def generate_vsl(
    vsl_data: VSLRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate VSL script."""
    result = vsl_service.generate_script(vsl_data, current_user, db)
    return result


@app.post("/voice/analyze", response_model=VoiceResponse)
def analyze_voice(
    voice_data: VoiceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze user's voice and create profile."""
    result = voice_service.analyze_voice(voice_data.answers, current_user, db)
    return result


@app.post("/funnel/build", response_model=FunnelResponse)
def build_funnel(
    funnel_data: FunnelRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Build landing page HTML."""
    result = funnel_service.build_funnel(funnel_data, current_user, db)
    return result


@app.post("/tester/run", response_model=TesterResponse)
def run_tester(
    tester_data: TesterRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Run launch insurance test (INSURANCE tier only)."""
    if current_user.tier != "INSURANCE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This feature requires INSURANCE tier"
        )

    result = tester_service.run_test(tester_data, current_user, db)
    return result
