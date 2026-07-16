# &#128211; Eduaction Student Success Analytics Dashboard

## &#128506; Overview

The Education Student Success Analytics Dashboard is an end-to-end analyitcs portfolio project that demonstrates how educational data can be transformed into meaningful insights for teachers, administrators, and school leadership.

Using a realistic synthetic K-12 dataset, the project follows a complete analytics workflow from raw data through Python data cleaning, SQL Server storage, and Power BI dashboard development.

The goal is to identify students who may be at risk academically by combining attendance, assessment, course performance, and intervention data into a unified reporting solution.

---

## &#128269; Project Objectives

This project demonstrates how to:

- Clean and validate messy educational datasets using Python
- Document and track data-quality issues
- Load cleaned datasets into SQL Server
- Perform analytical queries using SQL
- Build interactive Power BI dashboards
- Apply reproducible analytics workflows using Git and GitHub

---

## &#128187; Technologies

- Python
    - pandas
- SQL Server
- SQL
- Power BI
- Git
- GitHub

---

## &#127970; Project Structure

```text
education-student-success-dashboard/
|
├── data/
|  ├── raw/
|  └── cleaned/
|  |
|  └── cleaned/
|      └── him_deficiencies_cleaned.csv
|
├── python/
|   ├── 01_load_and_explore.py
|   ├── 02_clean_validate_student_data.py
|   ├── 03_clean_attendance.py
|   ├── 04_clean_assessment.py
|   ├── 05_clean_course_performance.py
|   ├── 06_clean_intervention.py
|   ├── 07_create_student_year_risk_summary.py
|   └── 08_create_data_quality_log.py
|
├── sql/
|   ├── 01_create_database.sql
|   ├── 02_create_tables.sql
|   ├── 03_load_data.sql
|   ├── 04_validation_queries.sql
|   ├── 05_analytics_queries.sql
|   └── 06_powerbi_views.sql
|
├── powerbi/
|
├── documentation/
|
└── README.md
```

---

```text
Raw CSV Files
        ↓
Python Data Exploration
        ↓
Data Cleaning & Validation
        ↓
Student Risk Summary
        ↓
Data Quality Log
        ↓
SQL Server Database
        ↓
SQL Analytics Queries
        ↓
Power BI Dashboard
```

---

## Current Progress

### &#9989; Completed

- Designed the project architecture
- Generated realistic synthetic education datasets
- Explored raw datasets
- Built Python data-cleaning workflows
- Standardized inconsistent values
- Validated missing and duplicate records
- Created student-level risk indicators
- Generated a data-quality log

### &#9888; In Progress
- Create SQL Server script for database creation, data loading, validation, and analytics
- Load cleaned datasets into SQL Server
- Develop analytical SQL queries
- Build Power BI dashboard
- Finalize project documentation
