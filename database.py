import os
import psycopg2.extras

TABLE = os.getenv("DATABASE_TABLE")

def get(command):
    # Remake the connection each time so if the connection gets terminated due to an error the server doesn't have to be restarted
    database = psycopg2.connect(
        f"dbname='{os.getenv('DATABASE_NAME')}' host='{os.getenv('DATABASE_IP')}' user='{os.getenv('DATABASE_USER')}' password='{os.getenv('DATABASE_PASSWORD')}'"
    )
    cursor = database.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(command)
    response = cursor.fetchall()
    cursor.close()
    return response

def put(command, values):
    # Remake the connection each time so if the connection gets terminated due to an error the server doesn't have to be restarted
    database = psycopg2.connect(
        f"dbname='{os.getenv('DATABASE_NAME')}' host='{os.getenv('DATABASE_IP')}' user='{os.getenv('DATABASE_USER')}' password='{os.getenv('DATABASE_PASSWORD')}'"
    )
    cursor = database.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(command, values)
    database.commit()
    cursor.close()