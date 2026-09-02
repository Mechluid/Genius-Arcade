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
from game_over import GameOver

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
        self.important_game_flags()
        self.stats = GameStats(self)
        self.create_panel_attribute()
        self.game_entities()
        self.game_time_props()
        self.add_up_balls()
        self.create_spikes()
        self.setup_menu_bar_text()
        self.setup_menu_panel_txt()
        self.create_bar()
        self.create_hearts()
        self.create_game_over_panel()
        self.create_game_over_txt()
        self.display_game_over_exits()

    def initialize_window_properties(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
        self.screen_width, self.screen_height = self.screen.get_rect().size
        self.top_bar_rect = pygame.Rect(0, 0, self.screen_width, 80)
        self.clock = pygame.time.Clock()

    def important_game_flags(self):
        self.launched_game = False
        self.start_game = False
        self.end_game = False

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
        self.game_update_time = pygame.time.get_ticks()

    def create_panel_attribute(self):
        self.panel_w = self.screen_width * self.settings.panel_width_ratio 
        self.panel_h = self.screen_height // 2 
        self.menu_panel = pygame.Rect(0, 0, self.panel_w, self.panel_h)
        self.menu_panel.centerx = self.screen.get_rect().centerx
        self.menu_panel.top = self.top_bar_rect.bottom

    def create_game_over_panel(self):
        self.g_o_panel_width = self.screen_width
        self.g_o_panel_height = self.panel_h * 0.5
        self.g_o_panel = pygame.Rect(0, 0, self.g_o_panel_width, self.g_o_panel_height)
        self.g_o_panel.center = self.screen.get_rect().center

    def create_hearts(self):
        for index in range(self.stats.heart_num):
            heart = Heart(self)
            heart.rect.x = self.heart_level.button_rect.right + (index * heart.rect.width)
            self.hearts.add(heart)

    def setup_menu_bar_text(self):
        display = '--:--'
        self.select_diff = MenuBar(self, f'Difficulty: {display}', 0.025)
        self.how_to_play = MenuBar(self, 'How to Play?', 0.167)
        self.score = MenuBar(self, f'Score: {display}', 0.309)
        self.high_score = MenuBar(self, f'High Score: {display}', 0.451)
        self.game_round = MenuBar(self, f'round: {display}', 0.593)
        self.remaining_balls = MenuBar(self, f'Balls: {display}', 0.735)
        self.heart_level = MenuBar(self, f'hearts:', 0.875)

    def setup_menu_panel_txt(self):
        if not self.launched_game:
            header_txt = 'Test Your Maths Knowledge'
            sub_txt = 'Solve Fast. Pop the ball. Beat the Clock.'
            self.header = MenuPanel(self, header_txt, 0.3, font= 'head')
            self.sub = MenuPanel(self, sub_txt, 0.5, font= 'sub')
            self.start = MenuPanel(self, 'Start Game', 0.8, font= 'label', color= 'head')
            self.start.button()
            self.diff_interact = MenuPanel(self, 'Select Difficulty', 0.65, font= 'intrct', color= 'sub')
            self.diff_interact.button()

    def create_game_over_txt(self):
        self.game_over_txt = GameOver(self, 'Game Over!!!', 0.5, 'main')

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
            if self.launched_game and not self.end_game:
                self.timing_balls()
                self.update_entities()
                self.entities_collisions()
                self.update_question()
            elif self.end_game:
                self.update_game_over_txt()
            self.clock.tick(self.settings.frame)
            self.screen_update()

    def check_events(self):
        '''Check inputs from the user during the gameplay'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.key_down_button(event)
            elif event.type == pygame.KEYUP:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not self.launched_game:
                    self.check_start_game_button(mouse_pos)
                else:
                    self.check_play_again_button(mouse_pos)
                    self.check_main_menu_bttn(mouse_pos)

    def check_start_game_button(self, mouse_pos):
        start_button_clicked = self.start.button_rect.collidepoint(mouse_pos)
        if start_button_clicked and not self.launched_game:
            self.launched_game = True
            self.stats.reset_stats()
            self.setting_game_stats()
            self.reset_game_entities()
            self.update_ball_elements()
            if not self.bars:
                self.create_bar()

    def update_ball_elements(self):
        '''Update both actual ball in the group and ball's onscreen text'''
        self.add_up_balls()
        self.update_ball_onscreen()

    def key_down_button(self, event):
        '''Check events during a user's keypress'''
        if event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        elif self.launched_game:
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
        h_score_msg = f'High Score: {self.stats.high_score}'
        self.score.update(score_msg)
        self.high_score.update(h_score_msg)
        
    def ball_removal(self):
        for ball in self.balls.sprites():
            ball.kill()
            self.update_ball_onscreen()
            break

    def check_play_again_button(self, mouse_pos):
        play_again_bttn_clicked = self.play_again.button_rect.collidepoint(mouse_pos)
        if play_again_bttn_clicked and self.end_game:
            self.end_game = False
            self.create_bar()
            self.reset_game_entities() # This reset a bar not moving, will comeback to it
            self.update_ball_elements()
            self.stats.reset_stats()
            self.setting_game_stats()
            self.get_ball_count()

    def check_main_menu_bttn(self, mouse_pos):
        main_menu_bttn_clicked = self.return_to_menu.button_rect.collidepoint(mouse_pos)
        if main_menu_bttn_clicked and self.end_game:
            self.launched_game = False
            self.end_game = False
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
        self.high_score.update(f'high score: {self.stats.high_score}')

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

    def game_ready(self):
            '''This starts the game (Spawning of the questions the user has to answer)'''
            if len(self.balls) >= self.settings.ball_count and not self.start_game:
                self.start_game = True
                self.change_bar_speed()
                self.previous_best = self.stats.high_score
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

# TODO: 
    def change_bar_speed(self, change_factor = None):
        if not change_factor:
            self.current_bar_speed = self.settings.bar_start_speed
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

        if not self.bars and not self.balls:
            self.stats.heart_num -= 1
            if self.stats.heart_num <= 0:
                self.end_game = True
                self.game_update_time = self.current_time
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
        self.result = GameOver(self, result_text, 0.42, 'sub')

    def display_game_over_exits(self):
        self.play_again = GameOver(self, 'Play Again', 0.6, 'label', 0.3)
        self.play_again.button()
        self.return_to_menu = GameOver(self, 'Main-Menu', 0.6, 'label', 0.7)
        self.return_to_menu.button()

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

    def update_game_over_txt(self):
        self.game_over_txt.update(0.5)
        self.result.update(0.5)

    def clear_qn_ans(self):
        '''Clears out both the question and answer text displayed on the screen'''
        self.strd_qn.empty()
        self.input_elements.empty()
        self.qn_update_time = self.current_time

    def clear_game_elements(self):
        self.clear_qn_ans()
        self.balls.empty()
        self.last_update_time = self.current_time

# TODO: Working on editing this  method to adjust the bar speed for the next round
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
        self.settings.ball_count += (previous_round * self.settings.added_ball)

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
        self.how_to_play.show_text()
        self.score.show_text()
        self.high_score.show_text()
        self.game_round.show_text()
        self.heart_level.show_text()
        self.remaining_balls.show_text()

    def countdown_timer(self):
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

    def screen_update(self):
        '''Updates screeen changes after each loop'''
        self.background_color_fill()
        if not self.end_game:
            if self.launched_game:
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
                self.countdown_timer()
            else:
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
        else:
            self.screen.fill(self.settings.panel_border_color, self.g_o_panel)
            self.game_over_txt.show_text()
            self.result.show_text()
            self.play_again.draw_button()
            self.play_again.show_text()
            self.return_to_menu.draw_button()
            self.return_to_menu.show_text()
        pygame.display.flip()

# To call the method to run the game without the code loosely placed.
if __name__ == '__main__':
    arcade_game = GeniusArcade()
    arcade_game.game_running()