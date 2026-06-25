import streamlit as st
import requests
import hashlib
import socket
from urllib.parse import urlparse
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="no-phishes | SOC Terminal", page_icon="⚡", layout="wide")

# 2. Inject Cyberpunk Custom CSS Styling
st.html("""
<style>
    /* Global Background and Main Vibe */
    .stApp {
        background-color: #0d1117 !important;
        color: #c9d1d9 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    
    /* Header Container Styling */
    .title-container {
        background: linear-gradient(135deg, #1f293d 0%, #0d1117 100%);
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #00ff66;
        box-shadow: 0 4px 20px rgba(0, 255, 102, 0.1);
        margin-bottom: 25px;
    }
    
    /* Input and Dashboard Card Customization */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 20px;
    }
    
    /* Force specific box borders to glow green on focus */
    input, select, textarea {
        background-color: #0d1117 !important;
        color: #00ff66 !important;
        border: 1px solid #30363d !important;
        font-family: 'Courier New', Courier, monospace !important;
    }
    input:focus {
        border-color: #00ff66 !important;
        box-shadow: 0 0 10px rgba(0, 255, 102, 0.5) !important;
    }
    
    /* Customization for the Primary Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #00ff66 0%, #00bc45 100%) !important;
        color: #0d1117 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 6px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 255, 102, 0.3) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 255, 102, 0.5) !important;
    }
</style>
""")

# 3. Secure API Key Vault Integration
try:
    VT_API_KEY = st.secrets["VT_API_KEY"]
except Exception:
    VT_API_KEY = "PASTE_YOUR_LOCAL_KEY_HERE_FOR_TESTING"

# 4. Styled Top Title Banner
st.html("""
<div class="title-container">
    <h1 style="color: #00ff66; margin: 0; font-size: 2.2rem;">⚡ PROJECT NO-PHISHES</h1>
    <p style="color: #8b949e; margin: 5px 0 0 0; font-size: 1rem;">Tactical Incident Forensics & Threat Infrastructure Tracking Console</p>
</div>
""")

# 5. Interface Split Layout
col_input, col_space, col_output = st.columns([1.2, 0.1, 1.8])

with col_input:
    st.markdown("<h3 style='color: #00ff66; margin-top:0;'>📥 ENGAGE INCIDENT FEED</h3>", unsafe_allow_html=True)
    
    platform = st.selectbox("Vectors / Delivery Platform:", 
                            ["Gmail / Email", "WhatsApp", "SMS", "Instagram", "Discord", "LinkedIn", "Other"])
    
    sender_identity = st.text_input("Attacker Signature (Email / Phone):", placeholder="e.g., alert@security-update-service.com")
    receiver_identity = st.text_input("Target Core Endpoint (Victim Destination):", placeholder="e.g., student_endpoint@cusp.edu")
    phishing_url = st.text_input("Payload URL / Suspect Link:", placeholder="https://malicious-login-portal.net")
    
    submit_btn = st.button("🚀 EXECUTE FORENSIC HARVEST")

with col_output:
    st.markdown("<h3 style='color: #00ff66; margin-top:0;'>📊 TERMINAL TELEMETRY READOUT</h3>", unsafe_allow_html=True)
    
    if submit_btn:
        if not phishing_url:
            st.warning("SYSTEM PROMPT: A target Payload URL is mandatory to execute lookup protocols.")
        elif VT_API_KEY in ["YOUR_API_KEY_HERE", "PASTE_YOUR_LOCAL_KEY_HERE_FOR_TESTING"]:
            st.error("HARDWARE ERROR: Global Threat Intelligence API access key missing.")
        else:
            with st.spinner("Decoding infrastructure payloads..."):
                
                # --- Infrastructure Logic ---
                try:
                    parsed_url = urlparse(phishing_url)
                    domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
                    ip_address = socket.gethostbyname(domain)
                    
                    geo_resp = requests.get(f"https://ipapi.co/{ip_address}/json/").json()
                    country = geo_resp.get("country_name", "Unknown Zone")
                    isp = geo_resp.get("org", "Unknown Core Network")
                except Exception:
                    ip_address = "Failed Resolution"
                    country = "Unknown Zone"
                    isp = "Unknown Core Network"

                # --- Threat Intel Analytics ---
                url_id = hashlib.sha256(phishing_url.encode()).hexdigest()
                api_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
                headers = {"accept": "application/json", "x-apikey": VT_API_KEY}
                
                vt_response = requests.get(api_url, headers=headers)
                malicious_count = 0
                
                if vt_response.status_code == 200:
                    stats = vt_response.json()['data']['attributes']['last_analysis_stats']
                    malicious_count = stats.get('malicious', 0)
                
                # --- Admin Output Terminal Tracker ---
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n[CRITICAL INCIDENT LOGGED - {current_time}]")
                print(f"Platform Vector: {platform} | Attacker: {sender_identity} | Victim: {receiver_identity}")
                print(f"URL: {phishing_url} | Node IP: {ip_address} ({country}) | Threats: {malicious_count}")
                print("-" * 60)
                
                # --- Graphical Dashboard Rendering ---
                st.markdown("<h4 style='color: #8b949e;'>📇 Target Classification Metrics</h4>", unsafe_allow_html=True)
                st.write(f"**Attack Vector Vectoring:** Intercepted via `{platform}`")
                st.write(f"**Threat Actor (Sender):** `{sender_identity if sender_identity else 'Anonymous Origin'}`")
                st.write(f"**Compromised Node (Receiver):** `{receiver_identity if receiver_identity else 'Anonymous Target'}`")
                
                st.markdown("<hr style='border-color: #30363d;'/>", unsafe_allow_html=True)
                st.markdown("<h4 style='color: #8b949e;'>🌐 Host Node Infrastructure Routing</h4>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Server Target IP", ip_address)
                c2.metric("Geographic Origin", country)
                c3.metric("Network Architecture (ISP)", isp)
                
                st.markdown("<hr style='border-color: #30363d;'/>", unsafe_allow_html=True)
                st.markdown("<h4 style='color: #8b949e;'>☣️ Global Threat Assessment Core</h4>", unsafe_allow_html=True)
                
                if malicious_count > 0:
                    st.markdown(f"<div style='background-color: rgba(255, 75, 75, 0.1); border: 1px solid #ff4b4b; padding: 15px; border-radius: 6px; color: #ff4b4b;'>🚨 **MALICIOUS INTENT CONFIRMED:** Blacklisted by {malicious_count} verified defense engines. Drop connections immediately.</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='background-color: rgba(0, 255, 102, 0.1); border: 1px solid #00ff66; padding: 15px; border-radius: 6px; color: #00ff66;'>🔒 **INTEGRITY NOMINAL:** Zero active malware or phishing signatures logged globally. Proceed with standard isolation tracking.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: #8b949e; font-style: italic;'>Console waiting for incident inputs. Populate data matrix in the left deck to execute analysis algorithms.</p>", unsafe_allow_html=True)
