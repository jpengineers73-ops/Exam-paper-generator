import streamlit as st
from datetime import datetime
# ... (rest of your imports stay the same)

# --- 1. USER ACCOUNTS WITH EXPIRY ---
# Format: "username": ["password", "YYYY-MM-DD"]
USERS = {
    "admin": ["admin123", "2026-12-31"], 
    "joy": ["joy73", "2024-05-20"],      # Example: Joy's sub expires soon
    "teacher1": ["science789", "2024-04-30"] 
}

def check_subscription(username):
    expiry_str = USERS[username][1]
    expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
    today = datetime.now().date()
    
    days_left = (expiry_date - today).days
    
    if days_left < 0:
        return "EXPIRED", 0
    return "ACTIVE", days_left

# --- 4. APP INTERFACE ---
# Inside your "if not st.session_state.logged_in:" block:
if login_button_clicked: # (Logic from your existing login)
    if user in USERS and USERS[user][0] == passwd:
        status, days = check_subscription(user)
        if status == "EXPIRED":
            st.error(f"❌ Your subscription expired on {USERS[user][1]}. Please renew below.")
            # Show your Payment QR code here
        else:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.rerun()

# Inside your "else:" (Logged in) block, add a reminder at the top:
status, days = check_subscription(st.session_state.user)
if days <= 5:
    st.warning(f"⚠️ Subscription Reminder: Your access expires in {days} days ({USERS[st.session_state.user][1]}).")


# --- 2. DATA CONFIGURATION ---
DATA_TREE = {
    "Class 7": {
        "Science": ["Heat", "Light", "Electricity"],
        "Maths": ["Integers", "Fractions and Decimals", "Simple equations", "Line and angles"]
    },
    "Class 8": {
        "Science": [
            "Crop Production and Management", 
            "Microorganisms Friend and Foe", 
            "Synthetic Fibres and Plastics"
        ],
        "Maths": ["Rational Numbers", "Linear Equations", "Understanding Quadrilaterals"]
    }
}

# --- 3. UTILITY FUNCTIONS ---
def clean_text(text):
    replacements = {'\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2013': '-', '\u2014': '-', '\u2022': '*'}
    for u, a in replacements.items():
        text = text.replace(u, a)
    return text.encode('latin-1', 'ignore').decode('latin-1')

def generate_pdf(school, student, std, sub, chp, questions):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(w=0, h=10, text=school.upper(), align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", '', 11)
    pdf.cell(w=95, h=8, text=f"Class: {std} | Subject: {sub}", align='L')
    pdf.cell(w=95, h=8, text=f"Total Marks: 50", align='R', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(w=95, h=8, text=f"Topic: {chp}", align='L')
    pdf.cell(w=95, h=8, text=f"Time: 1.30 Hours", align='R', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(w=0, h=10, text=f"STUDENT NAME: {student.upper()}", border='T', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Helvetica", '', 12)
    for i, item in enumerate(questions, 1):
        pdf.multi_cell(w=185, h=8, text=f"Q{i}. {item['q']} (2 Marks)")
        pdf.ln(2)
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 15)
    pdf.cell(w=0, h=10, text="--- ANSWER KEY ---", align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", '', 10)
    for i, item in enumerate(questions, 1):
        pdf.multi_cell(w=185, h=5, text=f"Q{i}: {item['a']}")
        pdf.ln(0.5)
    return pdf.output()

# --- 4. APP INTERFACE ---
st.set_page_config(page_title="Exam Generator Pro", page_icon="📝")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Exam_Paper Generator")
    user = st.text_input("Username")
    passwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user in USERS and USERS[user] == passwd:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid Username or Password")
            
    st.markdown("---")
    st.subheader("💳 Get Premium Access")
    
    # --- PAYMENT LOGIC ---
    upi_id = "9825072285@ptsbi"  # CHANGE THIS TO YOUR UPI ID
    biz_name = "Palash Group Tuition"
    pay_amount = "500"
    
    upi_url = f"upi://pay?pa={upi_id}&pn={biz_name.replace(' ', '%20')}&am={pay_amount}&cu=INR"
    qr = segno.make(upi_url)
    qr.save("upi_qr.png", scale=10)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.image("upi_qr.png", caption="Scan QR to Pay", width=180)
    with col_b:
        st.write(f"**Amount:** ₹{pay_amount}")
        st.markdown(
            f'<a href="{upi_url}" style="display: inline-block; padding: 12px 24px; background-color: #2e7d32; color: white; text-align: center; text-decoration: none; border-radius: 8px; font-weight: bold;">🚀 Pay via UPI App</a>',
            unsafe_allow_html=True
        )
    st.info("After payment, share the screenshot to whatsapp +9825072285 Admin to get your password.")

else:
    # --- MAIN APP ---
    st.sidebar.title("Welcome!")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("📝 Online Exam Generator")
    institute_name = st.text_input("Institute Name", "Palash Group Tuition")
    student_name = st.text_input("Student Name", placeholder="Enter student name...")

    col1, col2, col3 = st.columns(3)
    with col1:
        std_choice = st.selectbox("Class", options=list(DATA_TREE.keys()))
    with col2:
        sub_choice = st.selectbox("Subject", options=list(DATA_TREE[std_choice].keys()))
    with col3:
        chp_choice = st.selectbox("Chapter", options=DATA_TREE[std_choice][sub_choice])

    if st.button("Generate Paper"):
        if not student_name:
            st.error("Please enter a Student Name.")
        else:
            filename = os.path.join(std_choice, f"{chp_choice}.txt")
            if os.path.exists(filename):
                qa_bank = []
                with open(filename, "r", encoding="utf-8") as f:
                    for line in f:
                        if "|" in line:
                            parts = line.split("|")
                            if len(parts) >= 2:
                                qa_bank.append({"q": clean_text(parts[0].strip()), "a": clean_text(parts[1].strip())})
                
                if qa_bank:
                    random.shuffle(qa_bank)
                    selected = qa_bank[:25]
                    try:
                        pdf_data = generate_pdf(institute_name, student_name, std_choice, sub_choice, chp_choice, selected)
                        st.success(f"✅ Paper Generated for {student_name}!")
                        st.download_button(
                            label="📥 Download PDF", 
                            data=bytes(pdf_data), 
                            file_name=f"{sub_choice}_{chp_choice.replace(' ', '_')}.pdf", 
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"Error creating PDF: {e}")
                else:
                    st.error("File formatting error in .txt file.")
            else:
                st.error(f"File not found: {filename}")
