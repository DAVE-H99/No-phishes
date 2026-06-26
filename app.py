import streamlit as st
import requests
import hashlib
import socket
from urllib.parse import urlparse
from datetime import datetime

# 1. SYSTEM PAGE SETUP
st.set_page_config(page_title="no-phishes | SOC Terminal", page_icon="🛡️", layout="wide")

# 2. HIGH-VISIBILITY PROFESSIONAL TACTICAL STYLING (CUSTOM CSS)
st.html("""
<style>
    /* Global Page Body and High Contrast Typography */
    .stApp {
        background-color: #0b0f19 !important;
        color: #f0f4f8 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* Massive Bold White Title Container */
    .title-container {
        background: #111827;
        padding: 30px;
        border-radius: 12px;
        border: 2px solid #1f2937;
        border-left: 6px solid #38bdf8;
        margin-bottom: 30px;
    }
    
    /* High Visibility Input Card Boxes (Solid dark slate background) */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #111827 !important;
        border: 2px solid #1f2937 !important;
        border-radius: 10px !important;
        padding: 25px !important;
    }
    
    /* Make Input Text Bright Green and High Contrast */
    input, select, textarea {
        background-color: #030712 !important;
        color: #38bdf8 !important;
        border: 2px solid #374151 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Focus highlights */
    input:focus {
        border-color: #38bdf8 !important;
    }
    
    /* Fix the hard-to-read small labels on top of fields */
    label p {
        color: #f3f4f6 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px;
    }
    
    /* Text font clarity for descriptions and marks */
    span, p, stMarkdown {
        color: #f3f4f6 !important;
        font-size: 1.05rem !important;
    }

    /* Giant High-Contrast Output Cards */
    .metric-wrapper {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #374151;
        text-align: center;
    }
    
    /* Primary Call to Action Button styling */
    div.stButton > button {
        background: #38bdf8 !important;
        color: #030712 !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        width: 100% !important;
        box-shadow: 0 4px 14px rgba(56, 189, 248, 0.4) !important;
    }
    div.stButton > button:hover {
        background: #0ea5e9 !important;
        color: #ffffff !important;
    }
</style>
""")

# 3. SECURE CREDENTIAL VAULT INTEGRATION
try:
    VT_API_KEY = st.secrets["VT_API_KEY"]
    DB_API_URL = st.secrets["DB_API_URL"]
except Exception:
    VT_API_KEY = "PASTE_YOUR_LOCAL_KEY_HERE_FOR_TESTING"
    DB_API_URL = ""

# 4. SOLID TOP BANNER
st.html("""
<div class="title-container">
    <h1 style="color: #ffffff; margin: 0; font-size: 2.2rem; font-weight: 800; letter-spacing: 1px;">🛡️ PROJECT NO-PHISHES</h1>
    <p style="color: #9ca3af; margin: 8px 0 0 0; font-size: 1.1rem; font-weight: 500;">Phishing Attack Forensic Harvester & Live Threat Infrastructure Analyzer</p>
</div>
""")

# 5. SPLIT COLUMN INTERFACE GRAPHIC GRID
col_input, col_space, col_output = st.columns([1.2, 0.1, 1.8])

with col_input:
    st.markdown("<h2 style='color: #38bdf8; margin-top:0; font-weight:800;'>📥 TARGET DATA INPUT</h2>", unsafe_allow_html=True)
    
    platform = st.selectbox("1. Attack Vector / Platform Used:", ["Gmail / Email", "WhatsApp", "SMS", "Instagram", "Discord", "LinkedIn", "Other"])
    sender_identity = st.text_input("2. Attacker Identity (Email/Phone/User):", placeholder="e.g., login-security@axis-verify.com")
    receiver_identity = st.text_input("3. Victim / Target Identity (Email/Phone):", placeholder="e.g., student@cusp.edu")
    phishing_url = st.text_input("4. Suspicious Malicious URL / Link:", placeholder="https://secure-login-portal.net")
    
    st.markdown("<br>", unsafe_allow_html=True)
    submit_btn = st.button("🚀 RUN FORENSIC THREAT HARVEST")

with col_output:
    st.markdown("<h2 style='color: #38bdf8; margin-top:0; font-weight:800;'>📊 TELEMETRY REPORT OUTPUT</h2>", unsafe_allow_html=True)
    
    if submit_btn:
        if not phishing_url:
            st.error("❌ CRITICAL ERROR: You must provide a suspect website link to trigger the analyzer modules.")
        else:
            with st.spinner("Harvesting network infrastructure fingerprints..."):
                try:
                    parsed_url = urlparse(phishing_url)
                    domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
                    ip_address = socket.gethostbyname(domain)
                    geo_resp = requests.get(f"https://ipapi.co/{ip_address}/json/").json()
                    country = geo_resp.get("country_name", "Unknown Zone")
                    isp = geo_resp.get("org", "Unknown Network Host")
                except Exception:
                    ip_address, country, isp = "Failed Resolution", "Unknown Zone", "Unknown Network Host"

                url_id = hashlib.sha256(phishing_url.encode()).hexdigest()
                api_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
                headers = {"accept": "application/json", "x-apikey": VT_API_KEY}
                vt_response = requests.get(api_url, headers=headers)
                malicious_count = 0
                if vt_response.status_code == 200:
                    malicious_count = vt_response.json()['data']['attributes']['last_analysis_stats'].get('malicious', 0)
                
                # --- LIVE REAL-TIME DATABASE TRANSACTION ---
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if DB_API_URL:
                    payload = {
                        "time": current_time, "platform": platform, 
                        "sender": sender_identity if sender_identity else "Unknown",
                        "receiver": receiver_identity if receiver_identity else "Unknown",
                        "url": phishing_url, "ip": ip_address, "country": country, "flags": malicious_count
                    }
                    try:
                        requests.post(DB_API_URL, json=payload)
                    except Exception:
                        pass
                
                # --- METRIC PRESENTATION DISPLAY ---
                st.markdown("<h3 style='color: #ffffff; margin-bottom: 5px;'>📇 Target Framework Data</h3>", unsafe_allow_html=True)
                st.markdown(f"🔹 **Platform Delivery Stream:** `{platform}`")
                st.markdown(f"🔹 **Identified Threat Actor (Sender):** `{sender_identity if sender_identity else 'Anonymous Origin'}`")
                st.markdown(f"🔹 **Targeted Asset Point (Receiver):** `{receiver_identity if receiver_identity else 'Anonymous Target'}`")
                
                st.markdown("<hr style='border-color: #374151;'/>", unsafe_allow_html=True)
                st.markdown("<h3 style='color: #ffffff; margin-bottom: 15px;'>🌐 Infrastructure & Origin Routing</h3>", unsafe_allow_html=True)
                
                mc1, mc2, mc3 = st.columns(3)
                with mc1:
                    st.markdown(f"<div class='metric-wrapper'><p style='margin:0; color:#9ca3af; font-size:0.9rem;'>SERVER IP</p><h4 style='margin:5px 0 0 0; color:#38bdf8;'>{ip_address}</h4></div>", unsafe_allow_html=True)
                with mc2:
                    st.markdown(f"<div class='metric-wrapper'><p style='margin:0; color:#9ca3af; font-size:0.9rem;'>HOST COUNTRY</p><h4 style='margin:5px 0 0 0; color:#38bdf8;'>{country}</h4></div>", unsafe_allow_html=True)
                with mc3:
                    st.markdown(f"<div class='metric-wrapper'><p style='margin:0; color:#9ca3af; font-size:0.9rem;'>HOST ISP</p><h4 style='margin:5px 0 0 0; color:#38bdf8;'>{isp}</h4></div>", unsafe_allow_html=True)
                
                st.markdown("<hr style='border-color: #374151;'/>", unsafe_allow_html=True)
                st.markdown("<h3 style='color: #ffffff; margin-bottom: 15px;'>☣️ Global Threat Assessment Core</h3>", unsafe_allow_html=True)
                
                if malicious_count > 0:
                    st.markdown(f"<div style='background-color: #7f1d1d; border: 2px solid #ef4444; padding: 20px; border-radius: 8px; color: #fca5a5; font-size:1.1rem; font-weight:700;'>🚨 MALICIOUS THREAT DETECTED: This domain layout is confirmed malicious! Flagged by {malicious_count} global security vendor filters. Isolate immediately.</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='background-color: #064e3b; border: 2px solid #10b981; padding: 20px; border-radius: 8px; color: #a7f3d0; font-size:1.1rem; font-weight:700;'>🔒 INTEGRITY CHECK CLEAR
