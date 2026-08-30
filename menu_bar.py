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
                                                    self.settings.text_color, self.settings.screen_bottom_color)
        self.rect = self.image.get_rect()
        self.rect.x =  self.offset_x * self.screen.get_rect().width
        self.rect.centery = self.top_menu_bar.centery

    def button(self):
        self.button_width, self.button_height = ((self.rect.width + self.settings.button_padding), 
                                                 (self.rect.height + self.settings.button_padding))
        self.button_rect = pygame.Rect(0, 0, self.button_width, self.button_height)
        self.button_rect.center = self.rect.center
        self.corner_radius = self.button_height // 2

    def update(self, message):
        '''Handles the changes occuring on the menu bar'''
        self.message = message
        self.prep_menu_bar_text()
        self.button()
        
    def show_text(self):
        pygame.draw.rect(self.screen, self.settings.screen_bottom_color, self.button_rect, border_radius=self.corner_radius)
        self.screen.blit(self.image, self.rect)
