Grade Management System - Streamlit, Python, SQLite, Plotly
=========================================================

License
-------
The Grade Management System is a web-based application built using Streamlit and Python. It allows teachers to manage student grades efficiently, calculate averages, generate reports, and export data in various formats. The app features a modern user interface, secure user authentication, and interactive analytics.

Features
--------
- **User Authentication**:
    - Secure signup and login system.
    - Password hashing for security.
    - Date-based password authentication for added security.

- **Grade Management**:
    - Add, modify, and delete student records.
    - Calculate subject-wise averages and overall pass percentage.
    - Customizable grade thresholds (A, B, C, etc.).

- **Advanced Analytics**:
    - Interactive histograms to visualize marks distribution.
    - Subject-wise performance trends.

- **Export Options**:
    - Export records to Excel (.xlsx) and PDF (.pdf).

- **Responsive Design**:
    - Works seamlessly on all screen sizes (desktop, tablet, mobile).
    - Custom hamburger menu for sidebar navigation.

- **Database Integration**:
    - Uses SQLite for storing user and grade records.

Screenshots
-----------
- **Login Page**: Visual of the login page.
- **Dashboard**: Visual of the main dashboard.
- **Analytics**: Visual of the analytics page with interactive charts.

Installation
------------
**Prerequisites**:
- Python 3.7 or higher.
- Streamlit and other dependencies.

**Steps to Run the App**:
1. Clone the repository:
```bash
git clone https://github.com/shemaiscard/grade-management-system.git
cd grade-management-system
```

2. Install the required dependencies:
```bash
pip install streamlit pandas numpy sqlite3 plotly fpdf openpyxl
```

3. Run the app:
```bash
streamlit run app.py
```

4. Open the provided URL in your browser to interact with the app.

Usage
-----
**Signup**:
- Choose the Signup option from the sidebar.
- Enter a username, password, and a date for password authentication.
- Click Signup to create an account.

**Login**:
- Choose the Login option from the sidebar.
- Enter your username, password, and the date you used during signup.
- Click Login to access the dashboard.

**Add Record**:
- Navigate to Add Record from the sidebar.
- Enter the student's details (reference number, name, subjects, professors, and marks).
- Click Add Record to save the data.

**View Records**:
- Navigate to Display Records from the sidebar.
- View all student records in a card format.

**Export Data**:
- Navigate to Export to Excel or Export to PDF from the sidebar.
- Click the respective button to export records.

**Analytics**:
- Navigate to Generate Analytics from the sidebar.
- View interactive charts for marks distribution and subject-wise trends.

File Structure
--------------
```
grade-management-system/
├── app.py                  # Main application code
├── grades.db               # SQLite database file
├── grades.xlsx             # Exported Excel file
├── grades.pdf              # Exported PDF file
├── README.md               # Project documentation
└── requirements.txt        # List of dependencies
```

Technologies Used
-----------------
- **Streamlit**: For building the web app.
- **SQLite**: For database management.
- **Pandas**: For data manipulation and Excel export.
- **Plotly**: For interactive charts and analytics.
- **FPDF**: For generating PDF files.
- **OpenPyXL**: For Excel file handling.

Contributing
------------
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with clear messages.
4. Submit a pull request.

License
-------
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
-------
For questions or feedback, feel free to reach out:
- GitHub: shemaicard

Enjoy using the Grade Management System! 🚀
