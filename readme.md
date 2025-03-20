# FastAPI Project Setup Guide

## Prerequisites
- Python (>=3.x)
- pip (latest version recommended)
- Virtual environment (optional but recommended)
- Liquibase
- MySQL

## Installation Steps

### 1. Clone the Repository
```sh
git clone <repository-url>
cd <project-folder>
```

### 2. (Optional) Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.

#### For Windows (PowerShell)
```sh
python -m venv SeaVenv
SeaVenv\Scripts\activate
```

#### For macOS/Linux
```sh
python -m venv SeaVenv
source SeaVenv/bin/activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```
### 4. Create Database
```sh
CREATE DATABASE <DB_NAME>
```

### 5. Run Liquibase Migrations
```sh
cd liquibase
liquibase update
```
-Before running the Liquibase update, please create the liquibase.properties file and update all the field values.

## Running the FastAPI Application

### Start the Application
```sh
uvicorn main:app --reload
```

### Start application on specific port
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Additional Notes
- Ensure all required environment variables are set before running the application.
- If using a database, configure it properly before running migrations.
- Use `deactivate` to exit the virtual environment when done.

## Troubleshooting
If you encounter any issues, try:
- Checking Python and pip versions (`python --version`, `pip --version`)
- Ensuring dependencies are installed correctly (`pip list`)
- Activating the virtual environment properly before running commands

For further assistance, refer to the project documentation or raise an issue in the repository.
