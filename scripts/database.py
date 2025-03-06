from scripts.logger import Logging
from typing import Dict, List
import os
import sqlite3
from datetime import datetime

log = Logging.getLogger()
DATABASE = os.getenv("DATABASE")

class Database:
    def __init__(self):
        self.db_name = DATABASE

        if not os.path.exists(DATABASE):
            self.create_db()


    def create_db(self):
        '''Create a database if it doesn't exist.'''

        tables = [
            '''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    password TEXT NOT NULL
                );
            ''',
            '''
                CREATE TABLE IF NOT EXISTS messages (
                    message_id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    time DATE NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                );
            '''
        ]

        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                for table in tables:
                    cursor.execute(table)
                
                conn.commit()

        except sqlite3.Error as e:
            log.warning(f"ENCOUNTERED AN ERROR CREATING TABLE: {e}")


    def get_message_history(self, limit: int = 100) -> List[Dict]:
        '''
        Fetch recent chat messages in the database. Set a limit (optional) 
        to fetch the desired number of messages.
        '''
        query = '''
            SELECT name, message
            FROM messages
            INNER JOIN users ON users.user_id = messages.user_id 
            ORDER BY time
            LIMIT ?;
        '''
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute(query, (limit,))
                rows = cursor.fetchall()

                message_history = [dict(row) for row in rows]
        except sqlite3.Error as e:
            log.warning(f"ENCOUNTERED AN ERROR FETCHING CHAT HISTORY: {e}")
            raise RuntimeError('Cannot fetch chat history at the moment. Try again later.')

        return message_history
    

    def save_message(self, user_id: int, message: str):
        '''Save the message sent by the user.'''
        query = '''
            INSERT INTO messages
            (user_id, message, time)
            VALUES
            (?,?,?);
        '''

        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                cursor.execute(query, (user_id, message, datetime.now()))
                conn.commit()
        except sqlite3.Error as e:
            log.warning(f"ENCOUNTERED AN ERROR ADDING A MESSAGE: {e}")
            raise RuntimeError("Cannot send a message at the moment. Try again later.")


    def get_user(self, name: str) -> Dict[str, str]:
        '''Check the name of the user in the database and fetch credentials.'''
        query = '''
            SELECT * from users
            WHERE name=?;
        '''
        user = {}
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                cursor.execute(query, (name,))

                user_details = cursor.fetchone()
                
                if user_details:
                    user["id"], user["name"], user["password"] = user_details

        except sqlite3.Error as e:
            log.warning(f"ENCOUNTERED AN ERROR FETCHING USER DATA: {e}")
            raise RuntimeError("Cannot check credentials at the moment. Try again later.")

        return user


    def add_user(self, data: Dict[str, str]):
        '''Save user credentials in the database.'''
        query = '''
            INSERT INTO users
            (name, password)
            VALUES
            (?,?);
        '''
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()

                cursor.execute(query, (data["name"], data["password"]))
                conn.commit()
        except sqlite3.Error as e:
            log.warning(f"ENCOUNTERED AN ERROR ADDING USER: {e}")
            raise RuntimeError('Cannot sign up at the moment. Try again later')
        