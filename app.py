import streamlit as st
import requests
import jwt
import os

# API URL - CHANGE THIS AFTER DEPLOYMENT
API_URL = "http://localhost:8000"  # Change to your Render URL: "https://your-api.onrender.com"

# Session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None


def login(email, password):
    response = requests.post(f"{API_URL}/login", json={"email": email, "password": password})
    if response.status_code == 200:
        st.session_state.token = response.json()["token"]
        st.session_state.user = jwt.decode(st.session_state.token, options={"verify_signature": False})
        return True
    return False


def signup(email, password):
    response = requests.post(f"{API_URL}/signup", json={"email": email, "password": password})
    return response.status_code == 200


def get_profile():
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_URL}/user/profile", headers=headers)
    return response.json()


def create_checkout_session(price_id):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    body = {"price_id": price_id}
    response = requests.post(f"{API_URL}/subscribe", headers=headers, json=body)
    return response.json()


def render_spy_page(user_data):
    st.title("🏴‍☠️ Competitor Spy")
    st.markdown("Extract intel from any funnel. Find their weaknesses. Exploit them.")

    url = st.text_input("Enter competitor URL:", placeholder="https://competitor.com/funnel")

    if st.button("Deploy Spy", type="primary", use_container_width=True):
        if not url:
            st.error("Enter a URL")
            return

        with st.spinner("🕵️ Extracting intel..."):
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            response = requests.post(f"{API_URL}/spy", headers=headers, json={"url": url})

            if response.status_code != 200:
                st.error("Could not spy. Try again.")
                return

            data = response.json()

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🎯 Headline")
                st.code(data.get("headline", "N/A"), language='text')
            with col2:
                st.markdown("### 💰 Prices Found")
                for price in data.get("prices", []):
                    st.code(price)

            st.markdown("### ⚠️ Weaknesses to Exploit")
            st.success(data.get("ai_analysis", "Analysis complete"))

            st.markdown("### ⚔️ Your Kryptonite Strike")
            st.info(data.get("domino_statement", "Craft your domino statement"))


def render_vsl_page(user_data):
    st.title("🎬 VSL Architect")
    st.markdown("Generate teleprompter-ready scripts that convert cold traffic.")

    product = st.text_input("Product Name:", placeholder="Fat Loss System")
    audience = st.text_input("Target Audience:", placeholder="Busy moms aged 30-45")
    pain = st.text_input("Main Pain Point:", placeholder="Can't lose post-baby weight")
    result = st.text_input("Desired Result:", placeholder="Fit into pre-baby jeans in 90 days")

    if st.button("Generate Script", type="primary", use_container_width=True):
        if not all([product, audience, pain, result]):
            st.error("Fill all fields")
            return

        with st.spinner("📝 Writing your VSL..."):
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            body = {
                "product": product,
                "audience": audience,
                "pain": pain,
                "result": result
            }
            response = requests.post(f"{API_URL}/vsl/generate", headers=headers, json=body)

            script = response.json().get("script", "")
            st.code(script, language='text', line_numbers=True)
            st.download_button("📥 Download Script", script, "vsl_script.txt")


def render_voice_page(user_data):
    st.title("🎤 Voice DNA")
    st.markdown("Clone your voice so AI writes like YOU, not a robot.")

    questions = [
        "What's the biggest lie in your industry?",
        "What's the #1 result your clients get?",
        "Tell me about a time you almost gave up",
        "Why should someone trust you NOW?",
        "What do you hate about typical marketing?"
    ]

    answers = [st.text_area(q, height=80) for q in questions]

    if st.button("Clone My Voice", type="primary", use_container_width=True):
        if not all(answers):
            st.error("Answer all questions")
            return

        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        body = {"answers": answers}
        response = requests.post(f"{API_URL}/voice/analyze", headers=headers, json=body)

        profile = response.json().get("profile", "")
        st.success("✅ Voice profile created!")
        st.code(profile, language='json')


def render_funnel_page(user_data):
    st.title("📄 Funnel Builder")
    st.markdown("Generate complete landing page copy. Ugly design, maximum conversions.")

    product = st.text_input("Product Name:", placeholder="Fat Loss Fast Track")
    benefit = st.text_input("Main Benefit:", placeholder="Lose 20 lbs in 90 days without giving up wine")

    if st.button("Build Page", type="primary", use_container_width=True):
        if not product or not benefit:
            st.error("Fill both fields")
            return

        with st.spinner("🏗️ Building your page..."):
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            body = {"product": product, "benefit": benefit}
            response = requests.post(f"{API_URL}/funnel/build", headers=headers, json=body)

            html = response.json().get("html", "")
            st.code(html, language='html')
            st.download_button("📥 Download HTML", html, "funnel_page.html")


def render_tester_page(user_data):
    st.title("🚀 Launch Insurance Protocol")
    st.markdown("Simulate 10,000 buyers. Know your conversion rate BEFORE you spend $10K on ads.")

    if user_data['tier'] != 'INSURANCE':
        st.error("🚫 This is an INSURANCE-ONLY feature")

        st.markdown("""
        ### You've built the funnel. Now know if it'll work.

        **What you get:**
        - AI simulates 10,000 virtual buyers
        - Confidence score 0-100
        - Drop-off heatmap (exact seconds they leave)
        - Objection killer report
        - "Work for Free" guarantee

        **Choose your plan:**
        """)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ### Single Test
            **$997 one-time**

            Perfect for one funnel launch
            """)
            if st.button("Buy Single Test - $997", type="primary", use_container_width=True):
                session = create_checkout_session(os.getenv("INSURANCE_SINGLE_PRICE_ID"))
                st.markdown(f'<meta http-equiv="refresh" content="0;url={session["url"]}">', unsafe_allow_html=True)

        with col2:
            st.markdown("""
            ### Unlimited
            **$2,997/month**

            Unlimited tests + video breakdowns
            """)
            if st.button("Go Unlimited - $2,997/mo", type="primary", use_container_width=True):
                session = create_checkout_session(os.getenv("INSURANCE_UNLIMITED_PRICE_ID"))
                st.markdown(f'<meta http-equiv="refresh" content="0;url={session["url"]}">', unsafe_allow_html=True)

        return

    vsl = st.text_area("Paste VSL Script:", height=300, placeholder="Paste your 9-minute script here...")
    page = st.text_area("Paste Landing Page:", height=300, placeholder="Paste HTML or plain text...")

    if st.button("Run Deep Simulation", type="primary", use_container_width=True):
        if not vsl or not page:
            st.error("Paste both pieces")
            return

        with st.spinner("🧪 Simulating 10,000 buyers..."):
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            body = {"vsl": vsl, "page": page}
            response = requests.post(f"{API_URL}/tester/run", headers=headers, json=body)

            results = response.json()

            # Display metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Confidence Score", f"{results['score']}/100")
            col2.metric("Predicted Conversion", f"{results['predicted_conversion']}%")
            col3.metric("Projected Revenue", results['revenue_projection'])

            # Drop-off points
            st.markdown("### 🔥 Drop-Off Heatmap")
            for point in results['drop_off_points']:
                col1, col2, col3 = st.columns([1, 2, 2])
                col1.error(point['time'])
                col2.markdown(point['reason'])
                col3.success(point['fix'])

            # Objections
            st.markdown("### ⚔️ Objection Killer Scripts")
            for obj in results['objections']:
                st.markdown(f"**{obj['objection']}** ({obj['frequency']} of buyers)")
                st.code(obj['killer_script'], language='text')

            # Low score offer
            if results['score'] < 85:
                st.markdown("---")
                st.error("❌ Score too low! I can fix this for you.")
                st.markdown("""
                **Option 1:** Spend 40 hours fixing it yourself

                **Option 2:** Hire me to rewrite it for $5,000 (72-hour turnaround, guaranteed 85+)
                """)
                if st.button("YES, John - Fix My Funnel - $5,000", type="primary"):
                    st.info("Contact john@vsloverlord.pro to arrange payment and briefing.")


def render_dashboard_page(user_data):
    st.title("💰 Your Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Funnels Built", user_data['usage']['funnel'])
    col2.metric("VSL Scripts", user_data['usage']['vsl'])
    col3.metric("Spy Missions", user_data['usage']['spy'])
    col4.metric("Launch Tests", user_data['usage']['tester'] if user_data['tier'] == 'INSURANCE' else "🔒")

    st.markdown("---")

    if user_data['tier'] == 'INSURANCE':
        st.success("✅ Launch Insurance is ACTIVE")
        st.markdown("You can run unlimited funnel simulations.")
    else:
        st.info("🚀 Upgrade to Insurance to unlock Launch Tester")
        if st.button("Add Insurance - $997", type="primary"):
            session = create_checkout_session(os.getenv("INSURANCE_SINGLE_PRICE_ID"))
            st.markdown(f'<meta http-equiv="refresh" content="0;url={session["url"]}">', unsafe_allow_html=True)


# PAGE SETUP
st.set_page_config(
    page_title="VSL Overlord PRO",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# AUTH FLOW
if st.session_state.token is None:
    st.title("VSL Overlord PRO")
    st.markdown("### The AI That Builds $4.2 Billion Funnels")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Login
        Already a member? Sign in.
        """)
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", type="primary", key="login_btn"):
            if login(email, password):
                st.success("✅ Logged in!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

    with col2:
        st.markdown("""
        ### Start Trial
        7-day trial. Then $297/month.

        ✅ Unlimited funnel builds
        ✅ AI VSL scripts
        ✅ Competitor analysis
        ✅ Voice cloning

        Cancel anytime.
        """)
        trial_email = st.text_input("Email", key="trial_email")
        trial_password = st.text_input("Password", type="password", key="trial_password")

        if st.button("Start Trial - $297/month", type="primary", key="trial_btn"):
            if signup(trial_email, trial_password):
                if login(trial_email, trial_password):
                    st.success("✅ Trial started! Check your email.")
                    st.rerun()
            else:
                st.error("❌ Email already exists")

else:
    # MAIN APP
    user_data = get_profile()

    # SIDEBAR
    st.sidebar.title("🎯 VSL Overlord PRO")
    st.sidebar.markdown(f"**Plan:** {user_data['tier']}")
    st.sidebar.markdown(f"**Email:** {user_data['email'][:3]}***{user_data['email'][-4:]}")

    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.user = None
        st.rerun()

    # UPGRADE BANNER (for STANDARD users)
    if user_data['tier'] == 'STANDARD':
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        ### 🔥 UPGRADE TO INSURANCE

        **Launch Insurance Protocol:**
        - Simulate 10,000 buyers
        - Predict conversion rate
        - Fix problems before launch

        **$997 (one-time)** or **$2,997/month**
        """)

        col1, col2 = st.sidebar.columns(2)
        if col1.button("Single Test\n$997", type="primary"):
            session = create_checkout_session(os.getenv("INSURANCE_SINGLE_PRICE_ID"))
            st.markdown(f'<meta http-equiv="refresh" content="0;url={session["url"]}">', unsafe_allow_html=True)

        if col2.button("Unlimited\n$2,997/mo", type="primary"):
            session = create_checkout_session(os.getenv("INSURANCE_UNLIMITED_PRICE_ID"))
            st.markdown(f'<meta http-equiv="refresh" content="0;url={session["url"]}">', unsafe_allow_html=True)

    # MAIN NAVIGATION
    page = st.sidebar.radio("Choose Your Weapon:", [
        "🏴‍☠️ Competitor Spy",
        "🎬 VSL Architect",
        "🎤 Voice DNA",
        "📄 Funnel Builder",
        "🚀 Launch Tester",
        "💰 Dashboard"
    ])

    # RENDER PAGES
    if page == "🏴‍☠️ Competitor Spy":
        render_spy_page(user_data)
    elif page == "🎬 VSL Architect":
        render_vsl_page(user_data)
    elif page == "🎤 Voice DNA":
        render_voice_page(user_data)
    elif page == "📄 Funnel Builder":
        render_funnel_page(user_data)
    elif page == "🚀 Launch Tester":
        render_tester_page(user_data)
    elif page == "💰 Dashboard":
        render_dashboard_page(user_data)
