import psycopg2
import os
from dotenv import load_dotenv



def connection():
    load_dotenv()
    conn = psycopg2.connect(
        host=os.environ.get('DATABASE_HOST'),
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        port = os.environ.get('DB_PORT'),
        password=os.environ.get('DB_PASS'))

    return conn