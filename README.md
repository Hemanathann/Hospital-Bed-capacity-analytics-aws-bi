# Hospital Bed Capacity & Patient Flow Analytics (AWS + Power BI + Streamlit)

**Module:** COMP47780 – Cloud Computing (2025/26, Autumn)  
**Project:** Healthcare Big Data – Project 1 (Cloud-based Healthcare Data Warehouse)  
**Student:** Hemanathan Sasikala Karthikeyan  
**Student ID:** 25201772

This repository contains the full end-to-end implementation of a cloud-based healthcare analytics system using AWS (S3, Glue, Athena), Power BI, Python, and Streamlit. The aim is to analyse hospital capacity, patient demand, and staff experience across four services — Emergency, ICU, General Medicine, and Surgery — over 52 weeks.

---

## Quick summary

- Streamlit app: `streamlit_app/app.py` — interactive web dashboard
- Power BI report: `PowerBI Dashboard/HospitalCapacityDashboard.pbix` — two-page report
- Notebook: `HospitalBeds/notebooks/hospital_beds_eda.ipynb` — EDA, cleaning, feature engineering
- Final dataset used by the app: `streamlit_app/service_capacity_staff.csv`

---

## Prerequisites (tested)

- Python 3.10 (tested). Python 3.9 or 3.11 may work but 3.10 is recommended.
- pip
- Power BI Desktop (Windows) to open `.pbix`
- Recommended OS: Windows 10/11, macOS, or Linux

---

## 1. Run the Streamlit app (local)

1. Open terminal (PowerShell on Windows)

2. Change to the streamlit_app folder
```bash
cd "PATH/TO/Hospital-Bed-capacity-analytics-aws-bi/streamlit_app"
```

3. Create and activate a virtual environment
```bash
python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# or (cmd)
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

4. Install dependencies
```bash
pip install -r requirements.txt
```
If installation fails, try upgrading pip: `python -m pip install --upgrade pip` and re-run the install.

5. Confirm the dataset is present:
`streamlit_app/service_capacity_staff.csv` should exist. If the file is missing, place the CSV in the streamlit_app folder or point the app to its path (see override below).

6. Run the app locally
```bash
streamlit run app.py
```
Streamlit will print a local URL such as: http://localhost:8501 — open this in your browser.

Run for external access (example for EC2):
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```
If on EC2: ensure the Security Group allows inbound TCP 8501.

Optional: specify an alternate CSV path (if you moved the CSV)
```bash
# On macOS/Linux
DATA_PATH="/path/to/service_capacity_staff.csv" streamlit run app.py --server.port 8501 --server.address 0.0.0.0
# On Windows PowerShell
$env:DATA_PATH="C:\path\to\service_capacity_staff.csv"; streamlit run app.py
```
(The app checks the DATA_PATH environment variable if provided — if your app doesn't, I can add a small change; let me know.)

---

## 2. Open the Power BI Dashboard

1. Install Power BI Desktop (Windows).
2. Open: `PowerBI Dashboard/HospitalCapacityDashboard.pbix`

What you will see:
- Page 1 – Capacity vs Demand Overview (KPIs, weekly trends, service slicer)
- Page 2 – Service & Staff Experience (refusal rates, morale vs satisfaction bubble chart)

Note: The PBIX includes the visuals only — if it expects a direct dataset connection, the file in the repo is the same exported dataset used in the report. 

---

## 3. Inspect / re-run data preparation (Jupyter notebook)

Notebook: `HospitalBeds/notebooks/hospital_beds_eda.ipynb`

- Launch Jupyter Notebook / Lab:
```bash
pip install notebook    # or jupyterlab
jupyter notebook
```
- Open the notebook and run the cells. This notebook shows:
  - EDA of raw synthetic data
  - Cleaning and standardisation
  - Derived metrics: `bed_shortage`, `spare_capacity`, `utilisation_rate`, `refusal_rate`
  - Export of final dataset (service_capacity_staff.csv)

---

## 4. AWS/cloud notes (development workflow)

This project was developed with the following flow (not required to run the local submission):
Jupyter EDA → S3 → Glue (Spark) → Athena → Power BI + Streamlit → EC2 Deployment
Architecture diagram (high-level)

![Overall cloud architecture - pipeline from Jupyter to EC2](Screenshots/Overall%20cloud%20architecture%20%E2%80%93%20pipeline%20from%20Jupyter%20to%20EC2.png)

If deploying to EC2:
- Open TCP 8501 in EC2 Security Group
- Consider running Streamlit behind nginx or using a reverse proxy if exposing to internet

---

## 5. Troubleshooting

- "Module not found" after pip install:
  - Ensure the virtual environment is activated
  - Run `pip show streamlit` and check versions
- Port 8501 in use:
  - Kill the occupying process or run on another port: `--server.port 8502`
- PowerShell activation fails:
  - Execution policy blocks scripts. Run PowerShell as admin and:
    `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Missing CSV:
  - Confirm `streamlit_app/service_capacity_staff.csv` exists. If not, run the notebook to produce it.
- Browser not opening:
  - Copy the local URL printed by Streamlit into a browser manually.

---

## 6. Reproducibility checklist

- [ ] Python 3.10 installed
- [ ] Create and activate venv inside streamlit_app
- [ ] `pip install -r requirements.txt` completes without errors
- [ ] `streamlit run app.py` opens at http://localhost:8501 and shows the dashboard
- [ ] Power BI Desktop opens the PBIX file and shows visuals

---
Streamlit app — Capacity vs Demand (live UI)


- Simple link:
  [Open the live Streamlit app (HTTP)](http://108.130.199.242:8501/)
