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
        # Load images from images folder and scale them to fit the chess box
        IMAGES[image] = pygame.transform.scale(pygame.image.load('../images/' + image + '.png'), (SQUARE_SIZE, SQUARE_SIZE))  


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
            # Follow the chess board 2 dimension array index to get the color
            color = colors[((row + col) % 2)]
            # Draw a rectangle with the color to the screen(surface) with the size of the chess box from left to right and top to bottom
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


'''
Draw chessman on top of chess box the board
'''
def draw_chess_box(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            chessman = board[row][col]
            if chessman != '--':
                # Draw chessman onto corresponding chess box
                screen.blit(IMAGES[chessman], pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    


'''
Main driver file.
'''    
def main():
    # Safely initialize all imported pygame modules
    pygame.init()
    # Initialize a window or screen for displaying content
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    square = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
    # Create an object to help track time
    clock = pygame.time.Clock()
    # Fill surface with color
    screen.fill(pygame.Color(WHITE_COLOR))
    # Get the current game state
    game_state = chess_engine.game_state()
    # Load images
    load_images()
    # Selected chess box, keep track of the last click of user(tuple: (row, col))
    selected_chess_box = ()
    # Keep track of player clicks(two tuples: [(), ()])
    player_clicks = []
    # Main game loop
    running = True
    while running:
        for p in pygame.event.get():
            if p.type == pygame.QUIT:
                running = False
            if p.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse location (x, y)
                location = pygame.mouse.get_pos()
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                # If the user click the same chess box twice
                if selected_chess_box == (row, col):
                    # Make the selected chess box unselected
                    selected_chess_box = ()
                    # Clear the player clicks
                    player_clicks = []
                else:
                    selected_chess_box = (row, col)
                    # Append first chess box and second chess box to the player clicks
                    player_clicks.append(selected_chess_box)
                if len(player_clicks) == 2:
                    move = chess_engine.move(player_clicks[0], player_clicks[1], game_state.board)
                    print(move.get_chess_notaion())
                    game_state.make_move(move)
                    # Reset the player clicks
                    selected_chess_box = ()
                    player_clicks = []
            # Update the clock and limit the program to run < MAX_FPS frame per second
            clock.tick(MAX_FPS)
            # Update the full display surface to the screen
            pygame.display.flip()
            draw_game_state(screen, game_state)    
            
            
if __name__ == "__main__":
    main()