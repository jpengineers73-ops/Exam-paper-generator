import streamlit as st
from fpdf import FPDF
import os
import random
import segno
from datetime import datetime

# --- 1. USER ACCOUNTS ---
# Format: "username": ["password", "YYYY-MM-DD"]
USERS = {
    "admin": ["admin123", "2026-12-31"], 
    "joy": ["joy73", "2026-05-20"]
}

# --- 2. DATA & UTILS ---
# (Clean_text, generate_pdf, and get_days_left functions remain the same as before)
def clean_text(text):
    replacements = {'\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2013': '-', '\u2014': '-', '\u2022': '*'}
    for u, a in replacements.items(): text = text.replace(u, a)
    return text.encode('latin-1', 'ignore').decode('latin-1')

def generate_pdf(school, student, std, sub, chp, questions):
    pdf = FPDF(); pdf.set_auto_page_break(auto=True, margin=15); pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16); pdf.cell(w=0, h=10, text=school.upper(), align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", '', 11); pdf.cell(w=95, h=8, text=f"Class: {std} | Subject: {sub}", align='L'); pdf.cell(w=95, h=8, text=f"Total Marks: 50", align='R', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(w=0, h=10, text=f"STUDENT: {student.upper()}", border='T', new_x="LMARGIN", new_y="NEXT"); pdf.ln(5)
    pdf.set_font("Helvetica", '', 12)
    for i, item in enumerate(questions, 1):
        pdf.multi_cell(w=185, h=8, text=f"Q{i}. {item['q']} (2 Marks)"); pdf.ln(2)
    return pdf.output()

def get_days_left(username):
    expiry_date = datetime.strptime(USERS[username][1], "%Y-%m-%d").date()
    return (expiry_date - datetime.now().date()).days

# --- 3. STREAMLIT UI ---
st.set_page_config(page_title="Exam Generator Pro", page_icon="📝")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Staff Portal")
    
    # --- ADDING TABS FOR LOGIN & REGISTER ---
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register New Account"])
    
    with tab1:
        u_input = st.text_input("Username", key="login_user")
        p_input = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if u_input in USERS and USERS[u_input][0] == p_input:
                days = get_days_left(u_input)
                if days < 0: st.error("❌ Account Expired. Renew below.")
                else:
                    st.session_state.logged_in = True
                    st.session_state.current_user = u_input
                    st.rerun()
            else: st.error("Invalid credentials")

    with tab2:
        st.subheader("Create your credentials")
        reg_user = st.text_input("Choose Username", placeholder="e.g. amit_science")
        reg_pass = st.text_input("Choose Password", type="password")
        reg_school = st.text_input("School/Institute Name")
        
        if st.button("Submit Registration"):
            if reg_user and reg_pass:
                st.success(f"✅ Details for '{reg_user}' submitted! Now pay ₹500 below to activate your account.")
                st.info("Note: Your account will be active within 1 hour after payment verification.")
            else:
                st.warning("Please fill in Username and Password.")

    st.markdown("---")
    st.subheader("💳 Payment for Activation")
    
    # UPI PAYMENT LOGIC (Change to your UPI ID)
    upi_id = "9825072285@ptsbi" 
    upi_url = f"upi://pay?pa={upi_id}&pn=Palash%20Tuition&am=500&cu=INR"
    qr = segno.make(upi_url)
    
    c1, c2 = st.columns(2)
    with c1: st.image(qr.png_data_uri(scale=10), width=180)
    with c2:
        st.write("**Price:** ₹500 / Month")
        st.markdown(f'<a href="{upi_url}" style="display:inline-block;padding:12px;background:#2e7d32;color:white;text-decoration:none;border-radius:8px;">🚀 Pay via UPI App</a>', unsafe_allow_html=True)
    st.info("WhatsApp screenshot + your chosen Username to Admin after payment.")

else:
    # --- LOGGED IN APP ---
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))
    st.title("📝 Online Exam Generator")
    # ... (Rest of your generation logic remains here)
