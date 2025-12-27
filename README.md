# 🎯 VSL Overlord PRO

The AI-powered platform that builds $4.2 billion funnels. Complete with competitor analysis, VSL generation, voice cloning, and launch insurance.

## ✨ Features

- **🏴‍☠️ Competitor Spy**: Extract intel from any funnel and find weaknesses to exploit
- **🎬 VSL Architect**: Generate teleprompter-ready video sales letter scripts
- **🎤 Voice DNA**: Clone your writing voice for authentic AI-generated content
- **📄 Funnel Builder**: Create high-converting landing pages instantly
- **🚀 Launch Tester**: Simulate 10,000 buyers before spending on ads (Insurance tier)
- **💳 Stripe Integration**: Multi-tier subscription system
- **🔒 JWT Authentication**: Secure user accounts and session management

## 🏗️ Architecture

### Frontend
- **Framework**: Streamlit
- **Features**: Interactive UI, real-time generation, downloadable outputs
- **Location**: `app.py`

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL (SQLite for local dev)
- **Authentication**: JWT tokens with bcrypt hashing
- **AI Integration**: OpenAI GPT-4
- **Payments**: Stripe Checkout
- **Location**: `backend/`

## 📦 Project Structure

```
vsl-frontend/
├── app.py                          # Streamlit frontend
├── requirements.txt                # Frontend dependencies
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI application
│   │   ├── models.py              # SQLAlchemy models
│   │   ├── schemas.py             # Pydantic schemas
│   │   ├── auth.py                # JWT authentication
│   │   ├── database.py            # Database configuration
│   │   └── services.py            # Business logic
│   ├── requirements.txt           # Backend dependencies
│   └── run.py                     # Development server
├── .env.example                   # Environment variables template
├── Procfile                       # Render deployment config
├── runtime.txt                    # Python version
├── render.yaml                    # Render.com blueprint
└── DEPLOYMENT.md                  # Deployment guide

```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd vsl-frontend
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run Backend** (Terminal 1)
   ```bash
   cd backend
   pip install -r requirements.txt
   python run.py
   ```
   Backend runs on: http://localhost:8000

4. **Run Frontend** (Terminal 2)
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
   Frontend runs on: http://localhost:8501

### Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for full deployment instructions.

**Quick Deploy to Render.com:**
1. Push to GitHub
2. Connect to Render
3. Add environment variables
4. Deploy!

## 🔑 Required API Keys

| Service | Purpose | Get It From |
|---------|---------|-------------|
| OpenAI | AI generation | https://platform.openai.com/api-keys |
| Stripe | Payment processing | https://dashboard.stripe.com/apikeys |
| PostgreSQL | Database | Render.com (free tier) |

## 📚 API Endpoints

### Authentication
- `POST /signup` - Create new account
- `POST /login` - Authenticate and get JWT token
- `GET /user/profile` - Get current user profile

### Features
- `POST /spy` - Analyze competitor funnel
- `POST /vsl/generate` - Generate VSL script
- `POST /voice/analyze` - Create voice profile
- `POST /funnel/build` - Build landing page
- `POST /tester/run` - Run launch simulation (Insurance only)

### Payments
- `POST /subscribe` - Create Stripe checkout session

Full API documentation: http://localhost:8000/docs

## 💰 Pricing Tiers

### STANDARD ($297/month)
- Unlimited funnel builds
- VSL script generation
- Competitor analysis
- Voice cloning

### INSURANCE ($997 one-time or $2,997/month)
- Everything in STANDARD, plus:
- Launch Tester with 10,000 buyer simulation
- Predicted conversion rates
- Drop-off heatmaps
- Objection killer scripts

## 🧪 Testing

```bash
# Test backend API
curl http://localhost:8000/

# Create test user
curl -X POST http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Production database
- **Pydantic** - Data validation
- **python-jose** - JWT token handling
- **passlib** - Password hashing
- **Stripe** - Payment processing
- **OpenAI** - AI content generation
- **BeautifulSoup** - Web scraping

### Frontend
- **Streamlit** - Interactive web app framework
- **Requests** - HTTP client
- **JWT** - Token decoding

## 📝 Development Notes

- Backend auto-creates database tables on first run
- SQLite is used for local development
- PostgreSQL required for production
- All passwords are bcrypt hashed
- JWT tokens expire after 30 days
- CORS is enabled for all origins (configure for production)

## 🔒 Security

- Passwords hashed with bcrypt
- JWT tokens for authentication
- Environment variables for secrets
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy

## 🐛 Known Issues

- Stripe test mode requires test credit cards
- OpenAI API calls can be slow
- Free Render tier sleeps after 15min inactivity
- First request after sleep takes ~30 seconds

## 📄 License

This is a commercial product. All rights reserved.

## 🤝 Contributing

This is a private commercial project. Contact the owner for contribution guidelines.

## 📞 Support

For deployment issues, see [DEPLOYMENT.md](DEPLOYMENT.md)

For feature requests or bugs, contact the development team.

---

Built with ❤️ for funnel builders who want to dominate their market.
