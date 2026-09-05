import pygame

class FormField:
    '''Handles interactive text entry for login and registration.'''
    def __init__(self, game_instance, placeholder, y_ratio):
        self.screen = game_instance.screen
        self.settings = game_instance.settings
        self.menu_panel = game_instance.menu_panel
        self.placeholder = placeholder # The text entered by the user
        self.y_ratio = y_ratio
        self.input_text = ''  # Holds the actual characters the user types
        self.active = False # helps track if the field box is currently selected.
        
        # Text box dimensions
        self.width = game_instance.panel_w * 0.8  
        self.height = 55
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.create_field_box()
        self.prep_placholder_txt()
        # Colors for the field box interactive states - basically changes color when it is clicked on
        self.color_inactive = self.settings.panel_border_color
        self.color_active = (255, 255, 255) # Bright white when active
        self.current_color = self.color_inactive

    def create_field_box(self):
        '''Creating and centering the text box on the login page'''
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen.get_rect().centerx
        self.rect.top = self.menu_panel.top + (self.menu_panel.height * self.y_ratio)
        self.font = self.settings.placeholder_font

    def prep_placholder_txt(self):
        '''Renders the user input (string) passed into the placeholder parameter to the screen'''
        if self.input_text != '':
            display_str = self.input_text
            text_color = (255, 255, 255)
        else:
            display_str = self.placeholder # Solid white for typed text
            text_color = (150, 150, 150) # Dim grey for placeholder
        self.text_surface = self.font.render(display_str, True, text_color)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.centery = self.rect.centery
        self.text_rect.left = self.rect.left + 15 # Little gap for the placeholder text to start from

    def update_active_state(self, mouse_pos):
        '''Checks if the mouse clicked inside this specific box.'''
        if self.rect.collidepoint(mouse_pos):
            self.active = True
            self.current_color = self.color_active
        else:
            self.active = False
            self.current_color = self.color_inactive

    def update_text(self, new_character=None, delete=False):
        '''Updates the input string when the user types or hits backspace.'''
        if self.active:
            if delete:
                self.input_text = self.input_text[:-1] # Slices off the last character
            elif new_character:
                self.input_text += new_character
            self.prep_placholder_txt()

    def draw(self):
        '''Draws the field and placeholder text to the scene'''
        pygame.draw.rect(self.screen, self.settings.panel_color, self.rect) # draws the field box 
        pygame.draw.rect(self.screen, self.current_color, self.rect, width=2, border_radius=8)
        self.screen.blit(self.text_surface, self.text_rect)

