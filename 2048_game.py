import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 设置中文字体
try:
    # 尝试使用系统自带的中文字体
    font_path = pygame.font.match_font('simsun')  # Windows下的宋体
    if not font_path:
        font_path = pygame.font.match_font('notosanscjk')  # Linux下的思源黑体
    if not font_path:
        font_path = pygame.font.match_font('arialuni')  # 其他中文字体
    FONT = pygame.font.Font(font_path, 36)
except:
    # 如果找不到中文字体，就使用默认字体
    FONT = pygame.font.Font(None, 36)

# 颜色定义
COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# 游戏配置
WINDOW_SIZE = 400
GRID_SIZE = 4
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
PADDING = 10

# 创建窗口
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 100))
pygame.display.set_caption('2048游戏')

class Game2048:
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) 
                      for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        moved = False
        if direction == "UP":
            for j in range(GRID_SIZE):
                for i in range(1, GRID_SIZE):
                    if self.grid[i][j] != 0:
                        current = i
                        while current > 0 and (self.grid[current-1][j] == 0 or 
                                             self.grid[current-1][j] == self.grid[current][j]):
                            if self.grid[current-1][j] == self.grid[current][j]:
                                self.grid[current-1][j] *= 2
                                self.score += self.grid[current-1][j]
                                self.grid[current][j] = 0
                                moved = True
                                break
                            self.grid[current-1][j] = self.grid[current][j]
                            self.grid[current][j] = 0
                            current -= 1
                            moved = True

        elif direction == "DOWN":
            for j in range(GRID_SIZE):
                for i in range(GRID_SIZE-2, -1, -1):
                    if self.grid[i][j] != 0:
                        current = i
                        while current < GRID_SIZE-1 and (self.grid[current+1][j] == 0 or 
                                                       self.grid[current+1][j] == self.grid[current][j]):
                            if self.grid[current+1][j] == self.grid[current][j]:
                                self.grid[current+1][j] *= 2
                                self.score += self.grid[current+1][j]
                                self.grid[current][j] = 0
                                moved = True
                                break
                            self.grid[current+1][j] = self.grid[current][j]
                            self.grid[current][j] = 0
                            current += 1
                            moved = True

        elif direction == "LEFT":
            for i in range(GRID_SIZE):
                for j in range(1, GRID_SIZE):
                    if self.grid[i][j] != 0:
                        current = j
                        while current > 0 and (self.grid[i][current-1] == 0 or 
                                             self.grid[i][current-1] == self.grid[i][current]):
                            if self.grid[i][current-1] == self.grid[i][current]:
                                self.grid[i][current-1] *= 2
                                self.score += self.grid[i][current-1]
                                self.grid[i][current] = 0
                                moved = True
                                break
                            self.grid[i][current-1] = self.grid[i][current]
                            self.grid[i][current] = 0
                            current -= 1
                            moved = True

        elif direction == "RIGHT":
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE-2, -1, -1):
                    if self.grid[i][j] != 0:
                        current = j
                        while current < GRID_SIZE-1 and (self.grid[i][current+1] == 0 or 
                                                       self.grid[i][current+1] == self.grid[i][current]):
                            if self.grid[i][current+1] == self.grid[i][current]:
                                self.grid[i][current+1] *= 2
                                self.score += self.grid[i][current+1]
                                self.grid[i][current] = 0
                                moved = True
                                break
                            self.grid[i][current+1] = self.grid[i][current]
                            self.grid[i][current] = 0
                            current += 1
                            moved = True

        if moved:
            self.add_new_tile()

    def check_game_over(self):
        # 检查是否有空格
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    return False

        # 检查是否有相邻的相同数字
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if j < GRID_SIZE-1 and self.grid[i][j] == self.grid[i][j+1]:
                    return False
                if i < GRID_SIZE-1 and self.grid[i][j] == self.grid[i+1][j]:
                    return False
        return True

def draw_game(game):
    screen.fill((187, 173, 160))
    
    # 绘制网格
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = game.grid[i][j]
            color = COLORS.get(value, (237, 194, 46))
            pygame.draw.rect(screen, color,
                           (j*CELL_SIZE + PADDING,
                            i*CELL_SIZE + PADDING,
                            CELL_SIZE - 2*PADDING,
                            CELL_SIZE - 2*PADDING))
            if value != 0:
                font_size = 48 if value < 100 else 36 if value < 1000 else 24
                font = pygame.font.Font(None, font_size)
                text = font.render(str(value), True, (119, 110, 101) if value <= 4 else (249, 246, 242))
                text_rect = text.get_rect(center=(j*CELL_SIZE + CELL_SIZE//2,
                                                i*CELL_SIZE + CELL_SIZE//2))
                screen.blit(text, text_rect)

    # 绘制分数
    score_text = FONT.render(f'score: {game.score}', True, (119, 110, 101))
    screen.blit(score_text, (10, WINDOW_SIZE + 20))

    # 如果游戏结束，显示游戏结束信息和按钮
    if game.game_over:
        # 半透明遮罩
        s = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE + 100))
        s.set_alpha(128)
        s.fill((255, 255, 255))
        screen.blit(s, (0, 0))

        # 游戏结束文本
        game_over_text = FONT.render('游戏结束!', True, (119, 110, 101))
        text_rect = game_over_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2 - 50))
        screen.blit(game_over_text, text_rect)

        # 重新开始按钮
        pygame.draw.rect(screen, (142, 122, 102),
                        (WINDOW_SIZE//2 - 100, WINDOW_SIZE//2 + 20, 200, 40))
        restart_text = FONT.render('重新开始', True, (249, 246, 242))
        restart_rect = restart_text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2 + 40))
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()

def main():
    game = Game2048()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not game.game_over:
                if event.key == pygame.K_UP:
                    game.move("UP")
                elif event.key == pygame.K_DOWN:
                    game.move("DOWN")
                elif event.key == pygame.K_LEFT:
                    game.move("LEFT")
                elif event.key == pygame.K_RIGHT:
                    game.move("RIGHT")

            if event.type == pygame.MOUSEBUTTONDOWN and game.game_over:
                mouse_pos = pygame.mouse.get_pos()
                # 检查是否点击了重新开始按钮
                if (WINDOW_SIZE//2 - 100 <= mouse_pos[0] <= WINDOW_SIZE//2 + 100 and
                    WINDOW_SIZE//2 + 20 <= mouse_pos[1] <= WINDOW_SIZE//2 + 60):
                    game = Game2048()

        game.game_over = game.check_game_over()
        draw_game(game)
        clock.tick(60)

if __name__ == "__main__":
    main()