import pygame
from pygame.locals import DOUBLEBUF  # flag to enable double buffering

from models.Bird import Bird
from models.Pipe import Pipe


class Controller:
    def __init__(self):
        # config
        self.WIDTH = 1280 / 1.3
        self.HEIGHT = 720 / 1.3

        self.FPS_LIMIT = 60
        # make the gameplay consistent regardless of the resolution
        self.GRAVITY = self.HEIGHT / 720
        self.X_GRAVITY = self.WIDTH / 1280

        self.GAME_ICON = pygame.image.load('images/duck-ga9276d9c3_640.png')
        self.BG_IMG = pygame.image.load('images/Mountains_Loopable_56x31.png')
        self.BG_COLOR = 'lightblue'

        self.PLAYER_CHARACTER = None
        self.PIPES_ARRAY = None

        self.PIPE_GAP = 200
        self.PIPE_SPACING = 300
        self.pipe_total_width = None

        self.counter = 0
        self.running = False

    def play(self):
        pygame.init()
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), DOUBLEBUF)

        # performance improvements
        screen.set_alpha(None)  # turn off alpha, it is not needed
        self.BG_IMG = self.BG_IMG.convert_alpha()  # convert bg
        self.GAME_ICON = self.GAME_ICON.convert_alpha()

        # set window caption and icon
        pygame.display.set_caption("Bird Jumper")
        pygame.display.set_icon(self.GAME_ICON)

        # game clock
        clock = pygame.time.Clock()
        dt = 0  # delta time

        # player character
        self.PLAYER_CHARACTER = Bird(screen.get_width() / 4, screen.get_height() / 4, self.GRAVITY)

        # pipes setup
        self.PIPES_ARRAY = self.generate_pipes()
        last_pipe = self.PIPES_ARRAY[-1]

        self.running = True
        while self.running:
            # events
            # pygame.QUIT event => the user clicked X
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    # on [space, w, arrow_up] press -> jump
                    if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w]:
                        self.PLAYER_CHARACTER.jump()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # on mouse left click -> jump
                    if event.button == pygame.BUTTON_LEFT:
                        self.PLAYER_CHARACTER.jump()

            # background
            background = pygame.transform.scale(self.BG_IMG, (self.WIDTH, self.HEIGHT))
            screen.fill(self.BG_COLOR)
            screen.blit(background, (0, 0))

            # increment counter on every tick
            self.counter += 1
            # reset counter if it exceeds FPS_LIMIT
            if self.counter > self.FPS_LIMIT:
                self.counter = 0

            # bird animation
            self.PLAYER_CHARACTER.animate_wings(self.counter)

            # render bird
            self.PLAYER_CHARACTER.draw(screen)

            # render Pipes
            for pipe in self.PIPES_ARRAY:
                if pipe.is_visible():
                    pipe.draw(screen)
                else:
                    pipe.recycle(last_pipe.get_x() + self.pipe_total_width)
                    last_pipe = pipe

            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_w]:
            #     self.player_pos.y -= 500 * dt
            # if keys[pygame.K_s]:
            #     self.player_pos.y += 500 * dt
            # if keys[pygame.K_a]:
            #     self.player_pos.x -= 500 * dt
            # if keys[pygame.K_d]:
            #     self.player_pos.x += 500 * dt

            # limit FPS
            # dt is delta time in seconds since last frame, used for frame-rate-independent physics.
            dt = clock.tick(self.FPS_LIMIT) / 1000  # divide by 1000 to convert to seconds

            # update the display
            pygame.display.update()

        pygame.quit()

    def generate_pipes(self):
        pipe_width = Pipe(0, 1000, 0, 0).get_width()
        pipe_total_width = pipe_width + self.PIPE_SPACING

        self.pipe_total_width = pipe_total_width

        pipes_needed = int(self.WIDTH // pipe_total_width) + 1  # + 1 for extra pipe

        pipes = []
        new_pipe_position = self.WIDTH
        for i in range(pipes_needed):
            new_pipe = Pipe(new_pipe_position, self.HEIGHT, self.PIPE_GAP, self.X_GRAVITY)
            new_pipe_position += pipe_total_width

            pipes.append(new_pipe)

        return pipes
