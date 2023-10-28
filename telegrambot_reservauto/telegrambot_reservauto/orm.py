import os
import MySQLdb
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Database():
    def __init__(self) -> None:
        self.connection = None
        # Test connection
        self.connect()
        self.disconnect()
    
    def connect(self) -> None:
        try:
            # Connect to the database
            self.connection = MySQLdb.connect(
                host=os.getenv('DATABASE_HOST'),
                user=os.getenv('DATABASE_USERNAME'),
                passwd=os.getenv('DATABASE_PASSWORD'),
                db=os.getenv('DATABASE'),
                autocommit=True,
                ssl_mode='VERIFY_IDENTITY',
                # See https://planetscale.com/docs/concepts/secure-connections#ca-root-configuration
                # to determine the path to your operating systems certificate file.
                # ssl={ 'ca': '' }
                ssl={ 'ca': '/etc/ssl/cert.pem' } # For macOS
            )
        
        except MySQLdb.Error as e:
            print('MySQL Error:', e)
            self.disconnect()
    
    def disconnect(self) -> None:
        try:
            self.connection.close()

        except MySQLdb.Error as e:
            print('MySQL Error:', e)

    
    def get_tables(self) -> list:
        try:
            self.connect()

            # Create a cursor to interact with the database
            cursor = self.connection.cursor()

            # Execute 'SHOW TABLES' query
            cursor.execute('SHOW TABLES')

            # Fetch all the rows
            tables = cursor.fetchall()

            # Print out the tables
            print('Tables in the database:')
            for table in tables:
                print(table[0])
            
            return tables

        except MySQLdb.Error as e:
            print('MySQL Error:', e)
            return False

        finally:
            # Close the cursor and connection
            cursor.close()
            self.disconnect()
    
    def get_user(self, telegram_user_id) -> dict:
        try:
            self.connect()

            # Create a cursor to interact with the database
            cursor = self.connection.cursor()

            # Execute 'SELECT' query
            cursor.execute(f'SELECT * FROM users WHERE telegram_user_id = {telegram_user_id}')

            # Fetch all the rows
            user = cursor.fetchone()

            # Print out the tables
            print('User:')
            print(user)

            if user is None:
                return None
            
            return user[0]

        except MySQLdb.Error as e:
            print('MySQL Error:', e)
            return False

        finally:
            # Close the cursor and connection
            cursor.close()
            self.disconnect()

    def create_user(self, telegram_user, telegram_chat_id) -> bool:
        try:
            self.connect()

            # Create a cursor to interact with the database
            cursor = self.connection.cursor()

            # Execute 'INSERT' query
            cursor.execute(f'''INSERT INTO users (
telegram_user_id, 
telegram_username, 
telegram_first_name, 
telegram_last_name, 
telegram_language_code, 
telegram_chat_id
) VALUES (
"{telegram_user.id}", 
"{telegram_user.username}", 
"{telegram_user.first_name}", 
"{telegram_user.last_name}", 
"{telegram_user.language_code}", 
"{telegram_chat_id}"
)''')
            # 'INSERT INTO users (telegram_user_id, telegram_username, telegram_first_name, telegram_last_name, telegram_language_code, telegram_chat_id) VALUES ("123456", "myUsername", "John", "Doe", "en", "456789");'

            # Commit changes
            self.connection.commit()

            return True

        except MySQLdb.Error as e:
            print('MySQL Error:', e)
            return False

        finally:
            # Close the cursor and connection
            cursor.close()
            self.disconnect()