import pygame
import random
from pygame.sprite import Sprite
from math import prod

class Question(Sprite):
    def __init__(self, game_instance, min_number, max_number):
        super().__init__()
        self.screen = game_instance.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game_instance.settings
        self.fixed_pos = self.screen_rect.height - self.settings.qn_distance
        self.pick_random_operator()
        self.generate_random_num(min_number, max_number)
        self.operation = {'+': lambda a, b: a + b,
                          '-': lambda a, b: a - b,
                          'x': lambda a, b: a * b,
                          '/': lambda a, b: a // b # integer division
                          }
        self.create_equation()
        self.prep_equation()
        self.generate_answers()
    
    def pick_random_operator(self):
        '''Picks an operator to be displayed randomly'''
        self.operators = ['+', '-', 'x', '/'] # Planning to remove the divisor soon and add it in later rounds
        self.chosen_operator = random.choice(self.operators)

    def generate_random_num(self, min_number, max_number):
        '''Picks random numbers from a sample size to be operated on'''
        self.numbers = random.sample(range(min_number, max_number), 2)
        if self.chosen_operator == '/':
            self.a, self.b = prod(self.numbers), random.choice(self.numbers)
        elif self.chosen_operator == '-':
            self.a, self.b = max(self.numbers), min(self.numbers)
        else:
            self.a, self.b = self.numbers

    def prep_equation(self):
        '''Renders the equation string as an image to be displayed on the screen'''
        self.eqn_image = self.settings.text_font.render(self.message, True, 
                                                        self.settings.text_color, self.settings.screen_bottom_color)
        self.rect = self.eqn_image.get_rect()
        self.txt_message =f'Question: {self.a} {self.chosen_operator} {self.b}' # The text part of the 
        # rendered question image
        self.txt_width, self.txt_height = self.settings.text_font.size(self.txt_message)
        self.rect.bottom = self.screen_rect.height + self.settings.stealth_factor
        self.rect.x =  self.screen_rect.centerx - (self.rect.width / 2)

    def create_equation(self):
        self.message = f'Question: {self.a} {self.chosen_operator} {self.b} ________'

    def generate_answers(self):
        '''Provides a solution to the question formulated'''
        self.chosen_operation = self.operation[self.chosen_operator]
        self.answer = self.chosen_operation(self.a, self.b)

    def update(self):
        '''Updates the displayed question position on the screen'''
        if self.rect.bottom > self.fixed_pos:
            self.rect.y -= 10

    def show(self):
        '''DIsplays the rendered question image on the screen'''
        self.screen.blit(self.eqn_image, self.rect)