import pygame 
from pygame.sprite import Sprite
from pathlib import Path

class Heart(Sprite):
    '''Manages the heart icon depicting player's chances'''
    def __init__(self, game_instance):
        super().__init__()
        self.screen = game_instance.screen
        self.settings = game_instance.settings
        self.top_menu_bar = game_instance.top_bar_rect
        self.create_heart_image()

    def create_heart_image(self):
        image_path = Path(__file__).parent/ 'heart.bmp'
        self.image = pygame.image.load(image_path)
        self.scaled_size = (50, self.top_menu_bar.height)
        self.scaled_image = pygame.transform.smoothscale(self.image, self.scaled_size)
        self.rect = self.scaled_image.get_rect()

    def draw(self):
        self.screen.blit(self.scaled_image, self.rect)