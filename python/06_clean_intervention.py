"""
06_cleaned_intervention.py

Purpose: Clean the intervention table.

Input: data/raw/fact_intervention.csv

Output: data/cleaned/fact_intervention_cleaned.csv

Why this matters: Intervention data helps evaluate what supports students received and whether they were completed.
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

os.makedirs("../data/cleand", exist_ok=True)

# %%
# ----------------------------------------------------------------
# Load Raw Intervention Data
# ----------------------------------------------------------------

intervention = pd.read_csv("../data/raw/fact_intervention.csv")

# %%
# ----------------------------------------------------------------
# Clean Text Columns
# ----------------------------------------------------------------

intervention["student_id"] = intervention["student_id"].astype(str).str.strip()
intervention["intervention_type"] = intervention["intervention_type"].astype(str).str.strip()
intervention["completed_flag"] = intervention["completed_flag"].astype(str).str.strip()

# %%
# ----------------------------------------------------------------
# Standardize Completed Flag
# ----------------------------------------------------------------

# Convert values like yes, YES, Y, no, and N into Yes/No.
intervention.loc[intervention["completed_flag"].isin(["yes", "y"]), "completed_flag"] = "Yes"
intervention.loc[intervention["completed_flag"].isin(["no", "n"]), "completed_flag"] = "No"
intervention.loc[intervention["completed_flag"] == "nan", "completed_flag"] = pd.NA

# %%
# ----------------------------------------------------------------
# Convert Date Columns
# ----------------------------------------------------------------

# Convert date text into datetime values so dates can be compared.
intervention["intervention_type"] = pd.to_datetime(
    intervention["intervention_start_date"],
    errors="coerce"
)
intervention["intervention_end_date"] = pd.to_datetime(
    intervention["intervention_end_date"],
    errors="coerce"
)

# %%
# ----------------------------------------------------------------
# Clean Intervention Hours
# ----------------------------------------------------------------

intervention["intervention_hours"] = pd.to_numeric(
    intervention["intervention_hours"],
    errors="coerce"
)

# %%
# ----------------------------------------------------------------
# Remove Invalid End Dates
# ----------------------------------------------------------------

# The end date should not be earlier than the start date.
invalid_end_date = intervention["intervention_end_date"] < intervention["intervention_start_date"]
intervention.loc[invalid_end_date, "intervention_end_date"] = pd.NaT

# %%
# ----------------------------------------------------------------
# Add Intervention Duration
# ----------------------------------------------------------------

# Calculate how many days each intervention lasted.

# Calculate how many days each intervention lasted.
intervention["intervention_duration_days"] = (
    intervention["intervention_end_date"]
    - intervention["intervention_start_date"]
).dt.days
# %%
# ----------------------------------------------------------------
# Saved Cleaned Intervention File
# ----------------------------------------------------------------

intervention.to_csv("../data/cleaned/fact_intervention_cleaned.csv". index=False)
print("fact_intervention cleaned and saved.")