# Grade Management System

A web-based student grade management system built with **Streamlit**, Python, SQLite, and Plotly. Designed for teachers to manage records, track analytics, and export reports.

## Features

- **User Authentication**: Secure signup/login with password hashing and date-based 2FA
- **Grade Management**: Add, modify, delete student records; calculate averages and pass percentages
- **Advanced Analytics**: Interactive histograms and subject-wise performance trends (Plotly)
- **Export Options**: Excel (.xlsx) and PDF (.pdf) export
- **Responsive Design**: Works on desktop, tablet, and mobile

## Screenshots

**Login Page**
![Login](https://github.com/user-attachments/assets/c3ae809d-7d11-4572-a7b3-4f667b387554)

**Analytics Dashboard**
![Analytics](https://github.com/user-attachments/assets/0fda30eb-63f6-4c68-bdf8-c2e8f5f14947)

**App Overview**
![App](https://github.com/user-attachments/assets/e9737b4d-be4a-47e0-a421-17f904671704)

## Setup

```bash
git clone https://github.com/shemaiscard/grading-system-GUI.git
cd grading-system-GUI
pip install streamlit pandas numpy plotly fpdf openpyxl
streamlit run app.py
```

## Project Structure

```
grading-system-GUI/
├── app.py            Main application
├── grades.db         SQLite database (auto-created)
├── requirements.txt
└── README.md
```

## Tech Stack
Streamlit · SQLite · Pandas · Plotly · FPDF · OpenPyXL

## License
MIT License
