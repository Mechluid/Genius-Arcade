import pygame 

class MenuPanel():
    def __init__(self, game_instance, messsage, offset_y, font, color = None, bck_color = None): # type of text on panel
        self.screen = game_instance.screen
        self.settings = game_instance.settings
        self.panel = game_instance.menu_panel
        self.prep_menu_panel_txt(messsage, offset_y, font, color, bck_color)

    def check_text_type(self, font, color, bck_color):
        if color == None:
            color = font
        if bck_color == None:
            bck_color = font
        self.font = self.settings.font_size[font]
        self.font_color = self.settings.font_color[color]
        self.bckgrnd_color = self.settings.font_bckg_color[bck_color]                                                       

    def prep_menu_panel_txt(self, message, offset_y, font, color, bck_color):
        self.check_text_type(font, color, bck_color )
        self.image = self.font.render(message.title(), True,
                                                         self.font_color, self.bckgrnd_color)
        self.image_rect = self.image.get_rect()
        self.image_rect.centerx = self.panel.centerx
        self.image_rect.y = offset_y * self.panel.height

    def button(self):
        self.button_width, self.button_height = ((self.image_rect.width + self.settings.button_padding), 
                                                 (self.image_rect.height))
        self.button_rect = pygame.Rect(0, 0, self.button_width, self.button_height) 
        self.button_rect.center = self.image_rect.center
        self.corner_radius = self.button_height // 2

    def show_text(self):
        self.screen.blit(self.image, self.image_rect)

    def draw_button(self, button_color):
        pygame.draw.rect(self.screen, button_color, self.button_rect, border_radius=self.corner_radius)

        