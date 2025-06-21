import pygame
import math

# Initialize
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
FPS = 60
MAX_SCORE = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 20, 147)
BG_COLOR = (20, 20, 40)

# Fonts
score_font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 64)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Neon Pong")
clock = pygame.time.Clock()

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 100)
        self.speed = 7

    def move(self, direction):
        self.rect.y += self.speed * direction
        self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.height, self.rect.y))

    def draw(self):
        glow = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 155 + 100
        color = (0, glow, 255)
        pygame.draw.rect(screen, color, self.rect, border_radius=5)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, 20, 20)
        self.speed_x = 6
        self.speed_y = 6

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

        if self.rect.left <= 0:
            return "right"
        if self.rect.right >= SCREEN_WIDTH:
            return "left"
        return None

    def bounce(self):
        self.speed_x *= -1

    def reset(self):
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        self.speed_x *= -1

    def draw(self):
        pygame.draw.ellipse(screen, NEON_PINK, self.rect)
        # Trail effect
        for i in range(1, 5):
            trail_x = self.rect.x - i * self.speed_x
            trail_y = self.rect.y - i * self.speed_y
            pygame.draw.ellipse(screen, (255, 20, 147, max(50 - i*10, 0)), (trail_x, trail_y, 20, 20))

def draw_scores(left_score, right_score):
    left_text = score_font.render(f"Player 1: {left_score}", True, WHITE)
    right_text = score_font.render(f"Player 2: {right_score}", True, WHITE)
    screen.blit(left_text, (30, 20))
    screen.blit(right_text, (SCREEN_WIDTH - right_text.get_width() - 30, 20))

def show_game_over(winner):
    screen.fill(BG_COLOR)
    message = game_over_font.render(f"{winner} Wins!", True, WHITE)
    prompt = score_font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(message, message.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20)))
    screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40)))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def main():
    while True:
        left_paddle = Paddle(30, SCREEN_HEIGHT//2 - 50)
        right_paddle = Paddle(SCREEN_WIDTH - 40, SCREEN_HEIGHT//2 - 50)
        ball = Ball()

        left_score, right_score = 0, 0
        running = True
        
        while running:
            screen.fill(BG_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                left_paddle.move(-1)
            if keys[pygame.K_s]:
                left_paddle.move(1)
            if keys[pygame.K_UP]:
                right_paddle.move(-1)
            if keys[pygame.K_DOWN]:
                right_paddle.move(1)

            result = ball.move()

            if result == "left":
                right_score += 1
                ball.reset()
            elif result == "right":
                left_score += 1
                ball.reset()

            if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
                ball.bounce()

            left_paddle.draw()
            right_paddle.draw()
            ball.draw()
            draw_scores(left_score, right_score)

            if left_score >= MAX_SCORE:
                show_game_over("Player 1")
                break
            elif right_score >= MAX_SCORE:
                show_game_over("Player 2")
                break

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()