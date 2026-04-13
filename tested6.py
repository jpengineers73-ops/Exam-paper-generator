from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from fpdf import FPDF
import os
import random

class ScienceExamApp(App):
    def build(self):
        # Updated Data Tree with Maths for both classes
        self.data_tree = {
            "Class 7": {
                "Science": ["Heat", "Light", "Electricity"],
                "Maths": ["Integers", "Fractions and Decimals", "Simple Equations"]
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

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.add_widget(Label(text="EXAM GENERATOR PRO", font_size=24, bold=True, color=(0.2, 0.8, 0.4, 1)))

        self.student_name = TextInput(hint_text="Enter Student Name", multiline=False, size_hint_y=None, height=50)
        self.school_name = TextInput(hint_text="Enter School Name", multiline=False, size_hint_y=None, height=50)
        self.layout.add_widget(self.student_name)
        self.layout.add_widget(self.school_name)

        self.std_spinner = Spinner(text='Select Class', values=tuple(self.data_tree.keys()), size_hint_y=None, height=50)
        self.std_spinner.bind(text=self.update_subjects)
        
        self.sub_spinner = Spinner(text='Select Subject', values=(), size_hint_y=None, height=50)
        self.sub_spinner.bind(text=self.update_chapters)
        
        self.chp_spinner = Spinner(text='Select Chapter', values=(), size_hint_y=None, height=50)

        self.layout.add_widget(self.std_spinner)
        self.layout.add_widget(self.sub_spinner)
        self.layout.add_widget(self.chp_spinner)

        self.btn = Button(text="GENERATE PAPER (50 Marks)", size_hint_y=None, height=80, background_color=(0.1, 0.6, 0.2, 1), bold=True)
        self.btn.bind(on_press=self.generate_exam)
        self.layout.add_widget(self.btn)
        
        self.status = Label(text="Ready", font_size=14)
        self.layout.add_widget(self.status)
        return self.layout

    def update_subjects(self, spinner, text):
        if text in self.data_tree:
            self.sub_spinner.values = tuple(self.data_tree[text].keys())
            self.sub_spinner.text = 'Select Subject'
            self.chp_spinner.values = ()
            self.chp_spinner.text = 'Select Chapter'

    def update_chapters(self, spinner, text):
        std = self.std_spinner.text
        if std in self.data_tree and text in self.data_tree[std]:
            self.chp_spinner.values = tuple(self.data_tree[std][text])
            self.chp_spinner.text = 'Select Chapter'

    def clean_text(self, text):
        replacements = {'\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2013': '-', '\u2014': '-'}
        for u, a in replacements.items():
            text = text.replace(u, a)
        return text.encode('latin-1', 'ignore').decode('latin-1')

    def generate_exam(self, instance):
        std, sub, chp = self.std_spinner.text, self.sub_spinner.text, self.chp_spinner.text
        name, school = self.student_name.text.strip(), self.school_name.text.strip()
        
        if any(x.startswith("Select") for x in [std, sub, chp]) or not name:
            self.status.text = "⚠️ Fill all details!"
            return

        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, std, f"{chp}.txt")
        
        if not os.path.exists(filename):
            self.status.text = f"❌ Missing: {chp}.txt in {std}"
            return

        qa_bank = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if "|" in line:
                    q, a = line.split("|")
                    qa_bank.append({"q": self.clean_text(q), "a": self.clean_text(a)})

        random.shuffle(qa_bank)
        selected = qa_bank[:25] 

        pdf = FPDF()
        pdf.add_page()
        
        # Header Section
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(w=0, h=10, text=school.upper(), align='C', new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", '', 11)
        pdf.cell(w=95, h=8, text=f"Class: {std} | Subject: {sub}", align='L')
        pdf.cell(w=95, h=8, text=f"Total Marks: 50", align='R', new_x="LMARGIN", new_y="NEXT")
        
        pdf.cell(w=95, h=8, text=f"Topic: {chp}", align='L')
        pdf.cell(w=95, h=8, text=f"Time: 1.30 Hours", align='R', new_x="LMARGIN", new_y="NEXT")
        
        pdf.ln(2)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(w=0, h=10, text=f"STUDENT NAME: {name.upper()}", border='T', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

        # Questions
        pdf.set_font("Helvetica", '', 12)
        for i, item in enumerate(selected, 1):
            pdf.multi_cell(w=190, h=8, text=f"Q{i}. {item['q']} (2 Marks)")
            pdf.ln(2)

        # Answer Key Page (Compact)
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 15)
        pdf.cell(w=0, h=10, text="--- ANSWER KEY ---", align='C', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.set_font("Helvetica", '', 10)
        
        for i, item in enumerate(selected, 1):
            pdf.multi_cell(w=190, h=5, text=f"Q{i}: {item['a']}")
            pdf.ln(0.5)

        out_name = f"{name.replace(' ', '_')}_Maths_Science_Exam.pdf"
        try:
            pdf.output(out_name)
            self.status.text = f"✅ Saved: {out_name}"
        except Exception as e:
            self.status.text = f"❌ Error: {str(e)}"

if __name__ == '__main__':
    ScienceExamApp().run()
