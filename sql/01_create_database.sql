/*
01_create_database.sql

Purpose: Create a SQL Server database for the Education Student Success Dashboard project.

Why this matters: Before loading cleaned CSV files into SQL Server, we need a dedicated database to keep all project tables organized in one place.

This script:
    - Creates the project database if it does not already exist
    - Switches SQL Server into that database so later commands run in the right place

How to use: Run this script first in SQL Server Managemnt Studio (SSMS).
*/

IF DB_ID('education_student_success_dashboard') IS NULL
BEGIN
    CREATE DATABASE education_student_success_dashboard
END;
GO

USE education_student_success_dashboard;
GO