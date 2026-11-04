
# REST Persistent Data API

## Project Overview

This is a RESTful Clinical Records API using Flask, SQLAlchemy, Pydantic, SQLite, and JSONL.

The API allows clients to create and retrieve clinical records through HTTP requests. Records are persisted in a SQLite database and written to a JSONL file.

The application is based on the module example, with three added clinical data fields and an improvement to timestamp handling to preserve explicit UTC information.

## Dependencies

- **Python 3.14**
- **Flask** — REST API endpoints
- **SQLAlchemy** — Database models and persistence
- **Pydantic** — Request validation
- **SQLite** — Relational database storage
- **JSONL** — Append-only record storage

## Installation and Setup

Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the Flask application:

```bash
python main.py
```

The API runs on:

`http://127.0.0.1:8000`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/clinical/` | Create a clinical record |
| GET | `/clinical/` | Retrieve all stored clinical records |

### Clinical Record Fields

| Field | Type | Description |
|---|---|---|
| id | Integer | Auto-generated record identifier |
| patient_name | String | Patient name |
| age | Integer | Patient age (0–120) |
| diagnosis | String | Clinical diagnosis |
| recorded_at | String | Automatically generated UTC timestamp |
| blood_pressure | String | Additional field: blood pressure |
| heart_rate | Integer | Additional field: heart rate |
| medication | String | Additional field: medication |

All patient fields required.

## API Testing

All testing was performed locally using `curl` and test patient records.

### Test 1: POST — Create a Clinical Record

```bash
curl -i -X POST http://127.0.0.1:8000/clinical/ \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "Jane Doe",
    "age": 42,
    "diagnosis": "Hypertension",
    "blood_pressure": "120/80",
    "heart_rate": 72,
    "medication": "Lisinopril"
  }'
```

**Result: HTTP 201 Created**

```json
{
  "age": 42,
  "blood_pressure": "120/80",
  "diagnosis": "Hypertension",
  "heart_rate": 72,
  "id": 1,
  "medication": "Lisinopril",
  "patient_name": "Jane Doe",
  "recorded_at": "2026-11-04T18:40:15.781161+00:00"
}
```

### Test 2: GET — Retrieve Clinical Records

```bash
curl -i http://127.0.0.1:8000/clinical/
```

**Result: HTTP 200 OK**

The endpoint returned an array containing Jane Doe's complete record, including all three additional fields and the UTC timestamp.

### Test 3: SQLite Persistence

SQLite records were inspected using Python's built-in `sqlite3` module:

```bash
python -c "import sqlite3; db = sqlite3.connect('clinical_data.db'); print(db.execute('SELECT * FROM clinical_data').fetchall()); db.close()"
```

**Result:** The database contained Jane Doe's complete clinical record, including blood pressure, heart rate, medication, and the UTC timestamp.

### Test 4: JSONL Persistence

The JSONL file was inspected using:

```bash
cat data/clinical_data.jsonl
```

**Result:**

```json
{"id": 1, "patient_name": "Jane Doe", "age": 42, "diagnosis": "Hypertension", "recorded_at": "2026-11-04T18:40:15.781161+00:00", "blood_pressure": "120/80", "heart_rate": 72, "medication": "Lisinopril"}
```

The record matched the data stored in SQLite.

### Test 5: Input Validation

Two additional POST requests were submitted to check Pydantic validation.

| Test | Input | Result |
|---|---|---|
| Negative heart rate | `heart_rate: -10` | HTTP 400 Bad Request |
| Missing required field | Omitted `medication` | HTTP 400 Bad Request |

Both requests were rejected with validation messages.

SQLite, JSONL, and GET checks confirmed that the invalid records were not stored.

### Test 6: Persistence After Restart

The Flask application was stopped and restarted, followed by another GET request:

```bash
curl -i http://127.0.0.1:8000/clinical/
```

**Result: HTTP 200 OK**

The original Jane Doe record was correctly retrieved after the restart, confirming that the application preserves records between runs.

## UTC Timestamp Improvement

Since my discussion post for Module 4 was on Incompatible Time Representations, I modified the datetime retrieval in the assignment example.
The original example created timestamps using `datetime.utcnow()`, which produces timezone naive datetime values.

It was modified to generate timezone aware UTC timestamps using:

```python
datetime.now(timezone.utc).isoformat()
```

The timestamps are stored as ISO 8601 strings with UTC offsets, preserving timezone information in both SQLite and JSONL.

Testing shows that the timestamp `2026-11-04T18:40:15.781161+00:00` was preserved identically in both storage formats and remained unchanged after retrieval.

## Reflection

This assignment shows how a REST API can integrate multiple persistence mechanisms while maintaining consistent data representations. SQLAlchemy provided an interface for storing and retrieving clinical records in SQLite, and JSONL allowed each submitted record to be written to a separate file. Pydantic validates incoming requests before records were persisted, preventing invalid data from entering either storage system.

I added blood pressure, heart rate, and medication fields to the database model, validation schema, and API responses. Testing confirmed that these fields were preserved in SQLite and JSONL, including after restarting the application.

I also modified the timestamp implementation to use timezone-aware UTC values rather than naive datetime objects. This connected directly to the interoperability challenges discussed in Module 4, particularly the importance of preserving consistent time information. Overall, the assignment reinforced how validation, consistent data structures, and persistence support reliable integration between applications.
