# Streaming Financial Events Pipeline

A local data engineering project for generating, validating, transforming, and analyzing financial event data. The project simulates a near real-time financial event pipeline and provides a Streamlit dashboard to explore processed results.

## About

This project demonstrates an end-to-end financial data pipeline. It generates synthetic financial events, validates the incoming records, transforms them into analytics-ready tables, and stores the processed output in a local SQLite warehouse.

The goal of this project is to show how event-style data can be converted into structured datasets for reporting, monitoring, and dashboarding.

## What this project does

The pipeline follows this flow:

```text
Synthetic financial events
        ↓
Raw JSONL event files
        ↓
Validation and data quality checks
        ↓
Transformation pipeline
        ↓
SQLite warehouse
        ↓
Streamlit dashboard
```

## Features

* Generate synthetic financial event data
* Store raw events in JSONL format
* Validate event schema and required fields
* Clean and transform financial records
* Load processed data into a SQLite warehouse
* Inspect warehouse tables from the command line
* View event metrics through a Streamlit dashboard
* Includes tests for core pipeline logic
* Can be run locally or with Docker

## Tech Stack

* Python
* SQLite
* Pandas
* Streamlit
* Pytest
* Docker
* GitHub

## Project Structure

```text
.
├── dashboard.py
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── src/
│   └── financial_pipeline/
│       ├── cli.py
│       ├── generator.py
│       ├── pipeline.py
│       ├── quality.py
│       └── warehouse.py
├── tests/
├── README.md
└── .gitignore
```

## Main Components

### Event Generator

The generator creates synthetic financial event records. These records are saved as JSONL files and act as the raw input for the pipeline.

### Validation Layer

The validation step checks for missing fields, invalid values, incorrect event types, and malformed records before loading data into the warehouse.

### Transformation Pipeline

The transformation logic cleans the raw events and prepares them for analytics. This includes formatting fields, filtering invalid records, and creating structured outputs.

### SQLite Warehouse

The processed data is loaded into a local SQLite database. This keeps the project easy to run without requiring a cloud database or external service.

### Streamlit Dashboard

The dashboard provides a simple interface to view processed financial events, basic metrics, and data summaries.

## How to Run Locally

Clone the repository:

```bash
git clone https://github.com/dp24723/streaming-financial-events-pipeline.git
cd streaming-financial-events-pipeline
```

Create and activate a Python environment:

```bash
conda create -n financepipe python=3.11 -y
conda activate financepipe
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

If the editable install does not work, install from `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

## Generate Sample Financial Events

Run:

```bash
financial-pipeline generate --rows 1000 --out data/raw/events.jsonl
```

This creates a raw JSONL file with synthetic financial event records.

## Run the Pipeline

Run:

```bash
financial-pipeline run-local --input data/raw/events.jsonl --db data/warehouse/finance.db
```

This validates, transforms, and loads the financial events into a local SQLite warehouse.

## Inspect the Warehouse

Run:

```bash
financial-pipeline inspect --db data/warehouse/finance.db
```

This prints a quick summary of the processed tables and records.

## Run the Dashboard

Start the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

Open the local app:

```text
http://localhost:8501
```

The dashboard reads from the generated SQLite warehouse and displays processed financial event data.

## Run Tests

Run:

```bash
pytest -q
```

## Docker Usage

Build and run the project with Docker Compose:

```bash
docker compose up --build
```

This can be useful for testing the project in a clean environment.

## Example Use Case

A financial operations team may receive transaction or event records from multiple systems. Before those records can be used for reporting, they need to be validated, cleaned, transformed, and loaded into a structured format.

This project simulates that workflow using generated financial events and a local warehouse.

## Data Flow

1. Generate raw financial events.
2. Save events as JSONL input files.
3. Validate required fields and event structure.
4. Remove or flag invalid records.
5. Transform valid records into analytics-ready format.
6. Load processed output into SQLite.
7. Explore results through the dashboard.

## Deployment

This dashboard can be deployed on Streamlit Community Cloud.

To deploy:

1. Push this repository to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app.
4. Select this repository.
5. Set the main file path as:

```text
dashboard.py
```

6. Deploy the app.

If the deployed app needs sample data, generate the sample data locally and make sure the dashboard can create or load demo data when the app starts.

## Security and Git Ignore Notes

Generated data should not be committed unless it is a small sample file intended for demo use.

The following files and folders should stay ignored:

```text
.env
data/
__pycache__/
*.pyc
.DS_Store
.venv/
.streamlit/secrets.toml
```

## Future Improvements

* Add support for live event streaming
* Add Kafka or message queue integration
* Add Snowflake or PostgreSQL output support
* Add Airflow DAG for scheduled runs
* Add data quality reporting dashboard
* Add anomaly detection for suspicious events
* Add CI checks for pipeline tests
* Add dashboard filters for event type and date range

## Status

The current version supports local event generation, validation, transformation, SQLite loading, and dashboard visualization.
