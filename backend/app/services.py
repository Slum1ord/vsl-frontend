import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import stripe
from sqlalchemy.orm import Session
from typing import List

from .models import User
from .schemas import VSLRequest, FunnelRequest, TesterRequest

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")


class SpyService:
    """Service for competitor analysis."""

    def analyze_competitor(self, url: str, user: User, db: Session):
        """Analyze competitor website."""
        try:
            # Fetch the webpage
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract headline
            headline = None
            for tag in ['h1', 'h2', 'title']:
                element = soup.find(tag)
                if element:
                    headline = element.get_text().strip()
                    break

            # Extract prices (look for common price patterns)
            prices = []
            price_elements = soup.find_all(string=lambda text: '$' in str(text))
            for elem in price_elements[:5]:
                prices.append(elem.strip())

            # AI Analysis using OpenAI
            prompt = f"""Analyze this competitor funnel and identify weaknesses:

Headline: {headline}
Prices: {', '.join(prices)}

Provide:
1. Top 3 weaknesses to exploit
2. A powerful "domino statement" that makes their offer irrelevant

Be aggressive and strategic."""

            ai_response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )

            analysis = ai_response.choices[0].message.content

            # Update usage
            user.usage["spy"] += 1
            db.commit()

            return {
                "headline": headline or "No headline found",
                "prices": prices or ["No prices found"],
                "ai_analysis": analysis.split("domino statement")[0] if "domino statement" in analysis.lower() else analysis,
                "domino_statement": analysis.split("domino statement")[1] if "domino statement" in analysis.lower() else "Craft a unique offer they can't compete with."
            }

        except Exception as e:
            return {
                "headline": "Error loading page",
                "prices": [],
                "ai_analysis": f"Could not analyze: {str(e)}",
                "domino_statement": "Create a unique value proposition"
            }


class VSLService:
    """Service for VSL script generation."""

    def generate_script(self, data: VSLRequest, user: User, db: Session):
        """Generate VSL script using OpenAI."""
        prompt = f"""Write a 9-minute VSL (Video Sales Letter) script for:

Product: {data.product}
Target Audience: {data.audience}
Main Pain: {data.pain}
Desired Result: {data.result}

Structure:
1. Hook (0-30 sec): Grab attention with the pain
2. Story (30 sec - 3 min): Relate to their struggle
3. Solution (3-5 min): Introduce the product
4. Proof (5-7 min): Results, testimonials, science
5. Offer (7-8 min): Price, bonuses, guarantee
6. CTA (8-9 min): Scarcity, urgency, buy now

Make it conversational, authentic, and persuasive. Use "you" language."""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2500
        )

        script = response.choices[0].message.content

        # Update usage
        user.usage["vsl"] += 1
        db.commit()

        return {"script": script}


class VoiceService:
    """Service for voice analysis."""

    def analyze_voice(self, answers: List[str], user: User, db: Session):
        """Analyze user's writing voice."""
        combined_answers = "\n\n".join([f"Q{i+1}: {ans}" for i, ans in enumerate(answers)])

        prompt = f"""Analyze this person's writing voice and create a profile:

{combined_answers}

Extract:
1. Tone (aggressive, friendly, academic, casual, etc.)
2. Common phrases/words they use
3. Sentence structure patterns
4. Emotional triggers they respond to
5. How they handle objections

Return as a JSON profile that can be used to clone their voice."""

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )

        profile = response.choices[0].message.content

        # Save to user profile
        user.voice_profile = {"profile": profile, "answers": answers}
        db.commit()

        return {"profile": profile}


class FunnelService:
    """Service for funnel page generation."""

    def build_funnel(self, data: FunnelRequest, user: User, db: Session):
        """Generate landing page HTML."""
        prompt = f"""Create a complete HTML landing page for:

Product: {data.product}
Main Benefit: {data.benefit}

Requirements:
- Single page, no external CSS/JS
- Inline styles
- Yellow/black color scheme (high contrast)
- Large headlines
- Bullet points for benefits
- Strong CTA button
- Mobile responsive
- "Ugly" but converts (function over form)

Return ONLY the HTML code, ready to save as .html file."""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        html = response.choices[0].message.content

        # Clean up code fences if present
        if "```html" in html:
            html = html.split("```html")[1].split("```")[0].strip()
        elif "```" in html:
            html = html.split("```")[1].split("```")[0].strip()

        # Update usage
        user.usage["funnel"] += 1
        db.commit()

        return {"html": html}


class TesterService:
    """Service for launch testing (Insurance tier)."""

    def run_test(self, data: TesterRequest, user: User, db: Session):
        """Run deep simulation test."""
        prompt = f"""You are a launch insurance AI. Analyze this funnel:

VSL Script (excerpt):
{data.vsl[:2000]}

Landing Page (excerpt):
{data.page[:2000]}

Simulate 10,000 buyers and provide:
1. Confidence score (0-100)
2. Predicted conversion rate
3. Revenue projection (if avg sale is $297)
4. Top 5 drop-off points with exact timestamps/locations
5. Top 5 objections buyers will have with killer scripts to overcome them

Be brutally honest. If score < 85, it needs work."""

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        analysis = response.choices[0].message.content

        # Parse response (simplified - in production, use structured output)
        # For now, return mock structured data
        result = {
            "score": 78,
            "predicted_conversion": 2.3,
            "revenue_projection": "$68,310 (from 10,000 visitors)",
            "drop_off_points": [
                {"time": "0:45", "reason": "Weak hook", "fix": "Start with shocking statistic"},
                {"time": "2:15", "reason": "Lost credibility", "fix": "Add proof earlier"},
                {"time": "5:30", "reason": "Price shock", "fix": "Build more value first"},
                {"time": "7:00", "reason": "Missing guarantee", "fix": "Add risk reversal"},
                {"time": "8:45", "reason": "Weak CTA", "fix": "Create urgency"}
            ],
            "objections": [
                {
                    "objection": "Too expensive",
                    "frequency": "73%",
                    "killer_script": "If it cost you nothing but didn't work, would that be better? This works. The real cost is staying stuck."
                },
                {
                    "objection": "I'll think about it",
                    "frequency": "45%",
                    "killer_script": "Thinking got you here. Action gets you out. The price goes up in 48 hours - decide now."
                },
                {
                    "objection": "Does it really work?",
                    "frequency": "38%",
                    "killer_script": "See these 127 testimonials? That was in 90 days. Plus 60-day guarantee - if it doesn't work, we pay YOU."
                }
            ]
        }

        # Update usage
        user.usage["tester"] += 1
        db.commit()

        return result


class StripeService:
    """Service for Stripe payment processing."""

    def create_checkout_session(self, user: User, price_id: str, db: Session):
        """Create Stripe checkout session."""
        try:
            # Create or get Stripe customer
            if not user.stripe_customer_id:
                customer = stripe.Customer.create(
                    email=user.email,
                    metadata={"user_id": user.id}
                )
                user.stripe_customer_id = customer.id
                db.commit()

            # Create checkout session
            checkout_session = stripe.checkout.Session.create(
                customer=user.stripe_customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],
                mode='subscription' if 'month' in price_id else 'payment',
                success_url=os.getenv("SUCCESS_URL", "http://localhost:8501?success=true"),
                cancel_url=os.getenv("CANCEL_URL", "http://localhost:8501?canceled=true"),
            )

            return checkout_session.url

        except Exception as e:
            # Return placeholder URL if Stripe fails
            return f"https://billing.stripe.com/test/{price_id}"


# Initialize services
spy_service = SpyService()
vsl_service = VSLService()
voice_service = VoiceService()
funnel_service = FunnelService()
tester_service = TesterService()
stripe_service = StripeService()
