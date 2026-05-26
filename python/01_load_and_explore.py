"""
01_load_and_explore.py

Purpose: Load the raw education dataset CSV files and perform an initial exploration.

Why this matters:
    Before cleaning or analyzing data, analysts first inspect
    - Dataset size
    - Column names
    - Sample records
    - Missing values
    - Duplicate values

This helps identify potential data-quality issues early.
"""
# %%
# ----------------------------------------------------------------
# Import Libraries
# ----------------------------------------------------------------

# pandas is used for working with table-like data.
# It allows us to load and analyze CSV files.
import pandas as pd


# %%
# ----------------------------------------------------------------
# Load Raw Datasets
# ----------------------------------------------------------------

# Read each CSV file into a pandas DataFrame.
# Think of a DataFrame like an Excel spreadsheet inside Python.

students = pd.read_csv("../data/raw/dim_student.csv")
attendance = pd.read_csv("../data/raw/fact_attendance.csv")
assessment = pd.read_csv("../data/raw/fact_assessment.csv")
course = pd.read_csv("../data/raw/fact_course_performance.csv")
intervention = pd.read_csv("../data/raw/fact_intervention.csv")

# %%
# ----------------------------------------------------------------
# View Dataset Sizes
# ----------------------------------------------------------------

# .shape returns: (number of rows, number of columns)

# Example: (1500, 8)

# Meaning: 1500 rows, 8 columns

print("ROW AND COLUMN COUNTS")
print("---------------------")

print("students:", students.shape)
print("attendance:", attendance.shape)
print("assessment:", assessment.shape)
print("course:", course.shape)
print("intervention:", intervention.shape)

# %%
# ----------------------------------------------------------------
# View Column Names
# ----------------------------------------------------------------

# Understanding column names helps us understand what information exists in each dataset.

print("\nCOLUMN NAMES")
print("--------------")

# list () makes the output easier to read.
print("students:", list(students.columns))
print("attendance:", list(attendance.columns))
print("assessment:", list(assessment.columns))
print("course:", list(course.columns))
print("intervention:", list(intervention.columns))


# %%
# ----------------------------------------------------------------
# Preview Sample Data
# ----------------------------------------------------------------

# .head() displays the first 5 rows.

# This helps us quickly inspect:
# - formatting
# - missing values
# - strange entries
# - overall structure

print("\nSTUDENT PREVIEW")
print("-----------------")

print(student.head())

print("\nATTENDANCE PREVIEW")
print("--------------------")

print(attendance.head())

# %%
# ----------------------------------------------------------------
# Check for Missing Values
# ----------------------------------------------------------------

# .isna() identifies missing values
# .sum() counts them

# Missing values are important because they may require cleaning before analysis.

print("\nMISSING VALUES")
print("----------------")

print("\nstudents missing values:")
print(students.isna().sum())

print("\nattendance missing values")
print(attendance.isna().sum())

print("\nassessment missing values")
print(assessment.isna().sum())

print("\ncourse missing values")
print(course.isna().sum())

print("\nintervention missing values")
print(intervention.isna().sum())


# %%
# ----------------------------------------------------------------
# Check for Duplicate Student IDs
# ----------------------------------------------------------------

# student_id should be unique in dim_student

# duplicated() returns True or False for each row

# sum() counts how many duplicates exist

print("\nDUPLICATE CHECKS")
print("------------------")

duplicate_students = (
    students["student_id"]
    .duplicated()
    .sum()
)

print(
    "Duplicate student_id values in dim_student:",
    duplicate_students
)

# %%
# ----------------------------------------------------------------
# Completion Message
# ----------------------------------------------------------------

print("\nExploration complete.")