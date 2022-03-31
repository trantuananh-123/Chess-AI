"""User for storing all the information about the current state of a chess game and determining the valid moves at
the current state and keep a move log

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
"""


class game_state:
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
        self.is_checked = False
        self.move_log = []
        self.move_function = {'P': self.pawn_move, 'R': self.rook_move, 'N': self.knight_move, 'B': self.bishop_move,
                              'Q': self.queen_move, 'K': self.king_move}
        self.wK_location = (7, 4)
        self.bK_location = (0, 4)
        self.check_mate = False
        self.stale_mate = False

    # Take move as a parameter and execute the move on the board(Not working for castling, pawn promotion and
    # en-passant).
    def make_move(self, move):
        if self.board[move.start_row][move.start_col] != '--':
            self.board[move.start_row][move.start_col] = '--'
            self.board[move.end_row][move.end_col] = move.moved_chess_man
            # Log the move for undo or show history
            self.move_log.append(move)
            # Swap player
            self.white_turn = not self.white_turn
            # Update king location
            if move.moved_chess_man == 'wK':
                self.wK_location = (move.end_row, move.end_col)
            if move.moved_chess_man == 'bK':
                self.bK_location = (move.end_row, move.end_col)

    # Undo the last chess man's move
    def undo_move(self):
        # Make sure there is move to undo
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.moved_chess_man
            self.board[move.end_row][move.end_col] = move.captured_chess_man
            self.white_turn = not self.white_turn
            # Update king location
            if move.moved_chess_man == 'wK':
                self.wK_location = (move.start_row, move.start_col)
            if move.moved_chess_man == 'bK':
                self.bK_location = (move.start_row, move.start_col)

    # All move with considering checks
    def valid_move(self):
        # 1. Generate all possible moves
        moves = self.possible_move()
        # 2. Make the move for each possible move
        for i in range(len(moves) - 1, -1, -1):  # Back an index after remove an element
            self.make_move(moves[i])
            # 3. Generate all enemy's possible moves
            enemy_moves = self.possible_move()
            # 4. For each enemy move check if your king is being attacked
            self.white_turn = not self.white_turn
            if self.in_check():
                # 5. If your king is being attacked --> not a valid move
                moves.remove(moves[i])
            self.white_turn = not self.white_turn
            self.undo_move()
        if len(moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = False
            self.stale_mate = False
        return moves

    # Determine if current player is in check
    def in_check(self):
        if self.white_turn:
            return self.under_attack(self.wK_location[0], self.wK_location[1])
        return self.under_attack(self.bK_location[0], self.bK_location[1])

    # Determine if enemy can attack the chess box
    def under_attack(self, row, col):
        self.white_turn = not self.white_turn
        enemy_moves = self.possible_move()
        self.white_turn = not self.white_turn
        for move in enemy_moves:
            if move.end_row == row and move.end_col == col:
                return True
        return False

    # All move without considering checks
    def possible_move(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.white_turn) or (turn == 'b' and not self.white_turn):
                    chess_man = self.board[row][col][1]
                    self.move_function[chess_man](row, col, moves)
        return moves

    # Get pawn at location row and col possible move and add to moves[]
    def pawn_move(self, row, col, moves):
        if self.white_turn:
            if row - 1 >= 0:
                if self.board[row - 1][col] == '--':
                    moves.append(move((row, col), (row - 1, col), self.board))
                    if row == 6 and self.board[row - 2][col] == '--':
                        moves.append(move((row, col), (row - 2, col), self.board))
                if col - 1 >= 0:
                    if self.board[row - 1][col - 1][0] == 'b':
                        moves.append(move((row, col), (row - 1, col - 1), self.board))
                if col + 1 < 8:
                    if self.board[row - 1][col + 1][0] == 'b':
                        moves.append(move((row, col), (row - 1, col + 1), self.board))
        else:
            if row + 1 < 8:
                if self.board[row + 1][col] == '--':
                    moves.append(move((row, col), (row + 1, col), self.board))
                    if row == 1 and self.board[row + 2][col] == '--':
                        moves.append(move((row, col), (row + 2, col), self.board))
                if col - 1 >= 0:
                    if self.board[row + 1][col - 1][0] == 'w':
                        moves.append(move((row, col), (row + 1, col - 1), self.board))
                if col + 1 < 8:
                    if self.board[row + 1][col + 1][0] == 'w':
                        moves.append(move((row, col), (row + 1, col + 1), self.board))

    # Get rook at location row and col possible move and add to moves[]
    def rook_move(self, row, col, moves):
        # up, down, left, right
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        enemy_color = 'b' if self.white_turn else 'w'
        for direction in directions:
            for i in range(1, 8):
                end_row = row + i * direction[0]
                end_col = col + i * direction[1]
                if end_row < 0 or end_row >= 8 or end_col < 0 or end_col >= 8:
                    break
                elif self.board[end_row][end_col] == '--':
                    moves.append(move((row, col), (end_row, end_col), self.board))
                elif self.board[end_row][end_col][0] == enemy_color:
                    moves.append(move((row, col), (end_row, end_col), self.board))
                    break
                else:
                    break

    # Get knight at location row and col possible move and add to moves[]
    def knight_move(self, row, col, moves):
        directions = ((-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1))
        ally_color = 'w' if self.white_turn else 'b'
        for i in range(8):
            end_row = row + directions[i][0]
            end_col = col + directions[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                chess_man = self.board[end_row][end_col]
                if chess_man[0] != ally_color:
                    moves.append(move((row, col), (end_row, end_col), self.board))

    # Get bishop at location row and col possible move and add to moves[]
    def bishop_move(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'b' if self.white_turn else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = row + i * d[0]
                end_col = col + i * d[1]
                if end_row < 0 or end_row >= 8 or end_col < 0 or end_col >= 8:
                    break
                elif self.board[end_row][end_col] == '--':
                    moves.append(move((row, col), (end_row, end_col), self.board))
                elif self.board[end_row][end_col][0] == enemy_color:
                    moves.append(move((row, col), (end_row, end_col), self.board))
                    break
                else:
                    break

    # Get queen at location row and col possible move and add to moves[]
    def queen_move(self, row, col, moves):
        self.rook_move(row, col, moves)
        self.bishop_move(row, col, moves)

    # Get king at location row and col possible move and add to moves[]
    def king_move(self, row, col, moves):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        ally_color = 'w' if self.white_turn else 'b'
        for i in range(8):
            end_row = row + directions[i][0]
            end_col = col + directions[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                chess_man = self.board[end_row][end_col]
                if chess_man[0] != ally_color:
                    moves.append(move((row, col), (end_row, end_col), self.board))


class move:
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

    # Overide equal method
    def __eq__(self, object):
        if isinstance(object, move):
            return self.start_row == object.start_row and self.start_col == object.start_col and self.end_row == object.end_row and self.end_col == object.end_col

    def get_chess_notaion(self):
        # Add to make real chess notation
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        # file is vertical line on the board, rank is horizontal line on the board(ex: a1, b2, c3, d4, e5, f6, g7, h8)
        return self.colsToFiles[col] + self.rowsToRanks[row]
