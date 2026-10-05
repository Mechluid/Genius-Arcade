class GameStats:
    '''Manages the gameplay variables'''
    def __init__(self, game_instance):
        self.game = game_instance
        self.settings = game_instance.settings
        self.data_manager = game_instance.data_manager
        self.reset_stats()

    def reset_stats(self):
        self.game_round = 1
        self.score = 0
        self.heart_num = 3

    def get_current_high_score(self, difficulty=None):
        '''Asks DataManager for the logged-in user's high score on the active difficulty.'''
        if difficulty:
            return self.data_manager.get_high_score(self.game.active_user, difficulty)
        return self.data_manager.get_high_score(self.game.active_user, self.game.current_difficulty)
    
    def update_high_score(self):
        '''Tells DataManager to check and update if current score is a new record.'''
        if self.game.active_user:
            self.data_manager.update_high_score(
                self.game.active_user, 
                self.game.current_difficulty, 
                self.score
            )