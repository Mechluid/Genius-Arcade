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
        if self.filepath.exists() and self.filepath.read_text().strip():
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
            'secret_phrase': secret_phrase, # essential to reset user's passowrd
            'easy_high_score': 0, # default user high_score
            'medium_high_score' : 0,
            'hard_high_score' : 0
        }
        # Saving the new user information to the database
        self.save_users()
        return True # This to help with my pop up , once true, "Use profile created successfully"

    def update_user_password(self, username, new_password):
        '''Updates the user password and saves to the database.'''
        if username in self.users:
            self.users[username]['password'] = new_password
            self.save_users()
            return True
        return False
        
    def verify_login(self, username, password):
        '''Checks if username exists and password matches during user login'''
        # Checks if the userrname exists
        if username in self.users:
            # Checks if the entered password matches the stored password
            if self.users[username]['password'] == password:
                return True # Trigger the blurred welcome screen
        # If the username doesn't exist, Or the password was wrong, it returns False
        return False # This brings a popup like "invalid credentials"

    def get_high_score(self, username, difficulty):
        '''Retrieves the high score for a specific user and difficulty.'''
        if username in self.users:
            score_key = f"{difficulty}_high_score"
            return self.users[username].get(score_key, 0) # This prevents key error from python 
        # incase the key needed isn't available, it returns 0 instead.
        return 0

    def update_high_score(self, username, difficulty, new_score):
        '''Updates the high score for a user if the new score is higher.'''
        if username in self.users:
            score_key = f"{difficulty}_high_score"
            current_high = self.users[username].get(score_key, 0)
            if new_score > current_high:
                self.users[username][score_key] = new_score
                self.save_users()
                return True
        return False
    
    def reset_password(self, username, secret_phrase):
        '''Reset the user password'''
        # Checks if the username exists
        if username in self.users:
            # Checks if the entered secret_phrase matches the stored secret_phrase
            if self.users[username]['secret_phrase'] == secret_phrase:
                return 'success' # Changes the screen that shows something about new password , then confirm password
            return 'wrong_secret'
        # if username doesn't exist, or the secret phrase was wrong , it returns false
        return 'user_not_found' # This shows a pop up text that says "Invalid credantials"
