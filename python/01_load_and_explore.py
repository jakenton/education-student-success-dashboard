"""
01_load_and_explore.py

Purpose: Load the raw CSV files and print basic information about each dataset.

Why this matters:
    Before cleaning data, an analyst should first understand what files exist,
    what columns they contain, how many rows they have, and wether obvious
    missing values are present.
"""

import pandas as pd

students = pd.read_csv("../data/raw/dim_student.csv")
attendance = pd.read_csv("../data/raw/fact_attendance.csv")
assessment = pd.read_csv("../data/raw/fact_assessment.csv")
course = pd.read_csv("../data/raw/fact_course_performance.csv")
intervention = pd.read_csv("../data/raw/fact_intervention.csv")

print("ROW AND COLUMN COUNTS")
print("---------------------")
print("students:", students.shape)
print("attendance:", attendance.shape)
print("assessment:", assessment.shape)
print("course:", course.shape)
print("intervention:", intervention.shape)

print("\nCOLUMN NAMES")
print("--------------")
print("students:", list(students.columns))
print("attendance:", list(attendance.columns))
print("assessment:", list(assessment.columns))
print("course:", list(course.columns))
print("intervention:", list(intervention.columns))

print("\nSTUDENT PREVIEW")
print("-----------------")
print(student.head())

print("\nATTENDANCE PREVIEW")
print("--------------------")
print(attendance.head())

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

print("\nDUPLICATE CHECKS")
print("------------------")
duplicate_students = students["student_id"].duplicated().sum()
print("Duplicate student_id values in dim_student:", duplicate_students)

print("\nExploration complete.")