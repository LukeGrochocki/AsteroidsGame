import pygame

class Score():
    def __init__(self, font_size=32):
        self.score = 0
        self.font = pygame.font.SysFont("Arial", font_size)
    
    def increase_score(self):
        self.score += 1

    def update(self, screen):
        text_surface = self.font.render(f"Score: {self.score}", True, (255,255,255))
        screen.blit(text_surface, (10,10))