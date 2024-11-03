# SongID
# Database interactions / management

import logging
import psycopg2
from psycopg2 import sql
from config import DB_URL

logger = logging.getLogger(__name__)

def get_connection():
    return psycopg2.connect(DB_URL)


def initialise_database():
    logger.info('Initialising database...')
    connection = get_connection()
    cursor = connection.cursor()


    # TODO add counter for 
    
    # Create tables if they do not exist
    # TODO: Investigate bigint=8bytes, unnecessary for unix timestamp? 
    # TODO: add delete/constraint to prevent orphan records
    create_users_table = '''
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255),
        blocked_bot BOOLEAN DEFAULT FALSE,
        banned BOOLEAN DEFAULT FALSE,
        first_added BIGINT DEFAULT EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)::BIGINT,
        last_updated BIGINT DEFAULT EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)::BIGINT
    );
    '''
    
    # Logs each API request made by users, including the endpoint called, the status of the request, and the timestamp.
    create_api_requests_table = '''
    CREATE TABLE IF NOT EXISTS api_requests (
        request_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(user_id),
        endpoint VARCHAR(255) NOT NULL,
        status VARCHAR(50) NOT NULL,
        timestamp BIGINT DEFAULT EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)::BIGINT
    );
    '''

    # Stores music information, including the ISRC code, title, artist, year, and the user who first discovered the music.Stores music information, including the ISRC code, title, artist, year, and the user who first discovered the music.
    # TODO: Add acrcloud-metadata-date
    create_music_table = '''
    CREATE TABLE IF NOT EXISTS music (
        music_id SERIAL PRIMARY KEY,
        isrc VARCHAR(50) UNIQUE NOT NULL,
        title VARCHAR(255) NOT NULL,
        artist VARCHAR(255) NOT NULL,
        year INT,
        request_id INT REFERENCES api_requests(request_id)
    );
    '''

    # Create the identifications table to link successful API requests with music ISRC
    create_identifications_table = '''
    CREATE TABLE IF NOT EXISTS identifications (
        identification_id SERIAL PRIMARY KEY,
        request_id INT REFERENCES api_requests(request_id),
        music_id SERIAL REFERENCES music(music_id)
    );
    '''
    
    try:
        logger.info('Creating tables...')
        cursor.execute(create_users_table)
        cursor.execute(create_api_requests_table)
        cursor.execute(create_music_table)
        cursor.execute(create_identifications_table)
        connection.commit()
        logger.info('Database tables created successfully.')
    except Exception as e:
        logger.error(f'An error occurred whilst creating database: {e}')
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


def add_user(user_id, username, first_name, last_name):
    '''Add a user to the database.'''
    logger.info(f'Adding user {user_id} to database')
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            '''
            INSERT INTO users (user_id, username, first_name, last_name)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id) DO NOTHING;  -- Prevents duplicate entries
            ''',
            (user_id, username, first_name, last_name)
        )
        connection.commit()
    except Exception as e:
        logger.error(f'Error adding user: {e}')
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    initialise_database()