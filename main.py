import sys
from enum import Enum, auto

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot
from score import Score
from button import Button


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    OVER = auto()


def create_game_objects():
    """Create and return all sprite groups and gameplay objects for a fresh run."""
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    player = Player(350 , 350)
    asteroid_field = AsteroidField()
    score = Score()

    return {
        "updatable": updatable,
        "drawable": drawable,
        "asteroids": asteroids,
        "shots": shots,
        "player": player,
        "asteroid_field": asteroid_field,
        "score": score,
    }


def draw_centered_text(screen, font, text, y=None, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if y is None:
        text_rect.center = (480, 450)
    else:
        text_rect.center = (SCREEN_WIDTH // 2, y)

    screen.blit(text_surface, text_rect)


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroid Game")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 48)

    state = GameState.MENU
    dt = 0.0

    # Buttons created once instead of every frame
    menu_button = Button(350, 500, 250, 50, "Start Asteroid Game", (0, 0, 0))
    over_button = Button(350, 500, 250, 50, "Play Again?", (0, 0, 0))

    # Create first game session
    game = create_game_objects()

    running = True
    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        if state == GameState.MENU:
            draw_centered_text(screen, font, "Asteroid Game")
            menu_button.draw(screen)

            for event in events:
                if menu_button.is_clicked(event):
                    game = create_game_objects()   # fresh game
                    state = GameState.PLAYING
                    break

        elif state == GameState.PLAYING:
            log_state()

            game["updatable"].update(dt)

            # Only do this if your Player class still depends on manual cooldown reduction
            game["player"].cooldown -= dt

            game["score"].update(screen)

            # Player collision with asteroid
            for asteroid in game["asteroids"]:
                if asteroid.collides_with(game["player"]):
                    log_event("player_hit")
                    state = GameState.OVER
                    break

            # Only process shot collisions if still playing
            if state == GameState.PLAYING:
                for asteroid in list(game["asteroids"]):
                    for shot in list(game["shots"]):
                        if shot.collides_with(asteroid):
                            log_event("asteroid_shot")
                            shot.kill()
                            game["score"].increase_score()
                            asteroid.split()

            for item in game["drawable"]:
                item.draw(screen)

        elif state == GameState.OVER:
            draw_centered_text(screen, font, "GAME OVER")
            over_button.draw(screen)

            for event in events:
                if over_button.is_clicked(event):
                    game = create_game_objects()   # reset everything cleanly
                    dt = 0.0
                    state = GameState.PLAYING
                    break

        pygame.display.flip()
        dt = clock.tick(60) / 1000.0

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()