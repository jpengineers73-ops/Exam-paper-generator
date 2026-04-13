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
