import pygame
from random import randrange as rnd
import sys

WIDTH, HEIGHT = 1200, 800
fps = 60
# paddle settings
paddle_w = 330
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)
# ball settings
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1
# bonus ball settings
bonus_ball_radius = 15
bonus_ball_speed = 8
bonus_ball_rect = int(bonus_ball_radius * 2 ** 0.5)
bonus_ball = pygame.Rect(rnd(bonus_ball_rect, WIDTH - bonus_ball_rect), HEIGHT // 2, bonus_ball_rect, bonus_ball_rect)
bonus_dx, bonus_dy = 1, 1
bonus_ball_active = False
bonus_duration = 300  # Number of frames the bonus ball will be active
bonus_timer = 0
# blocks settings
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# background image
img = pygame.image.load('images (1).jpg').convert()

# Pause variables and font
paused = False
resume_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
exit_button_pause = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
pause_font = pygame.font.Font(None, 74)
game_over_font = pygame.font.Font(None, 100)  # Font for the game over message
win_font = pygame.font.Font(None, 100)  # Font for the win message

# Add a new variable to track game state
game_over = False

# Menu variables and font
menu_font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 100)

start_game_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
difficulty_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 190, 300, 60)

# Difficulty levels and corresponding paddle sizes
difficulty_levels = ["Easy", "Medium", "Hard"]
paddle_sizes = [(330, 35), (250, 35), (180, 35)]
current_difficulty = 0

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

# Initialize score
score = 0


def draw_score():
    score_text = menu_font.render(f"Score: {score}", True, pygame.Color('white'))
    sc.blit(score_text, (10, 10))

def draw_pause_menu():
    pygame.draw.rect(sc, (0, 128, 255), resume_button)
    pygame.draw.rect(sc, (255, 0, 0), exit_button_pause)

    resume_text = menu_font.render("Resume", True, pygame.Color('white'))
    exit_text_pause = menu_font.render("Exit", True, pygame.Color('white'))

    sc.blit(resume_text, (resume_button.x + (resume_button.width - resume_text.get_width()) // 2,
                          resume_button.y + (resume_button.height - resume_text.get_height()) // 2))
    sc.blit(exit_text_pause, (exit_button_pause.x + (exit_button_pause.width - exit_text_pause.get_width()) // 2,
                              exit_button_pause.y + (exit_button_pause.height - exit_text_pause.get_height()) // 2))

def draw_menu():
    pygame.draw.rect(sc, (0, 128, 255), start_game_button)
    pygame.draw.rect(sc, (255, 0, 0), exit_button)
    pygame.draw.rect(sc, (0, 255, 0), difficulty_button)

    start_game_text = menu_font.render("New Game", True, pygame.Color('white'))
    exit_text = menu_font.render("Exit", True, pygame.Color('white'))
    difficulty_text = menu_font.render(f"Difficulty: {difficulty_levels[current_difficulty]}", True,
                                       pygame.Color('white'))

    sc.blit(start_game_text, (start_game_button.x + (start_game_button.width - start_game_text.get_width()) // 2,
                              start_game_button.y + (start_game_button.height - start_game_text.get_height()) // 2))
    sc.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2,
                        exit_button.y + (exit_button.height - exit_text.get_height()) // 2))
    sc.blit(difficulty_text, (difficulty_button.x + (difficulty_button.width - difficulty_text.get_width()) // 2,
                              difficulty_button.y + (difficulty_button.height - difficulty_text.get_height()) // 2))


def draw_title():
    title_text = title_font.render("Arkanoid", True,
                                   (rnd(30, 256), rnd(30, 256), rnd(30, 256)))  # Random color for each letter
    sc.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
        hit_sound.play()  # Play hit sound effect
    elif delta_x > delta_y:
        dy = -dy
        hit_sound.play()  # Play hit sound effect
    elif delta_y > delta_x:
        dx = -dx
        hit_sound.play()  # Play hit sound effect
    return dx, dy


def detect_collision_bonus(bonus_dx, bonus_dy, bonus_ball, rect):
    if bonus_dx > 0:
        delta_x = bonus_ball.right - rect.left
    else:
        delta_x = rect.right - bonus_ball.left
    if bonus_dy > 0:
        delta_y = bonus_ball.bottom - rect.top
    else:
        delta_y = rect.bottom - bonus_ball.top

    if abs(delta_x - delta_y) < 10:
        bonus_dx, bonus_dy = -bonus_dx, -bonus_dy
        hit_sound.play()  # Play hit sound effect
    elif delta_x > delta_y:
        bonus_dy = -bonus_dy
        hit_sound.play()  # Play hit sound effect
    elif delta_y > delta_x:
        bonus_dx = -bonus_dx
        hit_sound.play()  # Play hit sound effect
    return bonus_dx, bonus_dy


def activate_bonus_ball():
    global bonus_ball_active, bonus_timer
    bonus_ball_active = True
    bonus_timer = bonus_duration
    bonus_ball.center = ball.center


def start_new_game():
    global paddle, ball, dx, dy, block_list, color_list, paused, game_over, score
    global bonus_ball, bonus_dx, bonus_dy, bonus_ball_active, bonus_timer
    paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)
    ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
    dx, dy = 1, -1
    block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
    color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]
    bonus_ball = pygame.Rect(rnd(bonus_ball_rect, WIDTH - bonus_ball_rect), HEIGHT // 2, bonus_ball_rect,
                             bonus_ball_rect)
    bonus_dx, bonus_dy = 1, 1
    bonus_ball_active = False
    bonus_timer = 0
    paused = False
    game_over = False
    score = 0


# Main menu function
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if start_game_button.collidepoint(event.pos):
                        start_new_game()
                        pygame.mixer.music.play(-1)  # Start playing the music when starting the game
                        button_click_sound.play()  # Play button click sound
                        return
                    elif exit_button.collidepoint(event.pos):
                        sys.exit()
                    elif difficulty_button.collidepoint(event.pos):
                        global current_difficulty
                        current_difficulty = (current_difficulty + 1) % len(difficulty_levels)
                        paddle_w, paddle_h = paddle_sizes[current_difficulty]
                        paddle.width = paddle_w
                        button_click_sound.play()  # Play button click sound

        sc.blit(img, (0, 0))
        draw_title()
        draw_menu()
        pygame.display.flip()
        clock.tick(fps)


# Run the main menu
main_menu()
# Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            elif event.key == pygame.K_ESCAPE:
                sys.exit()  # Press 'P' to toggle pause
                paused = not paused
            elif event.key == pygame.K_ESCAPE:  # Press 'Esc' to exit during game over or pause
                sys.exit()
            elif event.key == pygame.K_RETURN and (ball.bottom > HEIGHT or not len(
                    block_list)):  # Press 'Enter' for a new game after losing or winning
                start_new_game()
                pygame.mixer.music.play(-1)  # Start playing the music when starting the game
                button_click_sound.play()  # Play button click sound
            elif event.key == pygame.K_d:  # Press 'D' to toggle difficulty level
                current_difficulty = (current_difficulty + 1) % len(difficulty_levels)
                paddle_w, paddle_h = paddle_sizes[current_difficulty]
                paddle.width = paddle_w
                button_click_sound.play()  # Play button click sound
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if start_game_button.collidepoint(event.pos):
                    start_new_game()
                    pygame.mixer.music.play(-1)  # Start playing the music when starting the game
                    button_click_sound.play()  # Play button click sound
                elif exit_button.collidepoint(event.pos):
                    sys.exit()
                elif difficulty_button.collidepoint(event.pos):
                    current_difficulty = (current_difficulty + 1) % len(difficulty_levels)
                    paddle_w, paddle_h = paddle_sizes[current_difficulty]
                    paddle.width = paddle_w
                    button_click_sound.play()  # Play button click sound

    sc.blit(img, (0, 0))
    # drawing world
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

    if bonus_ball_active:
        pygame.draw.circle(sc, pygame.Color('blue'), bonus_ball.center, bonus_ball_radius)

    if not paused and not game_over:
        # ball movement
        ball.x += ball_speed * dx
        ball.y += ball_speed * dy
        # bonus ball movement
        if bonus_ball_active:
            bonus_ball.x += bonus_ball_speed * bonus_dx
            bonus_ball.y += bonus_ball_speed * bonus_dy

        # Обработка столкновений с краями окна для основного мяча
        if ball.centerx - ball_radius < 0 or ball.centerx + ball_radius > WIDTH:
            dx = -dx

        # Обработка столкновений с краями окна для бонусного мяча
        if bonus_ball_active:
            if bonus_ball.centerx - bonus_ball_radius < 0 or bonus_ball.centerx + bonus_ball_radius > WIDTH:
                bonus_dx = -bonus_dx

        # collision top
        if ball.centery < ball_radius:
            dy = -dy
        # collision paddle
        if ball.colliderect(paddle) and dy > 0:
            dx, dy = detect_collision(dx, dy, ball, paddle)
        # collision bonus ball
        if bonus_ball_active and bonus_ball.colliderect(paddle):
            bonus_dx, bonus_dy = detect_collision_bonus(bonus_dx, bonus_dy, bonus_ball, paddle)
        # collision blocks
        hit_index = ball.collidelist(block_list)
        if hit_index != -1:
            hit_rect = block_list.pop(hit_index)
            hit_color = color_list.pop(hit_index)
            dx, dy = detect_collision(dx, dy, ball, hit_rect)
            # special effect
            hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
            pygame.draw.rect(sc, hit_color, hit_rect)
            # Check if it's a special block to activate the bonus ball
            if rnd(1, 10) == 1:  # Adjust the probability as needed
                activate_bonus_ball()
            # Update the score when a block is hit
            score += 1

        # collision bonus ball with blocks
        if bonus_ball_active:
            hit_index_bonus = bonus_ball.collidelist(block_list)
            if hit_index_bonus != -1:
                hit_rect_bonus = block_list.pop(hit_index_bonus)
                hit_color_bonus = color_list.pop(hit_index_bonus)
                bonus_dx, bonus_dy = detect_collision_bonus(bonus_dx, bonus_dy, bonus_ball, hit_rect_bonus)
                hit_rect_bonus.inflate_ip(bonus_ball.width * 3, bonus_ball.height * 3)
                pygame.draw.rect(sc, hit_color_bonus, hit_rect_bonus)

                # Update the score when a block is hit by the bonus ball
                score += 1

        # win, game over
        if ball.bottom > HEIGHT:
            game_over = True
            game_over_sound.play()  # Play game over sound effect
            game_over_text = game_over_font.render("GAME OVER", True, pygame.Color('red'))
            sc.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
            draw_menu()
            pygame.display.flip()
            pygame.time.delay(3000)  # Display game over message for 3 seconds

        elif not len(block_list):
            game_over = True
            win_sound.play()  # Play win sound effect
            win_text = win_font.render("WIN!!!", True, pygame.Color('yellow'))
            sc.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
            draw_menu()
            pygame.display.flip()

        # control
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if key[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.right += paddle_speed  # Fix this line (removed the extra 'if' condition)

            # Обработка столкновения с краем окна для бонусного мяча
            if bonus_ball_active:
                if bonus_ball.centery + bonus_ball_radius > HEIGHT:
                    bonus_ball_active = False  # Деактивация бонусного мяча при достижении нижнего края окна

            # Update bonus ball status
            if bonus_ball_active:
                bonus_timer -= 1
                if bonus_timer <= 0:
                    bonus_ball_active = False

        else:
            # Display pause or game over message
            if paused:
                pause_text = pause_font.render("PAUSED", True, pygame.Color('white'))
                sc.blit(pause_text, (WIDTH // 2 - 100, HEIGHT // 2 - 30))
                draw_pause_menu()  # Use draw_pause_menu to display pause menu
            elif game_over:
                draw_menu()
            elif not len(block_list):
                win_text = win_font.render("WIN!!!", True, pygame.Color('yellow'))
                sc.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
                draw_menu()

            # update screen
        draw_score()
        pygame.display.flip()
        clock.tick(fps)