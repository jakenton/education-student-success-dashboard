"""
07_create_student_year_risk_summary.py

Purpose: Create a student-year risk summary table for SQL and Power BI.

Input: data/cleaned/fact_attendance_cleaned.csv
       data/cleaned/fact_assessment_cleaned.csv
       data/cleaned/fact_course_performance_cleaned.csv

Output: data/cleaned/student_year_risk_summary.csv

Why this matters: Power BI dashboards are easier to build when important metrics are already organized into a clean summary table.
"""

# %%
# ----------------------------------------------------------------
# Import Libraries
# ----------------------------------------------------------------

import pandas as pd
import os

# %%
# ----------------------------------------------------------------
# Create Cleaned Data Folder
# ----------------------------------------------------------------

os.makedirs("../data/cleaned", exist_ok=True)

# %%
# ----------------------------------------------------------------
# Load Cleaned Files
# ----------------------------------------------------------------

attendance = pd.read_csv("../data/cleaned/fact_attendance_cleaned.csv")
assessment = pd.read_csv("../data/cleaned/fact_assessment_cleaned.csv")
course = pd.read_csv("../data/cleaned/fact_course_performance_cleaned.csv")

# %%
# ----------------------------------------------------------------
# Create Basic or Below Assessment Flag
# ----------------------------------------------------------------

# This flag identifies assessment records where the student scored Basic or Below Basic.
assessment["basic_or_below_flag"] = 0
assessment.loc[
    assessment["proficiency_level"].isin(["Basic", "Below Basic"]),
    "basic_or_below_flag"
] = 1

# %%
# ----------------------------------------------------------------
# Summarize Assessments by Student and Year
# ----------------------------------------------------------------

# Create one assessment summary row per student school year.
assessment_summary = assessment.groupby(
    ["student_id", "school_year"],
    as_index=False
).agg(
    average_assessment_score=("assessment_score", "mean"),
    basic_or_below_count=("basic_or_below_flag", "sum")
)

# %%
# ----------------------------------------------------------------
# Summarize Course Performance by Student and Year
# ----------------------------------------------------------------

# Create one course summary row per student per school year.
course_summary = course.groupby(
    ["student_id", "school_year"],
    as_index=False
).agg(
    failed_course_count=("failed_course_flag", "sum"),
    average_final_grade=("final_grade", "mean")
)

# %%
# ----------------------------------------------------------------
# Start Risk Summary With Attendance Data
# ----------------------------------------------------------------

# Attendance already has one row per student per year.
risk_summary = attendance[[
    "student_id",
    "school_year",
    "attendance_rate",
    "chronic_absenteeism_flag"
]].copy()

# %%
# ----------------------------------------------------------------
# Add Assessment Summary
# ----------------------------------------------------------------

# This is similar to a SQL LEFT JOIN.
risk_summary = risk_summary.merge(
    assessment_summary,
    on=["student_id", "school_year"],
    how="left"
)

# %%
# ----------------------------------------------------------------
# Add Course Summary
# ----------------------------------------------------------------

risk_summary = risk_summary.merge(
    course_summary,
    on=["student_id", "school_year"],
    how="left"
)

# %%
# ----------------------------------------------------------------
# Create Overall At-Risk Flag
# ----------------------------------------------------------------

# Start by assuming each student is not at risk.
risk_summary["at_risk_flag"] = 0

# Flag students as at risk when attendance, assessment, or course failure criteria are met.
risk_summary.loc[
    (risk_summary["chronic_absenteeism_flag"] == 1)
    | (risk_summary["basic_or_below_count"] >= 1)
    | (risk_summary["failed_course_count"] >= 1),
    "at_risk_flag"
] = 1

# %%
# ----------------------------------------------------------------
# Create Risk Reason Flags
# ----------------------------------------------------------------

# These 1/0 fields make Power BI visuals easier to build.
risk_summary["risk_due_to_attendance"] = 0
risk_summary["risk_due_to_assessment"] = 0
risk_summary["risk_due_to_course_failure"] = 0

risk_summary.loc[risk_summary["chronic_absenteeism_flag"] == 1, "risk_due_to_attendance"] = 1
risk_summary.loc[risk_summary["basic_or_below_count"] >= 1, "risk_due_to_assessment"] = 1
risk_summary.loc[risk_summary["failed_course_count"] >= 1, "risk_due_to_course_failure"] = 1

# %%
# ----------------------------------------------------------------
# Save Student-Year Risk Summary
# ----------------------------------------------------------------

risk_summary.to_csv("../data/cleaned/student_year_risk_summary.csv", index=False)
print("student_year_risk_summary created and saved.")
# %%
