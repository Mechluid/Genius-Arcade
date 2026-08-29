import pygame
from pygame.sprite import Sprite
import random
import math
from pathlib import Path

class Ball(Sprite):
    """Initailize the ball's property and handles the motion"""
    def __init__(self, game_instance):
        super().__init__()
        self.screen = game_instance.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game_instance.settings
        self.bars = game_instance.bars
        self.top_frame = game_instance.top_bar_rect
        self.get_ball_image()
        # Ball postioning and precise motioning
        self.rect.x = (self.rect.width / 2)
        self.rect.y = self.top_frame.bottom
        self.x = float(self.rect.x) # For precise postioning of the ball when influenced by a given parameter
        self.y = float(self.rect.y) 
        self.ball_initial_parameters()
        # Impulse
        # This ensures the ball covers the maximum/required distance to another frame when it bounces off a frame
        self.impulse_x = (self.screen_rect.width * 0.8) / self.settings.frame # The impulse after a bounce on an horizontal axis.
        # Kinematics had to be involved to calculate the impulse but under the influence of gravity, that was why the accerelation
        # due to gravity and height were included, formular;  V = sqrt(2 * g * h)
        self.impulse_y = math.sqrt(2 * self.settings.a_y * self.screen_rect.height) # The impulse after a bounce on an horizontal axis.
        self.launched = False # To ensure new balls move horizontally and reaches the right frame before bouncing off
        self.bounced_this_frame = False # This is to avoid movement glitch when two frames' movement condition gets activated simultaneously.

    def ball_initial_parameters(self):
        self.dy = 0 # Velocity at rest in the y direction
        self.dx = 0 # Velocity at rest in the x 

    def get_ball_image(self):
        '''Used to get the ball image to be displayed on the screen'''
        image_path = Path(__file__).parent/ 'ball.bmp'
        self.ball_image = pygame.image.load(image_path)
        self.ball_diameter = 2 * self.settings.ball_radius # modifying the ball shape to better suit the game aesthetics
        self.scaled_ball_size = (self.ball_diameter, self.settings.ball_radius)
        self.ball_scaled_image = pygame.transform.smoothscale(self.ball_image, self.scaled_ball_size)
        self.rect = self.ball_scaled_image.get_rect()

    def update(self):
        '''Update in the ball's position when the game loop runs'''
        self.bounced_this_frame = False # TO avoid a glitch where the ball bounces in two different sides in one frame
        self._ball_vertical_movement()
        self._ball_horizontal_movement()

    def _ball_vertical_movement(self):
        '''Handles the vertical movement of the ball'''
        if self.launched:
            self.y += self.dy # Constant vertical velocity unless acted upon by an external force 
            self.dy += self.settings.a_y # this depicts the influence of gravity when the ball is in motion.
            self.rect.y = self.y # keeps the ball image postioning in sync with the influenced ball variable.
            self.check_top_bottom_edges()

    def _ball_horizontal_movement(self):
        '''Handles the horizontal movement of the ball'''
        self.x += self.dx
        if not self.launched:
            self.dx += self.settings.a_x # Handles the burst accerelation of the ball at the entry
        self.rect.x = self.x
        self.check_right_left_edges()

    def check_top_bottom_edges(self):
        '''Check top and bottom edges, reverse dy and help avoid getting stucked.'''
        for bar in self.bars:
            if self.rect.bottom >= bar.rect.top:
                # Snap to the bar's top edge so it doesn't get stuck to the frame edge
                self.rect.bottom = bar.rect.top
                self.y = float(self.rect.y)
                if not self.bounced_this_frame:
                    self.bounced_this_frame = True # This flag is to ensure the ball has no duplicate 
                    # bouncing off a edge motion in one frame, once true, it doesn't run for the remaining.
                    self.dx = self.impulse_x if random.random() > 0.5 else -self.impulse_x # introduces randomness in the ball's motion
                    self.dy = -self.impulse_y

        if self.rect.top <= self.top_frame.bottom:
            # Snap to ball to the top of the screen incase it movees beyond the wall.
            self.rect.top = self.top_frame.bottom
            self.y = float(self.rect.y)
            if not self.bounced_this_frame:
                self.bounced_this_frame = True
                self.dx = self.impulse_x if random.random() > 0.5 else -self.impulse_x
                self.dy = self.impulse_y 
    
    def check_right_left_edges(self):
        '''Check right and left edges by reversing dx to avoide getting stucked'''
        if self.rect.right >= self.screen_rect.right:
            # Snaps the ball to the screen right edge once the ball reaches the right edge or exceed it.
            self.rect.right = self.screen_rect.right
            self.x = float(self.rect.x)
            if not self.bounced_this_frame:
                self.bounced_this_frame = True
                if not self.launched:
                    self.launched = True
                    self.dy = self.impulse_y
                else:
                    self.dy = self.impulse_y if random.random() > 0.5 else -self.impulse_y 
                self.dx = -self.impulse_x

        elif self.rect.left <= 0:
            # Snaps the ball to the screen left edge once the ball reaches the left edge or exceed it.
            self.rect.left = 0
            self.x = float(self.rect.x)
            if not self.bounced_this_frame:
                self.bounced_this_frame = True
                self.dy = self.impulse_y if random.random() > 0.5 else -self.impulse_y 
                self.dx = self.impulse_x
    
    def __repr__(self):
        '''for easy debug of the ball's motion'''
        return (f' Ball: x = {self.rect.x }, y = {self.rect.y}')

    def draw(self):
        '''To draw the ball on the shared screen'''
        self.screen.blit(self.ball_scaled_image, self.rect)