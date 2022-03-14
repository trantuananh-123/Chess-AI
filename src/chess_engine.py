'''
User for storing all the information about the current state of a chess game and determining the valid moves at the current state and keep a move log

White side:
    wR: white Rook
    wN: white Knight
    wB: white Bishop
    wQ: white Queen
    wK: white King
    wP: white Pawn

Black side:
    bR: black Rook
    bN: black Knight
    bB: black Bishop
    bQ: black Queen
    bK: black King
    bP: black Pawn
'''


class game_state():
    def __init__(self):
        # board is an 8x8 2 dimension list, each element has 2 characters.
        # The first character represent the color of the chessman.
        # The second character represent the type of the chessman.
        # '--' represent empty chess box on the board.
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.white_turn = True
        self.black_turn = False
        self.move_log = []