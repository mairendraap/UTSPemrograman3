import os
import psycopg2


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("POSTGRES_DB", "student_risk"),
        user=os.getenv("POSTGRES_USER", "student"),
        password=os.getenv("POSTGRES_PASSWORD", "student123"),
        connect_timeout=5,
    )
