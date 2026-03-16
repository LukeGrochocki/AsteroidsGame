import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    
    def update(self, dt):
        self.position += (self.velocity * dt)
        
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            num = random.uniform(20,50)
            a1v = self.velocity.rotate(num)
            a2v = self.velocity.rotate(-num)
            a1r = self.radius - ASTEROID_MIN_RADIUS
            a2r = self.radius - ASTEROID_MIN_RADIUS

            asteroid1 = Asteroid(self.position.x, self.position.y, a1r)
            asteroid2 = Asteroid(self.position.x, self.position.y, a2r)

            asteroid1.velocity = a1v * 1.2
            asteroid2.velocity = a2v * 1.2