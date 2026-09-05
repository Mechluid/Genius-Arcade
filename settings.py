import pygame

class Settings:
    '''Stores the game settings'''
    def __init__(self):
        '''handles the variables to alter/change the behavior of the game'''
        # Screen
        self.frame = 60
        self.screen_bottom_color = (30, 34, 42) # Background bottom color 
        self.screen_top_color = (40, 44, 54) # Background top color
        self.panel_width_ratio = 0.4
        self.panel_color = (52, 58, 68)
        self.panel_border_color = (95, 194, 232)

        # Ball
        self.ball_radius = 60 
        self.added_ball_easy = 2 # Added ball per round
        self.added_ball_medium = 4
        self.added_ball_hard = 6
        self.a_y = 0.1 # The change in ball's velocity with time in y axis
        self.a_x = 0.3 # The chnage in ball's velocity with time in x axis
        self.ball_delay_ms = 500 # 0.5ms

        # Bar
        self.bar_color = (0, 212, 175)
        self.bar_start_speed_easy = 0.2
        self.bar_start_speed_medium = 0.3
        self.bar_start_speed_hard = 0.4
        self.speed_increase = 0.1 # 10% increase per round

        # Bar speed Factors
        self.failure_factor = 0.02 # 2% increase in speed each time a question goes unanswered

        # Spike
        self.spike_color = (253, 184, 19)
        self.spike_num = 15
        self.spike_height = 60
        self.spike_speed = 1
        self.smoothness_factor = 1 # To ensure smooth chain of spike movvement, filling up the gap created
        # by the removal of a spike instance.
        self.intitalize_dynamic_settings()

        # Text
        self.text_color = (230, 230, 235)
        # Using a monospaced technical font for the math/HUD
        self.text_font = pygame.font.SysFont('consolas', 48, bold=True)
        self.bar_txt_font = pygame.font.SysFont('consolas', 28, bold=True)
        self.panel_head_font = pygame.font.SysFont('trebuchetms', 60, bold= True)
        self.panel_sub_font = pygame.font.SysFont('trebuchetms', 35)
        self.panel_label_font = pygame.font.SysFont('trebuchetms', 50, bold= True)
        self.panel_intrct_font = pygame.font.SysFont('trebuchetms', 28, bold= True)
        self.panel_head_color = (255, 255, 255)
        self.panel_sub_color = (210, 215, 225)
        self.txt_delay_ms = 5000 # 5ms

        # Game Over font setting
        self.game_over_main = pygame.font.SysFont('trebuchetms', 90, bold= True)
        self.game_over_sub = pygame.font.SysFont('trebuchetms', 50, bold= True)
        self.game_over_label = pygame.font.SysFont('trebuchetms', 50, bold= True)
        self.g_o_txt_color = (0, 0, 0)
        self.g_o_button_color = (230, 230, 235)
        self.game_over_font = {'main': self.game_over_main, 'sub': self.game_over_sub, 'label': self.game_over_label}
        self.game_over_txt_color = {'main': self.text_color, 'sub' : self.text_color, 'label': self.g_o_txt_color}
        self.game_over_bckg_color = {'main': self.panel_border_color, 'sub': self.panel_border_color, 'label': self.g_o_button_color}
        self.g_o_txt_color = (0, 0, 0)
        
        # Font Panel Settings (Subset of Text)
        self.font_size = {'head' : self.panel_head_font, 'sub' : self.panel_sub_font, 'label': self.panel_label_font, 'intrct': self.panel_intrct_font}
        self.font_color = {'head' : self.panel_head_color, 'sub' : self.panel_sub_color, 'label': self.panel_border_color, 'intrct': self.panel_head_color}

        # Button (Subset of Text)
        self.button_padding = 20
        self.button_color = (0, 212, 175)
        self.button_border_color = (95, 194, 232)
        self.button_width = 350

        # Question (Subset of Text)
        self.qn_distance = 100 # Distance of the question from the bottom of the screen
        self.stealth_factor = 50 # this factor hides the message or equation once created before update method is called
        # to bring it visibly on the screen
        
        # Answer (Subset of Text)
        self.answer_x_offset = 50   # how far along the line the typed answer starts
        self.answer_y_offset = 7     # nudge so the answer sits ON the line, not above it

        # countdown
        self.count_down_font = pygame.font.SysFont('impact', 300)
        self.count_down_font_color = (255, 255, 255)

        # Login_placeholder_text properties
        self.placeholder_font = pygame.font.SysFont(None, 36)

        # COuntdown_phases
        # Define the phases: (multiplier, displayed_text, font color)
        self.countdown_phases = [
                            (0.75, "3", self.count_down_font_color),
                            (0.50, "2", self.count_down_font_color),
                            (0.25, "1", self.count_down_font_color),
                            (0.00, "GO!", (0, 255, 0))]

        self.game_mode_attr = {'easy':[self.added_ball_easy, self.bar_start_speed_easy],
                               'medium':[self.added_ball_medium, self.bar_start_speed_medium],
                               'hard':[self.added_ball_hard, self.bar_start_speed_hard]}

    def intitalize_dynamic_settings(self):
        self.ball_count = 5 # The amount of balls in a round