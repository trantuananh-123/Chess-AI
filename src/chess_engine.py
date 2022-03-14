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
        self.move_log = []
        
    def make_move(self, move):
        if self.board[move.start_row][move.start_col] != '--':
            self.board[move.start_row][move.start_col] = '--'
            self.board[move.end_row][move.end_col] = move.moved_chess_man
            # Log the move for undo or show history
            self.move_log.append(move)
            # Swap player
            self.white_turn = not self.white_turn
        
        
class move():
    # Chess notation
    ranksToRows = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    
    
    def __init__(self, start_pos, end_pos, board):
        self.start_row = start_pos[0]
        self.start_col = start_pos[1]
        self.end_row = end_pos[0]
        self.end_col = end_pos[1]
        self.moved_chess_man = board[self.start_row][self.start_col]
        self.captured_chess_man = board[self.end_row][self.end_col]
        
    def get_chess_notaion(self):
        # Add to make real chess notation
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)
    
    
    def get_rank_file(self, row, col):
        # file is vertical line on the board, rank is horizontal line on the board(ex: a1, b2, c3, d4, e5, f6, g7, h8)
        return self.colsToFiles[col] + self.rowsToRanks[row]