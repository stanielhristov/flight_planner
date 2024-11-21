import os

import psycopg2


def get_connection():
    # Retrieve environment variables with defaults if not set
    database = os.getenv('POSTGRES_DB', 'flight-db')  # Default: 'flight-db'
    host = os.getenv('POSTGRES_HOST', 'localhost')  # Default: 'localhost'
    user = os.getenv('POSTGRES_USER', 'admin')  # Default: 'admin'
    password = os.getenv('POSTGRES_PASSWORD', 'admin')  # Default: 'admin'
    port = os.getenv('POSTGRES_PORT', '5432')  # Default: '5432'

    return psycopg2.connect(
        database=database,
        host=host,
        user=user,
        password=password,
        port=port
    )
