# Hospital Bed Capacity & Patient Flow Analytics

**Module:** COMP47780 – Cloud Computing (2025/26, Autumn)  
**Project Option:** Project 1 – Healthcare Data Warehouse Management  
**Student:** Hemanathan Sasikala Karthikeyan (ID: 25201772)

This repository/ZIP contains:

- The **project report**
- All **source code**
- All **data files**
- Dashboards (Power BI and Streamlit)

Everything needed to run the implementation locally is included.

---

## 1. Folder Structure (what is inside the ZIP)

When you unzip the project, you should see a structure like:

```text
Cloud Project/
├─ HospitalBeds/
│  ├─ raw_data/                       # Original synthetic hospital data
│  │  ├─ patients.csv
│  │  ├─ services_weekly.csv
│  │  ├─ staff.csv
│  │  └─ staff_schedule.csv
│  ├─ exports/                        # Dimension & fact tables + final dataset
│  │  └─ service_capacity_staff.csv   # Final analytics dataset (service x week)
│  ├─ notebooks/
│     └─ hospital_beds_eda.ipynb      # Jupyter EDA & feature engineering
│
├─ PowerBI Dashboard/
│  └─ HospitalCapacityDashboard.pbix   # Power BI report (2 pages)
│
├─ streamlit_app/
│  ├─ app.py                           # Streamlit web dashboard
│  ├─ requirements.txt                 # Python dependencies
│  └─ service_capacity_staff.csv       # Same analytics dataset for the app
│
├─ Screenshots/                        # Screenshots used in the report
├─ Report_COMP47780_Cloud_Project_...pdf (or .docx)  # Final project report
└─ README.md                           # This file
You only need Python (for the Streamlit app) and Power BI Desktop (for the PBIX file) to run and check the project locally.
No AWS setup is required to execute the submitted version.
2. How to Run the Streamlit Dashboard (Python app)

This is the easiest way to see the analytics running in a browser.

2.1. Prerequisites

Python 3.10+ installed

pip installed

An internet browser (Chrome, Edge, etc.)

2.2. Steps

Open a terminal

On Windows: open PowerShell or Command Prompt

On macOS/Linux: open Terminal

Navigate to the streamlit_app folder inside the unzipped project

Example (adjust the path to where you unzipped):
cd "PATH/TO/Cloud Project/streamlit_app"

Create and activate a virtual environment (recommended)

# Create virtual environment
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate

# On macOS / Linux:
source .venv/bin/activate

Install required Python packages
# Create virtual environment
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate

# On macOS / Linux:
source .venv/bin/activate

Install required Python packages

pip install -r requirements.txt
This installs Streamlit, Pandas, Altair, etc.

Run the Streamlit app

streamlit run app.py

Open the dashboard in your browser

After a few seconds, Streamlit will show something like:

You can now view your Streamlit app in your browser.

Open http://localhost:8501 in your browser.

2.3. What you should see

The app has two tabs:

Capacity vs Demand Overview

KPIs: total bed shortage, spare bed capacity, average bed utilisation, average staff morale, average refusal rate

Line + layered charts of patient requests, patients admitted and available beds by week

Sidebar filters:

Service selection (Emergency, ICU, General Medicine, Surgery)

Week range slider

Service & Staff Experience

Bar chart: average refusal rate by service

Bubble chart: staff morale vs patient satisfaction (bubble size = bed shortage)

Table: utilisation %, refusal %, satisfaction, morale, bed shortage, spare capacity

Text block with key insights (e.g., Emergency as the most pressured service)

All metrics are based on the service_capacity_staff.csv dataset produced by the data pipeline.

3. How to Open the Power BI Dashboard

The Power BI dashboard gives another view of the same analytics.

3.1. Prerequisite

Power BI Desktop installed

3.2. Steps

Open Power BI Desktop.

Go to:

Cloud Project/PowerBI Dashboard/HospitalCapacityDashboard.pbix


Open the .pbix file.

3.3. What you should see

The report contains two pages:

Capacity vs Demand Overview

Weekly view of patient requests, admissions and available beds

KPIs (total bed shortage, spare capacity, average utilisation, satisfaction, refusal)

Slicer to filter by service

Service & Staff Experience

Average refusal rate by service

Staff morale vs patient satisfaction (bubble size = bed shortage)

Summary table of utilisation, refusal, satisfaction, morale, bed shortage and spare capacity by service

4. Jupyter Notebook (Optional – For Code Review)

The notebook is not required to run the dashboards, but shows how the dataset was prepared.

File:
Cloud Project/HospitalBeds/notebooks/hospital_beds_eda.ipynb


Open it in Jupyter Notebook or JupyterLab to see:

Loading of the raw hospital data from raw_data/

Basic EDA (row counts, missing values, distributions)

Creation of derived metrics:

bed_shortage

spare_capacity

utilisation_rate

refusal_rate

Export of the final table service_capacity_staff.csv into exports/

This notebook, together with the exported CSVs, corresponds to the data warehouse and feature engineering part of the project.
