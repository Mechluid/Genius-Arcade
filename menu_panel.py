import pygame 

class MenuPanel():
    '''Responsible for the game's menu panel texts and icons'''
    def __init__(self, game_instance, message, offset_y, font, color = None): # type of text on panel
        self.screen = game_instance.screen
        self.settings = game_instance.settings
        self.panel = game_instance.menu_panel
        self.font_type = font
        self.color = color
        self.offset_y = offset_y
        self.message = message
        self.prep_menu_panel_txt()
# TODO:
    def check_text_type(self):
        '''To classify the type of text and its properties to be displayed once game over'''
        self.font = self.settings.font_size[self.font_type]    
        if self.color:
            self.text_color = self.settings.font_color[self.color]
        else:
            self.text_color = self.settings.font_color[self.font_type]                                             

    def prep_menu_panel_txt(self):
        self.check_text_type()
        self.image = self.font.render(self.message.title(), True,
                                                         self.text_color)
        self.image_rect = self.image.get_rect()
        self.image_rect.centerx = self.panel.centerx
        self.image_rect.y = self.offset_y * self.panel.height

    def button(self):
        self.button_rect = self.image_rect.inflate(30, 10)
        self.button_rect.center = self.image_rect.center

    def show_text(self):
        self.screen.blit(self.image, self.image_rect)

    def draw_button(self):
        '''Draws the button'''
        pygame.draw.rect(self.screen, self.settings.button_color, self.button_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.settings.button_border_color, self.button_rect, width=2, border_radius=8)

        