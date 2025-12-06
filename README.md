# Hospital Bed Capacity & Patient Flow Analytics (AWS + Power BI + Streamlit)

**Module:** COMP47780 – Cloud Computing (2025/26, Autumn)  
**Project:** Healthcare Big Data – Project 1 (Cloud-based Healthcare Data Warehouse)  
**Student:** Hemanathan Sasikala Karthikeyan  
**Student ID:** 25201772

This repository contains the full end-to-end implementation of a cloud-based healthcare analytics system, built using AWS (S3, Glue, Athena), Power BI, Python, and Streamlit, along with the final project deliverables (Power BI report, Streamlit app, datasets, notebooks, and project report).

The aim of the project is to analyse hospital capacity, patient demand, and staff experience across four services — Emergency, ICU, General Medicine, and Surgery — over 52 weeks.

## 📁 1. Repository Structure

```text
Hospital-Bed-capacity-analytics-aws-bi/
│
├─ HospitalBeds/
│  ├─ raw_data/                         # Original synthetic data
│  ├─ exports/                          # Processed fact/dim tables + final dataset
│  ├─ notebooks/                        # Jupyter EDA & feature engineering
│
├─ PowerBI Dashboard/
│  └─ HospitalCapacityDashboard.pbix    # 2-page Power BI analytics report
│
├─ streamlit_app/
│  ├─ app.py                            # Streamlit dashboard
│  ├─ requirements.txt                  # Python dependencies
│  └─ service_capacity_staff.csv        # Final analytics dataset
│
├─ Screenshots/                         # Screens used in project report
│
├─ Report_COMP47780_Cloud_Project.pdf   # Final report submitted
│
└─ README.md                            # You are here
```

## 🚀 2. How to Run the Streamlit Dashboard (Python)

This is the easiest way to explore the analytics.

### Prerequisites

- Python 3.10+
- pip installed
- Any web browser

### Step-by-Step Instructions

**STEP 1 — Open Terminal**

- Windows: PowerShell  
- Mac/Linux: Terminal

**STEP 2 — Navigate to the project folder**

```bash
cd "PATH/TO/streamlit_app"
```

**STEP 3 — Create virtual environment**

```bash
python -m venv .venv
```

Activate it:

_Windows:_

```powershell
.venv\Scripts\activate
```

_Mac/Linux:_

```bash
source .venv/bin/activate
```

**STEP 4 — Install dependencies**

```bash
pip install -r requirements.txt
```

**STEP 5 — Run the Streamlit app**

```bash
streamlit run app.py
```

Streamlit will show:

> Local URL: http://localhost:8501

Open that link in your browser.

To run the app for external access (e.g., on an EC2 instance):

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Public URL used during development (example): `http://108.130.199.242:8501/`

## 📈 3. How to Open the Power BI Dashboard

### Prerequisite

- Power BI Desktop (free)

### Steps

1. Open Power BI Desktop.  
2. Load: `PowerBI Dashboard/HospitalCapacityDashboard.pbix`

### What You Will See

- **Page 1 – Capacity vs Demand Overview**
  - KPIs
  - Weekly trends of patients vs beds
  - Interactive slicer (Emergency, ICU, etc.)
- **Page 2 – Service & Staff Experience**
  - Refusal rate by service
  - Staff morale vs patient satisfaction bubble chart
  - Summary table of service performance

## 🧪 4. Jupyter Notebook (Data Preparation)

If you want to inspect the data pipeline:  
`HospitalBeds/notebooks/hospital_beds_eda.ipynb`

Open it using Jupyter Notebook.

This notebook includes:

- EDA of raw hospital data
- Cleaning and standardizing fields
- Creating derived metrics: `bed_shortage`, `spare_capacity`, `utilisation_rate`, `refusal_rate`
- Export of final dataset (`service_capacity_staff.csv`)

This parallels what would run in AWS Glue/Spark during production.

## ☁️ 5. AWS Cloud Workflow (Used During Development)

Although not required to execute the submitted version, the full cloud workflow used was:

Jupyter EDA → S3 → Glue (Spark) → Athena → Power BI + Streamlit → EC2 Deployment

High-level steps:

1. Upload raw data to AWS S3  
2. Transform using AWS Glue  
3. Query using AWS Athena  
4. Export processed data to Power BI + Streamlit  
5. Deploy Streamlit app on EC2

## 🧩 6. Features of This Software

- Interactive bed-capacity analytics  
- Service-level filtering (Emergency, ICU, GM, Surgery)  
- Weekly demand vs beds visualization  
- KPIs summarizing shortages, refusal rates & utilisation  
- Experience analytics: satisfaction vs morale  
- Bubble charts sized by bed shortages  
- Two full dashboards: Power BI + Streamlit  
- Cloud-ready architecture using AWS

## 📘 7. File Directory (Included in the ZIP/Repo)

- ✔ Project Report (PDF)  
- ✔ Source Code  
- ✔ All datasets  
- ✔ Dashboards  
- ✔ README (this file)  
- ✔ Screenshots

No external dependencies or AWS access is required to run the submitted version.

## 🧾 8. How to Reproduce the Full Project (Summary)

1. Run EDA notebook (optional)  
2. Open Power BI dashboard  
3. Run Streamlit web app

These three components demonstrate:

- Data warehouse design  
- Data transformation pipeline  
- Analytics and dashboarding  
- Cloud deployment experience

---

### 🏁 Final Notes

If you run into any installation issues, delete the virtual environment and reinstall:

```bash
rm -r .venv
python -m venv .venv
pip install -r requirements.txt
```
