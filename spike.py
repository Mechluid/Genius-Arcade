import pygame
from pygame.sprite import Sprite
import pygame.gfxdraw

class Spike(Sprite):
    def __init__(self, game_instamce, spike_index ):
        super().__init__()
        self.screen = game_instamce.screen
        self.settings = game_instamce.settings
        self.screen_width, self.screen_height = game_instamce.screen_width, game_instamce.screen_height
        self.width = (self.screen_width / self.settings.spike_num)
        self.x_conditioning = self.width * spike_index
        # X and Y co-ordinate of the spike (Where the image start from both directions respectively)
        self.x_coor, self.y_coor = self.x_conditioning, (self.screen_height - self.settings.spike_height)
        self.create_points()
        self.rect = pygame.Rect(self.x_coor, self.y_coor, self.width, self.settings.spike_height)

    def create_points(self):
        self.points = [[self.x_coor + (self.width / 2), (self.y_coor)], # Spike TIp
                            [self.x_coor, self.screen_height], # Spike bottom left
                            [(self.x_coor + self.width), self.screen_height] # Spike bottom right
                            ]
        
    def update(self):
        '''Handles the chain like motion of the spike image'''
        for points in self.points:
            points[0] += self.settings.spike_speed
        self.rect.x = self.points[1][0]

    def draw(self):
        points = [(int(px), int(py)) for px, py in self.points]
        pygame.gfxdraw.filled_polygon(self.screen, points, self.settings.spike_color)
        pygame.gfxdraw.aapolygon(self.screen, points, self.settings.spike_color)  # aa = the smooth outline, enable anti-aliasing