import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import hashlib
import datetime
import plotly.express as px
from fpdf import FPDF
import os

# Load custom CSS
def load_css():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(to right, #1a1a1a, #2d3436);
            color: #ffffff;
        }
        .stButton>button {
            background-color: #6c5ce7;
            color: white;
            border-radius: 10px;
            padding: 0.5rem 2rem;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #a29bfe;
            transform: translateY(-2px);
        }
        .css-1d391kg {
            background-color: #2d3436;
        }
        .stTextInput>div>div>input {
            background-color: #2d3436;
            color: white;
        }
        .stSelectbox>div>div>input {
            background-color: #2d3436;
            color: white;
        }
        .custom-card {
            background-color: #2d3436;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        @media (max-width: 600px) {
            .stButton>button {
                width: 100%;
            }
        }
        </style>
    """, unsafe_allow_html=True)

# Database Setup
def init_db():
    conn = sqlite3.connect('grades.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, signup_date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS records
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, ref_number INTEGER, name TEXT,
                  subjects TEXT, professors TEXT, marks TEXT, average REAL, grade TEXT)''')
    conn.commit()
    return conn

# Password Hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User Authentication
def signup(username, password, signup_date):
    if not username or not password or not signup_date:
        st.error("All fields are required.")
        return

    conn = init_db()
    c = conn.cursor()
    hashed_password = hash_password(password + str(signup_date))
    try:
        c.execute("INSERT INTO users (username, password, signup_date) VALUES (?, ?, ?)",
                  (username, hashed_password, str(signup_date)))
        conn.commit()
        st.success("Signup successful! Please login.")
    except sqlite3.IntegrityError:
        st.error("Username already exists.")

def login(username, password, login_date):
    if not username or not password or not login_date:
        st.error("All fields are required.")
        return

    conn = init_db()
    c = conn.cursor()
    hashed_password = hash_password(password + str(login_date))
    c.execute("SELECT id, signup_date FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = c.fetchone()
    if user:
        if str(login_date) == user[1]:  # Check if the login date matches the signup date
            st.session_state.user_id = user[0]
            st.success("Login successful!")
        else:
            st.error("Invalid date. Please use the date you signed up with.")
    else:
        st.error("Invalid username or password.")

# Grade Manager Class
class GradeManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.grade_thresholds = {'A': 90, 'B': 80, 'C': 70, 'D': 60, 'E': 50, 'F': 0}

    def calculate_grade(self, average):
        if average >= self.grade_thresholds['A']:
            return 'A'
        elif average >= self.grade_thresholds['B']:
            return 'B'
        elif average >= self.grade_thresholds['C']:
            return 'C'
        elif average >= self.grade_thresholds['D']:
            return 'D'
        elif average >= self.grade_thresholds['E']:
            return 'E'
        else:
            return 'F'

    def add_record(self, ref_number, name, subjects, professors, marks):
        if not ref_number or not name or not all(subjects) or not all(professors) or not all(str(mark) for mark in marks):
            st.error("All fields are required.")
            return

        average = np.mean(marks)
        grade = self.calculate_grade(average)
        conn = init_db()
        c = conn.cursor()
        c.execute("INSERT INTO records (user_id, ref_number, name, subjects, professors, marks, average, grade) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (self.user_id, ref_number, name, ','.join(subjects), ','.join(professors), ','.join(map(str, marks)), average, grade))
        conn.commit()
        st.success("Record added successfully!")

    def get_records(self):
        conn = init_db()
        c = conn.cursor()
        c.execute("SELECT * FROM records WHERE user_id = ?", (self.user_id,))
        records = c.fetchall()
        return records

    def display_records(self):
        records = self.get_records()
        if not records:
            st.warning("No records found.")
        else:
            st.write("### Student Records")
            for record in records:
                st.markdown(f"""
                <div class="custom-card">
                    <p><b>Reference Number:</b> {record[2]}</p>
                    <p><b>Name:</b> {record[3]}</p>
                    <p><b>Subjects:</b> {record[4]}</p>
                    <p><b>Professors:</b> {record[5]}</p>
                    <p><b>Marks:</b> {record[6]}</p>
                    <p><b>Average:</b> {record[7]:.2f}</p>
                    <p><b>Grade:</b> {record[8]}</p>
                </div>
                """, unsafe_allow_html=True)

    def calculate_averages(self):
        records = self.get_records()
        if not records:
            st.warning("No records found.")
        else:
            st.write("### Subject Averages")
            subjects = ['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5']
            marks = [list(map(int, record[6].split(','))) for record in records]
            averages = np.mean(marks, axis=0)
            for i, avg in enumerate(averages):
                st.write(f"{subjects[i]}: {avg:.2f}")

    def calculate_pass_percentage(self):
        records = self.get_records()
        if not records:
            st.warning("No records found.")
        else:
            pass_count = sum(1 for record in records if record[7] >= 50)
            pass_percentage = (pass_count / len(records)) * 100
            st.write(f"### Pass Percentage: {pass_percentage:.2f}%")

    def edit_grade_thresholds(self):
        st.write("### Edit Grade Thresholds")
        for grade, threshold in self.grade_thresholds.items():
            new_threshold = st.number_input(f"{grade} Threshold", value=threshold, min_value=0, max_value=100)
            self.grade_thresholds[grade] = new_threshold
        st.success("Grade thresholds updated successfully!")

    def export_to_excel(self):
        records = self.get_records()
        if not records:
            st.warning("No records to export.")
        else:
            df = pd.DataFrame(records, columns=["ID", "User ID", "Reference Number", "Name", "Subjects", "Professors", "Marks", "Average", "Grade"])
            df.to_excel("grades.xlsx", index=False)
            st.success("Records exported to Excel successfully!")

    def export_to_pdf(self):
        records = self.get_records()
        if not records:
            st.warning("No records to export.")
        else:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for record in records:
                pdf.cell(200, 10, txt=f"Reference Number: {record[2]}", ln=True)
                pdf.cell(200, 10, txt=f"Name: {record[3]}", ln=True)
                pdf.cell(200, 10, txt=f"Subjects: {record[4]}", ln=True)
                pdf.cell(200, 10, txt=f"Professors: {record[5]}", ln=True)
                pdf.cell(200, 10, txt=f"Marks: {record[6]}", ln=True)
                pdf.cell(200, 10, txt=f"Average: {record[7]:.2f}", ln=True)
                pdf.cell(200, 10, txt=f"Grade: {record[8]}", ln=True)
                pdf.cell(200, 10, txt="-" * 50, ln=True)
            pdf.output("grades.pdf")
            st.success("Records exported to PDF successfully!")

    def generate_analytics(self):
        records = self.get_records()
        if not records:
            st.warning("No records found.")
        else:
            marks = [list(map(int, record[6].split(','))) for record in records]
            df = pd.DataFrame(marks, columns=['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5'])
            st.write("### Marks Distribution")
            fig = px.histogram(df, barmode='group')
            st.plotly_chart(fig, width="stretch")

# Main App
def main():
    load_css()
    st.title("Grade Management System")
    st.markdown("---")

    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    if st.session_state.user_id is None:
        st.sidebar.title("Login/Signup")
        choice = st.sidebar.selectbox("Choose an option", ["Login", "Signup"])

        if choice == "Login":
            st.write("### Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_date = st.date_input("Enter the date you signed up with", min_value=datetime.date(2000, 1, 1))
            if st.button("Login"):
                login(username, password, login_date)

        elif choice == "Signup":
            st.write("### Signup")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            signup_date = st.date_input("Choose a date for password", min_value=datetime.date(2000, 1, 1))
            if st.button("Signup"):
                if password == confirm_password:
                    signup(username, password, signup_date)
                else:
                    st.error("Passwords do not match.")

    else:
        grade_manager = GradeManager(st.session_state.user_id)

        st.sidebar.title("Navigation")
        options = [
            "Add Record", "Display Records", "Calculate Averages",
            "Calculate Pass Percentage", "Edit Grade Thresholds",
            "Export to Excel", "Export to PDF", "Generate Analytics"
        ]
        choice = st.sidebar.selectbox("Choose an option", options)

        if choice == "Add Record":
            st.write("### Add New Record")
            ref_number = st.number_input("Reference Number", min_value=1, step=1)
            name = st.text_input("Name")
            subjects = [st.text_input(f"Subject {i+1}") for i in range(5)]
            professors = [st.text_input(f"Professor for Subject {i+1}") for i in range(5)]
            marks = [st.number_input(f"Marks for Subject {i+1}", min_value=0, max_value=100) for i in range(5)]
            if st.button("Add Record"):
                grade_manager.add_record(ref_number, name, subjects, professors, marks)

        elif choice == "Display Records":
            grade_manager.display_records()

        elif choice == "Calculate Averages":
            grade_manager.calculate_averages()

        elif choice == "Calculate Pass Percentage":
            grade_manager.calculate_pass_percentage()

        elif choice == "Edit Grade Thresholds":
            grade_manager.edit_grade_thresholds()

        elif choice == "Export to Excel":
            grade_manager.export_to_excel()

        elif choice == "Export to PDF":
            grade_manager.export_to_pdf()

        elif choice == "Generate Analytics":
            grade_manager.generate_analytics()

if __name__ == "__main__":
    main()