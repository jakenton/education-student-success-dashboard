/*
05_analytics_queries.sql

Purpose: Run analytical SQL queries for the Education Student Success Dashboard project.

Why this matters: These queries turn cleaned tables into useful insights.
They help answer questions such as
    - How many students are at risk?
    - Which schools have the highest at-risk rates?
    - Which risk reasons are most common?
    - How do assessment scores vary by subject?
    - What intervention types are used most often?

These queries are also useful preparation for Power BI visuals.
*/

USE education_student_success_dashboard;
GO

-- District-level overview.
SELECT
    COUNT(DISTINCT student_id) AS total_students,
    COUNT(*) AS total_student_year_records,
    SUM(at_risk_flag) AS at_risk_student_year_records,
    CAST(100.0 * SUM(at_risk_flag) / COUNT(*) AS DECIMAL(5, 3)) AS at_risk_rate_percent,
    CAST (AVG(attendance_rate) AS DECIMAL(5, 3)) AS average_attendance_rate,
    CAST (AVG(average_assessment_score) AS DECIMAL(5, 2)) AS average_assessment_score,
    CAST(AVG(average_final_grade) AS DECIMAL(5, 2)) AS average_final_grade
FROM dbo.student_year_risk_summary;
GO

-- At-risk rate by school.
SELECT
    s.school_name,
    COUNT(*) AS student_year_records,
    SUM(r.at_risk_flag) AS at_risk_records,
    CAST(100.0 * SUM(r.at_risk_flag) / COUNT(*) AS DECIMAL(5, 2)) AS at_risk_rate_percent
FROM dbo.student_year_risk_summary r
INNER JOIN dbo.dim_student s
    ON r.student_id = s.student_id
GROUP BY s.school_name
ORDER BY at_risk_rate_percent DESC;
GO

-- At-risk rate by grade level.
SELECT
    s.grade_level,
    COUNT(*) AS student_year_records,
    SUM(r.at_risk_flag) AS at_risk_records,
    CAST(100.0 * SUM(r.at_risk_flag) / COUNT(*) AS DECIMAL(5, 2)) AS at_risk_rate_percent
FROM dbo.student_year_risk_summary r
INNER JOIN dbo.dim_student s
    ON r.student_id = s.student_id
GROUP BY s.grade_level
ORDER BY s.grade_level;
GO

-- Risk reason counts.
SELECT
    SUM(risk_due_to_attendance) AS risk_due_to_attendance_count,
    SUM(risk_due_to_assessment) AS risk_due_to_assessment_count,
    SUM(risk_due_to_course_failure) AS risk_due_to_course_failure_count
FROM dbo.student_year_risk_summary;
GO

-- Assessment performance by subject.
SELECT
    subject,
    COUNT(*) AS assessment_records,
    CAST(AVG(assessment_score) AS DECIMAL(5, 2)) AS average_assessment_score
FROM dbo.fact_assessment
GROUP BY subject
ORDER BY average_assessment_score DESC;
GO

-- Proficiency distribution by subject.
SELECT
    subject,
    proficiency_level,
    COUNT(*) AS record_count
FROM dbo.fact_assessment
GROUP BY subject, proficiency_level
ORDER BY subject, proficiency_level;
GO

-- Chronic absenteesism by school.
SELECT
    s.school_name,
    COUNT(*) AS attendance_records,
    SUM(a.chronic_absenteeism_flag) AS chronic_absenteesism_records,
    CAST(100.0 * SUM(a.chronic_absenteeism_flag) / COUNT(*) AS DECIMAL(5, 2)) AS chronic_absenteesism_rate_percent
FROM dbo.fact_attendance a
INNER JOIN dbo.dim_student s
    ON a.student_id = s.student_id
GROUP BY s.school_name
ORDER BY chronic_absenteesism_rate_percent DESC;
GO

-- Intervention summary by intervention type.
SELECT
    intervention_type,
    COUNT(*) AS intervention_records,
    COUNT(DISTINCT student_id) AS students_served,
    CAST(AVG(intervention_hours) AS DECIMAL(6, 2)) AS average_intervention_hours,
    CAST(AVG(intervention_duration_days) AS DECIMAL(6, 2)) AS average_duration_days,
    SUM(CASE WHEN completed_flag = 'Yes' THEN 1 ELSE 0 END) AS completed_interventions
FROM dbo.fact_intervention
GROUP BY intervention_type
ORDER BY intervention_records DESC;
GO

-- Student-level detail for dashboard table visuals.
SELECT
    r.student_id,
    s.school_name,
    s.grade_level,
    r.school_year,
    r.attendance_rate,
    r.average_assessment_score,
    r.average_final_grade,
    r.at_risk_flag,
    r.risk_due_to_attendance,
    r.risk_due_to_assessment,
    r.risk_due_to_course_failure
FROM dbo.student_year_risk_summary r
INNER JOIN dbo.dim_student s
    ON r.student_id = s.student_id
ORDER BY
    r.at_risk_flag DESC,
    s.school_name,
    s.grade_level,
    r.student_id;
GO