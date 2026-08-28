import pygame
from pygame.sprite import Sprite

class InputBox(Sprite):
    def __init__(self, input, question, game_instance):
        super().__init__()
        self.screen = game_instance.screen
        self.input = f'{input}'
        self.settings = game_instance.settings
        self.question = question
        self.prep_input()

    def prep_input(self):
        '''Turns the string collected from the user to a rendered image to be displayed on the screen'''
        self.input_image = self.settings.text_font.render(self.input, True, 
                                                          self.settings.text_color, self.settings.screen_bottom_color)
        self.image_rect = self.input_image.get_rect()
        self.image_rect.bottom = self.question.rect.bottom - self.settings.answer_y_offset
        self.image_rect.x = self.question.rect.x + self.question.txt_width + self.settings.answer_x_offset

    def add_text(self, pressed_number):
        '''Adds strings to each other by catenation'''
        self.input += pressed_number
        self.prep_input()
        
    def remove_text(self):
        '''Removes an element from the already catenated string'''
        self.input = self.input[:-1]
        self.prep_input()

    def show(self):
        '''Responsible for the display of the text inputted by the user'''
        self.screen.blit(self.input_image, self.image_rect)
