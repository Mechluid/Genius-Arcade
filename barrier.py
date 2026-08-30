import pygame
from pygame.sprite import Sprite

class Barrier(Sprite):
    '''Handles the bar properties acting as a barrier to the balls in motion'''
    def __init__(self, game_instance):
        super().__init__()
        self.screen = game_instance.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game_instance.settings
        self.stats = game_instance.stats
        self.bar_width, self.bar_height = (game_instance.screen_width, 30)
        self.bar_x, self.bar_y = (0, self.screen_rect.centery - 300)
        self.rect = pygame.Rect(self.bar_x, self.bar_y, self.bar_width, self.bar_height)
        self.y = float(self.rect.y)

    def update(self, current_bar_speed):
        self.y += current_bar_speed
        self.rect.y = self.y

    def reset(self):
        '''It resets the bar to its intial position'''
        self.rect.y = self.bar_y
        self.y = float(self.rect.y)

    def __repr__(self):
        '''for easy debug of the bars's motion'''
        return (f'Bar_Distance: {self.rect.y}')
    
    def draw(self):
        '''Displays the rectangular bar trapping the balls '''
        pygame.draw.rect(self.screen, self.settings.bar_color, self.rect)
    