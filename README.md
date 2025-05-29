# Powerplant Coding Challenge

This project solves the challenge of calculating the optimal production plan for a set of power plants, taking into account fuel costs, efficiency, and each plant's constraints.

## Requirements

- Python 3.8 or higher

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jorgegadea/powerplant-coding-challenge
   cd your-repo
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Send a POST request to `/productionplan` with a JSON payload like those in the `example_payloads` folder.  
Example using `curl`:

```bash
curl -X POST http://localhost:8888/productionplan -H "Content-Type: application/json" -d @example_payloads/payload1.json
```

Or from PowerShell (one line):

```powershell
Invoke-RestMethod -Uri "http://localhost:8888/productionplan" -Method Post -ContentType "application/json" -InFile ".\example_payloads\payload1.json"
```

The response will be a JSON with the production plan.

## Interactive Documentation

While the API is running, you can access the interactive documentation (Swagger UI) at:  
[http://localhost:8888/docs](http://localhost:8888/docs)

## Tests

To run the automated tests:

```bash
python -m unittest discover tests
```

Or using `pytest`:

```bash
pytest
```

## Project Structure

```
powerplant-coding-challenge-test/
│
├── app/                        # Main API code
│   ├── __init__.py
│   ├── main.py                 # API entry point (FastAPI)
│   ├── logic.py                # Production plan calculation logic
│   └── models.py               # Data models (Pydantic)
│
├── requirements.txt            # Project dependencies
├── README.md                   # This file
│
├── example_payloads/           # Example payloads and expected responses
│   ├── payload1.json
│   ├── payload2.json
│   ├── payload3.json
│   └── response3.json
│
├── test/                       # Automated tests
│   ├── __init__.py
│   └── test_logic.py
```
--- 