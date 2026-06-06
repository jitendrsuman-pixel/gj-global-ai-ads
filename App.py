import streamlit as st
import datetime
import time
import re
import random
import os
import hashlib
import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai

# --- ⚙️ PRODUCTION CONFIGURATION (REAL OTP SYSTEM BUILT-IN) ---
SMTP_EMAIL = "armygamingtotal@gmail.com"  
SMTP_PASSWORD = "huopctngzcjkdcde"  # Secure Key integrated successfully

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

st.set_page_config(page_title="GJ GLOBAL AI ADS - Enterprise", page_icon="🚩", layout="wide")
OWNER_EMAIL = "armygamingtotal@gmail.com"

# --- 💾 APP STATE DATABASE INIT ---
if "users_db" not in st.session_state: 
    st.session_state.users_db = {}
if "current_user" not in st.session_state: 
    st.session_state.current_user = None
if "saved_gemini_key" not in st.session_state: 
    st.session_state.saved_gemini_key = ""
if "signup_stage" not in st.session_state:
    st.session_state.signup_stage = "form"
if "generated_otp" not in st.session_state:
    st.session_state.generated_otp = None
if "temp_user_data" not in st.session_state:
    st.session_state.temp_user_data = {}

fixed_prices = {
    "7 Days Free Trial": 0,
    "Silver (Monthly)": 19, 
    "Standard (6-Month)": 49, 
    "Standard (Yearly)": 249, 
    "Premium (Yearly)": 499
}
usd_to_inr_rate = 91.50
razorpay_link = "https://razorpay.me/@gjglobalaiads"
stripe_link = "https://checkout.stripe.com/recurring-autopilot"

indian_spied_data = [
    {"Target Winning Product": "Mini Portable Ultrasonic Washing Machine", "Estimated Daily Orders Managed": "1,450", "Calculated Product Win Rate Metric": "94%"},
    {"Target Winning Product": "Rechargeable Automatic Hair Braider Combo", "Estimated Daily Orders Managed": "890", "Calculated Product Win Rate Metric": "89%"},
    {"Target Winning Product": "Crystal Hair Eraser Exfoliator Node", "Estimated Daily Orders Managed": "2,120", "Calculated Product Win Rate Metric": "96%"}
]

# --- 🔒 SECURITY & EMAIL UTILITIES ---
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

def send_otp_email(target_email, otp_code):
    try:
        msg = MIMEText(f"Jai Shree Ram!\n\nYour 6-Digit Security Verification Code for GJ GLOBAL AI ADS is: {otp_code}\n\nValid for 10 minutes.")
        msg['Subject'] = f"{otp_code} is your GJ GLOBAL AI ADS Verification Code"
        msg['From'] = SMTP_EMAIL
        msg['To'] = target_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, target_email, msg.as_string())
        return True
    except Exception as e:
        return False

# --- 🚩 HEADER BLOCK ---
st.title("🚩 जय श्री RAM 🚩")
st.subheader("GJ GLOBAL AI ADS | ENTERPRISE HUB")
st.divider()

# --- 📝 PROPORTIONAL AUTHENTICATION SYSTEM ---
if st.session_state.current_user is None:
    st.markdown("### 🔐 Platform Access Gateway")
    auth_mode = st.tabs(["Create Account (Sign Up)", "Access Portal (Log In)"])
    
    with auth_mode[0]:
        if st.session_state.signup_stage == "form":
            st.write("#### Register New Enterprise Node")
            reg_name = st.text_input("Your Full Name:", key="reg_name")
            reg_email = st.text_input("Email Address (User ID):", key="reg_email").lower().strip()
            reg_phone = st.text_input("Mobile Number:", key="reg_phone")
            reg_pass = st.text_input("Choose Secure Password:", type="password", key="reg_pass")
            reg_plan = st.selectbox("Select Initial Access Plan:", list(fixed_prices.keys()), key="reg_plan")
            
            dollar_val = fixed_prices[reg_plan]
            final_price_str = "Status: FREE TRIAL" if reg_plan == "7 Days Free Trial" else f"Price: ₹{round(dollar_val * usd_to_inr_rate, 2)} Approx"
            st.info(final_price_str)
            
            st.write("") # Layout spacing
            
            # Smart Center Alignment Strategy for Universal Devices (Full Responsive Grid Layout)
            col_left, col_center, col_right = st.columns([1.0, 2.0, 1.0])
            with col_center:
                # use_container_width=True makes the button dynamically scale across Mobile, Tablets, or Monitors smoothly
                if st.button("Continue 🚀", key="signup_btn", use_container_width=True, type="primary"):
                    if reg_name and reg_email and reg_phone and reg_pass:
                        if reg_email in st.session_state.users_db:
                            st.error("User ID already registered! Please log in.")
                        else:
                            with st.spinner("Dispatching Secure OTP to your Email..."):
                                secure_otp = str(random.randint(100100, 999999))
                                if send_otp_email(reg_email, secure_otp):
                                    st.session_state.generated_otp = secure_otp
                                    st.session_state.temp_user_data = {
                                        "name": reg_name,
                                        "email": reg_email,
                                        "phone": reg_phone,
                                        "password": hash_password(reg_pass),
                                        "plan": reg_plan
                                    }
                                    st.session_state.signup_stage = "otp_verification"
                                    st.rerun()
                                else:
                                    st.error("Email Routing Fault. Please verify server connection configurations.")
                    else:
                        st.error("Please fill all fields completely before continuing.")
                    
        elif st.session_state.signup_stage == "otp_verification":
            st.write("#### 🛡️ OTP Code Verification layer")
            st.warning(f"Verification code token dispatched successfully to: **{st.session_state.temp_user_data['email']}** (Check Spam folder if not received)")
            
            otp_input = st.text_input("Enter 6-Digit Verification Code Received on Email:", key="otp_input_field")
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Verify & Create Account 🎉", key="final_confirm_btn", use_container_width=True):
                    if otp_input == st.session_state.generated_otp:
                        t_data = st.session_state.temp_user_data
                        trial_days = 7 if t_data["plan"] == "7 Days Free Trial" else 30
                        
                        st.session_state.users_db[t_data["email"]] = {
                            "name": t_data["name"],
                            "password": t_data["password"],
                            "plan": t_data["plan"],
                            "phone": t_data["phone"],
                            "signup_date": datetime.date.today(),
                            "days": trial_days
                        }
                        st.session_state.current_user = t_data["email"]
                        st.session_state.signup_stage = "form"
                        st.session_state.generated_otp = None
                        st.success("Verification Complete! Welcome Center Initialized.")
                        st.rerun()
                    else:
                        st.error("Invalid security verification code token! Please try again.")
            with col_b2:
                if st.button("Back to Form ↩️", key="back_to_form_btn", use_container_width=True):
                    st.session_state.signup_stage = "form"
                    st.rerun()
                
    with auth_mode[1]:
        st.write("#### User Authorization Node")
        login_email = st.text_input("Registered Email ID:", key="login_email").lower().strip()
        login_pass = st.text_input("Password Key:", type="password", key="login_pass")
        
        if st.button("Authorize Account Security 🔓", key="login_btn", use_container_width=True):
            if login_email in st.session_state.users_db and st.session_state.users_db[login_email]["password"] == hash_password(login_pass):
                st.session_state.current_user = login_email
                st.success("Access Granted!")
                st.rerun()
            else:
                st.error("Invalid Credentials or Record Missing.")
    st.stop()

# --- 🚀 SECURE APP ENTRY LAYER ---
user_data = st.session_state.users_db[st.session_state.current_user]
expiry_date = user_data['signup_date'] + datetime.timedelta(days=user_data['days'])
remaining_days = (expiry_date - datetime.date.today()).days

st.sidebar.markdown(f"### 👤 Active Session")
st.sidebar.write(f"**User:** {user_data['name']}")
st.sidebar.info(f"**Current Plan:** {user_data['plan']}")
st.sidebar.write(f"**Days Left:** {max(0, remaining_days)} Days")

if st.sidebar.button("Exit Gateway Session 🔒"):
    st.session_state.current_user = None
    st.rerun()

if datetime.date.today() > expiry_date:
    st.error("❌ SUBSCRIPTION / TRIAL LIFETIME EXPIRED! Please clear dues below to unfreeze.")
    st.write(f"Renew your license here: {razorpay_link}")
    st.stop()

# --- 🎯 MAIN DASHBOARD INTERFACE ---
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Meta Ads Automator", "🕵️ Competitor Tracker", "💳 Premium Subscription Store", "🤖 AI Support Desk"])

with tab1:
    st.markdown("### Meta AI Campaign Builder Engine")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛒 Store Config")
        raw_url = st.text_input("Target Storefront URL:", placeholder="https://yourstore.com")
        store_url = validate_and_fix_url(raw_url)
        product_desc = st.text_area("Product Strategy Narrative Context:")
    with col2:
        st.subheader("🔑 Access Vectors")
        gemini_key = st.text_input("Enter Gemini Secret API Key:", type="password")
        if gemini_key: 
            st.session_state.saved_gemini_key = sanitize_input(gemini_key)
            
        if st.button("Generate Smart Campaign & Launch 🚀", use_container_width=True):
            if not st.session_state.saved_gemini_key: 
                st.error("Missing Gemini Decryption Authorization Key.")
            elif not store_url: 
                st.error("Please insert a valid target domain URL context.")
            else:
                with st.spinner("Analyzing parameters via core system neural layer..."):
                    try:
                        os.environ["GOOGLE_API_VERSION"] = "v1"
                        genai.configure(api_key=st.session_state.saved_gemini_key)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        
                        smart_campaign_prompt = RAW_TEMPLATE.format(store_url, product_desc, store_url)
                        response = model.generate_content(smart_campaign_prompt)
                        st.success("Target Acquisition Framework Generated Successfully!")
                        st.markdown(response.text)
                        st.balloons()
                    except Exception as err:
                        st.error(f"Core Exception Node Rejected: {str(err)}")

with tab2:
    st.markdown("### 🕵️ Ad Intelligence Board & Winning Products")
    if user_data["plan"] == "Silver (Monthly)":
        st.error("🔒 Upgrade plan to lock active product tracking engines.")
    else:
        st.table(indian_spied_data)

with tab3:
    st.markdown("### 💳 Upgrade Your Subscription Tier")
    st.write("Apne operations ko upgrade karne ke liye niche diye gae premium tiers me se best package choose karein:")
    
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        st.subheader("Silver Package")
        st.write(f"Price: ₹{round(19 * usd_to_inr_rate)} / Month")
        st.write("Basic Automation & Funnels")
        st.write(f"Payment Link: {razorpay_link}")
        
    with p_col2:
        st.subheader("Standard Deal")
        st.write(f"Price: ₹{round(49 * usd_to_inr_rate)} / 6-Months")
        st.write("Full Competitor Tracker Engine Active")
        st.write(f"Payment Link: {razorpay_link}")
        
    with p_col3:
        st.subheader("Enterprise Premium")
        st.write(f"Price: ₹{round(499 * usd_to_inr_rate)} / Year")
        st.write("Max Speed Global Asset Tracking Stream")
        st.write(f"Payment Link: {stripe_link}")

with tab4:
    st.markdown("### 🤖 Enterprise Help Center Desk")
    user_query = st.text_input("State your roadblock parameter below:")
    if st.button("Transmit Question Node 💬", use_container_width=True):
        if not user_query: 
            st.warning("Empty question parameters cannot be routed.")
        elif not st.session_state.saved_gemini_key: 
            st.error("Input your Gemini Private Key in 'Tab 1' first.")
        else:
            with st.spinner("Processing solutions..."):
                try:
                    os.environ["GOOGLE_API_VERSION"] = "v1"
                    genai.configure(api_key=st.session_state.saved_gemini_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    support_prompt = f"Fix this issue safely: {user_query}. Respond natively in simple instructions."
                    response = model.generate_content(support_prompt)
                    st.info(response.text)
                except Exception as api_err:
                    st.error(f"Network Fault: {str(api_err)}")
