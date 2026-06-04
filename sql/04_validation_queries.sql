/*
04_validation_queries.sql

Purpose: Validate the data after it has been loaded into SQL Server.

Why this matters: Ater loading data, one should confirm that
    - Tables contain rows
    - Student IDs connect correctly across tables
    - Key numeric fields are within expected ranges
    - Risk flags use expected 1/0 values
    - Duplicates were not introduced

This script helps verify that the SQL database is ready for analysis.
*/

USE education_student_success_dashboard;
GO

-- Check row counts in all project tables.
SELECT 'dim_student' AS table_name,
COUNT(*) AS row_count
FROM dbo.dim_student

UNION ALL SELECT 'fact_attendance',
COUNT(*)
FROM dbo.fact_attendance

UNION ALL SELECT 'fact_assessment',
COUNT(*)
FROM dbo.fact_assessment

UNION ALL SELECT 'fact_course_performance',
COUNT(*)
FROM dbo.fact_course_performance

UNION ALL SELECT 'fact_intervention',
COUNT(*)
FROM dbo.fact_intervention

UNION ALL SELECT 'student_year_risk_summary',
COUNT(*)
FROM dbo.student_year_risk_summary

UNION ALL SELECT 'data_quality_log',
COUNT(*)
FROM dbo.data_quality_log

GO

-- dim_student should have one row per student_id.
SELECT
    student_id,
    COUNT(*) AS row_count
FROM dbo.dim_student
GROUP BY student_id
HAVING COUNT(*) > 1;
GO

-- Fact records should match a student in dim_student
SELECT
    'fact_attendance' AS table_name,
    COUNT(*) AS unmatched_student_rows
FROM dbo.fact_attendance a
LEFT JOIN dbo.dim_student s
    ON a.student_id = s.student_id
WHERE s.student_id IS NULL
UNION ALL
SELECT
    'fact_assessment',
    COUNT(*)
FROM dbo.fact_assessment a
LEFT JOIN dbo.dim_student s
    ON a.student_id = s.student_id
WHERE s.student_id IS NULL
UNION ALL
SELECT
    'fact_course_performance',
    COUNT(*)
FROM dbo.fact_course_performance c
LEFT JOIN dbo.dim_student s
    ON c.student_id = s.student_id
WHERE s.student_id IS NULL
UNION ALL
SELECT
    'fact_intervention',
    COUNT(*)
FROM dbo.fact_intervention i
LEFT JOIN dbo.dim_student s
    ON i.student_id = s.student_id
WHERE s.student_id IS NULL
UNION ALL
SELECT
    'student_year_risk_summary',
    COUNT(*)
FROM dbo.student_year_risk_summary r
LEFT JOIN dbo.dim_student s
    ON r.student_id = s.student_id
WHERE s.student_id IS NULL;
GO

-- Attendance rates should be between 0 and 1.
SELECT *
FROM dbo.fact_attendance
WHERE attendance_rate < 0
   OR attendance_rate > 1;
GO

-- Assessment scores should be between 0 and 100.
SELECT *
FROM dbo.fact_assessment
WHERE assessment_score < 0
   OR assessment_score > 100;
GO

-- Final grades should be between 0 and 100.
SELECT *
FROM dbo.fact_course_performance
WHERE final_grade < 0
   OR final_grade > 100;
GO

-- Risk flags should contain only 0, 1, or NULL.
SELECT *
FROM dbo.student_year_risk_summary
WHERE at_risk_flag NOT IN (0, 1)
   OR risk_due_to_attendance NOT IN (0, 1)
   OR risk_due_to_assessment NOT IN (0, 1)
   OR risk_due_to_course_failure NOT IN (0, 1)
GO

-- Review data-quality issues documented by Python.
SELECT *
FROM dbo.data_quality_log
ORDER BY table_name, issue_type;
GO