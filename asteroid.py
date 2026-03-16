import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH

class asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self):
        pygame.draw.circle(screen, "white", self.x, self.y, self.radius, LINE_WIDTH)
    
    def update(self, dt):
        