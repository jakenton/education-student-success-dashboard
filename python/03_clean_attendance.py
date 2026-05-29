"""
03_cleaned_attendance.py

Purpose: Clean the attendance table.

Input: data/raw/fact_attendance.csv

Output: data/cleaned/fact_attendance.csv

Why this matters: Attendance is one of the main indicators used to identify students who may need support.
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
# Load Raw Attendance Data
# ----------------------------------------------------------------

attendance = pd.read_csv("../data/raw/fact_attendance.csv")

# %%
# ----------------------------------------------------------------
# Clean Attendance Rate Format
# ----------------------------------------------------------------

# attendance_rate should be stored as a decimal.
# Example: 0.95 means 95%
# This section handles values like "94.5%", 94.5, and 0.945
attendance["attendance_rate"] = attendance["attendance_rate"].astype(str).str.strip()
attendance["attendance_rate"] = attendance["attendance_rate"].str.replace("%", "", regex=False)
attendance["attendance_rate"] = pd.to_numeric(attendance["attendance_rate"], errors="coerce")

# %%
# ----------------------------------------------------------------
# Convert Whole-Number Percentage to Decimals
# ----------------------------------------------------------------

# If a value is >1 and <=100, treat it as a percentage and divide by 100.
attendance.loc[
    (attendance["attendance_rate"] > 1) & (attendance["attendance_rate"] <= 100),
    "attendance_rate"
] = attendance["attendance_rate"] / 100

# %%
# ----------------------------------------------------------------
# Recalculate Missing Attendance Rates When Possible
# ----------------------------------------------------------------

# If attendance rate is missing, calculate it from days_present / days_enrolled.
missing_rate = attendance["attendance_rate"].isna()
attendance.loc[missing_rate, "attendance_rate"] = (
    attendance["days_present"] / attendance["days_enrolled"]
)
    # %%
# ----------------------------------------------------------------
# Remove Impossible Attendance Rates
# ----------------------------------------------------------------

# Attendance rates should be between 0 and 1.
invalid_rate = (
    (attendance["attendance_rate"] < 0)
    | (attendance["attendance_rate"] > 1)
)
attendance.loc[invalid_rate, "attendance_rate"] = pd.NA

# %%
# ----------------------------------------------------------------
# Add Chronic Absenteeism Flag
# ----------------------------------------------------------------

# A common education threshold is attendance below 90%.
attendance["chronic_absenteeism_flag"] = 0
attendance.loc[
    attendance["attendance_rate"] < 0.90,
    "chronic_absenteeism_flag"
] = 1

# %%
# ----------------------------------------------------------------
# Save Cleaned Attendance File
# ----------------------------------------------------------------

attendance.to_csv("../data/cleaned/fact_attendance_cleaned.csv", index=False)
print("fact_attendance cleaned and saved.")
# %%
