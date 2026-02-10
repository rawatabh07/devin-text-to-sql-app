# Text-to-SQL AI APP

A Streamlit application that translates natural language prompts into SQL queries and fetches results from a PostgreSQL database containing exam data.

## Features

- Natural language to SQL query translation using Google Gemini AI
- PostgreSQL database with exam scores data (1000 students)
- Results displayed in tabular format
- Safe query validation (only SELECT queries allowed)

## Setup

### Prerequisites

- Python 3.10+
- PostgreSQL

### Installation

1. Clone the repository:
```bash
git clone https://github.com/rawatabh07/devin-text-to-sql-app.git
cd devin-text-to-sql-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL and create a database:
```bash
psql -U postgres -c "CREATE USER devinuser WITH PASSWORD 'devinpass';"
psql -U postgres -c "CREATE DATABASE examsdb OWNER devinuser;"
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Google Gemini API key and database credentials
```

5. Load the CSV data into the database:
```bash
python load_data.py
```

6. Run the Streamlit app:
```bash
streamlit run app.py
```

## Database Schema

| Column | Type | Description |
|--------|------|-------------|
| roll_no | INTEGER (PK) | Student roll number |
| gender | VARCHAR | Student gender |
| division | VARCHAR | Student division (A-E) |
| test_preparation_course | VARCHAR | Completed or none |
| science | INTEGER | Science exam score |
| maths | INTEGER | Maths exam score |
| english | INTEGER | English exam score |

## Usage

1. Enter your Google Gemini API key in the sidebar
2. Type a natural language question in the text box (e.g., "Show all students who scored above 90 in Science")
3. Click "Generate SQL & Fetch Results"
4. View the generated SQL query and results in tabular format
