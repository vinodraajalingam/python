import random
import pygame as pg

snake_speed = 25

class Game:
    def __init__(self):
        pg.init()
        self.font = pg.font.Font(None, 36)
        self.score = 0
        self.surface = self.initialise_game_window()
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)
        self.running = True
        self.isPaused = True
        self.clock = pg.time.Clock()
        self.highscore = 0
        self.sound_played = False
        pg.mixer.init()

    @staticmethod
    def initialise_game_window():
        pg.display.set_caption("Vinod's Version of Snake Game")
        pg.display.set_icon(pg.image.load("resources/Snake.png"))
        surface = pg.display.set_mode((1000, 700))
        surface.fill((0, 153, 0))
        pg.display.flip()
        return surface

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.isPaused = not self.isPaused
                elif event.key == pg.K_RIGHT and self.snake.direction != 'Left':
                    self.snake.direction = 'Right'
                elif event.key == pg.K_LEFT and self.snake.direction != 'Right':
                    self.snake.direction = 'Left'
                elif event.key == pg.K_DOWN and self.snake.direction != 'Up':
                    self.snake.direction = 'Down'
                elif event.key == pg.K_UP and self.snake.direction != 'Down':
                    self.snake.direction = 'Up'

    def run(self):
        while self.running:
            self.handle_events()
            if self.isPaused:
                self.snake.move()
                self.checkhighscore()
            if not self.check_collision():
                self.render()
            self.clock.tick(10)
        pg.quit()

    def render(self):
        self.surface.fill((0, 153, 0))
        self.drawscore()
        self.snake.draw()
        self.apple.draw()
        pg.display.flip()

    def check_collision(self):
        if self.snake.snake_rect.colliderect(self.apple.apple_rect) and self.snake.snake_rect != (0,0,32,32):
            self.play_sound("pow-90398.mp3")
            self.grow()
            self.apple.move()

        # Check collision with window boundaries
        if self.snake.x[0] < 0 or self.snake.x[0] >= 990 or self.snake.y[0] < 0 or self.snake.y[0] >= 690:
            self.play_sound("crunch.wav")
            self.gameover()
            return True

        # Check collision with itself
        for i in range(1, self.snake.length):
            if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                self.play_sound("crunch.wav")
                self.gameover()
                return True
        return False

    def grow(self):
        self.snake.x.append(self.snake.x[-1])
        self.snake.y.append(self.snake.y[-1])
        self.snake.length += 1
        self.score += 1

    def gameover(self):
        self.surface.fill((50, 0, 0))
        gameover_texts = [f'Your score is {self.score}', 'Game Over! Press R to Restart or Esc to Quit']
        for text in range(len(gameover_texts)):
            gameover_text = self.font.render(gameover_texts[text], True, "White")
            if text == 0:
                if self.score < self.highscore:
                 self.surface.blit(gameover_text, (380, 300))
                else:
                 self.surface.blit(self.font.render(f'High Score : {self.score}', True, "White"), (380, 300))
                 with open("resources/highscore.txt", 'w') as file:
                  file.write(f"High Score : {self.score}")
            elif text == 1:
                self.surface.blit(gameover_text, (200, 340))
        pg.display.flip()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.running = False
                    return
                if event.type == pg.KEYDOWN and event.key == pg.K_r:
                    self.reset()#reset function added instead of creating new instance every time
                    return

    @staticmethod
    def play_sound(param):
        sound = pg.mixer.Sound(f"resources/{param}")
        pg.mixer.Sound.play(sound)
        del sound

    def drawscore(self):
        score_text = self.font.render(f"Score : {self.score}", True, "White")
        self.surface.blit(score_text, (850, 10))

    def checkhighscore(self):
        try:
            with open("resources/highscore.txt", 'r') as file:
                line = file.readline().strip()
                if line.startswith("High Score : "):
                    self.highscore = int(line.split(": ")[1])
                else:
                    self.highscore = 0
        except (FileNotFoundError, ValueError):
            self.highscore = 0
        if (self.score > self.highscore) and not self.sound_played:
            self.play_sound("highscore.mp3")
            self.sound_played = True

    def reset(self):
        self.score = 0
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)
        self.isPaused = True
        self.sound_played = False

class Apple:
    def __init__(self, surface):
        self.surface = surface
        self.apple_x = random.randint(50, 650)
        self.apple_y = random.randint(50, 650)
        self.apple_image = pg.image.load("resources/apple-logo.png")
        self.apple_rect = self.apple_image.get_rect()

    def draw(self):
        self.apple_rect.topleft = (self.apple_x, self.apple_y)
        self.surface.blit(self.apple_image, (self.apple_x, self.apple_y))

    def move(self):
        self.apple_x = random.randint(50, 650)
        self.apple_y = random.randint(50, 650)
        self.draw()


class Snake:
    def __init__(self, surface, length):
        self.surface = surface
        self.length = length
        self.direction = 'Right'
        self.x = [random.randint(150, 650)] * self.length
        self.y = [random.randint(150, 650)] * self.length
        self.block_image = pg.image.load("resources/square.png")
        self.snake_rect = self.block_image.get_rect()

    def move(self):
        # Update body positions
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # Update head position based on direction
        if self.direction == 'Right':
            self.x[0] += snake_speed
        elif self.direction == 'Left':
            self.x[0] -= snake_speed
        elif self.direction == 'Up':
            self.y[0] -= snake_speed
        elif self.direction == 'Down':
            self.y[0] += snake_speed

    def draw(self):
        for i in range(self.length):
            if i == 0:  # Update head's rect for collision detection
                self.snake_rect.topleft = (self.x[0], self.y[0])
            self.surface.blit(self.block_image, (self.x[i], self.y[i]))

if __name__ == '__main__':
    game = Game()
    game.run()
