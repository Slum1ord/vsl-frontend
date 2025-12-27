# VSL Overlord PRO - Deployment Guide

This guide will help you deploy the complete VSL Overlord PRO application (frontend + backend).

## 📋 Prerequisites

- GitHub account
- Render.com account (free tier available)
- OpenAI API key
- Stripe account (for payments)
- PostgreSQL database (Render provides free tier)

## 🚀 Quick Deployment on Render.com

### Step 1: Prepare Environment Variables

You'll need these API keys and secrets:

1. **OpenAI API Key**: Get from https://platform.openai.com/api-keys
2. **Stripe Keys**: Get from https://dashboard.stripe.com/apikeys
3. **Stripe Price IDs**: Create products in Stripe Dashboard
   - Create "Insurance Single" product → Get price ID
   - Create "Insurance Unlimited" subscription → Get price ID

### Step 2: Deploy Backend API

1. **Push this repository to GitHub** (if not already done)

2. **Go to Render.com** and click "New +" → "Web Service"

3. **Connect your GitHub repository**

4. **Configure the service:**
   - **Name**: `vsl-overlord-api`
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your branch name)
   - **Root Directory**: Leave blank
   - **Runtime**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

5. **Add Environment Variables** (in Render dashboard):
   ```
   DATABASE_URL=<Render will provide this>
   SECRET_KEY=<generate random 32+ character string>
   OPENAI_API_KEY=sk-...your-key...
   STRIPE_SECRET_KEY=sk_test_...your-key...
   STRIPE_PUBLISHABLE_KEY=pk_test_...your-key...
   INSURANCE_SINGLE_PRICE_ID=price_...
   INSURANCE_UNLIMITED_PRICE_ID=price_...
   SUCCESS_URL=https://your-frontend-url.com?success=true
   CANCEL_URL=https://your-frontend-url.com?canceled=true
   ```

6. **Add PostgreSQL Database**:
   - In Render dashboard, go to "New +" → "PostgreSQL"
   - Name it `vsl-overlord-db`
   - After creation, copy the "Internal Database URL"
   - Add it as `DATABASE_URL` in your web service environment variables

7. **Click "Create Web Service"**

8. **Copy the deployed URL** (e.g., `https://vsl-overlord-api.onrender.com`)

### Step 3: Deploy Frontend (Streamlit)

1. **Update Frontend Configuration**

   Edit `app.py` line 7:
   ```python
   API_URL = "https://your-actual-api-url.onrender.com"
   ```

2. **Deploy on Streamlit Community Cloud** (easiest option):

   - Go to https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - **Main file path**: `app.py`
   - Click "Deploy"

   OR

3. **Deploy on Render** (alternative):

   - Create another Web Service
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
   - No environment variables needed for frontend

### Step 4: Test Your Deployment

1. Visit your frontend URL
2. Click "Start Trial"
3. Create an account
4. Test the features (you'll need valid API keys for full functionality)

## 🔧 Local Development

### Backend

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the server
python run.py
```

Backend will be available at: http://localhost:8000
API docs: http://localhost:8000/docs

### Frontend

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit
streamlit run app.py
```

Frontend will be available at: http://localhost:8501

## 🔑 Environment Variables Reference

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | `postgresql://user:pass@host/db` |
| `SECRET_KEY` | JWT signing key | Yes | `your-super-secret-key-min-32-chars` |
| `OPENAI_API_KEY` | OpenAI API key | Yes | `sk-...` |
| `STRIPE_SECRET_KEY` | Stripe secret key | Yes | `sk_test_...` |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | Yes | `pk_test_...` |
| `INSURANCE_SINGLE_PRICE_ID` | Stripe price ID for single test | Yes | `price_...` |
| `INSURANCE_UNLIMITED_PRICE_ID` | Stripe price ID for unlimited | Yes | `price_...` |
| `SUCCESS_URL` | Redirect after payment success | No | Frontend URL + `?success=true` |
| `CANCEL_URL` | Redirect after payment cancel | No | Frontend URL + `?canceled=true` |

## 📝 Notes

- **Free tier limits**:
  - Render free tier sleeps after 15 min inactivity (first request will be slow)
  - PostgreSQL free tier has 1GB storage limit
  - Consider upgrading for production use

- **Security**:
  - Use strong `SECRET_KEY` in production
  - Never commit `.env` file to git
  - Keep API keys secure

- **Database migrations**:
  - Tables are auto-created on first run
  - For production, use Alembic migrations (already installed)

## 🐛 Troubleshooting

### Backend not starting
- Check Render logs for errors
- Verify all environment variables are set
- Ensure DATABASE_URL is correct

### Frontend can't connect to backend
- Verify API_URL in app.py matches deployed backend URL
- Check CORS settings if needed
- Test backend directly: `https://your-api.onrender.com/`

### Stripe checkout not working
- Verify Stripe keys are correct
- Check price IDs match your Stripe products
- Test in Stripe test mode first

## 📞 Support

For issues:
1. Check Render logs
2. Verify environment variables
3. Test endpoints at `/docs` on backend

## 🎉 You're Done!

Your VSL Overlord PRO is now live and ready to build funnels!
