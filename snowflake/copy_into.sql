-- ============================================================
-- Load raw JSON files from AWS S3 into Snowflake RAW table
-- ============================================================

USE WAREHOUSE COMPUTE_WH;
USE DATABASE JSONPLACEHOLDER_PIPELINE_DB;
USE SCHEMA RAW;

COPY INTO JSONPLACEHOLDER_RAW (raw_data, source_file)
FROM (
    SELECT
        $1 AS raw_data,
        METADATA$FILENAME AS source_file
    FROM @S3_JSONPLACEHOLDER_STAGE
)
FILE_FORMAT = JSON_FORMAT
ON_ERROR = 'ABORT_STATEMENT';

-- Validation queries

SELECT COUNT(*) AS total_rows
FROM JSONPLACEHOLDER_RAW;

SELECT *
FROM JSONPLACEHOLDER_RAW
LIMIT 10;