import streamlit as st
import requests
import hashlib
import socket
from urllib.parse import urlparse

# Page Setup
st.set_page_config(page_title="no-phishes | Incident Forensics", page_icon="🛡️", layout="wide")

# Secure API Key Check
try:
    # This looks for the hidden key on the cloud server
    VT_API_KEY = st.secrets["VT_API_KEY"]
except Exception:
    # This is only used when running locally on your own computer
    VT_API_KEY = "PASTE_YOUR_LOCAL_KEY_HERE_FOR_TESTING"


st.title("🛡️ Project no-phishes: Phishing Forensic & Investigation Dashboard")
st.write("An advanced defensive tool to dissect phishing attempts, trace threat origins, and catalog target indicators.")
st.markdown("---")

# Layout: Split into Input Form and Results Dashboard
col_input, col_space, col_output = st.columns([1.2, 0.1, 1.8])

with col_input:
    st.subheader("📥 Input Incident Telemetry")
    
    # User's Ideas Implemented as Structured Fields
    platform = st.selectbox("Where was this attack attempted?", 
                            ["Gmail / Email", "WhatsApp", "SMS", "Instagram", "Discord", "LinkedIn", "Other"])
    
    sender_identity = st.text_input("Sender's Identity (Email, Phone #, or Username):", placeholder="e.g., support@secure-bank-update.com")
    receiver_identity = st.text_input("Receiver's / Victim's Identity (Email or Phone #):", placeholder="e.g., victim@gmail.com")
    phishing_url = st.text_input("Suspicious Phishing URL / Link:", placeholder="https://login-verification-page.com")
    
    submit_btn = st.button("🚀 Analyze & Log Attack Details")

with col_output:
    st.subheader("📊 Forensic Investigation Report")
    
    if submit_btn:
        if not phishing_url:
            st.warning("Please enter the suspicious URL to run the technical tracking.")
        elif VT_API_KEY in ["YOUR_API_KEY_HERE", "PASTE_YOUR_LOCAL_KEY_HERE_FOR_TESTING"]:
            st.error("Configuration Error: Missing VirusTotal API Key.")
        else:
            with st.spinner("Analyzing infrastructure and threat vectors..."):
                
                # --- Feature 1: Extract Server Infrastructure Data (Where it comes from) ---
                try:
                    parsed_url = urlparse(phishing_url)
                    domain = parsed_url.netloc if parsed_url.netloc else parsed_url.path
                    
                    # Resolve domain name to an IP Address
                    ip_address = socket.gethostbyname(domain)
                    
                    # Call a free GeoIP API to trace the location of the attacker's server
                    geo_resp = requests.get(f"https://ipapi.co/{ip_address}/json/").json()
                    country = geo_resp.get("country_name", "Unknown Location")
                    isp = geo_resp.get("org", "Unknown Hosting Provider")
                except Exception:
                    ip_address = "Could not resolve"
                    country = "Unknown Origin"
                    isp = "Unknown Infrastructure"

                # --- Feature 2: VirusTotal Security Scan ---
                url_id = hashlib.sha256(phishing_url.encode()).hexdigest()
                api_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
                headers = {"accept": "application/json", "x-apikey": VT_API_KEY}
                
                vt_response = requests.get(api_url, headers=headers)
                malicious_count = 0
                
                if vt_response.status_code == 200:
                    stats = vt_response.json()['data']['attributes']['last_analysis_stats']
                    malicious_count = stats.get('malicious', 0)
                
                # --- Displaying Your Custom Fields ---
                st.markdown("### 📇 Incident Metadata")
                st.write(f"**Platform Target Vectors:** Attempted via `{platform}`")
                st.write(f"**Attacker Footprint (Sender):** `{sender_identity if sender_identity else 'Not Disclosed'}`")
                st.write(f"**Victim Target Core (Receiver):** `{receiver_identity if receiver_identity else 'Not Disclosed'}`")
                
                st.markdown("---")
                st.markdown("### 🌐 Infrastructure & Origin Tracking")
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Resolved IP", ip_address)
                c2.metric("Hosting Origin Country", country)
                c3.metric("Hosting Network (ISP)", isp)
                
                st.markdown("---")
                st.markdown("### ☣️ Global Threat Assessment")
                if malicious_count > 0:
                    st.error(f"🚨 ALERT: Confirmed Threat. Flagged by {malicious_count} security vendors.")
                else:
                    st.success("🔒 System Advisory: No immediate global malicious flags found on this URL footprint.")
    else:
        st.info("Fill out the incident telemetry form on the left to generate the live defensive forensic dashboard.")