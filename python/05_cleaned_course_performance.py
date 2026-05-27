"""
05_cleaned_course_performance.py

Purpose: Clean the course performance table.

Input: data/raw/fact_course_performance.csv

Output: data/cleaned/fact_course_performance_cleaned.csv

Why this matters: Course grades and failures are important academic outcome measures.
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
# Load Raw Course Performance Data
# ----------------------------------------------------------------

course = pd.read_csv("../data/raw/fact_course_performance.csv")

# %%
# ----------------------------------------------------------------
# Clean Text Columns
# ----------------------------------------------------------------

course["student_id"] = course["student_id"].astype(str).str.strip()
course["subject"] = course["subject"].astype(str).str.strip()

# %%
# ----------------------------------------------------------------
# Clean Final Grades
# ----------------------------------------------------------------

# final_grade should be numeric and between 0 and 100.
course["final_grade"] = pd.to_numeric(course["final_grade"], errors="coerce")
invalid_grade = (
    (course["final_grade"] < 0)
    | (course["final_grade"] > 100)
)
course.loc[invalid_grade, "final_grade"] = pd.NA

# %%
# ----------------------------------------------------------------
# Standardize Failed Course Flag
# ----------------------------------------------------------------

# Convert values like 1, 0, Y, N, yes, and no into consistent 1/0 flag.
course["final_course_grade"] = course["final_course_grade"].astype(str).str.strip().str.lower()
course.loc[course["final_course_grade"].isin(["1", "yes", "y"]), "failed_course_flag"] = 1
course.loc[course["final_course_grade"].isin(["0", "no", "n"]), "failed_course_flag"] = 0
course["failed_course flag"] = pd.to_numeric(course["final_course_flag"], errors="coerce")

# %%
# ----------------------------------------------------------------
# Recalculate Missing Failed Course Flags
# ----------------------------------------------------------------

# If failed_course_flag is missing, recreate it from final_grade when possible.
missing_flag = course["failed_course flag"].isna()
course.loc[missing_flag & (course["final_grade"] < 60), "failed_course_flag"] = 1
course.loc[missing_flag & (course["final_grade"] >= 60), "failed_course_flag"] = 0

# %%
# ----------------------------------------------------------------
# Add Passed Course Flag
# ----------------------------------------------------------------

# This creates the opposite of failed_course_flag for easier reporting.
course["passed_course_flag"] = 0
course.loc[course["failed_course flag"] == 0, "passed_course_flag"] = 1

# %%
# ----------------------------------------------------------------
# Remove Duplicate Course Records
# ----------------------------------------------------------------

# Each student should have one course record per student, school year, and subject.
course = course.drop_duplicates(subset=["student_id", "school_year", "subject"])

# %%
# ----------------------------------------------------------------
# Save Cleaned Course Performance File
# ----------------------------------------------------------------

course.to_csv("../data/cleaned/fact_course_performance_cleaned.csv", index=False)
print("fact_course_performance cleaned and saved.")