from pathlib import Path
import json

class GameStats:
    '''Manages the gameplay variables'''
    def __init__(self, game_instance):
        self.settings = game_instance.settings
        self.path = Path(__file__).parent / 'high_score.txt'
        if self.path.exists():
            self.high_score = json.loads(self.path.read_text())
        else:
            self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        self.game_round = 1
        self.score = 0
        self.heart_num = 3

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            value = json.dumps(self.high_score)
            self.path.write_text(value)