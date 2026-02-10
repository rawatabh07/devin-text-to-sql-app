import streamlit as st
import psycopg2
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "examsdb")
DB_USER = os.getenv("DB_USER", "devinuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "devinpass")

TABLE_SCHEMA = """
Table name: exams
Columns:
- roll_no (INTEGER, PRIMARY KEY): Student roll number
- gender (VARCHAR): Student gender ('male' or 'female')
- division (VARCHAR): Student division ('A', 'B', 'C', 'D', or 'E')
- test_preparation_course (VARCHAR): Whether the student completed test preparation ('completed' or 'none')
- science (INTEGER): Science exam score
- maths (INTEGER): Maths exam score
- english (INTEGER): English exam score
"""


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def generate_sql(user_query, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""You are a SQL expert. Given the following PostgreSQL database schema:

{TABLE_SCHEMA}

Convert the following natural language question into a valid PostgreSQL SQL query.
Only return the SQL query, nothing else. Do not include any explanation, markdown formatting, or code blocks.
Make sure the query is safe and only uses SELECT statements (no INSERT, UPDATE, DELETE, DROP, etc.).

Question: {user_query}

SQL Query:"""

    response = model.generate_content(prompt)
    sql_query = response.text.strip()
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    return sql_query


def execute_query(sql_query):
    conn = get_db_connection()
    try:
        df = pd.read_sql_query(sql_query, conn)
        return df, None
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()


def main():
    st.set_page_config(page_title="Text-to-SQL AI APP", layout="wide")
    st.title("Text-to-SQL AI APP")

    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            help="Enter your Google Gemini API key to enable text-to-SQL translation.",
        )
        if api_key:
            st.success("API Key provided")
        else:
            st.warning("Please enter your Google Gemini API Key to get started.")

        st.markdown("---")
        st.subheader("Database Schema")
        st.code(TABLE_SCHEMA, language="text")

    st.markdown(
        "Enter a natural language question about the exam data, "
        "and the app will translate it into a SQL query and fetch the results."
    )

    user_query = st.text_area(
        "Enter your question:",
        placeholder="e.g., Show all students who scored above 90 in Science",
        height=100,
    )

    if st.button("Generate SQL & Fetch Results", type="primary"):
        if not api_key:
            st.error("Please provide your Google Gemini API Key in the sidebar.")
            return

        if not user_query.strip():
            st.error("Please enter a question.")
            return

        with st.spinner("Generating SQL query..."):
            try:
                sql_query = generate_sql(user_query, api_key)
            except Exception as e:
                st.error(f"Error generating SQL: {e}")
                return

        st.subheader("Generated SQL Query")
        st.code(sql_query, language="sql")

        unsafe_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE"]
        if any(keyword in sql_query.upper() for keyword in unsafe_keywords):
            st.error("The generated query contains unsafe operations. Only SELECT queries are allowed.")
            return

        with st.spinner("Executing query..."):
            df, error = execute_query(sql_query)

        if error:
            st.error(f"Error executing query: {error}")
        elif df is not None and not df.empty:
            st.subheader("Query Results")
            st.dataframe(df, use_container_width=True)
            st.caption(f"Total rows returned: {len(df)}")
        else:
            st.info("The query returned no results.")


if __name__ == "__main__":
    main()
