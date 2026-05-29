"""
02_clean_students.py

Purpose: Clean the student dimension table

Input: data/raw/dim_student.csv

Output: data/cleaned/dim_student_cleaned.csv

Why this matters: The student table should have one row per student and consistent category values.
"""

# %%
# ----------------------------------------------------------------
# Import Libraries
# ----------------------------------------------------------------

# pandas is used to load, clean, and save table-like data.
import pandas as pd

# os is used here to create the cleaned data folder if needed.
import os

# %%
# ----------------------------------------------------------------
# Create Cleaned Data Folder
# ----------------------------------------------------------------

# Create the folder where cleaned CSV files will be saved.
os.makedirs("../data/cleaned", exist_ok=True)

# %%
# ----------------------------------------------------------------
# Load Raw Student Data
# ----------------------------------------------------------------

# Read the raw student CSV file into a pandas DataFrame.
students = pd.read_csv("../data/raw/dim_student.csv")

# %%
# ----------------------------------------------------------------
# Remove Extra Spaces from Text Columns
# ----------------------------------------------------------------

# Extra spaces can cause duplicate-looking categories.
# Example: "Central Academy" and "Central Academy " are different to Python.
students["student_id"] = students["student_id"].astype(str).str.strip()
students["school_name"] = students["school_name"].astype(str).str.strip()
students["gender"] = students["gender"].astype(str).str.strip()
students["race_ethnicity"] = students["race_ethnicity"].astype(str).str.strip()
students["english_learner_status"] = students["english_learner_status"].astype(str).str.strip()
students["special_education_status"] = students["special_education_status"].astype(str).str.strip()
students["economically_disadvantaged_flag"] = students["economically_disadvantaged_flag"].astype(str).str.strip()

# %%
# ----------------------------------------------------------------
# Standardize Yes/No Fields
# ----------------------------------------------------------------

# Convert to lowercase first so values are easier to compare.
students["english_learner_status"] = students["english_learner_status"].str.lower()
students["special_education_status"] = students["special_education_status"].str.lower()
students["economically_disadvantaged_flag"] = students["economically_disadvantaged_flag"].str.lower()

# Convert common yes/no variations into consistent labels.
students.loc[students["english_learner_status"].isin(["yes", "y"]), "english_learner_status"] = "Yes"
students.loc[students["english_learner_status"].isin(["no", "n"]), "english_learner_status"] = "No"
students.loc[students["special_education_status"].isin(["yes", "y"]), "special_education_status"] = "Yes"
students.loc[students["special_education_status"].isin(["no", "n"]), "special_education_status"] = "No"
students.loc[students["economically_disadvantaged_flag"].isin(["yes", "y"]), "economically_disadvantaged_flag"] = "Yes"
students.loc[students["economically_disadvantaged_flag"].isin(["no", "n"]), "economically_disadvantaged_flag"] = "No"

# %%
# ----------------------------------------------------------------
# Clean Blank-Like Values
# ----------------------------------------------------------------

# After converting columns to text, missing values may appear as the string "nan".
students = students.replace("nan", "")

# %%
# ----------------------------------------------------------------
# Remove Duplicate Student IDs
# ----------------------------------------------------------------

# student_id should be unique in this table.
students = students.drop_duplicates(subset=["student_id"])

# %%
# ----------------------------------------------------------------
# Save Cleaned Student File
# ----------------------------------------------------------------

# index=False prevents pandas from adding an extra row-number column.
students.to_csv("../data/cleaned/dim_student_cleaned.csv", index=False)

print("dim_student cleaned and saved.")