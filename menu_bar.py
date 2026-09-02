import pygame

class MenuBar:
    '''Handles the icons and texts displayed on the game's menu bar'''
    def __init__(self, game_instance, message, offset_x):
        self.screen = game_instance.screen
        self.settings = game_instance.settings
        self.top_menu_bar = game_instance.top_bar_rect
        self.message = message
        self.offset_x = offset_x
        self.prep_menu_bar_text()
        self.button()

    def prep_menu_bar_text(self):
        self.image = self.settings.bar_txt_font.render(self.message.title(), True, 
                                                    self.settings.text_color)
        self.image_rect = self.image.get_rect()
        self.image_rect.x =  self.offset_x * self.screen.get_rect().width
        self.image_rect.centery = self.top_menu_bar.centery

    def button(self):
        self.button_rect = self.image_rect.inflate(30, 10)
        self.button_rect.center = self.image_rect.center

    def update(self, message):
        '''Handles the changes occuring on the menu bar'''
        self.message = message
        self.prep_menu_bar_text()
        self.button()
        
    def show_text(self):
        pygame.draw.rect(self.screen, self.settings.button_color, self.button_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.settings.button_border_color, self.button_rect, width=2, border_radius=8)
        self.screen.blit(self.image, self.image_rect)
