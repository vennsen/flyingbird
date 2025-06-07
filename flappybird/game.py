from collections import defaultdict

import pygame
import random
import os

ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")


def load_cropped_image(path, scale=None):
    """Load an image and crop to the largest contour."""
    image = pygame.image.load(path).convert_alpha()
    if scale is not None:
        image = pygame.transform.scale(image, scale)

    mask = pygame.mask.from_surface(image)
    components = mask.connected_components()

    if components:
        largest = max(components, key=lambda m: m.count())
        rect = largest.get_bounding_rects()[0]
        cropped = image.subsurface(rect).copy()

        mask_surface = largest.to_surface(
            setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0)
        )
        mask_crop = mask_surface.subsurface(rect)
        cropped.blit(mask_crop, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    else:
        rect = image.get_bounding_rect()
        cropped = image.subsurface(rect).copy()

    return cropped

WIDTH, HEIGHT = 288, 512
BIRD_X = 50
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
PIPE_WIDTH = 52
GAP_SIZE = 100
GRAVITY = 0.25
JUMP_STRENGTH = -4.8

class Bird:
    def __init__(self):
        self.y = HEIGHT // 2
        self.vel = 0
        self.image = load_cropped_image(
            os.path.join(ASSET_DIR, "bird.png"),
            scale=(BIRD_WIDTH, BIRD_HEIGHT),
        )
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(centerx=BIRD_X, centery=self.y)

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.y = int(self.y)

    def jump(self):
        self.vel = JUMP_STRENGTH

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.top_rect, self.top_mask, self.top_pipe_image = None, None, None
        self.bottom_rect, self.bottom_mask, self.bottom_pipe_image = None, None, None
        top_height = random.randint(50, HEIGHT - GAP_SIZE - 50)
        bottom_height = HEIGHT - top_height - GAP_SIZE

        object_list = ["pipe.png", "green_pipe.png", "red_pipe.png", "white_pipe.png", "lamp_post.png", "banyan_tree.png"]
        object_choice = random.choice(object_list)
        pipe_surface = load_cropped_image(os.path.join(ASSET_DIR, object_choice))

        no_top_image = defaultdict(lambda : False)
        no_top_image["banyan_tree.png"] = True
        no_top_image["lamp_post.png"] = True

        if not no_top_image[object_choice]:
            self.top_pipe_image = pygame.transform.flip(
                pygame.transform.scale(pipe_surface, (PIPE_WIDTH, top_height)), False, True
            )
            self.top_mask = pygame.mask.from_surface(self.top_pipe_image)
            self.top_rect = self.top_pipe_image.get_rect(topleft=(self.x, 0))

        self.bottom_pipe_image = pygame.transform.scale(
            pipe_surface, (PIPE_WIDTH, bottom_height)
        )
        self.bottom_mask = pygame.mask.from_surface(self.bottom_pipe_image)
        self.bottom_rect = self.bottom_pipe_image.get_rect(
            topleft=(self.x, HEIGHT - bottom_height)
        )

    def update(self):
        self.x -= 2
        if self.top_rect:
            self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0

    def collide(self, bird):
        if self.top_pipe_image and self.top_rect.colliderect(bird.rect):
            offset = (bird.rect.left - self.top_rect.left, bird.rect.top - self.top_rect.top)
            if self.top_mask.overlap(bird.mask, offset):
                return True
        if self.bottom_rect.colliderect(bird.rect):
            offset = (bird.rect.left - self.bottom_rect.left, bird.rect.top - self.bottom_rect.top)
            if self.bottom_mask.overlap(bird.mask, offset):
                return True
        return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    bg_image = pygame.image.load(os.path.join(ASSET_DIR, "bg_image.png")).convert()
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

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
                if pipe.collide(bird):
                    game_over = True
            if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
                game_over = True
            score += 1

        screen.blit(bg_image, (0, 0))
        for pipe in pipes:
            if pipe.top_pipe_image:
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
