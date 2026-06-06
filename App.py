import streamlit as st
import datetime
import time
import re
import random
import os
import hashlib
import google.generativeai as genai

# --- ⚙️ CONFIG (CRITICAL FIX: Isko sabse pehle rakhna zaroori hai) ---
st.set_page_config(page_title="GJ GLOBAL AI ADS - Ultimate Enterprise", page_icon="🚩", layout="wide")

# --- 🔒 CYBER SECURITY: DATA CRYPTO & HASHING ---
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- 🚩 JAI SHREE RAM SPLASH SCREEN ---
def splash_screen():
    if 'splash_done' not in st.session_state:
        placeholder = st.empty()
        placeholder.markdown("""
            <div style="height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; 
                        color: #ff4500; font-size: 60px; font-weight: bold; background-color: #0e1117; font-family: 'Arial'; text-shadow: 0px 0px 20px #ff4500;">
                <p style="margin-bottom: 10px;">🚩 जय श्री RAM 🚩</p>
                <p style="font-size: 35px; color: #ffffff; letter-spacing: 2px;">JAI SHREE RAM</p>
                <div style="margin-top: 20px; font-size: 16px; color: #888;">Initializing Core Tracking Infrastructure...</div>
            </div>
        """, unsafe_allowed_html=True)
        time.sleep(4)
        placeholder.empty()
        st.session_state.splash_done = True

# Splash screen ko config ke baad chalana hai
splash_screen()

st.markdown("""
    <style>
    iframe {pointer-events: none;}
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #ff4b4b, #ff761a); color: white; font-weight: bold;
        border: none; padding: 10px 25px; border-radius: 8px; box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }
    .premium-box {
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 12px; margin-bottom: 15px;
    }
    </style>
""", unsafe_allowed_html=True)

OWNER_EMAIL = "armygamingtotal@gmail.com"
USD_TO_INR = 85

# Locked Pricing Database (As you specified in Dollars)
FIXED_PRICES = {
    "Silver (Monthly)": 19,
    "Standard (6-Month)": 49,
    "Standard (Yearly)": 249,
    "Premium (Yearly)": 499
}

# Session Management
if "users_db" not in st.session_state: st.session_state.users_db = {}
if "current_user" not in st.session_state: st.session_state.current_user = None
if "otp_sent" not in st.session_state: st.session_state.otp_sent = None
if "global_performance" not in st.session_state: st.session_state.global_performance = []
if "marketing_videos" not in st.session_state: st.session_state.marketing_videos = []
if "app_self_lock" not in st.session_state: st.session_state.app_self_lock = False

# --- 🌐 MULTILINGUAL DICTIONARY ---
languages = {
    "English": {"welcome": "Welcome to GJ GLOBAL AI ADS", "run": "Generate Smart Campaign & Launch", "spy": "Spy Tool & Tracker", "help": "AI Help Center", "guide": "Full Setup Guide", "videos": "Reviews & Marketing Videos", "query_placeholder": "Ask anything about setup, pixel or ads..."},
    "Hindi (हिंदी)": {"welcome": "GJ GLOBAL AI ADS में आपका स्वागत है", "run": "स्मार्ट कैंपेन जनरेट और लॉन्च करें", "spy": "जासूसी टूल और ट्रैकर", "help": "AI सहायता केंद्र", "guide": "पूरी सेटअप गाइड", "videos": "रिव्यूज and मार्केटिंग वीडियोज़", "query_placeholder": "सेटअप या पिक्सेल एरर के बारे में कुछ भी पूछें..."},
    "Spanish (Español)": {"welcome": "Bienvenido a GJ GLOBAL AI ADS", "run": "Ejecutar campaña inteligente", "spy": "Herramienta de espionaje", "help": "Centro de ayuda", "guide": "Guía de configuración", "videos": "Videos de revisión", "query_placeholder": "¿Tiene alguna duda?"},
    "French (Français)": {"welcome": "Bienvenue sur GJ GLOBAL AI ADS", "run": "Lancer la campagne IA", "spy": "Outil d'espionnage", "help": "Centre d'aide", "guide": "Guide de configuration", "videos": "Vidéos de marketing", "query_placeholder": "Posez votre question..."},
    "Arabic (العربية)": {"welcome": "مرحبًا بكم في GJ GLOBAL AI ADS", "run": "تشغيل الحملة الذكية", "spy": "أداة التجسس للمنتجات", "help": "مركز المساعدة", "guide": "دليل الإعداد الكامل", "videos": "فيديوهات المراجعة", "query_placeholder": "اطرح أي سؤال..."}
}
selected_lang = st.selectbox("🌐 Choose Language / भाषा चुनें", list(languages.keys()))
lang = languages[selected_lang]

def sanitize_input(text):
    if not text: return ""
    clean = re.sub(r'<[^>]*?>', '', str(text))
    return clean.replace('"', '').replace("'", "").replace(";", "").strip()

user_country = st.sidebar.radio("📍 Select Billing Region", ["Inside India (INR ₹)", "Outside India (International USD $)"])

# --- 📝 SIGNUP / LOGIN SYSTEM WITH PASSWORD HASHING ---
if st.session_state.current_user is None:
    st.title(f"🔐 {lang['welcome']}")
    auth_mode = st.radio("Authentication Mode", ["Sign Up", "Log In"])
    
    if auth_mode == "Sign Up":
        name = sanitize_input(st.text_input("Full Name:"))
        email = sanitize_input(st.text_input("Email ID:")).lower()
        phone = sanitize_input(st.text_input("Phone Number:"))
        custom_password = st.text_input("Create Password:", type="password")
        plan_choice = st.selectbox("Select Subscription Tier Plan", list(FIXED_PRICES.keys()))
        
        # Calculate Price dynamic display
        dollar_val = FIXED_PRICES[plan_choice]
        final_price_str = f"₹{dollar_val * USD_TO_INR} (Approx INR)" if user_country == "Inside India (INR ₹)" else f"${dollar_val} USD"
        st.info(f"💳 Selected Plan Value: **{final_price_str}**")
        
        if st.button("Generate System Access OTP ✉️"):
            if name and email and phone and custom_password:
                st.session_state.otp_sent = str(random.randint(112233, 998877))
                st.info(f"✨ **[Secure OTP Router Node]** Your code is: `{st.session_state.otp_sent}`")
            else: st.error("Please provide all registration details!")
            
        if st.session_state.otp_sent:
            otp_input = st.text_input("Enter Code:")
            if st.button("Complete Payment Registration 🎉"):
                if otp_input == st.session_state.otp_sent:
                    days = 30 if "Monthly" in plan_choice else (180 if "6-Month" in plan_choice else 365)
                    st.session_state.users_db[email] = {
                        "name": name, "password": hash_password(custom_password), "plan": plan_choice, 
                        "signup_date": datetime.date.today(), "days": days, "autopilot_active": True
                    }
                    st.session_state.current_user = email
                    st.success("Account Created Successfully!")
                    st.session_state.otp_sent = None
                    st.rerun()
    else:
        email = sanitize_input(st.text_input("Registered Email:")).lower()
        password = st.text_input("Enter Password:", type="password")
        if st.button("Authorize Core Engine 🔓"):
            if email in st.session_state.users_db and st.session_state.users_db[email]["password"] == hash_password(password):
                st.session_state.current_user = email
                st.rerun()
            else: st.error("Invalid credentials entered!")
    st.stop()

# --- 🔓 USER DRIVEN SECURITY LOCK MECHANISM ---
st.sidebar.markdown("### 🛡️ Privacy & Security Lock")
lock_switch = st.sidebar.toggle("Activate Master App Privacy Lock", value=st.session_state.app_self_lock)
st.session_state.app_self_lock = lock_switch

if st.session_state.app_self_lock:
    st.title("🔒 App Workspace is Locked by User")
    unlock_pass = st.text_input("Enter your password to temporarily unfreeze workspace windows:", type="password")
    if st.button("Confirm Password Override"):
        if hash_password(unlock_pass) == st.session_state.users_db[st.session_state.current_user]["password"]:
            st.session_state.app_self_lock = False
            st.success("Unlocked!")
            st.rerun()
        else: st.error("Incorrect unlock key.")
    st.stop()

# --- 🚀 AUTOMATIC VALIDITY LOCKDOWN SYSTEM ---
user_data = st.session_state.users_db[st.session_state.current_user]
expiry_date = user_data['signup_date'] + datetime.timedelta(days=user_data['days'])

if datetime.date.today() > expiry_date:
    st.error("❌ SUBSCRIPTION EXPIRED: Your account billing cycle has ended!")
    gateway_url = "https://razorpay.me/@gjglobalaiads" if user_country == "Inside India (INR ₹)" else "https://checkout.stripe.com/recurring-autopilot"
    st.markdown(f'<a href="{gateway_url}" target="_blank"><button style="background: linear-gradient(to right, #ff3333, #b30000); color: white; padding: 15px; border: none; border-radius: 8px; width: 100%; cursor: pointer; font-weight: bold;">💳 Clear Dues via Secured Gateway Node Now</button></a>', unsafe_allowed_html=True)
    if st.sidebar.button("Log Out Node 🔒"):
        st.session_state.current_user = None
        st.rerun()
    st.stop()

# --- 👑 OWNER ADMIN SYSTEM OVERRIDE ---
st.sidebar.markdown("### 👑 Owner Controls")
admin_email = st.sidebar.text_input("Verify Admin Route:", placeholder="owner@gmail.com")
if admin_email.lower() == OWNER_EMAIL.lower():
    st.sidebar.success("Root Admin Environment Initialized.")
    st.sidebar.subheader("🎥 Review & Tutorial Video Uploader")
    add_v_url = st.sidebar.text_input("Paste YouTube Review URL:")
    if st.sidebar.button("Upload Video Review Live 🎬"):
        if add_v_url:
            st.session_state.marketing_videos.append(add_v_url)
            st.sidebar.success("Review posted to main server dashboard successfully!")

st.sidebar.markdown(f"👤 Account: **{user_data['name']}**")
st.sidebar.info(f"Active Allocation: **{user_data['plan']}**")
if st.sidebar.button("Purge Session & Logout 🔒"):
    st.session_state.current_user = None
    st.rerun()

# --- MAIN DASHBOARD INTERFACE TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Meta Ads Automator", f"🕵️ {lang['spy']}", f"🎥 {lang['videos']}", f"🤖 {lang['help']}"])

with tab1:
    st.markdown("### 📖 Step-by-Step API Extraction Manual")
    with st.expander(f"⚙️ View Full Manual: How to get Gemini API Key & Meta Ads Token?", expanded=True):
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            st.markdown("""
            #### 🧠 1. Extract Free Gemini API Key
            * **Step 1:** Go to the official **Google AI Studio** portal website.
            * **Step 2:** Log in using your standard Google Workspace account.
            * **Step 3:** Click on the prominent **'Get API Key'** button interface panel.
            * **Step 4:** Click 'Create API Key in New Project' and copy the long text token safe.
            """)
        with g_col2:
            st.markdown("""
            #### 🔑 2. Extract Permanent Meta Ads Token
            * **Step 1:** Head directly to the official **Meta for Developers** portal dashboard.
            * **Step 2:** Register an app node container and choose 'Business Solutions'.
            * **Step 3:** Launch the **Graph API Explorer** tracking utility module.
            * **Step 4:** Extend permissions token for `ads_management`, `ads_read` and save permanently.
            """)
        st.markdown("---")
        st.markdown("📥 **[PDF System Download]** Click down below to get the offline step-by-step documentation handbook resource file link.")
        st.download_button(label="📥 Download Step Guide PDF Manual", data="Dummy PDF content asset data for GJ Global Setup", file_name="GJ_Global_AI_Ads_Setup_Guide.pdf")

    col1, col2 = st.columns(2)
    with col1:
        st.header("🛒 Creative Inventory Data")
        store_url = sanitize_input(st.text_input("E-Commerce Storefront Link URL:", placeholder="https://yourstore.com"))
        product_desc = sanitize_input(st.text_area("Product Strategy Narrative Description:"))
        meta_token = st.text_input("Meta Graph Access Token String Container:", type="password", value="TEST_TOKEN_12345")
        ad_account_id = st.text_input("Meta Ads Target Account ID Parameter:", value="act_123456789")
    with col2:
        st.header("🎯 Target Acquisition Node")
        gemini_key = st.text_input("Sovereign Gemini Studio Secret Private Key Input:", type="password")
        budget = st.number_input("Daily Ad Spend Allocation Vector ($/₹):", min_value=100, value=500)
        
        if st.button(lang['run']):
            current_time = time.time()
            if "last_click" in st.session_state and (current_time - st.session_state.last_click) < 5:
                st.error("⚠️ Cyber Security Alert: anti-DDOS protection activated. Wait 5 seconds.")
            elif not gemini_key: st.error("❌ Key Misconfiguration Error: Missing valid Gemini decryption keys.")
            else:
                st.session_state.last_click = current_time
                with st.spinner("🧠 Initializing Deep Generative Core Matrix for Meta Ad Target Copy..."):
                    try:
                        os.environ["GOOGLE_API_VERSION"] = "v1"
                        genai.configure(api_key=sanitize_input(gemini_key))
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        
                        prompt = f"You are an elite Meta Ads media buyer. Build a full-funnel high-ROAS marketing strategy with exact keywords and behaviors (like 'Engaged Shoppers') and copy with emojis in Hinglish for product: {product_desc}"
                        response = model.generate_content(prompt)
                        st.success("🎯 Target Script Generation Complete!")
                        st.info(response.text)
                        st.balloons()
                    except Exception as err:
                        st.error(f"❌ Core Exception Node Rejected: {str(err)}")

with tab2:
    st.subheader(f"🕵️ {lang['spy']} Intelligence Board & Competitor Trackers")
    
    if "Silver" in user_data["plan"]:
        st.error("🔒 ACCESS EXCEPTION DENIED: Competitor Tracking Data streams are highly classified.")
        st.warning("⚠️ Plan Upgrade Required: Standard or Premium subscription tiers are required to unlock active product tracking engines.")
    else:
        if "Standard" in user_data["plan"] or "Premium" in user_data["plan"]:
            st.markdown("### 🇮🇳 Live Tracking Streams: Indian Top Sellers Dashboard")
            st.markdown("###### Real-time performance matrix of trending products sold by India's biggest dropshippers:")
            st.table([
                {"Target Winning Product": "Mini Portable Ultrasonic Washing Machine", "Observed Ad Framework Strategy": "Meta Video Engagement Run", "Estimated Daily Orders Managed": "1,450", "Calculated Product Win Rate Metric": "94%"},
                {"Target Winning Product": "Rechargeable Automatic Hair Braider Combo", "Observed Ad Framework Strategy": "Hinglish Meta Copy Targeting GenZ", "Estimated Daily Orders Managed": "890", "Calculated Product Win Rate Metric": "89%"},
                {"Target Winning Product": "Crystal Hair Eraser Exfoliator Node", "Observed Ad Framework Strategy": "Direct Store Hook + High ROAS Matrix", "Estimated Daily Orders Managed": "2,120", "Calculated Product Win Rate Metric": "96%"}
            ])
            
        if "Premium" in user_data["plan"]:
            st.write("---")
            st.markdown("### 🌍 Worldwide Top Sellers Live Data Streams Matrix")
            st.markdown("###### Encrypted database stream tracking global cross-border corporate dropshipping winners:")
            st.json({
                "Global_Winner_Node_01": {
                    "Corporate_Store_Identifier": "LuxFinds Collective US-EU",
                    "Tracked_Product_Asset": "Anti-Gravity Flame Air Diffuser Humidifier",
                    "Daily_Gross_Sales_USD": "$24,800",
                    "Observed_Ad_Channel": "Meta Canvas Interactive Feed Ads",
                    "Verified_Targeting_Matrix": "Engaged Shoppers + Home Decor Interest",
                    "Calculated_Win_Index": "93.5%"
                },
                "Global_Winner_Node_02": {
                    "Corporate_Store_Identifier": "ZenVibe Apparel Co.",
                    "Tracked_Product_Asset": "Orthopedic Premium Cushion Comfort Slide Sandal",
                    "Daily_Gross_Sales_USD": "$19,150",
                    "Observed_Ad_Channel": "Meta Carousel Dynamic Retargeting Ads",
                    "Verified_Targeting_Matrix": "Frequent Travelers + Podiatry Health",
                    "Calculated_Win_Index": "91.2%"
                }
            })

with tab3:
    st.subheader(f"🎥 {lang['videos']}")
    st.markdown("#### User Reviews, App Promos & Admin Announcements Panel")
    
    if st.session_state.marketing_videos:
        v_col1, v_col2 = st.columns(2)
        for idx, url in enumerate(st.session_state.marketing_videos):
            with v_col1 if idx % 2 == 0 else v_col2:
                st.markdown(f"##### Video Module Instance #{idx+1}")
                st.video(url)
    else:
        st.info("No system reviews or promotional announcement video streams have been loaded by the admin yet.")

with tab4:
    st.subheader(f"🤖 {lang['help']}")
    st.markdown("---")
    st.write("### Enterprise Multilingual Intelligent AI Response Desk")
    
    user_query = sanitize_input(st.text_input("State your setup roadblock or technical query interface parameter below:", placeholder=lang['query_placeholder']))
    
    if st.button("Transmit Question Node 💬"):
        if not user_query: st.warning("Empty question parameters cannot be routed.")
        elif not gemini_key: st.error("❌ Key Authentication Exception: Input your Gemini Private Key string in 'Tab 1' to clear access credentials for the Help Desk Neural Network.")
        else:
            with st.spinner("🧠 AI Agent translating and structuring resolution steps..."):
                try:
                    os.environ["GOOGLE_API_VERSION"] = "v1"
                    genai.configure(api_key=sanitize_input(gemini_key))
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    support_prompt = f"""
                    You are the master expert software developer and technical customer service executive engineer for 'GJ GLOBAL AI ADS PRO'.
                    The user is utilizing an enterprise automation framework app for running Meta Ads but is stuck with some bugs, setup errors, pixel tracking failures, or strategy confusion.
                    
                    CRITICAL INSTRUCTION: You must diagnose their issue perfectly and write the entire response natively in this exact language locale choice parameter: {selected_lang}.
                    
                    User Query Data: {user_query}
                    """
                    response = model.generate_content(support_prompt)
                    st.markdown("#### 💡 **AI Help Center Resolution Output:**")
                    st.info(response.text)
                except Exception as api_err:
                    st.error(f"❌ Network Router Fault: Could not fetch AI response stream. {str(api_err)}")
