/*
02_create_tables.sql

Purpose: Create SQL Server tables for the cleaned education analytics CSV files.

Why this matters: Python cleaned and validated the data.
SQL Server will now store the cleaned data in structured tables so the user can
    - Query it with SQL
    - Validate relationships between tables
    - Create analysis outputs
    - Connect Power BI to the database

This script creates tables for the following:
    - Student demographics
    - Attendance
    - Assessments
    - Course performance
    - Interventions
    - Student-year risk summary
    - Data-quality log

How to use: Run this script after 01_create_database.sql.
*/

USE education_student_success_dashboard;
GO

-- Drop existing tables so this script can be rerun while developing the project.
DROP TABLE IF EXISTS dbo.data_quality_log;
DROP TABLE IF EXISTS dbo.student_year_risk_summary;
DROP TABLE IF EXISTS dbo.fact_intervention;
DROP TABLE IF EXISTS dbo.fact_course_performance;
DROP TABLE IF EXISTS dbo.fact_assessment;
DROP TABLE IF EXISTS dbo.fact_attendance;
DROP TABLE IF EXISTS dbo.dim_student
GO

-- dim student contains one row per student
CREATE TABLE dbo.dim_student (
    student_id VARCHAR(20) NOT NULL,
    school_name VARCHAR(100) NULL,
    grade_level INT NULL,
    gender VARCHAR(50) NULL,
    race_ethnicity VARCHAR(100) NULL,
    english_learner_status VARCHAR(10) NULL,
    special_education_status VARCHAR(10) NULL,
    economically_disadvantaged_flag VARCHAR(10) NULL,
    CONSTRAINT PK_dim_student PRIMARY KEY (student_id)
);
GO

-- fact_attendance contains attendance metrics by student and school year.
CREATE TABLE dbo.fact_attendance (
    student_id VARCHAR(20) NOT NULL,
    school_year INT NOT NULL,
    days_enrolled INT NULL,
    days_present INT NULL,
    attendance_rate DECIMAL(5, 3) NULL,
    chronic_absenteeism_flag INT NULL
);
GO

-- fact_assessment contains assessment results by student, school year, and subject.
CREATE TABLE dbo.fact_assessment (
    student_id VARCHAR(20) NOT NULL,
    school_year INT NOT NULL,
    subject VARCHAR(50) NULL,
    assessment_score DECIMAL (5, 2) NULL,
    proficiency_level VARCHAR(50) NULL
);
GO

-- fact_course_performance contains final grades and pass/fail flags.
CREATE TABLE dbo.fact_course_performance (
    student_id VARCHAR(20) NOT NULL,
    school_year INT NOT NULL,
    subject VARCHAR(50) NULL,
    final_grade DECIMAL(5, 2) NULL,
    failed_course_flag INT NULL,
    passed_course_flag INT NULL
);
GO

-- fact_intervention contains student intervention records.
CREATE TABLE dbo.fact_intervention (
    student_id VARCHAR(20) NOT NULL,
    school_year INT NOT NULL,
    intervention_type VARCHAR(100) NULL,
    intervention_start_date DATE NULL,
    intervention_end_date DATE NULL,
    intervention_hours DECIMAL(6, 2) NULL,
    completed_flag VARCHAR(10) NULL,
    intervention_duration_days INT NULL
);
GO

-- student_year_risk_summary combines key risk indicators into one row per student-year.
CREATE TABLE dbo.student_year_risk_summary (
    student_id VARCHAR(20) NOT NULL,
    school_year INT NOT NULL,
    attendance_rate DECIMAL(5, 3) NULL,
    chronic_absenteeism_flag INT NULL,
    average_assessment_score DECIMAL(5, 2) NULL,
    basic_or_below_count INT NULL,
    failed_course_count INT NULL,
    average_final_grade DECIMAL(5, 2) NULL,
    at_risk_flag INT NULL,
    risk_due_to_attendance INT NULL,
    risk_due_to_assessment INT NULL,
    risk_due_to_course_failure INT NULL
);
GO

-- data_quality_log stores the data-quality issues documentated during Python cleaning.
CREATE TABLE dbo.data_quality_log (
    table_name VARCHAR(100) NULL,
    issues_type VARCHAR(200) NULL,
    affected_rows INT NULL,
    action_taken VARCHAR(500) NULL
);
GO

-- Confirm that tables were created.
SELECT
    TABLE_SCHEMA,
    TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
GO