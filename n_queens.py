import threading
import time, sys

import pygame
pygame.init()
pygame.display.set_caption('Eight Queens')

N = 8 # Grid number
GRID_SIZE = 50
TEXT_HEIGHT = 30
LIGHT_COLOR = (255, 206, 158)
DARK_COLOR = (209, 139, 71)
queen_img = pygame.image.load('./images/queen.png')
queen_img = pygame.transform.scale(queen_img, (GRID_SIZE, GRID_SIZE))
golden_queen_img = pygame.image.load('./images/queen2.png')
golden_queen_img = pygame.transform.scale(golden_queen_img, (GRID_SIZE, GRID_SIZE))
# Set up the drawing window
screen = pygame.display.set_mode([GRID_SIZE * N, GRID_SIZE * N + TEXT_HEIGHT])
font = pygame.font.SysFont("Arial", int(TEXT_HEIGHT * 0.8))

def draw_board():
    # Fill the background with white
    screen.fill((255, 255, 255))
    for i in range(N):
        for j in range(N):
            color = LIGHT_COLOR if (i + j) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(screen, color, (i * GRID_SIZE, j * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    text = font.render('Number of solutions: 0', True, (0, 0, 0))
    screen.blit(text, (0, GRID_SIZE * N))
    pygame.display.flip()

def place_queen(i, j):
    screen.blit(queen_img, (i * GRID_SIZE, j * GRID_SIZE))
    pygame.display.flip()
    time.sleep(.1)

def remove_queen(i, j):
    color = LIGHT_COLOR if (i + j) % 2 == 0 else DARK_COLOR
    pygame.draw.rect(screen, color, (i * GRID_SIZE, j * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.display.flip()
    time.sleep(.1)
    
def flip_solution(queen_set, queen_img):
    for i, j in queen_set:
        color = LIGHT_COLOR if (i + j) % 2 == 0 else DARK_COLOR
        pygame.draw.rect(screen, color, (i * GRID_SIZE, j * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        screen.blit(queen_img, (i * GRID_SIZE, j * GRID_SIZE))
    pygame.display.flip()
    
def run_n_queens():
    n_solutions = 0
    col_set = set()
    diag_set = set()
    anti_diag_set = set()
    queen_set = set()
    def dfs(row):
        nonlocal n_solutions
        for col in range(N):
            diag = row - col
            anti_diag = row + col
            if col not in col_set and diag not in diag_set and anti_diag not in anti_diag_set:
                queen_set.add((col, row))
                place_queen(col, row)
                if row < N - 1:
                    col_set.add(col)
                    diag_set.add(diag)
                    anti_diag_set.add(anti_diag)
                    dfs(row + 1)
                    col_set.discard(col)
                    diag_set.discard(diag)
                    anti_diag_set.discard(anti_diag)
                else: # Come to a solution
                    n_solutions += 1
                    try:
                        pygame.draw.rect(screen, (255, 255, 255), (0, GRID_SIZE * N, GRID_SIZE * N, TEXT_HEIGHT))
                        text = font.render('Number of solutions: {}'.format(n_solutions), True, (0, 0, 0))
                        screen.blit(text, (0, GRID_SIZE * N))
                        pygame.display.flip()
                        flip_solution(queen_set, golden_queen_img)
                        time.sleep(1)
                        flip_solution(queen_set, queen_img)
                    except pygame.error:
                        sys.exit(0)
                queen_set.discard((col, row))
                remove_queen(col, row)
                
    dfs(0)

if __name__ == '__main__':
    
    draw_board()
    
    threading.Thread(target=run_n_queens, daemon=True).start()
    
    # Run until the user asks to quit
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break
    
    # Done! Time to quit.
    pygame.quit()