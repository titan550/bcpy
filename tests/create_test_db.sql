USE master;
GO
IF DB_ID (N'bcpy_test_db') IS NOT NULL
DROP DATABASE bcpy_test_db;
GO
CREATE DATABASE bcpy_test_db;
GO
