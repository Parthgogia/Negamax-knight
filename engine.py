import numpy as np;
class game_state():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["__","__","__","__","__","__","__","__",],
            ["__","__","__","__","__","__","__","__",],
            ["__","__","__","__","__","__","__","__",],
            ["__","__","__","__","__","__","__","__",],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.white_move = True
        self.move_log = []

    #doesn't work for pawn promotion, castling and en-passant
    def make_move(self,move):
        self.board[move.initial_row][move.initial_col] = "__"
        self.board[move.final_row][move.final_col] = move.piece_moved
        self.move_log.append(move)
        self.white_move = not self.white_move

    def undo_move(self):
        if len(self.move_log)!=0:
            move = self.move_log.pop()
            self.board[move.initial_row][move.initial_col] = move.piece_moved
            self.board[move.final_row][move.final_col] = move.piece_captured
            self.white_move = not self.white_move

    def get_legal_moves(self):
        return self.get_possible_moves()
    
    def get_possible_moves(self):
        moves =[Move((6,4),(4,4),self.board)]
        for r in range (len(self.board)):
            for c in range(len(self.board[r])):
                piece_color = self.board[r][c][0]
                if (piece_color=='w' and self.white_move) or (piece_color=='b' and not self.white_move):
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.get_pawn_moves(r,c,moves)
                    elif piece == 'Q':
                        self.get_queen_moves(r,c,moves)
                    elif piece == 'R':
                        self.get_rook_moves(r,c,moves)
                    elif piece == 'B':
                        self.get_bishop_moves(r,c,moves)
                    elif piece == 'N':
                        self.get_knight_moves(r,c,moves)
                    else:
                        self.get_king_moves(r,c,moves)
        return moves
    

    def get_pawn_moves(self,r,c,moves):
        pass
    def get_queen_moves(self,r,c,moves):
        pass
    def get_rook_moves(self,r,c,moves):
        pass
    def get_bishop_moves(self,r,c,moves):
        pass
    def get_knight_moves(self,r,c,moves):
        pass
    def get_king_moves(self,r,c,moves):
        pass
    







class Move():
    rows_to_ranks = {0:"8", 1:"7", 2:"6", 3:"5", 4:"4", 5:"3",6:"2", 7:"1"}
    ranks_to_rows = {a:b for a,b in rows_to_ranks.items()}
    cols_to_files = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}
    files_to_cols = {a:b for a,b in cols_to_files.items()}

    def __init__(self, initial_sq, final_sq, board):
        self.initial_row = initial_sq[0]
        self.initial_col = initial_sq[1]
        self.final_row = final_sq[0]
        self.final_col = final_sq[1]
        self.piece_moved = board[self.initial_row][self.initial_col]
        self.piece_captured = board[self.final_row][self.final_col]
        self.move_id = self.initial_row*1000+self.initial_col*100+self.final_row*10+self.final_col

    #operator overloading for equal to compare 2 moves
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.move_id == other.move_id
        return False

    def get_chess_square(self,r,c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
        
    def get_chess_move(self):
        return self.get_chess_square(self.initial_row,self.initial_col) + " -> "+self.get_chess_square(self.final_row,self.final_col)
