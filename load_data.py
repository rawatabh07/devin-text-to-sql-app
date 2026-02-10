import csv
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "examsdb")
DB_USER = os.getenv("DB_USER", "devinuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "devinpass")


def load_data():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS exams;")
    cur.execute(
        """
        CREATE TABLE exams (
            roll_no INTEGER PRIMARY KEY,
            gender VARCHAR(10),
            division VARCHAR(5),
            test_preparation_course VARCHAR(20),
            science INTEGER,
            maths INTEGER,
            english INTEGER
        );
        """
    )

    with open("exams.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(
                """
                INSERT INTO exams (roll_no, gender, division, test_preparation_course, science, maths, english)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    int(row["Roll no"]),
                    row["gender"].strip(),
                    row["Division"].strip(),
                    row["test preparation course"].strip(),
                    int(row["Science"]),
                    int(row["Maths"]),
                    int(row["English"]),
                ),
            )

    conn.commit()
    cur.close()
    conn.close()
    print("Data loaded successfully into the 'exams' table.")


if __name__ == "__main__":
    load_data()
