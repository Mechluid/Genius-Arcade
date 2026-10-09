import pygame
import sys

from settings import Settings
from ball import Ball
from barrier import Barrier
from spike import Spike
from questions import Question
from Input_block import InputBox
from menu_bar import MenuBar
from game_stats import GameStats
from menu_panel import MenuPanel
from heart import Heart
from form_field import FormField
from data_manager import DataManager

class GeniusArcade:
    '''
    Overall class to manage game assets, behavior, and the main run loop.
    This class serves as the central engine for the game. It is responsible 
    for initializing Pygame, configuring the display window, tracking game states, 
    and orchestrating all interactive elements including balls, spikes, UI panels, 
    and player statistics.
    '''
    def __init__(self):
        '''Initialize the game'''
        pygame.init()
        self.initialize_window_properties()
        self.settings = Settings()
        self.data_manager = DataManager()
        self.important_game_flags()
        self.stats = GameStats(self)
        self.create_panel_attribute()
        self.game_entities()
        self.game_time_props()
        self.add_up_balls()
        self.create_spikes()
        self.setup_menu_bar_text()
        self.setup_menu_panel_txt()
        self.setup_login_panel_entities()
        self.setup_reset_panel_entities()
        self.setup_acc_creation_entities()
        self.setup_pause_entities()
        self.setup_game_over_entities()
        self.create_bar()
        self.create_hearts()
        self.create_game_over_txt()
        self.active_user = None

    def initialize_window_properties(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
        self.screen_width, self.screen_height = self.screen.get_rect().size
        self.top_bar_rect = pygame.Rect(0, 0, self.screen_width, 80)
        self.clock = pygame.time.Clock()

    def important_game_flags(self):
        self.game_state = 'login'
        self.start_game = False # Tracks if the game is started (When the gameplay begins)
        self.dropdown_open = False # Tracks if the difficulty list is visible
        self.current_difficulty = 'medium' # Default state difficulty
        self.show_login_error = False # Prompts the user if credentials are invalid
        self.show_reset_error = False 
        # Tracks navigation history for automatic back navigation
        self.state_history = []
        self.reset_phase = 1
        self.create_phase = 1
        self.show_create_error = False

    def game_entities(self):
        self.bars = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.strd_qn = pygame.sprite.Group()
        self.input_elements = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()

    def game_time_props(self):
        self.last_update_time = pygame.time.get_ticks()
        self.qn_update_time = pygame.time.get_ticks()

    def create_panel_attribute(self):
        self.panel_w = self.screen_width * self.settings.panel_width_ratio 
        self.panel_h = self.screen_height // 2 
        self.menu_panel = pygame.Rect(0, 0, self.panel_w, self.panel_h)
        self.menu_panel.centerx = self.screen.get_rect().centerx
        self.menu_panel.top = self.top_bar_rect.bottom

    def create_hearts(self):
        for index in range(self.stats.heart_num):
            heart = Heart(self)
            heart.rect.x = self.heart_level.button_rect.right + (index * heart.rect.width)
            self.hearts.add(heart)

    def setup_menu_bar_text(self):
        display = '--:--'
        self.back_button = MenuBar(self, 'Back', 0, text_spacing=30)
        self.quit_game = MenuBar(self, f'Quit', text_spacing=30, allign_right=True)
        self.pause_button = MenuBar(self, 'Pause', text_spacing=30, allign_right=True)
        self.select_diff = MenuBar(self, f'Difficulty: {display}', self.back_button.rect.right)
        self.score = MenuBar(self, f'Score: {display}', self.select_diff.rect.right)
        self.high_score = MenuBar(self, f'High Score: {display}', self.score.rect.right)
        self.game_round = MenuBar(self, f'round: {display}', self.high_score.rect.right)
        self.remaining_balls = MenuBar(self, f'Balls: {display}', self.game_round.rect.right)
        self.heart_level = MenuBar(self, f'hearts:', self.remaining_balls.rect.right)

    def setup_menu_panel_txt(self):
        header_txt = 'Test Your Maths Knowledge'
        sub_txt = 'Solve Fast. Pop the ball. Beat the Clock.'
        self.header = MenuPanel(self, header_txt, 0.3, font= 'head')
        self.sub = MenuPanel(self, sub_txt, 0.5, font= 'sub')
        self.start = MenuPanel(self, 'Start Game', 0.8, font= 'label', color= 'head')
        self.start.button()
        self.diff_interact = MenuPanel(self, 'Select Difficulty', 0.65, font= 'intrct', color= 'sub')
        self.diff_interact.button()
        self.drop_down_texts()

    def setup_login_panel_entities(self):
        self.login_header = MenuPanel(self, 'Welcome to Genius Arcade', 0.3, font='head')
        self.login_sub = MenuPanel(self, 'Please sign in to save your scores', 0.42, font='sub')
        # FOr the username and password field 
        self.username_field = FormField(self, 'Username', 0.45)
        self.password_field = FormField(self, 'Password', 0.57)
        # Submit field
        self.login_btn = MenuPanel(self, 'Log in', 0.85, font='sub', color='head')
        self.login_btn.button()
        self.login_btn.button_rect.size = self.password_field.rect.size
        self.login_btn.button_rect.center = self.login_btn.rect.center
        # reset_password
        self.reset_pass = MenuPanel(self, 'Forgotten password?', 0.95, font='sub', color='head')
        self.create_acc = MenuPanel(self, 'Create new account', 1.2, font='sub', color='head')
        self.create_acc.button()
        self.create_acc.button_rect.size = self.login_btn.button_rect.size
        self.create_acc.button_rect.center = self.create_acc.rect.center

    def setup_reset_panel_entities(self):
        # Phase 1 Entities
        self.phase1_header = MenuPanel(self, 'Find Your Account', 0.3, font='head')
        self.phase1_sub = MenuPanel(self, 'Enter your username and secret phrase to continue', 0.43, font='sub')
        self.reset_continue_btn = MenuPanel(self, 'Continue', 0.85, font='sub', color='head')
        self.reset_continue_btn.button()
        self.reset_continue_btn.button_rect.size = self.username_field.rect.size
        self.reset_continue_btn.button_rect.center = self.reset_continue_btn.rect.center
        self.secret_phrase_field = FormField(self, 'Secret phrase', 0.57)
        # Phase 2 Entities
        self.phase2_header = MenuPanel(self, 'Reset Password', 0.3, font='head')
        self.phase2_sub = MenuPanel(self, 'Your new password must be at least 6 characters', 0.43, font='sub')
        self.new_password_field = FormField(self, 'New password', 0.45)
        self.confirm_password_field = FormField(self, 'Confirm password', 0.57)
        self.reset_confirm_btn = MenuPanel(self, 'Confirm', 0.85, font='sub', color='head')
        self.reset_confirm_btn.button()
        self.reset_confirm_btn.button_rect.size = self.new_password_field.rect.size
        self.reset_confirm_btn.button_rect.center = self.reset_confirm_btn.rect.center  
        # Phase 3 Entities
        self.phase3_header = MenuPanel(self, 'Password Reset Successful!', 0.35, font='head')
        self.phase3_sub = MenuPanel(self, 'Your account password has been updated. Please log in.', 0.48, font='sub')
        self.reset_to_login_btn = MenuPanel(self, 'Back to Login', 0.72, font='sub', color='head')
        self.reset_to_login_btn.button()
        self.reset_to_login_btn.button_rect.size = self.username_field.rect.size
        self.reset_to_login_btn.button_rect.center = self.reset_to_login_btn.rect.center

    def setup_acc_creation_entities(self):
        # Phase 1 Entities
        # Header & Subtext
        self.create_header = MenuPanel(self, 'Create An Account', 0.2, font='head')
        self.create_sub = MenuPanel(self, 'Fill in your details to get started', 0.3, font='sub')
        # The 4 Dedicated Registration Fields
        self.reg_username_field = FormField(self, 'Username', 0.33)
        self.reg_secret_field = FormField(self, 'Secret phrase (for recovery)', 0.45)
        self.reg_password_field = FormField(self, 'Password (min. 6 chars)', 0.57)
        self.reg_confirm_field = FormField(self, 'Confirm password', 0.69)
        # Confirm / Submit Action Button
        self.create_confirm_btn = MenuPanel(self, 'Create Account', 0.95, font='sub', color='head')
        self.create_confirm_btn.button()
        self.create_confirm_btn.button_rect.size = self.reg_username_field.rect.size
        self.create_confirm_btn.button_rect.center = self.create_confirm_btn.rect.center
        # Phase 2 Entities
        self.create_success_header = MenuPanel(self, 'Account Created!', 0.35, font='head')
        self.create_success_sub = MenuPanel(self, 'Your account is ready. Sign in to start playing!', 0.48, font='sub')
        self.create_to_login_btn = MenuPanel(self, 'Back to Login', 0.72, font='sub', color='head')
        self.create_to_login_btn.button()
        self.create_to_login_btn.button_rect.size = self.reg_username_field.rect.size
        self.create_to_login_btn.button_rect.center = self.create_to_login_btn.rect.center
#TODO: Work on the pasuse sub caption.
    def setup_pause_entities(self):
        # Header & Subtext
        self.pause_header = MenuPanel(self, 'Game Paused', 0.25, font='head')
        self.pause_sub = MenuPanel(self, 'Take a breath. Ready when you are.', 0.35, font='sub')
        
        # The 4 Buttons
        self.pause_resume_btn = MenuPanel(self, 'Resume Game', 0.46, font='sub', color='head')
        self.pause_restart_btn = MenuPanel(self, 'Restart Game', 0.66, font='sub', color='head')
        self.pause_menu_btn = MenuPanel(self, 'Main Menu', 0.86, font='sub', color='head')
        self.pause_quit_btn = MenuPanel(self, 'Quit to Desktop', 1.06, font='sub', color='head')
        
        self.pause_buttons = [
            self.pause_resume_btn, 
            self.pause_restart_btn, 
            self.pause_menu_btn, 
            self.pause_quit_btn
        ]
        # Give all buttons uniform size and alignment
        btn_size = self.login_btn.button_rect.size
        for btn in self.pause_buttons:
            btn.button()
            btn.button_rect.size = btn_size
            btn.button_rect.center = btn.rect.center

    def setup_game_over_entities(self):
        self.play_again = MenuPanel(self, 'Play Again', font='sub', offset_y=0.95, offset_x=0.4, color='head')
        self.play_again.button()
        self.return_to_menu = MenuPanel(self, 'Main-Menu', font='sub', offset_y=0.95, offset_x=0.6, color='head')
        self.return_to_menu.button()

    def drop_down_texts(self):
        '''Customizing the dropdown texts that pop when select difiiculty is clicked'''
        # Getting the width and x postion of the main difficulty button.
        drop_width = self.diff_interact.button_rect.width
        drop_x = self.diff_interact.button_rect.centerx
        gap = 4 # the spacing between the difficulty buttons
        self.opt_easy = MenuPanel(self, 'Easy', 0.65, font='intrct', color='head')
        self.opt_med = MenuPanel(self, 'Medium', 0.65, font='intrct', color='head')
        self.opt_hard = MenuPanel(self, 'Hard', 0.65, font='intrct', color='head')
        self.options = [self.opt_easy, self.opt_med, self.opt_hard]
        for option in self.options:
            option.button()
        self.opt_easy.button_rect.top = self.diff_interact.button_rect.bottom + gap
        self.opt_med.button_rect.top = self.opt_easy.button_rect.bottom + gap
        self.opt_hard.button_rect.top = self.opt_med.button_rect.bottom + gap
        for option in self.options:
            option.button_rect.width = drop_width
            option.button_rect.centerx = drop_x
            option.rect.center = option.button_rect.center

    def go_back(self):
        '''Automatically returns to the previous game state and cleans up state flags.'''
        if self.game_state == 'reset':
            self.show_reset_error = False
            if self.reset_phase == 2:
                # Step back from Phase 2 to Phase 1
                self.reset_phase = 1
                # Clear partially typed passwords
                self.new_password_field.clear_text()
                self.confirm_password_field.clear_text()
            elif self.reset_phase == 1:
                # Exit the reset flow back to login
                self.game_state = 'login'
                self.username_field.clear_text()
                self.secret_phrase_field.clear_text()
        elif self.game_state == 'create':
            self.show_create_error = False
            self.create_phase = 1
            self.game_state = 'login'
            # Wipe the registration fields clean
            self.reg_username_field.clear_text()
            self.reg_secret_field.clear_text()
            self.reg_password_field.clear_text()
            self.reg_confirm_field.clear_text()
        elif self.game_state == 'menu':
            self.username_field.clear_text()
            self.password_field.clear_text()
            self.game_state = 'login'
        elif self.state_history:
            # Changes present state to previous state
            self.game_state = self.state_history.pop()

    def create_game_over_txt(self):
        self.game_over_txt = MenuPanel(self, 'Game Over!!!', font='head', offset_y=0.7)

    def create_spikes(self):
        '''Creates a number of spikes to be used in chain-belt kind of motion'''
        for spike_index in range(-1, self.settings.spike_num + self.settings.smoothness_factor):
            new_spike = Spike(self, spike_index)
            self.spikes.add(new_spike)
    
    def create_bar(self):
        bar = Barrier(self)
        self.bars.add(bar)

    def add_up_balls(self):
        '''Creates a number of x initial balls to start the game'''
        new_ball = Ball(self)
        self.balls.add(new_ball)

    def game_running(self):
        '''Starts the game loop'''
        while True:
            self.current_time = pygame.time.get_ticks()
            self.check_events()
            if self.game_state == 'playing':
                self.timing_balls()
                self.update_entities()
                self.entities_collisions()
                self.update_question()
            self.clock.tick(self.settings.frame)
            self.screen_update()

    def check_events(self):
        '''Check inputs from the user during the gameplay'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Check events during a user's keypress
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif self.game_state == 'playing':
                    if event.unicode.isdigit():
                        pressed_num = str(event.unicode)
                        self.handling_input_element(pressed_num)
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.check_answer()
                        self.finish_game_round()
                    elif event.key == pygame.K_BACKSPACE:
                        if self.input_elements:
                            for input_element in self.input_elements:
                                input_element.remove_text()
                    elif event.key == pygame.K_ESCAPE:
                        self.screen_veil()
                        self.game_state = 'pause'
                elif self.game_state == 'login':
                    # This clears the error message once the keyboard makes an edit
                    if self.show_login_error:
                        self.show_login_error = False
                    if event.key == pygame.K_BACKSPACE:
                        # It send the delete command to both fields, of which can be executed if "active"
                        self.username_field.update_text(delete=True)
                        self.password_field.update_text(delete=True)
                    elif event.key == pygame.K_TAB:
                        # This ignores these keys so they don't print weird block characters
                        pass       
                    elif event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                        self.evaluate_login_entry()
                    else:
                        # event.unicode captures the actual character typed (including uppercase or any character at all) to give 
                        # users flexibility when crafting their credentials
                        self.username_field.update_text(new_character=event.unicode)
                        self.password_field.update_text(new_character=event.unicode)
                elif self.game_state == 'welcome':
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.game_state = 'menu'
                elif self.game_state == 'reset':
                    if self.show_reset_error:
                        self.show_reset_error = False
                    if self.reset_phase == 1:
                        if event.key == pygame.K_BACKSPACE:
                            self.secret_phrase_field.update_text(delete=True)
                            self.username_field.update_text(delete=True)
                        elif event.key == pygame.K_TAB:
                            # This ignores these keys so they don't print weird block characters
                            pass  
                        elif event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                            self.evaluate_reset_phase1_entry()              
                        else:
                            # event.unicode captures the actual character typed (including uppercase)
                            self.secret_phrase_field.update_text(new_character=event.unicode)
                            self.username_field.update_text(new_character=event.unicode)
                    elif self.reset_phase == 2:
                        if event.key == pygame.K_BACKSPACE:
                            self.new_password_field.update_text(delete=True)
                            self.confirm_password_field.update_text(delete=True)
                        elif event.key == pygame.K_TAB:
                            # This ignores these keys so they don't print weird block characters
                            pass 
                        elif event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                            self.evaluate_reset_phase2_entry()  
                        else:
                            self.new_password_field.update_text(new_character=event.unicode)
                            self.confirm_password_field.update_text(new_character=event.unicode)
                elif self.game_state == 'create':
                    if self.show_create_error:
                        self.show_create_error = False
                    if self.create_phase == 1:
                        if event.key == pygame.K_BACKSPACE:
                            self.reg_username_field.update_text(delete=True)
                            self.reg_secret_field.update_text(delete=True)
                            self.reg_password_field.update_text(delete=True)
                            self.reg_confirm_field.update_text(delete=True)
                        elif event.key == pygame.K_TAB:
                            # This ignores these keys so they don't print weird block characters
                            pass           
                        elif event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                            self.evaluate_create_phase1_entry()     
                        else:
                            # event.unicode captures the actual character typed (including uppercase)
                            self.reg_username_field.update_text(new_character=event.unicode)
                            self.reg_secret_field.update_text(new_character=event.unicode)
                            self.reg_password_field.update_text(new_character=event.unicode)
                            self.reg_confirm_field.update_text(new_character=event.unicode)
                elif self.game_state == 'pause':
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = 'playing'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.game_state not in ('welcome', 'game_over', 'playing', 'pause'):
                    if self.quit_game.button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif self.back_button.button_rect.collidepoint(mouse_pos):
                        self.go_back()
                else:
                    self.check_continue_bttn(mouse_pos)
                    self.check_play_again_button(mouse_pos)
                    self.check_main_menu_bttn(mouse_pos)
                if self.game_state == 'menu':
                    self.check_menu_clicks(mouse_pos)
                elif self.game_state == 'login':
                    self.check_login_clicks(mouse_pos)
                elif self.game_state == 'reset':
                    self.check_reset_password_click(mouse_pos)
                elif self.game_state == 'create':
                    self.check_create_account_clicks(mouse_pos)
                elif self.game_state == 'playing':
                    if self.pause_button.button_rect.collidepoint(mouse_pos):
                        self.screen_veil()
                        self.game_state = 'pause'
                elif self.game_state == 'pause':
                     self.check_paused_clicks(mouse_pos)
                        
    def screen_veil(self):
            snapshot = self.screen.copy()
            tiny = pygame.transform.smoothscale(snapshot, (self.screen_width // 10, self.screen_height // 10))
            blurred = pygame.transform.smoothscale(tiny, (self.screen_width, self.screen_height))
            # Create the dark tint overlay (SRCALPHA enables transparency)
            dark_tint = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            dark_tint.fill((0, 0, 0, 160))  # Potrays about 60% black tint
            # THis is to Stamp the dark tint onto the blurred snapshot
            blurred.blit(dark_tint, (0, 0))
            self.blurred_background = blurred

    def trigger_error(self, message, error_type='reset'):
        '''Renders the error surface ONCE when a validation error occurs.'''
        if error_type == 'create':
            self.create_error_surface = self.settings.error_font.render(message, True, (255, 50, 50))
            self.create_error_rect = self.create_error_surface.get_rect()
            self.create_error_rect.bottomleft = (self.reg_username_field.rect.left, self.reg_username_field.rect.top - 5)
            self.show_create_error = True
        elif error_type == 'reset':
            self.reset_error_surface = self.settings.error_font.render(message, True, (255, 50, 50))
            self.reset_error_rect = self.reset_error_surface.get_rect()
            self.reset_error_rect.bottomleft = (self.new_password_field.rect.left, self.new_password_field.rect.top - 5)
            self.show_reset_error = True
        elif error_type == 'login':
            self.login_error_surface = self.settings.error_font.render(message, True, (255, 50, 50))
            self.login_error_rect = self.login_error_surface.get_rect()
            self.login_error_rect.bottomleft = (self.username_field.rect.left, self.username_field.rect.top - 5)
            self.show_login_error = True

    def check_reset_password_click(self, mouse_pos):
        # Update field color when they are clicked
        if self.reset_phase == 1:
            self.secret_phrase_field.update_active_state(mouse_pos)
            self.username_field.update_active_state(mouse_pos)
            if self.reset_continue_btn.button_rect.collidepoint(mouse_pos):
                self.evaluate_reset_phase1_entry()
        elif self.reset_phase == 2:
            self.new_password_field.update_active_state(mouse_pos)
            self.confirm_password_field.update_active_state(mouse_pos)
            # Ensures a minimum password character length
            if self.confirm_password_field.rect.collidepoint(mouse_pos):
                if len(self.new_password_field.input_text) < 6:
                    self.trigger_error("Password must be at least 6 characters!")
                else:
                    self.show_reset_error = False
            if self.reset_confirm_btn.button_rect.collidepoint(mouse_pos):
                self.evaluate_reset_phase2_entry()
        elif self.reset_phase == 3:
            if self.reset_to_login_btn.button_rect.collidepoint(mouse_pos):
                self.show_reset_error = False
                self.game_state = 'login'
                self.show_login_error = False
                # Reset state flags incase of future visits.
                self.reset_phase = 1
                self.reset_target_user = None
                # Wipes all field completely
                self.username_field.clear_text()
                self.password_field.clear_text()
                self.secret_phrase_field.clear_text()
                self.new_password_field.clear_text()
                self.confirm_password_field.clear_text()

    def evaluate_reset_phase1_entry(self):
        # Grabbing the user typed text to be used for comparison
        entered_user = self.username_field.input_text
        entered_secret = self.secret_phrase_field.input_text
        # Saving the current user, so every other details of the user synces automatically 
        self.evaluation = self.data_manager.reset_password(entered_user, entered_secret)
        if self.evaluation == 'success':
            self.reset_target_user = entered_user
            self.reset_phase = 2
            self.show_reset_error = False
        elif self.evaluation == 'wrong_secret':
            self.trigger_error("secret phrase is not valid, try again!")
        elif self.evaluation == 'user_not_found':
            self.trigger_error("Username is not found, try again!")

    def evaluate_reset_phase2_entry(self):
        new_pass = self.new_password_field.input_text
        confirm_pass = self.confirm_password_field.input_text
        current_password = self.data_manager.users[self.reset_target_user]['password']
        # Minimum length check
        if len(new_pass) < 6:
            self.trigger_error("Password must be at least 6 characters!")
        # Old password re-use check
        elif new_pass == current_password:
            self.trigger_error("New password cannot be same as old password!")
        # Confirmation match check
        elif new_pass != confirm_pass:
            self.trigger_error("Passwords do not match!")
        # If conditions met successful upon clciking on the confirm button
        else:
            self.data_manager.update_user_password(self.reset_target_user, new_pass)
            self.show_reset_error = False
            self.reset_phase = 3

    def check_create_account_clicks(self, mouse_pos):
        if self.create_phase == 1:
            self.reg_username_field.update_active_state(mouse_pos)
            self.reg_secret_field.update_active_state(mouse_pos)
            self.reg_password_field.update_active_state(mouse_pos)
            self.reg_confirm_field.update_active_state(mouse_pos)
            if self.create_confirm_btn.button_rect.collidepoint(mouse_pos):
               self.evaluate_create_phase1_entry()
        elif self.create_phase == 2:
            if self.create_to_login_btn.button_rect.collidepoint(mouse_pos):
                self.game_state = 'login'
                self.create_phase = 1
                self.show_create_error = False
                self.reg_username_field.clear_text()
                self.reg_secret_field.clear_text()
                self.reg_password_field.clear_text()
                self.reg_confirm_field.clear_text()
                self.username_field.clear_text()
                self.password_field.clear_text()

    def evaluate_create_phase1_entry(self):
        entered_user = self.reg_username_field.input_text.strip()
        entered_secret = self.reg_secret_field.input_text.strip()
        entered_pass = self.reg_password_field.input_text
        entered_confirm = self.reg_confirm_field.input_text
# Handling the errors to be encountered in this phase, but structured in a sort of hierarchy where erros are given priority
# depending on the situation at that point.
        if not all((entered_user, entered_secret, entered_pass, entered_confirm)):
            # Returns True one of the varaible returns "" or None, meaning each and every form field must be field 
            # before any account creation
            self.trigger_error("All fields are required!", error_type='create')
        elif entered_user in self.data_manager.users: # Prevents username duplicates in the database system.
            self.trigger_error("Username already exists, choose another!", error_type='create')
        elif len(entered_secret) < 3: # Ensures the user types minumum of 3 characters as secret phrase
            self.trigger_error("Secret Phrase must be at least 3 characters!", error_type='create')
        elif len(entered_pass) < 6: # Ensuring the User types minimum of 6 characters as password.
            self.trigger_error("Password must be at least 6 characters!", error_type='create')
        elif entered_pass != entered_confirm: # Ensures the User confirms password correctly.
            self.trigger_error("Passwords do not match!", error_type='create')
        else:
            self.data_manager.add_user(entered_user, entered_pass, entered_secret)
            self.show_create_error = False
            self.create_phase = 2

    def check_login_clicks(self, mouse_pos):
        '''Helps confirm if a user has clicked a field and changes color in respect'''
        self.username_field.update_active_state(mouse_pos)
        self.password_field.update_active_state(mouse_pos)
        if self.login_btn.button_rect.collidepoint(mouse_pos):
            self.evaluate_login_entry()
        if self.reset_pass.rect.collidepoint(mouse_pos):
            self.game_state = 'reset'
            self.reset_phase = 1
            # Clearing the field boxes freshly for next round of action.
            self.username_field.clear_text()
            self.password_field.clear_text()
        if self.create_acc.button_rect.collidepoint(mouse_pos):
            self.game_state = 'create'
            self.create_phase = 1
            self.show_create_error = False
            # Wipe registration fields completely fresh
            self.reg_username_field.clear_text()
            self.reg_secret_field.clear_text()
            self.reg_password_field.clear_text()
            self.reg_confirm_field.clear_text()

    def evaluate_login_entry(self):
        # Grabbing the user typed text to be used for comparison
        entered_username = self.username_field.input_text
        entered_password = self.password_field.input_text
        # Passing the input text inorder to compare against the saved user's details
        if self.data_manager.verify_login(entered_username, entered_password):
            # Saving the current user, so every other details of the user synces automatically 
            self.active_user = entered_username
            # Generate a blurred background for the welcome text to be displayed on after login
            self.screen_veil()
            # Create the continue button to switch game stats from welcome game state to menu state
            self.continue_btn = MenuPanel(self, "Continue", 0, font='intrct', color='head')
            self.continue_btn.button()
            self.continue_btn.button_rect.bottomright = (self.screen_width - 30, self.screen_height - 30)
            self.continue_btn.rect.center = self.continue_btn.button_rect.center

            # If it matches, there is a game state chnage.
            self.game_state = 'welcome'
            self.show_login_error = False
        else:
            # This shows a failure pop up text, showing 'Invalid credentials' prompting the user to check the input text.
            self.trigger_error("Invalid login credentials.", error_type='login')

    def check_paused_clicks(self, mouse_pos):
        # When paused:
        if self.pause_resume_btn.button_rect.collidepoint(mouse_pos):
            self.game_state = 'playing'
        elif self.pause_restart_btn.button_rect.collidepoint(mouse_pos):
            self.game_state = 'playing'
            self.previous_best = self.stats.get_current_high_score() # Capture the previous best score before the user plays again
            self.reset_game_entities() # This reset a bar not moving, will comeback to it
            self.update_ball_elements()
            self.stats.reset_stats()
            self.setting_game_stats()
            if not self.bars:
                self.create_bar()
            self.get_ball_count()
        elif self.pause_menu_btn.button_rect.collidepoint(mouse_pos):
            self.reset_game_entities() 
            self.stats.reset_stats()
            self.game_state = 'menu'
        elif self.pause_quit_btn.button_rect.collidepoint(mouse_pos):
            pygame.quit()
            sys.exit()
                

    def check_dropdown_txts(self, mouse_pos):
        if self.opt_easy.button_rect.collidepoint(mouse_pos):
            self.diff_interact.update('Easy')
            self.current_difficulty = 'easy'
        elif self.opt_med.button_rect.collidepoint(mouse_pos):
            self.diff_interact.update('Medium')
            self.current_difficulty = 'medium'
        elif self.opt_hard.button_rect.collidepoint(mouse_pos):
            self.diff_interact.update('Hard')
            self.current_difficulty = 'hard'

    def check_panel_interact_buttons(self, mouse_pos):
        if self.start.button_rect.collidepoint(mouse_pos):
            self.game_state = 'playing'
            self.check_game_mode_attr()
            self.previous_best = self.stats.get_current_high_score() # Captures the previous best score before the game starts
            self.stats.reset_stats()
            self.setting_game_stats()
            self.reset_game_entities()
            self.update_ball_elements()
            if not self.bars:
                self.create_bar()
        elif self.diff_interact.button_rect.collidepoint(mouse_pos):
            self.dropdown_open = True

    def check_menu_clicks(self, mouse_pos):
        if self.dropdown_open:
            self.check_dropdown_txts(mouse_pos)
            # Close the dropdown regardless of where clicked
            self.dropdown_open = False
        # Dropdown closed
        else:
            self.check_panel_interact_buttons(mouse_pos)

    def check_continue_bttn(self, mouse_pos):
        '''Responsible for switching game state from the welcome screen to the menu game state/screen'''
        if self.continue_btn.button_rect.collidepoint(mouse_pos):
            self.game_state = 'menu'

    def update_ball_elements(self):
        '''Update both actual ball in the group and ball's onscreen text'''
        self.add_up_balls()
        self.update_ball_onscreen()

    def check_answer(self):
        '''Check user answer against stored answer'''
        for question in self.strd_qn:
            for answer in self.input_elements:
                if answer.input == str(question.answer):
                    self.ball_removal()
                    self.stats.score += 50
                    self.stats.update_high_score()
                    self.update_scores_data()
                    self.clear_qn_ans()

    def update_scores_data(self):
        score_msg = f'Score: {self.stats.score}'
        h_score_msg = f'High Score: {self.stats.get_current_high_score()}'
        self.score.update(score_msg)
        self.high_score.update(h_score_msg)
        
    def ball_removal(self):
        for ball in self.balls.sprites():
            ball.kill()
            self.update_ball_onscreen()
            break

    def check_play_again_button(self, mouse_pos):
        play_again_bttn_clicked = self.play_again.button_rect.collidepoint(mouse_pos)
        if play_again_bttn_clicked:
            self.game_state = 'playing'
            self.create_bar()
            self.previous_best = self.stats.get_current_high_score() # Capture the previous best score before the user plays again
            self.reset_game_entities() # This reset a bar not moving, will comeback to it
            self.update_ball_elements()
            self.stats.reset_stats()
            self.setting_game_stats()
            self.get_ball_count()

    def check_main_menu_bttn(self, mouse_pos):
        main_menu_bttn_clicked = self.return_to_menu.button_rect.collidepoint(mouse_pos)
        if main_menu_bttn_clicked:
            self.game_state = 'menu'
            self.reset_menu_displays()

    def reset_menu_displays(self):
        '''Resets the existing menu UI text back to their default states'''
        display = '--:--'
        self.select_diff.update(f'Difficulty: {display}')
        self.score.update(f'Score: {display}')
        self.high_score.update(f'High Score: {display}')
        self.game_round.update(f'round: {display}')
        self.remaining_balls.update(f'balls: {display}')
        self.heart_level.update(f'hearts:')

    def update_ball_onscreen(self):
        msg = f'Balls: {len(self.balls)}'
        self.remaining_balls.update(msg)

    def handling_input_element(self, pressed_num):
        '''Handles the text inputted by the user'''
        for question in self.strd_qn:
            if question.rect.bottom <= question.fixed_pos:
                if not self.input_elements:
                    input_element = InputBox(pressed_num, question, self)
                    self.input_elements.add(input_element)
                else:
                    for input_element in self.input_elements:
                        input_element.add_text(pressed_num)

    def setting_game_stats(self):
        display = 0
        self.score.update(f'Score: {display}')
        self.game_round.update(f'round: {self.stats.game_round}')
        self.high_score.update(f'high score: {self.stats.get_current_high_score()}')

    def timing_balls(self):
        '''
        Adds up more balls within a set interval till it reaches the allowable number of balls in a round
        '''
        if not self.start_game:
            if ((self.current_time - self.last_update_time) >= self.settings.ball_delay_ms
                and len(self.balls) < self.settings.ball_count):
                self.update_ball_elements()
                self.last_update_time = self.current_time
            self.game_ready()

    def check_game_mode_attr(self):
        if self.current_difficulty == 'easy':
            self.added_balls, self.bar_start_speed = self.settings.game_mode_attr['easy']
            game_mode_txt = f'Difficulty: Easy'
        elif self.current_difficulty == 'medium':
            self.added_balls, self.bar_start_speed = self.settings.game_mode_attr['medium']
            game_mode_txt = f'Difficulty: Medium'
        elif self.current_difficulty == 'hard':
            self.added_balls, self.bar_start_speed = self.settings.game_mode_attr['hard']
            game_mode_txt = f'Difficulty: Hard'
        self.select_diff.update(game_mode_txt)

    def game_ready(self):
            '''This starts the game (Spawning of the questions the user has to answer)'''
            if len(self.balls) >= self.settings.ball_count and not self.start_game:
                self.start_game = True
                self.change_bar_speed()
                self.qn_update_time = self.current_time

    def update_entities(self):
        '''Handles the update of the game elements'''
        for unique_ball in self.balls:
            unique_ball.update()
        self.check_ball_collisions()
        self.update_spikes()
        self.update_bar()

    def update_bar(self):
        '''Handle the movement of the bar trapping the balls'''
        if self.start_game:
            for bar in self.bars.copy():
                bar.update(self.current_bar_speed)

    def change_bar_speed(self, change_factor = None):
        if not change_factor:
            self.current_bar_speed = self.bar_start_speed
        else:
            self.current_bar_speed *= (1 + self.settings.failure_factor)

    def update_spikes(self):
        '''
        Handles the horizontal movement of the spike which ensures a chain like movement
        '''
        for spike in self.spikes.sprites():
            spike.update()
        self.check_spike()

    def check_spike(self):
        '''
        Checks for spikes reaching the right end of the scrren and removes it onces it passes, adding
        a new one simultaneously at a position before the first visible spike at the scrren extreme left 
        '''
        for spike in self.spikes.copy():
            if spike.points[1][0] >= self.screen_width:
                self.spikes.remove(spike)

        if len(self.spikes) < (self.settings.spike_num + self.settings.smoothness_factor):
            new_spike = Spike(self, -1)
            self.spikes.add(new_spike)

    def check_ball_collisions(self):
        '''Handles the collision between two balls in contact'''
        collisions = pygame.sprite.groupcollide(self.balls, self.balls, False, False)
        for ball, others in collisions.items():
            for other in others:
                if ball != other:
                    ball.dx, other.dx = other.dx, ball.dx
                    ball.dy, other.dy = other.dy, ball.dy

    def entities_collisions(self):
        '''Handles the collision between game entities'''
        for spike in self.spikes:
            for bar in self.bars:
                if bar.rect.bottom >= spike.rect.top:
                    bar.kill()

            for ball in self.balls:
                if ball.rect.bottom >= spike.rect.top:
                    ball.kill()
                    self.update_ball_onscreen()

        if not self.bars and not self.balls:
            self.stats.heart_num -= 1
            if self.stats.heart_num <= 0:
                self.screen_veil()
                self.game_state = 'game_over'
                self.end_game_texts()
            else:
                self.create_bar()
                self.reset_game_entities() # This reset a bar not moving, will comeback to it
                self.update_ball_elements()
                self.get_ball_count()

    def end_game_texts(self):
        if self.stats.score > self.previous_best:
            result_text = 'New high score reached!!!'
        else:
            result_text = 'Keep Praticing'
        self.result = MenuPanel(self, result_text, font='head', offset_y=0.8)

    def update_question(self):
        '''Handles the rendering and positioning of the question on the screen'''
        if self.start_game and self.bars:
            if not self.strd_qn:
                new_qn = Question(self, 1, 10)
                self.strd_qn.add(new_qn)
            self.strd_qn.update()

            if (self.current_time - self.qn_update_time) >= self.settings.txt_delay_ms:
                self.clear_qn_ans()
                self.change_bar_speed('failure')

    def clear_qn_ans(self):
        '''Clears out both the question and answer text displayed on the screen'''
        self.strd_qn.empty()
        self.input_elements.empty()
        self.qn_update_time = self.current_time

    def clear_game_elements(self):
        self.clear_qn_ans()
        self.balls.empty()
        self.last_update_time = self.current_time

    def finish_game_round(self):
        if not self.balls:
            self.stats.game_round += 1
            self.reset_game_entities()
            self.get_ball_count()
            self.game_round.update(f'round: {self.stats.game_round}')
            self.update_ball_elements()
            self.change_bar_speed()

    def get_ball_count(self):
        '''To get ball count for a particular round'''
        previous_round = self.stats.game_round - 1
        self.settings.ball_count += (previous_round * self.added_balls)

    def reset_game_entities(self):
        if self.start_game:
            self.start_game = False
        for bar in self.bars:
            bar.reset()
        self.settings.intitalize_dynamic_settings()
        self.clear_game_elements()

    def background_color_fill(self):
        self.screen.fill(self.settings.screen_bottom_color)
        self.screen.fill(self.settings.screen_top_color, self.top_bar_rect)
        self.select_diff.show_text()
        self.score.show_text()
        self.high_score.show_text()
        self.game_round.show_text()
        self.heart_level.show_text()
        self.remaining_balls.show_text()

    def draw_countdown_timer(self):
        if not self.start_game:
            balls_left = self.settings.ball_count - len(self.balls)
            if balls_left > 0:
                # Triggers at 30%, but guarantees a minimum of 4 balls so 3, 2, 1, and GO all display
                trigger_threshold = max(4, self.settings.ball_count * 0.30)
                if balls_left <= trigger_threshold:
                    # DImming the screen
                    overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 150))
                    self.screen.blit(overlay, (0, 0))
                    # splitting the threshold into perfect quarters
                    for multiplier, displayed_txt, text_color in self.settings.countdown_phases:
                        if balls_left > trigger_threshold * multiplier:
                            break
                    # Drawing the text over the overlay
                    text_surface = self.settings.count_down_font.render(displayed_txt, True, text_color)
                    text_rect = text_surface.get_rect(center = self.screen.get_rect().center)
                    self.screen.blit(text_surface, text_rect)

    def draw_panel_txts(self):
        self.screen.fill(self.settings.panel_color, self.menu_panel)
        color = self.settings.panel_border_color
        p = self.menu_panel
        t = 2  # the 2 = border thickness, outline only
        pygame.draw.line(self.screen, color, p.topleft, p.bottomleft, t) # Left
        pygame.draw.line(self.screen, color, p.topright, p.bottomright, t) # right
        pygame.draw.line(self.screen, color, p.bottomleft,p.bottomright, t)  # bottom
        self.header.show_text()
        self.sub.show_text()
        self.start.draw_button()
        self.start.show_text()
        self.diff_interact.draw_button()
        self.diff_interact.show_text()

    def draw_game_entities(self):
        for ball in self.balls:
            ball.draw()
        for bar in self.bars:
            bar.draw()
        if self.bars:
            for qn in self.strd_qn:
                qn.show()
            for element in self.input_elements:
                element.show()
        for spike in self.spikes:
            spike.draw()
        for index, heart in enumerate(sorted(self.hearts, key=lambda h: h.rect.x)):
            if index < self.stats.heart_num:
                heart.draw()

    def draw_game_over_txts(self):
        self.screen.blit(self.blurred_background, (0, 0))
        self.game_over_txt.show_text()
        self.result.show_text()
        self.play_again.draw_button()
        self.play_again.show_text()
        self.return_to_menu.draw_button()
        self.return_to_menu.show_text()

    def draw_login_texts(self):
        self.login_header.show_text()
        self.login_sub.show_text()
        self.username_field.draw()
        self.password_field.draw()
        self.login_btn.draw_button()
        self.login_btn.show_text()
        self.reset_pass.show_text()
        self.create_acc.draw_button()
        self.create_acc.show_text()

    def draw_welcome_dashboard(self):
        # Renders the welcome text on top of the blurred background
        welcome_txt = f"Welcome back, {self.active_user.title()}!"
        txt_color = self.settings.count_down_font_color
        text_surface = self.settings.welcome_txt_font.render(welcome_txt, True, txt_color)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, (self.screen_height // 3 - 20)))
        self.screen.blit(text_surface, text_rect)
        # Subtext
        sub_txt = "Let's pick up where you left off..." 
        sub_surf = self.settings.stats_font.render(sub_txt, True, (180, 220, 255))
        sub_rect = sub_surf.get_rect(center=(self.screen_width // 2, (self.screen_height // 3 + 50)))
        self.screen.blit(sub_surf, sub_rect)
        # Drawing player last saved stats on the welcome back screen.
        modes = ["easy", "medium", "hard"]
        x_positions = [self.screen_width // 5, self.screen_width // 2, (self.screen_width * 4 // 5)]
        base_y = self.screen_height // 2 + 20
        for i, mode in enumerate(modes):
            # Draws the mode title, putting the stats in its column
            mode_surf = self.settings.stats_font.render(mode.title(), True, (200, 200, 200)) # Slightly dimmed color
            mode_rect = mode_surf.get_rect(center=(x_positions[i], base_y)) 
            self.screen.blit(mode_surf, mode_rect)
            
            # Draw Highest Score for the mode column
            score_surf = self.settings.stats_font.render(f"Highest score - {self.stats.get_current_high_score(mode)}", True, (255, 255, 255))
            score_rect = score_surf.get_rect(center=(x_positions[i], base_y + 80))
            self.screen.blit(score_surf, score_rect)

    def draw_welcome_state(self):
         # Draws the blurred background
        self.screen.blit(self.blurred_background, (0, 0))
        self.draw_welcome_dashboard()
        self.continue_btn.draw_button()
        self.continue_btn.show_text()

    def draw_pause_menu(self):
        self.pause_header.show_text()
        self.pause_sub.show_text()
        for bttns in self.pause_buttons:
            bttns.draw_button()
            bttns.show_text()

    def draw_pause_state(self):
        self.screen.blit(self.blurred_background, (0, 0))
        self.draw_pause_menu()

    def screen_update(self):
        '''Updates screen changes after each loop'''
        if self.game_state not in ('login','reset','create'):
            self.background_color_fill()
        else:
            self.screen.fill(self.settings.screen_bottom_color)
        if self.game_state == 'login':
            # Draws the error once the flag is True
            if self.show_login_error:
                self.screen.blit(self.login_error_surface, self.login_error_rect)
            self.draw_login_texts()
        elif self.game_state == 'create':
            if self.show_create_error:
                self.screen.blit(self.create_error_surface, self.create_error_rect)
            # Regustration form
            if self.create_phase == 1:
                self.create_header.show_text()
                self.create_sub.show_text()
                self.reg_username_field.draw()
                self.reg_secret_field.draw()
                self.reg_password_field.draw()
                self.reg_confirm_field.draw()
                self.create_confirm_btn.draw_button()
                self.create_confirm_btn.show_text()
            elif self.create_phase == 2:
                self.create_success_header.show_text()
                self.create_success_sub.show_text()
                self.create_to_login_btn.draw_button()
                self.create_to_login_btn.show_text()
        elif self.game_state == 'reset':
            if self.show_reset_error:
                self.screen.blit(self.reset_error_surface, self.reset_error_rect)
            if self.reset_phase == 1:
                self.username_field.draw()
                self.secret_phrase_field.draw()
                self.phase1_header.show_text()
                self.phase1_sub.show_text()
                self.reset_continue_btn.draw_button()
                self.reset_continue_btn.show_text()
            elif self.reset_phase == 2:
                self.phase2_header.show_text()
                self.phase2_sub.show_text()
                self.new_password_field.draw()
                self.confirm_password_field.draw()
                self.reset_confirm_btn.draw_button()
                self.reset_confirm_btn.show_text()
            elif self.reset_phase == 3:
                self.phase3_header.show_text()
                self.phase3_sub.show_text()
                self.reset_to_login_btn.draw_button()
                self.reset_to_login_btn.show_text()
        elif self.game_state == 'welcome':
            self.draw_welcome_state()
        elif self.game_state == 'menu':
            self.draw_panel_txts()
            # DROPDOWN TEXTS
            if self.dropdown_open:
                dropdown_height = self.opt_hard.button_rect.bottom - self.opt_easy.button_rect.top
                # A solid color for the ddifficulty buttons to stay on.
                dropdown_bg = pygame.Rect(
                    self.opt_easy.button_rect.left, 
                    self.opt_easy.button_rect.top, 
                    self.opt_easy.button_rect.width, 
                    dropdown_height
                ) # Drawing the background rectangle , pygame.rect(x,y,width, height)
                pygame.draw.rect(self.screen, self.settings.panel_color, dropdown_bg)
                button_border = self.settings.panel_border_color
                for option in [self.opt_easy, self.opt_med, self.opt_hard]:
                    option.draw_button(self.settings.panel_color)
                    pygame.draw.rect(self.screen, button_border, option.button_rect, width=2, border_radius=8)
                    option.show_text()     
        elif self.game_state == 'playing':
            self.pause_button.show_text()
            self.draw_game_entities()
            self.draw_countdown_timer()
        elif self.game_state == 'pause':
            self.draw_pause_state()
        elif self.game_state == 'game_over':
            self.draw_game_over_txts()
        if self.game_state in ('welcome', 'game_over', 'playing', 'pause'):
            pass
        else:
            self.quit_game.show_text()
        if self.game_state == 'reset' and self.reset_phase == 3:
            pass
        elif self.game_state == 'create' and self.create_phase == 2:
            pass
        elif self.game_state in ('welcome', 'game_over', 'playing', 'pause'):
            pass
        else:
            self.back_button.show_text()
        pygame.display.flip()

# To call the method to run the game without the code loosely placed.
if __name__ == '__main__':
    arcade_game = GeniusArcade()
    arcade_game.game_running()