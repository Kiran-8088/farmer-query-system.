# KrishiSetu - Farmer Agricultural Facility Grievance & Query System

A full-stack web application designed for farmers to report difficulties, breakdowns, and delays related to agricultural facilities (such as irrigation canals, fertilizer supplies, seed centers, cold storages, and subsidy disbursements) directly to higher authorities for swift redressal.

## 🌾 Key Features & CRUD Operations

- **Create (C)**: Farmers can register new grievance tickets specifying their contact information, affected agricultural facility, category, urgency level, and detailed difficulty descriptions.
- **Read (R)**: Real-time dashboard with search & filter capabilities (by category, status, urgency, or keyword), detailed view of grievances, and live statistics cards.
- **Update (U)**:
  - **Farmer Mode**: Edit grievance details before official review.
  - **Higher Authority Mode**: Review escalated issues, transition statuses (*Submitted* → *Under Review* → *In Progress* → *Resolved* / *Rejected*), and attach official resolution directives and remarks.
- **Delete (D)**: Delete grievance tickets with safety confirmation modals.
- **Dual Role Switcher**: Interactive header toggle allowing you to switch between **Farmer View** and **Authority View** without needing login credentials for testing.

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask REST API
- **Database**: SQLite3 (zero-configuration, built-in)
- **Frontend**: Responsive HTML5, Modern CSS3 with glassmorphism & dark green agricultural theme, Vanilla JavaScript (Fetch API)
- **Icons & Typography**: Google Fonts (Outfit & Inter), FontAwesome 6

---

## 🚀 How to Run the Application

1. Open your terminal or command prompt.
2. Clone or navigate to the project directory:
   ```bash
   git clone https://github.com/<your-username>/farmer-query-system.git
   cd farmer-query-system

   Install dependencies:
bash

Install dependencies
python -m pip install -r requirements.txt
Start the server:
bash


python app.py
Open your web browser and visit:
http://127.0.0.1:5000