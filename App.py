import streamlit as st
import datetime
import time
import re
import random
import os
import hashlib
import google.generativeai as genai

# --- 🎯 BASE AI PROMPT TEMPLATE ---
RAW_TEMPLATE = """
You are a multi-million dollar elite Meta Ads buyer. 
Construct a high-ROAS master funnel strategy for this product.

PRODUCT DETAILS:
- Link: {}
- Description: {}

Generate structured output:
1. TARGET AUDIENCE: Persona, Meta Interest Stacks, Behavioral Filters.
2. 3-STAGE FUNNEL: TOFU (Cold Stacking), MOFU (Warm Custom Audiences), BOFU (Hot Urgency Retargeting).
3. AD COPY VAULT: 3 frameworks written natively in emotion-driven Hinglish with emojis (Hook Alpha, Hook Beta, Hook Gamma).

Naturally mention the verified link {} inside conversion call-to-actions.
"""

# --- ⚙️ CONFIG (SABSE PEHLE RUN HONA ZAROORI HAI) ---
st.set_page_config(page_title="GJ GLOBAL AI ADS", page_icon="🚩", layout="wide")
OWNER_EMAIL = "armygamingtotal@gmail.com"

# --- 🚩 PREMIUM HEADER DESIGN (Zero-Crash Python 3.14 Version) ---
st.markdown("""
    <div style="background: linear-gradient(45deg, #ff4500, #ff761a); padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(255, 69, 0, 0.3);">
        <h1 style="color: white; margin: 0; font-size: 32px; font-family: 'Arial'; letter-spacing: 1px;">🚩 जय श्री RAM 🚩</h1>
        <p style="color: #ffe6cc; margin: 5px 0 0 0; font-size: 16px; font-weight: bold; letter-spacing: 2px;">JAI SHREE RAM | GJ GLOBAL AI ADS CORE INTERFACE</p>
    </div>
""", unsafe_allowed_html=True)

# --- 🔒 SECURITY UTILITIES ---
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def sanitize_input(text):
    if not text: return ""
    return re.sub(r'<[^>]*?>', '', str(text)).replace('"', '').replace("'", "").strip()

def validate_and_fix_url(url):
    url = sanitize_input(url)
    if not url: return ""
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url
    return url

# --- 💾 APP STATE INIT ---
if "fixed_prices" not in st.session_state:
    st.session_state.fixed_prices = {"Silver (Monthly)": 19, "Standard (6-Month)": 49, "Standard (Yearly)": 249, "Premium (Yearly)": 499}
if "usd_to_inr_rate" not in st.session_state: st.session_state.usd_to_inr_rate = 91.50
if "razorpay_link" not in st.session_state: st.session_state.razorpay_link = "https://razorpay.me/@gjglobalaiads"
if "stripe_link" not in st.session_state: st.session_state.stripe_link = "https://checkout.stripe.com/recurring-autopilot"

if "indian_spied_data" not in st.session_state:
    st.session_state.indian_spied_data = [
        {"Target Winning Product": "Mini Portable Ultrasonic Washing Machine", "Estimated Daily Orders Managed": "1,450", "Calculated Product Win Rate Metric": "94%"},
        {"Target Winning Product": "Rechargeable Automatic Hair Braider Combo", "Estimated Daily Orders Managed": "890", "Calculated Product Win Rate Metric": "89%"},
        {"Target Winning Product": "Crystal Hair Eraser Exfoliator Node", "Estimated Daily Orders Managed": "2,120", "Calculated Product Win Rate Metric": "96%"}
    ]

if "users_db" not in st.session_state: st.session_state.users_db = {}
if "current_user" not in st.session_state: st.session_state.current_user = None
if "otp_sent" not in st.session_state: st.session_state.otp_sent = None
if "marketing_videos" not in st.session_state: st.session_state.marketing_videos = []
if "app_self_lock" not in st.session_state: st.session_state.app_self_lock = False
if "saved_gemini_key" not in st.session_state: st.session_state.saved_gemini_key = ""

# --- 🌐 LANGUAGE SETTINGS ---
languages = {
    "English": {"welcome": "Welcome to GJ GLOBAL AI ADS", "run": "Generate Smart Campaign & Launch", "spy": "Spy Tool & Tracker", "help": "AI Help Center", "query_placeholder": "Ask anything..."},
    "Hindi (हिंदी)": {"welcome": "GJ GLOBAL AI ADS में आपका स्वागत है", "run": "स्मार्ट कैंपेन लॉन्च करें", "spy": "जासूसी टूल", "help": "AI सहायता केंद्र", "query_placeholder": "कुछ भी पूछें..."}
}
selected_lang = st.selectbox("🌐 Choose Language / भाषा चुनें", list(languages.keys()))
lang = languages[selected_lang]
user_country = st.sidebar.radio("📍 Billing Region", ["Inside India (INR ₹)", "Outside India (USD $)"])

# --- 📝 AUTH SYSTEM ---
if st.session_state.current_user is None:
    st.subheader(f"🔐 {lang['welcome']}")
    auth_mode = st.radio("Mode", ["Sign Up", "Log In"])
    
    if auth_mode == "Sign Up":
        name = sanitize_input(st.text_input("Full Name:"))
        email = sanitize_input(st.text_input("Email ID:")).lower()
        phone = sanitize_input(st.text_input("Phone Number:"))
        custom_password = st.text_input("Password:", type="password")
        plan_choice = st.selectbox("Plan", list(st.session_state.fixed_prices.keys()))
        
        dollar_val = st.session_state.fixed_prices[plan_choice]
        final_price_str = f"₹{round(dollar_val * st.session_state.usd_to_inr_rate, 2)}" if user_country == "Inside India (INR ₹)" else f"${dollar_val} USD"
        st.info(f"💳 Value: {final_price_str}")
        
        if st.button("Generate OTP ✉️"):
            if name and email and phone and custom_password:
                st.session_state.otp_sent = str(random.randint(112233, 998877))
                st.info(f"✨ OTP: `{st.session_state.otp_sent}`")
            else: st.error("Please fill all details!")
            
        if st.session_state.otp_sent:
            otp_input = st.text_input("Enter Code:")
            if st.button("Register 🎉"):
                if otp_input == st.session_state.otp_sent:
                    st.session_state.users_db[email] = {"name": name, "password": hash_password(custom_password), "plan": plan_choice, "phone": phone, "signup_date": datetime.date.today(), "days": 30}
                    st.session_state.current_user = email
                    st.success("Success!")
                    st.session_state.otp_sent = None
                    st.rerun()
    else:
        email = sanitize_input(st.text_input("Email:")).lower()
        password = st.text_input("Password:", type="password")
        if st.button("Login 🔓"):
            if email in st.session_state.users_db and st.session_state.users_db[email]["password"] == hash_password(password):
                st.session_state.current_user = email
                st.rerun()
            else: st.error("Invalid credentials!")
    st.stop()

# --- 🔒 SECURITY WALLS ---
user_data = st.session_state.users_db[st.session_state.current_user]
st.sidebar.markdown(f"👤 Account: **{user_data['name']}** ({user_data['plan']})")

if st.sidebar.button("Logout 🔒"):
    st.session_state.current_user = None
    st.rerun()

# --- 👑 ADMIN CONTROLS ---
admin_email = st.sidebar.text_input("Verify Admin Route:", placeholder="owner@gmail.com")
if admin_email.lower() == OWNER_EMAIL.lower():
    st.sidebar.success("Admin Control Active!")
    st.session_state.usd_to_inr_rate = st.sidebar.number_input("Set Dollar Rate:", value=st.session_state.usd_to_inr_rate)

# --- 🎯 MAIN INTERFACE TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Meta Ads Automator", "🕵️ Tracker", "🎥 Reviews", "🤖 Help Center"])

with tab1:
    st.markdown("### 📖 Setup Guide Manual")
    st.info("Get Gemini API Key via Google AI Studio & Meta Access Token via Meta for Developers dashboard.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.header("🛒 Store Data")
        raw_url = st.text_input("Storefront URL:", placeholder="https://yourstore.com")
        store_url = validate_and_fix_url(raw_url)
        product_desc = sanitize_input(st.text_area("Product Strategy Narrative Description:"))
    with col2:
        st.header("🎯 Target Acquisition Node")
        gemini_key = st.text_input("Gemini Secret Key Input:", type="password")
        if gemini_key: st.session_state.saved_gemini_key = sanitize_input(gemini_key)
        
        if st.button(lang['run']):
            if not st.session_state.saved_gemini_key: st.error("❌ Missing valid Gemini key.")
            elif not store_url: st.error("❌ Please enter a valid campaign URL.")
            else:
                with st.spinner("🔒 Activating AI Buying Engine..."):
                    try:
                        os.environ["GOOGLE_API_VERSION"] = "v1"
                        genai.configure(api_key=st.session_state.saved_gemini_key)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        
                        smart_campaign_prompt = RAW_TEMPLATE.format(store_url, product_desc, store_url)
                        response = model.generate_content(smart_campaign_prompt)
                        st.success("🎯 Strategy Deployment Complete!")
                        st.markdown(response.text)
                        st.balloons()
                    except Exception as err:
                        st.error(f"❌ Error: {str(err)}")

with tab2:
    st.subheader("🕵️ Tracking Dashboard")
    if "Silver" in user_data["plan"]:
        st.error("🔒 Upgrade plan to lock active product tracking engines.")
    else:
        st.table(st.session_state.indian_spied_data)

with tab3:
    st.subheader("🎥 Video Module Panel")
    st.info("No system reviews loaded yet.")

with tab4:
    st.subheader("🤖 AI Help Center Desk")
    user_query = sanitize_input(st.text_input("State your roadblock below:"))
    if st.button("Transmit Question Node 💬"):
        if not user_query: st.warning("Please type something.")
        elif not st.session_state.saved_gemini_key: st.error("❌ Input your Gemini Private Key in 'Tab 1' first.")
        else:
            with st.spinner("🧠 Analyzing query..."):
                try:
                    os.environ["GOOGLE_API_VERSION"] = "v1"
                    genai.configure(api_key=st.session_state.saved_gemini_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    support_prompt = f"Fix this issue safely: {user_query}. Respond natively in choice: {selected_lang}"
                    response = model.generate_content(support_prompt)
                    st.info(response.text)
                except Exception as api_err:
                    st.error(f"❌ Network Fault: {str(api_err)}")
