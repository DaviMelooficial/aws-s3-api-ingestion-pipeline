# AWS S3 API Ingestion Pipeline

## Project Objective

S3 Loader is a lightweight ingestion pipeline that extracts JSON data from a public API and stores it in Amazon S3 using a partitioned raw-layer structure.

The goal is to provide a practical foundation for analytics engineering workflows and prepare the next step toward Snowflake + dbt modeling.

## Why This Project Exists

This project exists to provide a simple and reproducible end-to-end pipeline from data extraction to analytics modeling.
It bridges the gap between raw API ingestion and analytics-ready datasets by organizing data in layers and adding observability from the start.

## Problem It Solves

Without a structured ingestion flow, raw API data often becomes hard to trace, validate, and transform.
This pipeline solves that by:

1. Standardizing ingestion into an S3 raw layer.
2. Applying a clear layered architecture toward Snowflake + dbt.
3. Enabling data lineage visibility and model documentation with dbt Docs.
4. Improving operational reliability with centralized logging and explicit failure behavior.

## Current Progress

1. API extraction implemented with timeout and HTTP status validation.
2. Centralized logging implemented with console and file output.
3. Rotating log files implemented to control log growth.
4. S3 upload implemented with `ContentType="application/json"`.
5. Environment variable validation implemented for `S3_BUCKET_NAME`.

## Data Flow

```text
Public API
  ↓
Python Extractor
  ↓
AWS S3 Raw Layer
  ↓
Snowflake Raw Layer
  ↓
dbt Transformations
  ↓
Analytics Models / Mart Layer
```

## Architecture Clarity

The project follows a layered architecture with explicit responsibilities:

1. Ingestion Layer: Python extractor and S3 loader.
2. Storage Layer: S3 raw zone with partitioned object paths.
3. Warehouse Layer: Snowflake raw/staging structures.
4. Transformation Layer: dbt models and tests.
5. Consumption Layer: analytics marts for BI and reporting.

## Architecture

- `main.py`
  - Orchestrates pipeline execution.
  - Loads environment variables.
  - Validates `S3_BUCKET_NAME` before running.
  - Builds the partitioned S3 key and triggers extract/load.

- `services/extract.py`
  - Calls the source API with a 10-second timeout.
  - Logs status code and response reason.
  - Uses `raise_for_status()` to fail fast on HTTP errors.
  - Returns serialized JSON payload.

- `services/load.py`
  - Uploads data to Amazon S3 via `boto3`.
  - Sets JSON content type on uploaded objects.
  - Logs success and raises errors on failure.

- `services/logger_config.py`
  - Central logger configuration.
  - Writes logs to terminal and `logs/app.log`.
  - Uses rotation: max 1 MB per file, 3 backups.

## Tooling Decisions

1. Python: lightweight orchestration and API ingestion.
2. Requests: straightforward HTTP handling with `raise_for_status()` support.
3. Boto3: native AWS SDK integration for S3 uploads.
4. Snowflake: scalable cloud warehouse for analytical workloads.
5. dbt: modular SQL transformations, testing, documentation, and lineage.
6. Rotating logs: operational observability with controlled file size.

## Folder Structure

```text
S3_loader/
|- main.py
|- requirements.txt
|- README.md
|- .env.example
|- services/
|  |- extract.py
|  |- load.py
|  |- logger_config.py
|- logs/
```

## Requirements

- Python 3.10+
- AWS credentials configured locally (profile, environment variables, or IAM role)
- Existing S3 bucket

Dependencies in `requirements.txt`:
- `boto3`
- `requests`
- `python-dotenv`

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables.

Use `.env.example` as reference:

```env
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=
S3_BUCKET_NAME=
```

## Run

```bash
python main.py
```

## S3 Output Pattern

```text
marketing_data/raw/jsonplaceholder/year=YYYY/month=MM/data_YYYYMMDD_HHMMSS.json
```

Example:

```text
marketing_data/raw/jsonplaceholder/year=2026/month=04/data_20260426_101530.json
```

## Logging and Error Handling

- Logs are emitted to console and `logs/app.log`.
- HTTP and runtime exceptions are logged with stack traces.
- Errors are re-raised to fail the pipeline clearly.

## dbt Section

- dbt profile configured for Snowflake.
- Profile name: `placeholders_pipeline`.
- Target: `dev`.
- Authentication configured with private key (`private_key_path`).
- Current direction: use S3 raw data as source for future Snowflake + dbt models.

## dbt Docs Visualization

You can explore model documentation and lineage graph locally with dbt Docs.

1. Generate metadata files:

```bash
dbt docs generate
```

2. Start the documentation server:

```bash
dbt docs serve
```

After starting the server, you can visualize:

1. Model lineage (DAG) and dependencies.
2. Model, source, and column descriptions.
3. Test coverage and model-level metadata.
4. Database objects materialized by dbt.

## Roadmap

1. Add retry and exponential backoff for transient API/S3 failures.
2. Add automated tests for extraction and loading modules.
3. Add ingestion metadata such as run id and record count.
4. Build curated models in Snowflake + dbt.