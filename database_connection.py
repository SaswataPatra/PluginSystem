import psycopg2


def connection():
    conn = psycopg2.connect(
        host="postgresdb.ctgcc3olpy9z.ap-south-1.rds.amazonaws.com",
        database="atlan",
        user='postgres',
        port = 5432,
        password='password')

    return conn