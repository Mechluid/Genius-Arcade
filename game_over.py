import pygame

class GameOver:
    '''Handles the on-screen texts and icons when the game played is over'''
    def __init__(self, game_instance, message, offset_y, text_type, offset_x= None):
        self.screen = game_instance.screen
        self.settings = game_instance.settings
        self.message = message
        self.offset_y = offset_y
        self.text_type = text_type
        self.offset_x = offset_x
        self.prep_game_over_txt()

    def prep_game_over_txt(self):
        '''Responsible for rendering the text and its properties on the screen'''
        self.font = self.settings.game_over_font[self.text_type]
        self.txt_color = self.settings.game_over_txt_color[self.text_type]
        self.bckg_color = self.settings.game_over_bckg_color[self.text_type]
        self.image = self.font.render(self.message.title(), True, self.txt_color, 
                                      self.bckg_color)
        self.rect = self.image.get_rect()
        if self.text_type != 'label':
            self.rect.x = self.screen.get_rect().width + self.settings.stealth_factor
        else:
            self.rect.centerx = self.screen.get_rect().width * self.offset_x
        self.rect.centery = self.screen.get_rect().height * self.offset_y

    def update(self, offset):
        '''Handles the text-on-entering motion'''
        if self.rect.centerx > offset * self.screen.get_rect().width:
            self.rect.x -= 10

    def button(self):
        self.button_width, self.button_height = ((self.rect.width + self.settings.button_padding), 
                                                         (self.rect.height))
        self.button_rect = pygame.Rect(0, 0, self.button_width, self.button_height) 
        self.button_rect.center = self.rect.center
        self.corner_radius = self.button_height // 2

    def show_text(self):
        '''Shows text on screen'''
        self.screen.blit(self.image, self.rect)

    def draw_button(self):
        '''Draws the button the screen'''
        pygame.draw.rect(self.screen, self.bckg_color, self.button_rect, border_radius=self.corner_radius)
        
    