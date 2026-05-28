"""
09_create_data_quality_log.py

Purpose: Create a simple data-quality log from the raw and cleaned files.

Output: data/cleaned/data_quality_log.csv

Why this matters: It's crucial to document data-quality issues and cleaning decisions.
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
# Load Raw Files
# ----------------------------------------------------------------

raw_students = pd.read_csv("../data/raw/dim_student.csv")
raw_attendance = pd.read_csv("../data/raw/fact_attendance.csv")
raw_assessment = pd.read_csv("../data/raw/fact_assessment.csv")
raw_course = pd.read_csv("../data/raw/fact_course.csv")
raw_invervention = pd.read_csv("../data/raw/fact_invervention.csv")

# %%
# ----------------------------------------------------------------
# Load Cleaned Files
# ----------------------------------------------------------------

clean_attendance = pd.read_csv("../data/raw/fact_attendance_cleaned.csv")
clean_assessment = pd.read_csv("../data/raw/fact_assessment_cleaned.csv")
clean_course = pd.read_csv("../data/raw/fact_course_cleaned.csv")
clean_invervention = pd.read_csv("../data/raw/fact_invervention_cleaned.csv")

# %%
# ----------------------------------------------------------------
# Create Empty Lists For The Log
# ----------------------------------------------------------------

# Each list will become one column in the final data-quality log.
table_names = []
issues_types = []
affected_rows = []
actions_taken = []

# %%
# ----------------------------------------------------------------
# Log Student Table Issues
# ----------------------------------------------------------------

student_duplicates = raw_students["student_id"].duplicated().sum()
table_names.append("dim_student")
issues_types.append("Duplicate student_id values")
affected_rows.append(student_duplicates)
actions_taken.append("Removed duplicate student records, if any")

# %%
# ----------------------------------------------------------------
# Log Attendance Table Issues
# ----------------------------------------------------------------

# Count values that were stored with percent signs.
raw_attendance_rate_text = raw_attendance["attendance_rate"].astype(str)
percent_formatted_count = raw_attendance_rate_text.str.contains("%", regex=False).sum()
table_names.append("fact_attendance")
issues_types.append("Attendance rates stored as percentages")
affected_rows.append(percent_formatted_count)
actions_taken.append("Converted percentage-formatted values to decimals")

# Count missing attendance rates after cleaning.
missing_clean_attendance = clean_attendance["attendance_rate"].isna().sum()
table_names.append("fact_attendance")
issues_types.append("Missing or invalid attendance rates after cleaning")
affected_rows.append(missing_clean_attendance)
actions_taken.append("Left as missing when a valid value could not be confirmed")

# %%
# ----------------------------------------------------------------
# Log Assessment Table Issues
# ----------------------------------------------------------------

missing_clean_scores = clean_assessment["assessment_score"].isna().sum()
table_names.append("fact_assessment")
issues_types.append("Missing or invalid assessment scores after cleaning")
affected_rows.append(missing_clean_scores)
actions_taken.append("Set impossible scores outside 0 to 100 to missing")

# %%
# ----------------------------------------------------------------
# Log Course Tables Issues
# ----------------------------------------------------------------

# The difference between raw and cleaned rows shows how many duplicates were removed.
removed_course_duplicates = len(raw_course) - len(clean_course)
table_names.append("fact_course_performance")
issues_types.append("Duplicate course records removed")
affected_rows.append(removed_course_duplicates)
actions_taken.append("Kept one record per student, school, year, and subject")

# %%
# ----------------------------------------------------------------
# Log Intervention Tables Issues
# ----------------------------------------------------------------

missing_completed_flags = clean_invervention("completed_flag").isna().sum()
table_names.append("fact_intervention")
issues_types.append("Missing completed_flag values after cleaning")
affected_rows.append(missing_completed_flags)
actions_taken.append("Left as missing when completion status could not be confirmed")

missing_end_dates = clean_invervention["intervention_end_date"].isna().sum()
table_names.append("fact_intervention")
issues_types.append("Missing or invalid intervention_end_date values after cleaning")
affected_rows.append(missing_end_dates)
actions_taken.append("Set invalid end dates to missing")

# %%
# ----------------------------------------------------------------
# Create Data-Quality Log Dataframe
# ----------------------------------------------------------------

data_quality_log = pd.DataFrame({
    "table_name": table_names,
    "issue_type": issues_types,
    "affected_rows": affected_rows,
    "action_taken": actions_taken
})

# %%
# ----------------------------------------------------------------
# Save Data-Quality Log
# ----------------------------------------------------------------

data_quality_log.to_csv("../data/cleaned/data_quality_log.csv", index=False)
print("data_quality_log created and saved.")