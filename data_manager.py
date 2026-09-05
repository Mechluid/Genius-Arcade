import json
from pathlib import Path

class DataManager:
    '''Handles reading, writing, and updating user credentials via JSON.'''
    def __init__(self):
        # Set the path to user_data.json in the current directory
        self.filepath = Path(__file__).parent / 'user_data.json'
        # Initialize the user saved details immediately upon creation
        self.users = self.load_users()

    def load_users(self):
        '''Helps read the stored user's information if it exists.'''
        if self.filepath.exists():
            return json.loads(self.filepath.read_text())
        return {}

    def save_users(self):
        '''Saves the updated user information back to the database''' # TO call it each time game ends or gameover to save user progress
        json_string = json.dumps(self.users, indent=4)
        self.filepath.write_text(json_string)

    def add_user(self, username, password, secret_phrase):
        '''Creates a new account and saves it to the database.'''
        # This helps to prevent overwriting an existing account
        if username in self.users:
            return False # THis tells me if the user is already in the database , therefore prompting something like 'username'  already exist, login
        # Add the new user to database setup
        self.users[username] = {
            'password': password,
            'secret_phrase': secret_phrase # essential to reset user's passowrd
        }
        # Saving the new user information to the database
        self.save_users()
        return True # This to help with my pop up , once true, "Use profile created successfully"
        
    def verify_login(self, username, password):
        '''Checks if username exists and password matches during user login'''
        # Checks if the userrname exists
        if username in self.users:
            # Checks if the entered password matches the stored password
            if self.users[username]['password'] == password:
                return True # Trigger the blurred welcome screen
        # If the username doesn't exist, Or the password was wrong, it returns False
        return False # This brings a popup like "invalid credentials"

    def reset_password(self, username, secret_phrase):
        '''Reset the user password'''
        # Checks if the username exists
        if username in self.users:
            # Checks if the entered secret_phrase matches the stored secret_phrase
            if self.users[username]['secret_phrase'] == secret_phrase:
                return True # Changes the screen that shows something about new password , then confirm password
        # if username doesn't exist, or the secret phrase was wrong , it returns false
        return False # This shows a pop up text that says "Invalid credantials"
