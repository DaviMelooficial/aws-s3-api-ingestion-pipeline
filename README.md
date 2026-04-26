# S3 Loader

## Project Objective

S3 Loader is a simple data ingestion pipeline that extracts JSON data from a public API and stores it in an Amazon S3 bucket using a partitioned path structure.

The main goal is to provide a lightweight and practical ETL-style foundation for analytics workflows, where raw data is collected and organized for later processing.

## What This Project Does

1. Calls an API endpoint (`https://jsonplaceholder.typicode.com/posts`).
2. Validates HTTP responses and raises errors for failed requests.
3. Converts the response payload to JSON text.
4. Uploads the file to S3 using a time-based folder structure.
5. Writes execution logs to both console and file.

## Current Architecture

- `main.py`
  - Orchestrates the pipeline execution.
  - Loads environment variables.
  - Builds the S3 file path.
  - Calls extraction and load services.

- `services/extract.py`
  - Handles API requests.
  - Validates status codes with `raise_for_status()`.
  - Returns serialized JSON data.

- `services/load.py`
  - Sends data to Amazon S3 via `boto3`.

- `services/logger_config.py`
  - Configures centralized logging.
  - Logs are written to `logs/app.log` with rotation.

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
- AWS credentials configured locally (AWS CLI profile, environment variables, or IAM role)
- An existing S3 bucket

Dependencies are listed in `requirements.txt`:
- `boto3`
- `requests`
- `python-dotenv`

## Setup

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your environment variables.

Example `.env`:

```env
S3_BUCKET_NAME=your-bucket-name
```

## How to Run

```bash
python main.py
```

## Output in S3

Files are uploaded with a partition-like path pattern:

```text
marketing_data/raw/jsonplaceholder/year=YYYY/month=MM/data_YYYYMMDD_HHMMSS.json
```

Example:

```text
marketing_data/raw/jsonplaceholder/year=2026/month=04/data_20260426_101530.json
```

## Logging and Error Handling

- Logs are emitted to:
  - Console
  - `logs/app.log`
- HTTP errors and unexpected exceptions are logged with stack traces.
- Log files use rotation to avoid unlimited growth.