#optimized random
import pygame
import time
from numpy import random
import tkinter as tk
from tkinter import ttk

def valid(x, y):
    if x < 0 or y < 0 or x > 2 or y > 2: return False
    else: return True

def mini_max(depth, row, col, maximizing_player, alpha, beta):
    score = board[row][col]
    best_row = row
    best_col = col

    if depth == 0:                          #base case: reached required depth
        return score, best_row, best_col

    for x in {-1, 0, 1}:                    #loop for rows
        for y in {-1, 0, 1}:                #loop for columns
            if x == 0 and y == 0: continue
            if x != 0 and y != 0: continue
            if not valid(row+x, col+y): continue

            if maximizing_player:
                score, _, _ = mini_max(depth-1, row+x, col+y, False, alpha, beta)

                if score > alpha:           #update alpha
                    alpha = score
                    best_row = row+x
                    best_col = col+y
            else:
                score, _, _ = mini_max(depth-1, row+x, col+y, True, alpha, beta)

                if score < beta:            #update beta
                    beta = score
                    best_row = row+x
                    best_col = col+y

    return score, best_row, best_col


def move(cur_x, cur_y):
    return mini_max(depth=1, row=cur_x, col=cur_y, maximizing_player=True, alpha=-10000, beta=10000)

def draw_board(x, y, score=0, max_score=0, goal=10, step=0):
    screen.fill(BLACK)

    for row in range(3):
        for column in range(3):
            color = WHITE
            if row == x and column == y: color = GREEN
            pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN + 100, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
            text = numbers_font.render(str(board[row][column]), True, (0, 128, 0))
            screen.blit(text, [(MARGIN + WIDTH) * column + MARGIN + 100, (MARGIN + HEIGHT) * row + MARGIN])

        draw_text(screen, "Score: %s    Max Score: %s" %(score, max_score), MARGIN, (MARGIN + HEIGHT) * 4 + MARGIN)
        draw_text(screen, "Goal: %s     Step: %s" %(goal, step), MARGIN, (MARGIN + HEIGHT) * 4 + MARGIN + 50)

    clock.tick(500)
    pygame.display.flip()

def draw_text(surf, text, x, y, pos=0):
    text_surface = text_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    if pos == 0: text_rect.midleft = (x, y)
    else: text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def generate_new_board():
    global board

    board = list()
    for _ in range (0, 3):
        temp = []
        for _ in range(0, 3):
            n = random.randint(-1, 2)
            temp.append(n)
        board.append(temp)

def play(goal=50, max_steps=1000, max_score=-100000, x=2, y=0):

    generate_new_board()

    draw_board(2, 0)

    for i in range(max_steps+1):
        pygame.event.pump()
        _, row, col = move(x, y)
        board[row][col] = board[row][col] + board[x][y]
        score = board[row][col]
        max_score = max(max_score, board[row][col])
        board[x][y] = random.randint(-1, 2)
        draw_board(row, col, score, max_score, goal, i)
        time.sleep(3/max_steps)
        x = row
        y = col

    print("Final Score:", score)
    print("Max Score: ", max_score)
    if score >= goal:
        draw_text(screen, "WIN!!", 150, (MARGIN + HEIGHT) * 4 + MARGIN + 100, 1)
        print("WIN!!")
    else:
        draw_text(screen, "LOSE!!", 150, (MARGIN + HEIGHT) * 4 + MARGIN + 100, 1)
        print("LOSE!!")

    clock.tick(500)
    pygame.display.flip()

def btn_onclick():
    play(int(goal.get()), int(steps.get()))

board = []                      #game board, 2D list
MAX, MIN = 10000, -10000        #initial values for beta and alpha respectively
root = None                     #root window for tkinter

BLACK = (0, 0, 0)               #colors for game GUI
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 400 // 8                #window size for game GUI
HEIGHT = 400 // 8
MARGIN = 5

WINDOW_SIZE = [400, 400]        #window size for tkinter window

if __name__ == "__main__":

    generate_new_board()

    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("game")

    numbers_font = pygame.font.SysFont("comicsansms", 30)
    text_font = pygame.font.SysFont("comicsansms", 30)

    done = False

    clock = pygame.time.Clock()

    draw_board(2, 0)

    window = tk.Tk()

    window.title("Python Tkinter Text Box")
    window.minsize(600, 400)

    label = ttk.Label(window, text="Goal:")
    label.grid(column=1, row=1)
    goal = tk.StringVar()
    goalEntered = ttk.Entry(window, width=15, textvariable=goal)
    goalEntered.grid(column=2, row=1)

    label2 = ttk.Label(window, text="Steps:")
    label2.grid(column=1, row=3)
    steps = tk.StringVar()
    stepsEntered = ttk.Entry(window, width=15, textvariable=steps)
    stepsEntered.grid(column=2, row=3)

    button = ttk.Button(window, text="Start", command=btn_onclick)
    button.grid(column=3, row=2)

    window.mainloop()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    pygame.quit()
