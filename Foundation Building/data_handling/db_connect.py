import psycopg2 # type: ignore
from psycopg2 import sql # type: ignore

# Database connection details
db_config = {
    "dbname": "your_db_name",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("Connected to the database.")

    # Sample query to fetch data
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print("PostgreSQL version:",db_version)

except Exception as e:
    print(f"Error: {e}")
finally:
    if conn:
        cursor.close()
        conn.close()
        print("Database connection closed.")