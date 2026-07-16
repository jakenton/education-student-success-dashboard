/*
03_load_data.sql

Purpose: Load cleaned CSV files from the data/cleaned folder into SQL Server tables.

Why this matters: The Python scripts created cleaned CSV files.
This script moves those cleaned datasets into SQL Server so they can be queried, validated, and eventually used as the data source for Power BI.

Important: The file paths *must* by updated so they match the project location on the user's computer.

Example: C:\Data-Analytics-Projects\education-student-success-dashboard\data\cleaned\

How to use: Run this script after 01_create_database.sql.
*/

USE education_student_success_dashboard;
GO

-- Cleanr existing data so the script can be rerun.
TRUNCATE TABLE dbo.data_quality_log;
TRUNCATE TABLE dbo.student_year_risk_summary;
TRUNCATE TABLE dbo.fact_intervention;
TRUNCATE TABLE dbo.fact_course_performance;
TRUNCATE TABLE dbo.fact_assessment;
TRUNCATE TABLE dbo.fact_attendance;
TRUNCATE TABLE dbo.dim_student;
GO

-- Load student dimension data.
BULK INSERT dbo.dim_student
FROM 'C:\\Data-Analytics-Projects\education-student-success-dashboard\data\cleaned\dim_student_cleaned.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK,
    KEEPNULLS
);
GO

-- Load attendance data.
BULK INSERT dbo.fact_attendance
FROM 'C:\\Data-Analytics-Projects\education-student-success-dashboard\data\cleaned\fact_attendance_cleaned.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK,
    KEEPNULLS
);
GO

-- Load assessment data.
BULK INSERT dbo.fact_assessment
FROM 'C:\\Data-Analytics-Projects\education-student-success-dashboard\data\cleaned\fact_assessment_cleaned.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK,
    KEEPNULLS
);
GO

-- Load course performance data.
BULK INSERT dbo.fact_course_performance
FROM 'C:\\Data-Analytics-Projects\education-student-success-dashboard\data\cleaned\fact_course_performance_cleaned.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK,
    KEEPNULLS
);
GO

-- Load intervention data.
BULK INSERT dbo.fact_intervention
FROM 'C:\\Data-Analytics-Projects\education-student-success-dashboard\data\cleaned\fact_intervention_cleaned.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDQUOTE = '"',
    ROWTERMINATOR = '0x0a',
    CODEPAGE = '65001',
    TABLOCK,
    KEEPNULLS
);
GO

-- Load student-year risk summary.
BULK INSERT dbo.student_year_risk_summary
FROM 'C:\\Data-Analytics-Projects\education-student-success-dashboard\data\cleaned\student_year_risk_summary.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK,
    KEEPNULLS
);
GO

-- Load data-quality log.
BULK INSERT dbo.data_quality_log
FROM 'C:\\Data-Analytics-Projects\education-student-success-dashboard\data\cleaned\data_quality_log.csv'
WITH (
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0a',
    TABLOCK,
    KEEPNULLS
);
GO

-- Confirm row counts after loading.
SELECT 'dim_student' AS table_name,
COUNT (*) AS row_count
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

UNION ALL SELECT 'fact_year_risk_summary',
COUNT(*)
FROM dbo.fact_year_risk_summary

UNION ALL SELECT 'data_quality_log',
COUNT(*)
FROM dbo.data_quality_log
GO