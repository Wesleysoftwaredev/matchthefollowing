import pygame
import random

# -------------------- setup --------------------
pygame.init()
clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

font = pygame.font.SysFont("Bauhaus 93", 60)
white = (255, 255, 255)

# game state
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500  # ms
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

# -------------------- assets --------------------
bg = pygame.image.load("img/bg2.png").convert()
ground_img = pygame.image.load("img/grass.png").convert_alpha()
button_img = pygame.image.load("img/restart.png").convert_alpha()

# -------------------- helpers --------------------
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def reset_game():
    global score, pass_pipe, flying, game_over, ground_scroll, last_pipe
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = screen_height // 2
    flappy.vel = 0
    score = 0
    pass_pipe = False
    flying = False
    game_over = False
    ground_scroll = 0
    last_pipe = pygame.time.get_ticks() - pipe_frequency

# -------------------- sprites --------------------
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        for num in range(1, 4):
            self.images.append(pygame.image.load(f"img/bird{num}.png").convert_alpha())
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = 0
        self.clicked = False

    def update(self):
        global flying, game_over

        if flying and not game_over:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 760:  # stay above ground line
                self.rect.y += int(self.vel)

        if not game_over:
            # jump
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                if flying:  # allow first click to start without instant jump if you prefer, remove 'if flying'
                    self.vel = -10
                else:
                    flying = True
                    self.vel = -10
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False

            # flap animation
            flap_cooldown = 5
            self.counter += 1
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images)
                self.image = self.images[self.index]

            # rotate based on velocity
            self.image = pygame.transform.rotate(self.images[self.index], -2 * self.vel)
        else:
            # tilt down on death
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    # position: 1 = top pipe, -1 = bottom pipe
    def __init__(self, x, y, position):
        super().__init__()
        image = pygame.image.load("img/pipe.png").convert_alpha()
        if position == 1:
            image = pygame.transform.flip(image, False, True)
            self.image = image
            self.rect = self.image.get_rect(bottomleft=(x, y - pipe_gap // 2))
        else:
            self.image = image
            self.rect = self.image.get_rect(topleft=(x, y + pipe_gap // 2))

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        return action

# -------------------- groups & instances --------------------
pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()
flappy = Bird(100, screen_height // 2)
bird_group.add(flappy)

button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

# -------------------- main loop --------------------
run = True
while run:
    clock.tick(fps)

    # background & sprites
    screen.blit(bg, (0, 0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()

    # ground
    screen.blit(ground_img, (ground_scroll, 760))

    # spawn pipes
    if flying and not game_over:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_y = screen_height // 2 + random.randint(-120, 120)
            bottom_pipe = Pipe(screen_width, pipe_y, -1)
            top_pipe = Pipe(screen_width, pipe_y, 1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # move ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    # scoring (when bird passes the first pair of pipes)
    if len(pipe_group) > 0:
        first_pipe = pipe_group.sprites()[0]
        if (not pass_pipe and
            flappy.rect.left > first_pipe.rect.left and
            flappy.rect.right < first_pipe.rect.right):
            pass_pipe = True
        if pass_pipe and flappy.rect.left > first_pipe.rect.right:
            score += 1
            pass_pipe = False

    # collisions with pipes or top of screen
    if pygame.sprite.spritecollide(flappy, pipe_group, False) or flappy.rect.top <= 0:
        game_over = True

    # hit the ground
    if flappy.rect.bottom >= 760:
        game_over = True
        flying = False

    # draw score
    draw_text(str(score), font, white, screen_width // 2, 20)

    # restart when game over
    if game_over:
        if button.draw(screen):
            reset_game()

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
