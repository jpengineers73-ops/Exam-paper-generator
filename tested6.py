import streamlit as st
from fpdf import FPDF
import os
import random

# --- 1. DATA CONFIGURATION ---
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

# --- 2. UTILITY FUNCTIONS ---
def clean_text(text):
    """Replaces characters that Helvetica cannot render."""
    replacements = {
        '\u2018': "'", '\u2019': "'", 
        '\u201c': '"', '\u201d': '"', 
        '\u2013': '-', '\u2014': '-',
        '\u2022': '*'
    }
    for u, a in replacements.items():
        text = text.replace(u, a)
    return text.encode('latin-1', 'ignore').decode('latin-1')

def generate_pdf(school, student, std, sub, chp, questions):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- Page 1: Question Paper ---
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

    # --- Page 2: Answer Key ---
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 15)
    pdf.cell(w=0, h=10, text="--- ANSWER KEY ---", align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", '', 10)
    for i, item in enumerate(questions, 1):
        pdf.multi_cell(w=185, h=5, text=f"Q{i}: {item['a']}")
        pdf.ln(0.5)
        
    return pdf.output()

# --- 3. STREAMLIT WEB UI ---
st.set_page_config(page_title="Exam Generator Pro", page_icon="📝")
st.title("📝 Online Exam Generator")

school_name = st.text_input("School Name", "Global Public School")
student_name = st.text_input("Student Name", placeholder="Type student name here...")

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
                            q, a = parts[0], parts[1]
                            qa_bank.append({
                                "q": clean_text(q.strip()), 
                                "a": clean_text(a.strip())
                            })
            
            if qa_bank:
                random.shuffle(qa_bank)
                selected = qa_bank[:25]
                
                try:
                    pdf_data = generate_pdf(school_name, student_name, std_choice, sub_choice, chp_choice, selected)
                    st.success(f"✅ Paper Generated for {student_name}!")
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_data,file_name=f"{sub_choice}_{chp_choice}.pdf
                        file_name=f"{sub_choice}_{chp_choice}.pdf",
                        mime="application/pdf"
                        st.download_button(
    label="📥 Download PDF",
    data=bytes(pdf_data),  # This converts bytearray to standard bytes
    file_name=f"{sub_choice}_{chp_choice}.pdf",
    mime="application/pdf"
                except Exception as e:
                    st.error(f"Error creating PDF: {e}")
            else:
                st.error("File format error: Use 'Question | Answer' in your txt files.")
        else:
            st.error(f"File not found: {filename}. Check your GitHub folders.")
         
