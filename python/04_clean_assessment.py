"""
04_cleaned_assessment.py

Purpose: Clean the assessment table.

Input: data/raw/fact_assessment.csv

Output: data/cleaned/fact_assessment.csv

Why this matters: Assessment data helps measure academic performance and identity students who may need support
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
# Load Raw Assessment Data
# ----------------------------------------------------------------

assessment = pd.read_csv("../data/raw/fact_assessment.csv")

# %%
# ----------------------------------------------------------------
# Clean Text Columns
# ----------------------------------------------------------------

# Remove extra spaces so categories are consistent.
assessment["student_id"] = assessment["student_id"].astype(str).str.strip()
assessment["subject"] = assessment["subject"].astype(str).str.strip()
assessment["proficiency_level"] = assessment["proficiency_level"].astype(str).str.strip()

# %%
# ----------------------------------------------------------------
# Standardize Proficiency Labels
# ----------------------------------------------------------------

# Convert labels like "PROFICIENT" and "proficient" into one standard value.
assessment["proficiency_level"] = assessment["proficiency_level"].str.lower()
assessment.loc[assessment["proficiency_level"] == "advanced", "proficiency_level"] = "Advanced"
assessment.loc[assessment["proficiency_level"] == "proficient", "proficiency_level"] = "Proficient"
assessment.loc[assessment["proficiency_level"] == "basic", "proficiency_level"] = "Basic"
assessment.loc[assessment["proficiency_level"] == "below basic", "proficiency_level"] = "Below Basic"

# %%
# ----------------------------------------------------------------
# Clean Assessment Scores
# ----------------------------------------------------------------

# assessment_score should be numeric and between 0 and 100.
assessment["assessment_score"] = pd.to_numeric(assessment["assessment_score"], errors="coerce")
invalid_score = (
    (assessment["assessment_score"] < 0)
    | (assessment["assessment_score"] > 100)
)
assessment.loc[invalid_score, "assessment_score"] = pd.NA

# %%
# ----------------------------------------------------------------
# Save Cleaned Assessment File
# ----------------------------------------------------------------

assessment.to_csv("../data/cleaned/fact_assessment_cleaned.csv", index=False)
print("fact_assessment cleaned and saved.")
# %%
