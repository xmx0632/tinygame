#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
import numpy

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # 初始化音频系统

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Breakout Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Paddle properties
PADDLE_WIDTH = 150
PADDLE_HEIGHT = 20
paddle_x = (WINDOW_WIDTH - PADDLE_WIDTH) // 2
paddle_y = WINDOW_HEIGHT - 40

# Ball properties
BALL_SIZE = 10
ball_x = WINDOW_WIDTH // 2
ball_y = WINDOW_HEIGHT // 2
ball_dx = 5
ball_dy = -5

# Brick properties
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = WINDOW_WIDTH // BRICK_WIDTH
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT + 50, 
                          BRICK_WIDTH - 2, BRICK_HEIGHT - 2)
        bricks.append(brick)

# Score
score = 0

# Create system sounds using pygame
# 击中砖块的"叮"声（高频短促）
hit_sound = pygame.mixer.Sound(pygame.sndarray.array([4096 * numpy.sin(2.0 * numpy.pi * 880.0 * x / 44100) for x in range(int(44100/8))]).astype(numpy.int16))
# 击球的"咚"声（低频较长）
paddle_sound = pygame.mixer.Sound(pygame.sndarray.array([4096 * numpy.sin(2.0 * numpy.pi * 150.0 * x / 44100) for x in range(int(44100/4))]).astype(numpy.int16))

# 在游戏循环前定义按钮矩形（全局变量）
replay_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 + 20, 120, 40)
quit_button_rect = pygame.Rect(WINDOW_WIDTH // 2 + 20, WINDOW_HEIGHT // 2 + 20, 120, 40)

# Game loop
running = True
clock = pygame.time.Clock()

# Game states
game_over = False
game_won = False  # 添加通关状态标志

# 设置中文字体
try:
    font_path = pygame.font.match_font('simsun')  # Windows下的宋体
    if not font_path:
        font_path = pygame.font.match_font('notosanscjk')  # Linux下的思源黑体
    if not font_path:
        font_path = pygame.font.match_font('arialuni')  # 其他中文字体
    FONT = pygame.font.Font(font_path, 36)
    GAME_OVER_FONT = pygame.font.Font(font_path, 64)
    BUTTON_FONT = pygame.font.Font(font_path, 36)
except:
    FONT = pygame.font.Font(None, 36)
    GAME_OVER_FONT = pygame.font.Font(None, 64)
    BUTTON_FONT = pygame.font.Font(None, 36)

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and (game_over or game_won):  # 修改判断条件
            mouse_pos = pygame.mouse.get_pos()
            if replay_button_rect.collidepoint(mouse_pos):
                # Reset game
                game_over = False
                game_won = False  # 重置通关状态
                score = 0
                ball_x = WINDOW_WIDTH // 2
                ball_y = WINDOW_HEIGHT // 2
                ball_dx = 5
                ball_dy = -5
                paddle_x = (WINDOW_WIDTH - PADDLE_WIDTH) // 2
                bricks.clear()
                for row in range(BRICK_ROWS):
                    for col in range(BRICK_COLS):
                        brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT + 50,
                                          BRICK_WIDTH - 2, BRICK_HEIGHT - 2)
                        bricks.append(brick)
            elif quit_button_rect.collidepoint(mouse_pos):
                running = False
    
    # Move paddle (only if game is not over or won)
    if not game_over and not game_won:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= 7
        if keys[pygame.K_RIGHT] and paddle_x < WINDOW_WIDTH - PADDLE_WIDTH:
            paddle_x += 7
    
    # Clear screen
    window.fill(BLACK)

    if game_over:
        # Draw game over screen
        game_over_text = GAME_OVER_FONT.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        window.blit(game_over_text, game_over_rect)

        # Draw replay button
        button_text = BUTTON_FONT.render("Play Again", True, WHITE)
        pygame.draw.rect(window, BLUE, replay_button_rect)
        text_rect = button_text.get_rect(center=replay_button_rect.center)
        window.blit(button_text, text_rect)

        # Draw quit button
        quit_text = BUTTON_FONT.render("Quit Game", True, WHITE)
        pygame.draw.rect(window, RED, quit_button_rect)
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
        window.blit(quit_text, quit_text_rect)

    elif game_won:  # 通关画面
        # Draw victory screen
        victory_text = GAME_OVER_FONT.render("VICTORY!", True, WHITE)
        victory_rect = victory_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        window.blit(victory_text, victory_rect)

        # Draw replay button
        button_text = BUTTON_FONT.render("Play Again", True, WHITE)
        pygame.draw.rect(window, BLUE, replay_button_rect)
        text_rect = button_text.get_rect(center=replay_button_rect.center)
        window.blit(button_text, text_rect)

        # Draw quit button
        quit_text = BUTTON_FONT.render("Quit Game", True, WHITE)
        pygame.draw.rect(window, RED, quit_button_rect)
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
        window.blit(quit_text, quit_text_rect)

    else:
        # Move ball
        ball_x += ball_dx
        ball_y += ball_dy
        
        # Ball collision with walls
        if ball_x <= 0 or ball_x >= WINDOW_WIDTH - BALL_SIZE:
            ball_dx *= -1
        if ball_y <= 0:
            ball_dy *= -1
        if ball_y >= WINDOW_HEIGHT:
            game_over = True
            continue

        # Ball collision with paddle
        paddle = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        if paddle.collidepoint(ball_x, ball_y):
            ball_dy *= -1
            paddle_sound.play()
        
        # Ball collision with bricks
        for brick in bricks[:]:
            if brick.collidepoint(ball_x, ball_y):
                bricks.remove(brick)
                ball_dy *= -1
                score += 10
                hit_sound.play()
                
                # 检查是否所有砖块都被消除
                if len(bricks) == 0:
                    game_won = True
                    continue
        
        # Draw game elements
        pygame.draw.rect(window, BLUE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.circle(window, WHITE, (int(ball_x), int(ball_y)), BALL_SIZE)
        for brick in bricks:
            pygame.draw.rect(window, RED, brick)

    # Draw score (always show score)
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (10, 10))
    
    # Update display
    pygame.display.flip()
    
    # Control game speed
    clock.tick(60)

# Quit game
pygame.quit()
