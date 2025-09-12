import pygame
import numpy as np
import time
from utils.directions import LEFT,RIGHT,UP,DOWN

# --- settings ---
GRID_SIZE = 4
TILE_SIZE = 100
GAP = 10
WIDTH = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * GAP
HEIGHT = WIDTH
FPS = 60
ANIM_DURATION = 0.15  # seconds

# --- colors ---
BG = (250, 248, 239)
GRID_BG = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
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
    2048: (237, 194, 46),
}
TEXT_COLOR_LIGHT = (249, 246, 242)
TEXT_COLOR_DARK = (119, 110, 101)
ARROW_COLOR = (50, 50, 50)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Display Function")
font = pygame.font.SysFont("Arial", 32, bold=True)
clock = pygame.time.Clock()

# keep last state for animation
_last_board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

def lerp(a, b, t):
    return a + (b - a) * t

def draw_tile(val, x, y, scale=1.0):
    rect_size = TILE_SIZE * scale
    offset = (TILE_SIZE - rect_size) / 2
    rect = pygame.Rect(x + offset, y + offset, rect_size, rect_size)
    color = TILE_COLORS.get(val, TILE_COLORS[max(TILE_COLORS.keys())])
    pygame.draw.rect(screen, color, rect, border_radius=8)
    if val != 0:
        text = str(val)
        surf = font.render(text, True, TEXT_COLOR_LIGHT if val >= 8 else TEXT_COLOR_DARK)
        tw, th = surf.get_size()
        screen.blit(surf, (rect.centerx - tw/2, rect.centery - th/2))

def draw_arrow(direction):
    """Draw arrow in the center of the board showing the last move."""
    cx = WIDTH // 2
    cy = HEIGHT // 2
    size = 40
    # define simple triangle for arrow
    if direction == UP:
        points = [(cx, cy - size), (cx - size//2, cy + size//2), (cx + size//2, cy + size//2)]
    elif direction == DOWN:
        points = [(cx, cy + size), (cx - size//2, cy - size//2), (cx + size//2, cy - size//2)]
    elif direction == LEFT:
        points = [(cx - size, cy), (cx + size//2, cy - size//2), (cx + size//2, cy + size//2)]
    elif direction == RIGHT:
        points = [(cx + size, cy), (cx - size//2, cy - size//2), (cx - size//2, cy + size//2)]
    else:
        return
    pygame.draw.polygon(screen, ARROW_COLOR, points)

def display_board(board: np.ndarray, arrow):
    """
    Display the given board with animation from previous board.
    board: np.ndarray (4x4), integers
    arrow: Optional[str] in ["UP","DOWN","LEFT","RIGHT"] to draw an arrow
    """
    global _last_board
    start_time = time.time()
    while True:
        now = time.time()
        t = (now - start_time) / ANIM_DURATION
        if t > 1: t = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(BG)
        pygame.draw.rect(screen, GRID_BG, (0,0,WIDTH,HEIGHT), border_radius=8)

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x = c * (TILE_SIZE + GAP) + GAP
                y = r * (TILE_SIZE + GAP) + GAP
                val0 = _last_board[r,c]
                val1 = board[r,c]

                if val0 != val1 and val1 != 0:
                    scale = lerp(0.5, 1.0, t)
                    draw_tile(val1, x, y, scale)
                else:
                    draw_tile(val1, x, y)

        if arrow:
            draw_arrow(arrow)

        pygame.display.flip()
        clock.tick(FPS)

        if t >= 1:
            break

    _last_board = board.copy()
