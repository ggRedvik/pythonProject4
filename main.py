import pygame
from random import randrange as rnd
import sys

WIDTH, HEIGHT = 1200, 800
fps = 60

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Initialize music for the main menu
pygame.mixer.init()
pygame.mixer.music.load('1618804671_geometrydash.mp3')  # Replace 'your_music_file.mp3' with the actual filename
pygame.mixer.music.set_volume(0.1)  # Adjust the volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Start playing the music in a loop

# Load sound effects
hit_sound = pygame.mixer.Sound('1618808442_hit.mp3')  # Replace 'hit_sound.wav' with the actual sound file
game_over_sound = pygame.mixer.Sound(
    '1618808253_smerti.mp3')  # Replace 'game_over_sound.wav' with the actual sound file
win_sound = pygame.mixer.Sound('1618808152_level.mp3')  # Replace 'win_sound.wav' with the actual sound file
button_click_sound = pygame.mixer.Sound('1618808449_nazhatie.mp3')  # Replace with the actual sound file


class Game:
    def __init__(self):
        # paddle settings
        self.paddle_w = 330
        self.paddle_h = 35
        self.paddle_speed = 15
        self.paddle = pygame.Rect(WIDTH // 2 - self.paddle_w // 2, HEIGHT - self.paddle_h - 10, self.paddle_w, self.paddle_h)
        # ball settings
        self.ball_radius = 20
        self.ball_speed = 6
        self.ball_rect = int(self.ball_radius * 2 ** 0.5)
        self.ball = pygame.Rect(rnd(self.ball_rect, WIDTH - self.ball_rect), HEIGHT // 2, self.ball_rect, self.ball_rect)
        self.dx, self.dy = 1, -1
        # bonus ball settings
        self.bonus_ball_radius = 15
        self.bonus_ball_speed = 8
        self.bonus_ball_rect = int(self.bonus_ball_radius * 2 ** 0.5)
        self.bonus_ball = pygame.Rect(rnd(self.bonus_ball_rect, WIDTH - self.bonus_ball_rect), HEIGHT // 2, self.bonus_ball_rect,
                                 self.bonus_ball_rect)
        self.bonus_dx, self.bonus_dy = 1, 1
        self.bonus_ball_active = False
        self.bonus_duration = 300  # Number of frames the bonus ball will be active
        self.bonus_timer = 0
        # blocks settings
        self.block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
        self.color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

        # background image
        self.img = pygame.image.load('images (1).jpg').convert()

        # Pause variables and font
        self.paused = False
        self.resume_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        self.exit_button_pause = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
        self.pause_font = pygame.font.Font(None, 74)
        self.game_over_font = pygame.font.Font(None, 100)  # Font for the game over message
        self.win_font = pygame.font.Font(None, 100)  # Font for the win message

        # Add a new variable to track game state
        self.game_over = False

        # Menu variables and font
        self.menu_font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 100)

        self.start_game_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        self.exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
        self.difficulty_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 190, 300, 60)

        # Difficulty levels and corresponding paddle sizes
        self.difficulty_levels = ["Easy", "Medium", "Hard"]
        self.paddle_sizes = [(330, 35), (250, 35), (180, 35)]
        self.current_difficulty = 0

        # Initialize score
        self.score = 0

    def draw_score(self):
        self.score_text = self.menu_font.render(f"Score: {self.score}", True, pygame.Color('white'))
        sc.blit(self.score_text, (10, 10))

    def draw_pause_menu(self):
        pygame.draw.rect(sc, (0, 128, 255), self.resume_button)
        pygame.draw.rect(sc, (255, 0, 0), self.exit_button_pause)

        self.resume_text = self.menu_font.render("Resume", True, pygame.Color('white'))
        self.exit_text_pause = self.menu_font.render("Exit", True, pygame.Color('white'))

        sc.blit(self.resume_text, (self.resume_button.x + (self.resume_button.width - self.resume_text.get_width()) // 2,
                              self.resume_button.y + (self.resume_button.height - self.resume_text.get_height()) // 2))
        sc.blit(self.exit_text_pause, (self.exit_button_pause.x + (self.exit_button_pause.width - self.exit_text_pause.get_width()) // 2,
                                  self.exit_button_pause.y + (self.exit_button_pause.height - self.exit_text_pause.get_height()) // 2))

    def draw_menu(self):
        pygame.draw.rect(sc, (0, 128, 255), self.start_game_button)
        pygame.draw.rect(sc, (255, 0, 0), self.exit_button)
        pygame.draw.rect(sc, (0, 255, 0), self.difficulty_button)

        start_game_text = self.menu_font.render("New Game", True, pygame.Color('white'))
        exit_text = self.menu_font.render("Exit", True, pygame.Color('white'))
        difficulty_text = self.menu_font.render(f"Difficulty: {self.difficulty_levels[game.current_difficulty]}", True,
                                           pygame.Color('white'))

        sc.blit(start_game_text, (self.start_game_button.x + (self.start_game_button.width - start_game_text.get_width()) // 2,
                                  self.start_game_button.y + (self.start_game_button.height - start_game_text.get_height()) // 2))
        sc.blit(exit_text, (self.exit_button.x + (self.exit_button.width - exit_text.get_width()) // 2,
                            self.exit_button.y + (self.exit_button.height - exit_text.get_height()) // 2))
        sc.blit(difficulty_text, (self.difficulty_button.x + (self.difficulty_button.width - difficulty_text.get_width()) // 2,
                                  self.difficulty_button.y + (self.difficulty_button.height - difficulty_text.get_height()) // 2))


    def draw_title(self):
        title_text = self.title_font.render("Arkanoid", True,
                                       (rnd(30, 256), rnd(30, 256), rnd(30, 256)))  # Random color for each letter
        sc.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))


    def detect_collision(self, rect):
        if self.dx > 0:
            delta_x = self.ball.right - rect.left
        else:
            delta_x = rect.right - self.ball.left
        if self.dy > 0:
            delta_y = self.ball.bottom - rect.top
        else:
            delta_y = rect.bottom - self.ball.top

        if abs(delta_x - delta_y) < 10:
            self.dx, self.dy = -self.dx, -self.dy
            hit_sound.play()  # Play hit sound effect
        elif delta_x > delta_y:
            self.dy = -self.dy
            hit_sound.play()  # Play hit sound effect
        elif delta_y > delta_x:
            self.dx = -self.dx
            hit_sound.play()  # Play hit sound effect


    def detect_collision_bonus(self, rect):
        if self.bonus_dx > 0:
            delta_x = self.bonus_ball.right - rect.left
        else:
            delta_x = rect.right - self.bonus_ball.left
        if self.bonus_dy > 0:
            delta_y = self.bonus_ball.bottom - rect.top
        else:
            delta_y = rect.bottom - self.bonus_ball.top

        if abs(delta_x - delta_y) < 10:
            self.bonus_dx, self.bonus_dy = -self.bonus_dx, -self.bonus_dy
            hit_sound.play()  # Play hit sound effect
        elif delta_x > delta_y:
            self.bonus_dy = -self.bonus_dy
            hit_sound.play()  # Play hit sound effect
        elif delta_y > delta_x:
            self.bonus_dx = -self.bonus_dx
            hit_sound.play()  # Play hit sound effect
        # return bonus_dx, bonus_dy


    def activate_bonus_ball(self):
        self.bonus_ball_active = True
        self.bonus_timer = self.bonus_duration
        self.bonus_ball.center = self.ball.center


    def start_new_game(self):
        self.paddle = pygame.Rect(WIDTH // 2 - self.paddle_w // 2, HEIGHT - self.paddle_h - 10, self.paddle_w, self.paddle_h)
        self.ball = pygame.Rect(rnd(self.ball_rect, WIDTH - self.ball_rect), HEIGHT // 2, self.ball_rect, self.ball_rect)
        self.dx, self.dy = 1, -1
        self.block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
        self.color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]
        self.bonus_ball = pygame.Rect(rnd(self.bonus_ball_rect, WIDTH - self.bonus_ball_rect), HEIGHT // 2, self.bonus_ball_rect,
                                 self.bonus_ball_rect)
        self.bonus_dx, self.bonus_dy = 1, 1
        self.bonus_ball_active = False
        self.bonus_timer = 0
        self.paused = False
        self.game_over = False
        self.score = 0

    # Main menu function
    def main_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.start_game_button.collidepoint(event.pos):
                            self.start_new_game()
                            pygame.mixer.music.play(-1)  # Start playing the music when starting the game
                            button_click_sound.play()  # Play button click sound
                            return
                        elif self.exit_button.collidepoint(event.pos):
                            sys.exit()
                        elif self.difficulty_button.collidepoint(event.pos):
                            self.current_difficulty = (self.current_difficulty + 1) % len(self.difficulty_levels)
                            self.paddle_w, self.paddle_h = self.paddle_sizes[self.current_difficulty]
                            self.paddle.width = self.paddle_w
                            button_click_sound.play()  # Play button click sound

            sc.blit(self.img, (0, 0))
            self.draw_title()
            self.draw_menu()
            pygame.display.flip()
            clock.tick(fps)


# Run the main menu
game = Game()
game.main_menu()
# Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game.paused = not game.paused
            elif event.key == pygame.K_ESCAPE:
                sys.exit()  # Press 'P' to toggle pause
            elif event.key == pygame.K_ESCAPE:  # Press 'Esc' to exit during game over or pause
                sys.exit()
            elif event.key == pygame.K_RETURN and (game.ball.bottom > HEIGHT or not len(
                    game.block_list)):  # Press 'Enter' for a new game after losing or winning
                game.start_new_game()
                pygame.mixer.music.play(-1)  # Start playing the music when starting the game
                button_click_sound.play()  # Play button click sound
            elif event.key == pygame.K_d:  # Press 'D' to toggle difficulty level
                game.current_difficulty = (game.current_difficulty + 1) % len(game.difficulty_levels)
                game.paddle_w, game.paddle_h = game.paddle_sizes[game.current_difficulty]
                game.paddle.width = game.paddle_w
                button_click_sound.play()  # Play button click sound
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if game.start_game_button.collidepoint(event.pos):
                    game.start_new_game()
                    pygame.mixer.music.play(-1)  # Start playing the music when starting the game
                    button_click_sound.play()  # Play button click sound
                elif game.exit_button.collidepoint(event.pos):
                    sys.exit()
                elif game.difficulty_button.collidepoint(event.pos):
                    game.current_difficulty = (game.current_difficulty + 1) % len(game.difficulty_levels)
                    game.paddle_w, game.paddle_h = game.paddle_sizes[game.current_difficulty]
                    game.paddle.width = game.paddle_w
                    button_click_sound.play()  # Play button click sound

    sc.blit(game.img, (0, 0))
    # drawing world
    [pygame.draw.rect(sc, game.color_list[color], block) for color, block in enumerate(game.block_list)]
    pygame.draw.rect(sc, pygame.Color('darkorange'), game.paddle)
    pygame.draw.circle(sc, pygame.Color('white'), game.ball.center, game.ball_radius)

    if game.bonus_ball_active:
        pygame.draw.circle(sc, pygame.Color('blue'), game.bonus_ball.center, game.bonus_ball_radius)

    if not game.paused and not game.game_over:
        # ball movement
        game.ball.x += game.ball_speed * game.dx
        game.ball.y += game.ball_speed * game.dy
        # bonus ball movement
        if game.bonus_ball_active:
            game.bonus_ball.x += game.bonus_ball_speed * game.bonus_dx
            game.bonus_ball.y += game.bonus_ball_speed * game.bonus_dy

        # Обработка столкновений с краями окна для основного мяча
        if game.ball.centerx - game.ball_radius < 0 or game.ball.centerx + game.ball_radius > WIDTH:
            game.dx = -game.dx

        # Обработка столкновений с краями окна для бонусного мяча
        if game.bonus_ball_active:
            if game.bonus_ball.centerx - game.bonus_ball_radius < 0 or game.bonus_ball.centerx + game.bonus_ball_radius > WIDTH:
                game.bonus_dx = -game.bonus_dx

        # collision top
        if game.ball.centery < game.ball_radius:
            game.dy = -game.dy
        # collision paddle
        if game.ball.colliderect(game.paddle) and game.dy > 0:
            game.detect_collision(game.paddle)
        # collision bonus ball
        if game.bonus_ball_active and game.bonus_ball.colliderect(game.paddle):
            game.detect_collision_bonus(game.paddle)
        # collision blocks
        hit_index = game.ball.collidelist(game.block_list)
        if hit_index != -1:
            hit_rect = game.block_list.pop(hit_index)
            hit_color = game.color_list.pop(hit_index)
            game.detect_collision(hit_rect)
            # special effect
            hit_rect.inflate_ip(game.ball.width * 3, game.ball.height * 3)
            pygame.draw.rect(sc, hit_color, hit_rect)
            # Check if it's a special block to activate the bonus ball
            if rnd(1, 10) == 1:  # Adjust the probability as needed
                game.activate_bonus_ball()
            # Update the score when a block is hit
            game.score += 1

        # collision bonus ball with blocks
        if game.bonus_ball_active:
            hit_index_bonus = game.bonus_ball.collidelist(game.block_list)
            if hit_index_bonus != -1:
                hit_rect_bonus = game.block_list.pop(hit_index_bonus)
                hit_color_bonus = game.color_list.pop(hit_index_bonus)
                game.detect_collision_bonus(hit_rect_bonus)
                hit_rect_bonus.inflate_ip(game.bonus_ball.width * 3, game.bonus_ball.height * 3)
                pygame.draw.rect(sc, hit_color_bonus, hit_rect_bonus)

                # Update the score when a block is hit by the bonus ball
                game.score += 1

        # win, game over
        if game.ball.bottom > HEIGHT:
            game.game_over = True
            game_over_sound.play()  # Play game over sound effect
            game_over_text = game.game_over_font.render("GAME OVER", True, pygame.Color('red'))
            sc.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
            game.draw_menu()
            pygame.display.flip()
            pygame.time.delay(3000)  # Display game over message for 3 seconds

        elif not len(game.block_list):
            game.game_over = True
            win_sound.play()  # Play win sound effect
            win_text = game.win_font.render("WIN!!!", True, pygame.Color('yellow'))
            sc.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
            game.draw_menu()
            pygame.display.flip()

        # control
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and game.paddle.left > 0:
            game.paddle.left -= game.paddle_speed
        if key[pygame.K_RIGHT] and game.paddle.right < WIDTH:
            game.paddle.right += game.paddle_speed  # Fix this line (removed the extra 'if' condition)

            # Обработка столкновения с краем окна для бонусного мяча
            if game.bonus_ball_active:
                if game.bonus_ball.centery + game.bonus_ball_radius > HEIGHT:
                    game.bonus_ball_active = False  # Деактивация бонусного мяча при достижении нижнего края окна

            # Update bonus ball status
            if game.bonus_ball_active:
                game.bonus_timer -= 1
                if game.bonus_timer <= 0:
                    game.bonus_ball_active = False

        else:
            # Display pause or game over message
            if game.paused:
                pause_text = game.pause_font.render("PAUSED", True, pygame.Color('white'))
                sc.blit(pause_text, (WIDTH // 2 - 100, HEIGHT // 2 - 30))
                game.draw_pause_menu()  # Use draw_pause_menu to display pause menu
            elif game.game_over:
                game.draw_menu()
            elif not len(game.block_list):
                win_text = game.win_font.render("WIN!!!", True, pygame.Color('yellow'))
                sc.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
                game.draw_menu()

            # update screen
        game.draw_score()
        pygame.display.flip()
        clock.tick(fps)