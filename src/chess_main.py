'''
Main driver file. Use for handling user input and displaying current game state object.
'''


import pygame as pygame
import chess_engine

# Board and square size
WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION

# Game max FPS
MAX_FPS = 15

# Store images 
IMAGES = {}

# Colors
WHITE_COLOR = pygame.Color('#ffffff')
BROWN_COLOR = pygame.Color('#813000')
'''
Initialize a global dictionary for storing all the images. This will be call only once in the main.
'''
def load_images():
    chessman_images = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for image in chessman_images:
        IMAGES[image] = pygame.transform.scale(pygame.image.load('../images/' + image + '.png'), (SQUARE_SIZE, SQUARE_SIZE))


'''
Main driver file.
'''    
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('white'))
    game_state = chess_engine.game_state()
    load_images()
    running = True
    while running:
        for p in pygame.event.get():
            if p.type == pygame.QUIT:
                running = False
            clock.tick(MAX_FPS)
            pygame.display.flip()  
            draw_game_state(screen, game_state)      


'''
Responsible for game graphics within current game state
'''
def draw_game_state(screen, game_state):
    draw_board(screen) 
    # add in chessman highlighting or move suggestions(later)
    draw_chess_box(screen, game_state.board) 
    

'''
Draw chess box on the board.
The top left square is always light.
'''
def draw_board(screen):
    colors = [pygame.Color(WHITE_COLOR), pygame.Color(BROWN_COLOR)]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


'''
Draw chessman on top of chess box the board
'''
def draw_chess_box(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            chessman = board[row][col]
            if chessman != '--':
                screen.blit(IMAGES[chessman], pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    

if __name__ == "__main__":
    main()