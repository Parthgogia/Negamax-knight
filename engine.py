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
        self.move_functions = {'P':self.get_pawn_moves, 'R':self.get_rook_moves, 'N':self.get_knight_moves,
                              'Q': self.get_queen_moves, 'K':self.get_king_moves, 'B': self.get_bishop_moves}

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
        moves =[]
        for r in range (len(self.board)):
            for c in range(len(self.board[r])):
                piece_color = self.board[r][c][0]
                if (piece_color=='w' and self.white_move) or (piece_color=='b' and not self.white_move):
                    piece = self.board[r][c][1]
                    self.move_functions[piece](r,c,moves) #calling function for get the piece moves using dict
        return moves
    

    def get_pawn_moves(self,r,c,moves):
        if self.white_move: #white pawn moves
            
            if self.board[r-1][c]=="__": #forward moves
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=="__":
                    moves.append(Move((r,c),(r-2,c),self.board))

            if c-1>=0 and self.board[r-1][c-1][0]=='b': #left captures
                moves.append(Move((r,c),(r-1,c-1),self.board))

            if c+1<=7 and self.board[r-1][c+1][0]=='b': #right captures
                moves.append(Move((r,c),(r-1,c+1),self.board))


        else: #black pawn moves
            
            if self.board[r+1][c]=="__": #forward moves
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=="__":
                    moves.append(Move((r,c),(r+2,c),self.board))

            if c-1>=0 and self.board[r+1][c-1][0]=='w': #right captures
                moves.append(Move((r,c),(r+1,c-1),self.board))

            if c+1<=7 and self.board[r+1][c+1][0]=='w': #left captures
                moves.append(Move((r,c),(r+1,c+1),self.board))

        #pawn promotion and en passant moves are yet to to be generated

    
    def get_rook_moves(self,r,c,moves):
        directions = ((1,0),(-1,0),(0,1),(0,-1))
        enemy_color = 'b' if self.white_move else 'w'

        for d in directions:
            for i in range(1,8):
                final_row = r + d[0]*i
                final_col = c + d[1]*i

                if 0<=final_row<8 and 0<=final_col<8:
                    end_piece = self.board[final_row][final_col]

                    if end_piece == '__': #can move to empty space
                        moves.append(Move((r,c),(final_row,final_col),self.board))
                    elif end_piece[0] == enemy_color: #can capture an enemy piece
                        moves.append(Move((r,c),(final_row,final_col),self.board))
                        break   #cannot move further in that direction
                    else:
                        break # neither capture nor move further in that direction

                else:
                    break #out of bounds




    def get_bishop_moves(self,r,c,moves):
        directions = ((1,1),(-1,-1),(-1,1),(1,-1))
        enemy_color = 'b' if self.white_move else 'w'

        for d in directions:
            for i in range(1,8):
                final_row = r + d[0]*i
                final_col = c + d[1]*i

                if 0<=final_row<8 and 0<=final_col<8:
                    end_piece = self.board[final_row][final_col]

                    if end_piece == '__': #can move to empty space
                        moves.append(Move((r,c),(final_row,final_col),self.board))
                    elif end_piece[0] == enemy_color: #can capture an enemy piece
                        moves.append(Move((r,c),(final_row,final_col),self.board))
                        break   #cannot move further in that direction
                    else:
                        break # neither capture nor move further in that direction

                else:
                    break #out of bounds

    def get_queen_moves(self,r,c,moves):
        self.get_bishop_moves(r,c,moves)
        self.get_rook_moves(r,c,moves)



    def get_knight_moves(self,r,c,moves):
        knight_moves = ((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2))
        for move in knight_moves:
            if 0<=r+move[0]<8 and 0<=c+move[1]<8:

                if self.white_move and self.board[r+move[0]][c+move[1]][0] !='w': #white knight moves
                    moves.append(Move((r,c),(r+move[0],c+move[1]),self.board))

                elif not self.white_move and self.board[r+move[0]][c+move[1]][0] !='b': #black knight moves
                    moves.append(Move((r,c),(r+move[0],c+move[1]),self.board))


    def get_king_moves(self,r,c,moves):
        king_moves= ((-1,-1),(-1,0),(-1,1),(1,-1),(1,0),(1,1),(0,-1),(0,1))
        piece_color = 'w' if self.white_move else 'b'

        for i in range(8):
            final_row = r + king_moves[i][0]
            final_col = c + king_moves[i][1]
            if 0<=final_row<8 and 0<=final_col<8:
                end_piece = self.board[final_row][final_col]
                if end_piece[0] != piece_color: #end piece should not be of the same color as king
                    moves.append(Move((r,c),(final_row,final_col),self.board))
 
        
    


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
