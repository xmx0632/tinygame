#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 设置中文字体
try:
    font_path = pygame.font.match_font('simsun')  # Windows下的宋体
    if not font_path:
        font_path = pygame.font.match_font('notosanscjk')  # Linux下的思源黑体
    if not font_path:
        font_path = pygame.font.match_font('arialuni')  # 其他中文字体
    FONT = pygame.font.Font(font_path, 36)
except:
    FONT = pygame.font.Font(None, 36)

# 颜色定义
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# 游戏设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10

# 创建窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇')

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.food = self.create_food()
        self.game_over = False

    def create_food(self):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), 
                       random.randint(0, GRID_HEIGHT - 1))
            if position not in self.positions:
                return position

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        if not self.game_over:
            cur = self.get_head_position()
            x, y = self.direction
            new = (cur[0] + x, cur[1] + y)
            
            # 检查是否撞墙
            if (new[0] < 0 or new[0] >= GRID_WIDTH or 
                new[1] < 0 or new[1] >= GRID_HEIGHT):
                self.game_over = True
                return

            # 检查是否撞到自己
            if new in self.positions[2:]:
                self.game_over = True
                return

            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

            if new == self.food:
                self.length += 1
                self.score += 10
                self.food = self.create_food()

    def render(self):
        # 绘制蛇身
        for position in self.positions:
            rect = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE,
                             GRID_SIZE - 1, GRID_SIZE - 1)
            pygame.draw.rect(screen, self.color, rect)

        # 绘制食物
        rect = pygame.Rect(self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE,
                          GRID_SIZE - 1, GRID_SIZE - 1)
        pygame.draw.rect(screen, RED, rect)

# 方向定义
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def draw_game(snake):
    screen.fill(BLACK)
    snake.render()
    
    # 绘制分数
    score_text = FONT.render(f'Score: {snake.score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # 如果游戏结束，显示游戏结束信息和按钮
    if snake.game_over:
        # 半透明遮罩
        s = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        s.set_alpha(128)
        s.fill(WHITE)
        screen.blit(s, (0, 0))

        # 游戏结束文本
        game_over_text = FONT.render('Game Over!', True, BLACK)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 100))
        screen.blit(game_over_text, text_rect)

        # 重新开始按钮
        restart_button = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2, 200, 40)
        pygame.draw.rect(screen, GRAY, restart_button)
        restart_text = FONT.render('Play Again', True, WHITE)
        restart_rect = restart_text.get_rect(center=restart_button.center)
        screen.blit(restart_text, restart_rect)

        # 结束游戏按钮
        quit_button = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 60, 200, 40)
        pygame.draw.rect(screen, GRAY, quit_button)
        quit_text = FONT.render('Game Over', True, WHITE)
        quit_rect = quit_text.get_rect(center=quit_button.center)
        screen.blit(quit_text, quit_rect)

    pygame.display.flip()

def main():
    snake = Snake()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if not snake.game_over:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT

            if event.type == pygame.MOUSEBUTTONDOWN and snake.game_over:
                mouse_pos = pygame.mouse.get_pos()
                # 检查是否点击了重新开始按钮
                restart_button = pygame.Rect(WINDOW_WIDTH//2 - 100, 
                                          WINDOW_HEIGHT//2, 200, 40)
                if restart_button.collidepoint(mouse_pos):
                    snake.reset()
                
                # 检查是否点击了结束游戏按钮
                quit_button = pygame.Rect(WINDOW_WIDTH//2 - 100, 
                                        WINDOW_HEIGHT//2 + 60, 200, 40)
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        snake.update()
        draw_game(snake)
        clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    main()