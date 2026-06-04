/*
06_powerbi_views.sql

Purpose: Create SQL views that can be used as clean Power BI data sources.

Why this matters: Power BI can connect directly to tables, but views are often cleaner.
A view lets one save commonly used joins and calculations in SQL Server.

This script creates the following:
    - vw_student_risk_detail
    - vw_school_risk_summary
    - vw_subject_assessment_summary
    - vw_intervention_summary

How to use: Run this after loading and validating the data.
*/

USE education_student_success_dashboard;
GO

CREATE OR ALTER VIEW dbo.vw_student_risk_detail AS
SELECT
    r.student_id,
    s.school_name,
    s.grade_level,
    s.gender,
    s.race_ethnicity,
    s.english_learner_status,
    s.special_education_status,
    s.economically_disadvantaged_flag,
    r.school_year,
    r.attendance_rate,
    r.chronic_absenteeism_flag,
    r.average_assessment_score,
    r.basic_or_below_count,
    r.failed_course_count,
    r.average_final_grade,
    r.at_risk_flag,
    r.risk_due_to_attendance,
    r.risk_due_to_assessment,
    r.risk_due_to_course_failure
FROM dbo.student_year_risk_summary r
INNER JOIN dbo.dim_student s
    ON r.student_id = s.student_id;
GO

CREATE OR ALTER VIEW dbo.vw_school_risk_summary AS
SELECT
    s.school_name,
    r.school_year,
    COUNT(*) AS student_year_records,
    SUM(r.at_risk_flag) AS at_risk_records,
    CAST(100.0 * SUM(r.at_risk_flag) / COUNT(*) AS DECIMAL(5, 2)) AS at_risk_rate_percent,
    CAST(AVG(r.attendance_rate) AS DECIMAL(5, 3)) AS average_attendance_rate,
    CAST(AVG(r.average_assessment_score) AS DECIMAL(5, 2)) AS average_assessment_score,
    CAST(AVG(r.average_final_grade) AS DECIMAL(5, 2)) AS average_final_grade
FROM dbo.student_year_risk_summary r
INNER JOIN dbo.dim_student s
    ON r.student_id = s.student_id
GROUP BY
    s.school_name,
    r.school_year;
GO

CREATE OR ALTER VIEW dbo.vw_subject_assessment_summary AS
SELECT
    school_year,
    subject,
    proficiency_level,
    COUNT(*) AS assessment_records,
    CAST(AVG(assessment_score) as DECIMAL(5, 2)) AS average_assessment_score
FROM dbo.fact_assessment
GROUP BY
    school_year,
    subject,
    proficiency_level;
GO

CREATE OR ALTER VIEW dbo.vw_intervention_summary AS
SELECT
    school_year,
    subject,
    proficiency_level;
GO

CREATE OR ALTER VIEW dbo.vw_intervention_summary AS
SELECT
    school_year,
    intervention_type,
    COUNT(*) AS intervention_records,
    COUNT(DISTINCT student_id) AS students_served,
    CAST(AVG(intervention_hours) AS DECIMAL(6, 2)) AS average_intervention_hours,
    CAST(AVG(intervention_duration_days) AS DECIMAL(6, 2)) AS average_duration_days,
    SUM(CASE WHEN completed_flag = 'Yes' THEN 1 ELSE 0 END) AS completed_interventions
FROM dbo.fact_intervention
GROUP BY
    school_year,
    intervention_type;
GO

SELECT
    TABLE_SCHEMA,
    TABLE_NAME
FROM INFORMATION_SCHEMA.VIEWS
ORDER BY TABLE_NAME;
GO