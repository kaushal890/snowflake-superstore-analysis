-- ============================================================
-- 02_load_data.sql
-- Loads the Superstore CSV from the stage into the orders table
-- Prerequisite: upload SampleSuperstore.csv to @retail_stage 
-- via Snowsight Database Explorer
-- ============================================================

USE DATABASE retail_db;
USE SCHEMA analytics;

-- Verify the file is in the stage
LIST @retail_stage;

-- Load data
COPY INTO orders
FROM @retail_stage/SampleSuperstore.csv
FILE_FORMAT = (
  TYPE = 'CSV'
  SKIP_HEADER = 1
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  NULL_IF = ('', 'NULL')
  EMPTY_FIELD_AS_NULL = TRUE
)
ON_ERROR = 'CONTINUE';

-- Verify load (should return 9,994)
SELECT COUNT(*) AS row_count FROM orders;
SELECT * FROM orders LIMIT 10;
