-- ============================================================
-- 01_setup.sql
-- Creates database, schema, table, stage, and file format
-- ============================================================

-- Create warehouse if not already present
CREATE WAREHOUSE IF NOT EXISTS analytics_wh 
  WITH WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60;

-- Create database and schema
CREATE DATABASE IF NOT EXISTS retail_db;
CREATE SCHEMA IF NOT EXISTS retail_db.analytics;

USE DATABASE retail_db;
USE SCHEMA analytics;

-- Create orders table matching the Superstore CSV (13 columns)
CREATE OR REPLACE TABLE orders (
  ship_mode     STRING,
  segment       STRING,
  country       STRING,
  city          STRING,
  state         STRING,
  postal_code   STRING,
  region        STRING,
  category      STRING,
  sub_category  STRING,
  sales         NUMBER(12,2),
  quantity      INT,
  discount      NUMBER(5,2),
  profit        NUMBER(12,2)
);

-- Create stage for CSV upload
CREATE OR REPLACE STAGE retail_stage
  FILE_FORMAT = (
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    DATE_FORMAT = 'AUTO'
    NULL_IF = ('', 'NULL')
    EMPTY_FIELD_AS_NULL = TRUE
  );
