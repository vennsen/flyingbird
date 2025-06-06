import pygame
import random
import os

ASSET_DIR = os.path.join(os.path.dirname(__file__), 'assets')

# Initialize Pygame temporarily to load images and get their dimensions
pygame.init()

# Load bird image to get its dimensions for constants
_BIRD_IMG_TEMP = pygame.image.load(os.path.join(ASSET_DIR, "bird.png"))
BIRD_WIDTH = _BIRD_IMG_TEMP.get_width()
BIRD_HEIGHT = _BIRD_IMG_TEMP.get_height()
del _BIRD_IMG_TEMP # Free memory

# Load pipe image to get its width for the constant
_PIPE_IMG_TEMP = pygame.image.load(os.path.join(ASSET_DIR, "pipe.jpg"))
PIPE_WIDTH = _PIPE_IMG_TEMP.get_width()
del _PIPE_IMG_TEMP # Free memory

pygame.quit() # Quit the temporary Pygame instance

WIDTH, HEIGHT = 288, 512
BIRD_X = 50
# BIRD_WIDTH, BIRD_HEIGHT, and PIPE_WIDTH are now set dynamically above
GAP_SIZE = 100
GRAVITY = 0.25
JUMP_STRENGTH = -4.5

class Bird:
    def __init__(self):
        self.y = HEIGHT // 2
        self.vel = 0
        self.image = pygame.image.load(os.path.join(ASSET_DIR, "bird.png")).convert_alpha()
        self.rect = self.image.get_rect(centerx=BIRD_X, centery=self.y)

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.y = int(self.y)

    def jump(self):
        self.vel = JUMP_STRENGTH

class Pipe:
    def __init__(self):
        self.pipe_surface = pygame.image.load(os.path.join(ASSET_DIR, "pipe.jpg")).convert()
        self.bottom_pipe_image = self.pipe_surface
        self.top_pipe_image = pygame.transform.flip(self.pipe_surface, False, True)
        self.x = WIDTH
        top_height = random.randint(50, HEIGHT - GAP_SIZE - 50)
        bottom_height = HEIGHT - top_height - GAP_SIZE
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, top_height)
        self.bottom_rect = pygame.Rect(self.x, HEIGHT - bottom_height, PIPE_WIDTH, bottom_height)

    def update(self):
        self.x -= 2
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0

    def collide(self, bird_rect):
        return self.top_rect.colliderect(bird_rect) or self.bottom_rect.colliderect(bird_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    bird = Bird()
    pipes = []
    score = 0
    running = True
    game_over = False

    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, 1500)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.jump()
                if event.key == pygame.K_r and game_over:
                    return main()
            if event.type == spawn_event and not game_over:
                pipes.append(Pipe())

        if not game_over:
            bird.update()
            for pipe in pipes:
                pipe.update()
            pipes = [p for p in pipes if not p.off_screen()]
            for pipe in pipes:
                if pipe.collide(bird.rect):
                    game_over = True
            if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
                game_over = True
            score += 1

        screen.fill((135, 206, 235))  # sky blue
        for pipe in pipes:
            screen.blit(pipe.top_pipe_image, pipe.top_rect)
            screen.blit(pipe.bottom_pipe_image, pipe.bottom_rect)
        screen.blit(bird.image, bird.rect)

        score_surf = font.render(f"Score: {score//30}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))

        if game_over:
            over_surf = font.render("Game Over! Press R to restart", True, (255, 0, 0))
            screen.blit(over_surf, (20, HEIGHT//2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
