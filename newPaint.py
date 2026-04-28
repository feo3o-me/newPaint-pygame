import pygame
from CTkColorPicker import *
import customtkinter

# =========== #
# INIT

pygame.init()
pygame.font.init()
running = True
clock = pygame.time.Clock()

# =========== #
# Constants

WIDTH = 1024
HEIGHT = 768
CANVAS_W = 900
CANVAS_H = 768
ROWS = 50
COLS = 45
PIXEL_SIZE = WIDTH // ROWS
FPS = 100
BLACK = "#3B3B3B"
WHITE = "#FFFFFF"
GRAY = "#636363"
BACKGROUND_COLOR = BLACK

# =========== #
# Buttons
window = pygame.display.set_mode((WIDTH, HEIGHT))
change = pygame.image.load('resources/c.png').convert_alpha()
eraser = pygame.image.load('resources/e.png').convert_alpha()
clear = pygame.image.load('resources/x.png').convert_alpha()
drawing_color = WHITE

class Button():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw_button(self):
        """Draw the buttons"""

        action = False

        pos = pygame.mouse.get_pos()

        # Check for collision and click
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
                action = True

        window.blit(self.image, (self.rect.x, self.rect.y))

        return action

color = Button(925, 15, change)
erase = Button(925, 100, eraser)
clear = Button(925, 185, clear)


# =========== #
# Functions

def ask_color():
        pick_color = AskColor() # open the color picker
        color = pick_color.get() # get the color string
        button.configure(fg_color=color)

        return color

root = customtkinter.CTk()

button = customtkinter.CTkButton(master=root, text="CHOOSE COLOR", text_color="black", command=ask_color)
button.pack(padx=30, pady=20)

grid = []

def canvas(rows, cols, color):
    """Fills the screen with a grid, making pixels"""
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            grid[i].append(color)

    return grid

grid = canvas(ROWS, COLS, BACKGROUND_COLOR)

def paint(window, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(window, pixel, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    for i in range(ROWS + 1):
        pygame.draw.line(window, GRAY, (0, i * PIXEL_SIZE), (CANVAS_W, i * PIXEL_SIZE))
    for j in range(COLS + 1):
        pygame.draw.line(window, GRAY, (j * PIXEL_SIZE, 0), (j * PIXEL_SIZE, CANVAS_H))

def draw(window):
    """Draw and update the screen"""
    global drawing_color
    global grid
    window.fill(BACKGROUND_COLOR)
    paint(window, grid)

    x = color.draw_button()
    y = erase.draw_button()
    z = clear.draw_button()

    if x == True:
        drawing_color = ask_color()
        color.clicked == False

    if y == True:
        drawing_color = BACKGROUND_COLOR
        erase.clicked == False

    if z == True:
        drawing_color = WHITE
        clear.clicked == False
    
    pygame.display.update()

def get_row_col_from_pos(pos):
    x, y = pos
    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE

    if row >= ROWS:
        raise IndexError

    return row, col

# =========== #
# Main Loop

while running:

    clock.tick(FPS) # Limits FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            row, col = get_row_col_from_pos(pos)
            if row < ROWS and col < COLS:
                grid[row][col] = drawing_color

    draw(window)

pygame.quit()