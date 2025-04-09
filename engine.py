import copy

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
        self.white_king_location = (7,4)
        self.black_king_location = (0,4)
        self.in_check = False
        self.pins = []
        self.checks = []
        self.current_castling_rights = castling_rights(True,True,True,True)
        self.castling_rights_log = [copy.deepcopy(self.current_castling_rights)]
        self.enpassant_square = () #stores the coordinates of a square at which enpassant is possible
        self.enpassant_possible_log = [self.enpassant_square]
        self.checkmate = False
        self.stalemate = False
        

    #doesn't work for pawn promotion, castling and en-passant
    def make_move(self,move):
        self.board[move.initial_row][move.initial_col] = "__"
        self.board[move.final_row][move.final_col] = move.piece_moved
        self.move_log.append(move)
        self.white_move = not self.white_move
        
        if move.piece_moved == 'wK':
            self.white_king_location = (move.final_row,move.final_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.final_row,move.final_col)

        #castle move
        if move.is_castle_move:
            if move.final_col-move.initial_col ==2: #king side castle
                self.board[move.final_row][move.final_col-1] = self.board[move.final_row][move.final_col+1] #copy the rook to new location
                self.board[move.final_row][move.final_col+1] = "__" # remove the old rook

            else: #queen side castle
                self.board[move.final_row][move.final_col+1] = self.board[move.final_row][move.final_col-2] #copy the rook to new location
                self.board[move.final_row][move.final_col-2] = "__" # remove the old rook
        
        #pawn promotion move
        if move.is_pawn_promotion:
            # promotion_choice = input("Promote to Q, R, B or N: ")
            promotion_choice = 'Q'          
            self.board[move.final_row][move.final_col] = move.piece_moved[0] + promotion_choice

        #en passant move
        if move.is_enpassant_move:
            self.board[move.initial_row][move.final_col] = "__"

        #update the castling rights 
        self.update_castling_rights(move)

        #update the en passant square
        if move.piece_moved[1] == 'P' and abs(move.initial_row - move.final_row) == 2:
            self.enpassant_square = ((move.initial_row + move.final_row)//2,move.initial_col)
        else:
            self.enpassant_square = ()

        #update en passant rights log
        self.enpassant_possible_log.append(self.enpassant_square)
        


    def undo_move(self):
        if len(self.move_log)!=0:
            move = self.move_log.pop()
            self.board[move.initial_row][move.initial_col] = move.piece_moved
            self.board[move.final_row][move.final_col] = move.piece_captured
            self.white_move = not self.white_move

            if move.piece_moved == 'wK':
                self.white_king_location = (move.initial_row,move.initial_col)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.initial_row,move.initial_col)

            #undo castle move
            if move.is_castle_move:
                if move.final_col-move.initial_col ==2: #king side castle
                    self.board[move.final_row][move.final_col+1] = self.board[move.final_row][move.final_col-1]
                    self.board[move.final_row][move.final_col-1] = "__"
                else:
                    self.board[move.final_row][move.final_col-2] = self.board[move.final_row][move.final_col+1]
                    self.board[move.final_row][move.final_col+1] = "__"
                
            #undo en passant move
            if move.is_enpassant_move:
                self.board[move.final_row][move.final_col] = "__"
                self.board[move.initial_row][move.final_col] = move.piece_captured

            #undo the castling rights
            self.castling_rights_log.pop()
            self.current_castling_rights = copy.deepcopy(self.castling_rights_log[-1])

            #update the en passant square
            self.enpassant_possible_log.pop()
            self.enpassant_square = self.enpassant_possible_log[-1]
                
            #update checkmate and stalemate flags
            self.checkmate = False
            self.stalemate = False


    #castling rights change when a rook or king moves, or rook is captured
    def update_castling_rights(self,move):
        if move.piece_moved == 'wK':
            self.current_castling_rights.wks = False
            self.current_castling_rights.wqs = False
        
        elif move.piece_moved == 'bK':
            self.current_castling_rights.bks = False
            self.current_castling_rights.bqs = False
        
        elif move.piece_moved == 'wR':
            if move.initial_row == 7 and move.initial_col == 0:
                self.current_castling_rights.wqs = False
            elif move.initial_row == 7 and move.initial_col == 7:
                self.current_castling_rights.wks = False

        elif move.piece_moved == 'bR':
            if move.initial_row == 0 and move.initial_col == 0:
                self.current_castling_rights.bqs = False
            elif move.initial_row == 0 and move.initial_col == 7:
                self.current_castling_rights.bks = False

        if move.piece_captured == 'wR':
            if move.final_row == 7:
                if move.final_col == 0:
                    self.current_castling_rights.wqs = False
                elif move.final_col == 7:
                    self.current_castling_rights.wks = False
        
        elif move.piece_captured == "bR":
            if move.final_row == 0:
                if move.final_col == 0:
                    self.current_castling_rights.bqs = False
                elif move.final_col == 7:
                    self.current_castling_rights.bks = False
   
                
        
        self.castling_rights_log.append(copy.deepcopy(self.current_castling_rights))
    

    def get_legal_moves(self):
        moves = []
        self.in_check,self.pins,self.checks =self.check_for_pins_and_checks()
        king_row,king_col = (self.white_king_location[0],self.white_king_location[1]) if self.white_move else \
                            (self.black_king_location[0],self.black_king_location[1])
        
        if self.in_check:
            if len(self.checks)==1: #only one piece attacking the king -> block or move king or capture
                moves = self.get_possible_moves()
                check = self.checks[0] #check info
                check_row,check_col = check[0],check[1]
                piece_attacking = self.board[check_row][check_col]

                valid_squares = []
                # incase of a knight, cannot block check -> either capture or move king
                if piece_attacking[1] == 'N': 
                    valid_squares = [(check_row,check_col)]
                else:
                    #generate row,col to which a piece can be moved to that blocks the check or capture attacking piece
                    for i in range(1,8):
                        valid_square = (king_row + check[2]*i, king_col + check[3]*i) #check[2],check[3] are the row,col direction of check
                        valid_squares.append(valid_square)  #will also include captures since loop breaks after reaching the attacking piece
                        if valid_square[0] == check_row and valid_square[1] == check_col: #reached the piece that is attacking the king
                            break
                
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].piece_moved[1] !='K': #if king isn't moved, you must block or capture
                        if not (moves[i].final_row,moves[i].final_col) in valid_squares:
                            moves.remove(moves[i])
            
            else: #double check ->king must move
                self.get_king_moves(king_row,king_col,moves)

        else: #not in check
            moves = self.get_possible_moves()

        if len(moves) == 0 and self.in_check:
            self.checkmate = True
        elif len(moves)==0:
            self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return moves

    def check_for_pins_and_checks(self):
        pins = []
        checks = []
        in_check = False
        if self.white_move:
            enemy_color = 'b'
            my_color = 'w'
            initial_row = self.white_king_location[0]
            initial_col = self.white_king_location[1]
        else:
            enemy_color = 'w'
            my_color = 'b'
            initial_row = self.black_king_location[0]
            initial_col = self.black_king_location[1]

        directions = ((1,0),(-1,0),(0,1),(0,-1),(-1,-1),(-1,1),(1,1),(1,-1))

        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1,8):
                final_row = initial_row +d[0]*i
                final_col = initial_col +d[1]*i
                if 0<=final_row<8 and 0<=final_col<8:
                    end_piece = self.board[final_row][final_col]

                    if end_piece[0]==my_color and end_piece[1]!='K' : #piece is of same color as king
                        if possible_pin == ():
                            possible_pin = (final_row,final_col,d[0],d[1])
                        else: #there is already an ally piece in this direction, hence no pins in this direction
                            break
                    
                    elif end_piece[0] == enemy_color:
                        type = end_piece[1]
                        """
                        1) check for rook attacking the king in directions 0-3
                        2) check for bishop attacking the king in directions 4-7
                        3) check for queen attacking the king in all directions
                        4) check for king attacking king in all directions but only one square (to avoid kings being moved next to each other)
                        5) check for pawn attacking king in direction specific to color but only one sqaure
                        6) checks from knights are handled separately afterwards
                        """
                        if(0<=j<=3 and type =='R') or \
                            (4<=j<=7 and type =='B') or \
                            (type =='Q') or \
                            (i==1 and type == 'K') or \
                            (i==1 and type == 'P' and ((enemy_color=='w' and 6<=j<=7) or (enemy_color =='b' and 4<=j<=5))):
                            
                            if possible_pin == (): #no piece blocking check
                                in_check = True
                                checks.append((final_row,final_col,d[0],d[1]))
                                break  #no more checks in this direction

                            else: #a piece is blocking the check
                                pins.append(possible_pin)
                                break
                        
                        else: #there are no checks possible
                            break 


                else: #out of bounds
                    break
            
        #knight checks
        knight_moves = ((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2))
        for move in knight_moves:
            final_row = initial_row + move[0]
            final_col = initial_col + move[1]
            if 0<=final_row<8 and 0<=final_col<8:
                end_piece = self.board[final_row][final_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N':
                    in_check = True
                    checks.append((final_row,final_col,move[0],move[1]))

        return in_check,pins,checks



    def sqaure_under_attack(self,r,c,ally_color):
        enemy_color = 'b' if ally_color == 'w' else 'w'
        directions = ((1,0),(-1,0),(0,1),(0,-1),(-1,-1),(-1,1),(1,1),(1,-1))

        for j in range(len(directions)):
            d = directions[j]
            for i in range(1, 8):
                final_row = r + d[0] * i
                final_col = c + d[1] * i

                if 0<=final_row<8 and 0<=final_col<8:
                    end_piece = self.board[final_row][final_col]
                    if end_piece[0] == ally_color:
                        break
                    elif end_piece[0] == enemy_color:
                        type = end_piece[1]
                        """
                        Possibilities
                        1) Rook in any orthogonal directions
                        2) Bishop in any diagonal
                        3) Queen in orthogonal or diagonal directions
                        4) King in any direction to 1 square (to prevent king move controlled by another king)
                        5) Pawn if one square away in any diagonal
                        """
                        if(0<=j<=3 and type =='R') or \
                            (4<=j<=7 and type =='B') or \
                            (type =='Q') or \
                            (i==1 and type == 'K') or \
                            (i==1 and type == 'P' and ((enemy_color=='w' and 6<=j<=7) or (enemy_color =='b' and 4<=j<=5))):
                            return True
                        else: #no attacks in this direction
                            break
                else: #out of bounds
                    break    
                
    
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
        is_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                is_pinned = True
                pin_direction = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break


        if self.white_move: #white pawn moves
            
            if self.board[r-1][c]=="__": #forward moves
                if not is_pinned or pin_direction == (-1,0):
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if r==6 and self.board[r-2][c]=="__":
                        moves.append(Move((r,c),(r-2,c),self.board))

            if not is_pinned or pin_direction == (-1,-1):
                if c-1>=0 and self.board[r-1][c-1][0]=='b': #left captures
                    moves.append(Move((r,c),(r-1,c-1),self.board))
                elif c-1>=0 and (r-1,c-1) == self.enpassant_square: #left en passant captures
                    moves.append(Move((r,c),(r-1,c-1),self.board,is_enpassant_move=True))


            if not is_pinned or pin_direction == (-1,1):
                if c+1<=7 and self.board[r-1][c+1][0]=='b': #right captures       
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                elif c+1<=7 and (r-1,c+1) == self.enpassant_square: #right en passant captures
                    moves.append(Move((r,c),(r-1,c+1),self.board,is_enpassant_move=True))


        else: #black pawn moves
            
            if self.board[r+1][c]=="__": #forward moves
                if not is_pinned or pin_direction == (1,0):
                    moves.append(Move((r,c),(r+1,c),self.board))
                    if r==1 and self.board[r+2][c]=="__":
                        moves.append(Move((r,c),(r+2,c),self.board))

            if not is_pinned or pin_direction == (1,-1):
                if c-1>=0 and self.board[r+1][c-1][0]=='w': #right captures       
                    moves.append(Move((r,c),(r+1,c-1),self.board))
                elif c-1>=0 and (r+1,c-1) == self.enpassant_square: #right en passant captures
                    moves.append(Move((r,c),(r+1,c-1),self.board,is_enpassant_move=True))


            if not is_pinned or pin_direction == (1,1):
                if c+1<=7 and self.board[r+1][c+1][0]=='w': #left captures
                    moves.append(Move((r,c),(r+1,c+1),self.board))
                elif c+1<=7 and (r+1,c+1) == self.enpassant_square: #left en passant captures
                    moves.append(Move((r,c),(r+1,c+1),self.board,is_enpassant_move=True))        


    
    def get_rook_moves(self,r,c,moves):
        is_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                is_pinned = True
                pin_direction = (self.pins[i][2],self.pins[i][3])
                if self.board[r][c][1] !='Q': #queen moves function uses rook and bishop moves so only remove it in bishop moves
                    self.pins.remove(self.pins[i])
                break


        directions = ((1,0),(-1,0),(0,1),(0,-1))
        enemy_color = 'b' if self.white_move else 'w'

        for d in directions:
            for i in range(1,8):
                final_row = r + d[0]*i
                final_col = c + d[1]*i

                if 0<=final_row<8 and 0<=final_col<8:
                    if not is_pinned or pin_direction == d or pin_direction == (-d[0],-d[1]): #can move both towards the pin and away from the pin

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
        is_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                is_pinned = True
                pin_direction = (self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((1,1),(-1,-1),(-1,1),(1,-1))
        enemy_color = 'b' if self.white_move else 'w'

        for d in directions:
            for i in range(1,8):
                final_row = r + d[0]*i
                final_col = c + d[1]*i

                if 0<=final_row<8 and 0<=final_col<8:
                    if not is_pinned or pin_direction == d or pin_direction == (-d[0],-d[1]): #can move both towards the pin and away from the pin

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
        self.get_rook_moves(r,c,moves)
        self.get_bishop_moves(r,c,moves)


    def get_knight_moves(self,r,c,moves):
        is_pinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                is_pinned = True
                self.pins.remove(self.pins[i])
                break

        knight_moves = ((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2))
        for move in knight_moves:
            if 0<=r+move[0]<8 and 0<=c+move[1]<8:
                if not is_pinned:
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

                    #place the king on final sqaure and check for checks
                    if piece_color == 'w':
                        self.white_king_location = (final_row,final_col) 
                    else :
                        self.black_king_location = (final_row,final_col)

                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((r,c),(final_row,final_col),self.board))
                    
                    #place the king back on the original square
                    if piece_color == 'w':
                        self.white_king_location = (r,c)                    
                    else:
                        self.black_king_location = (r,c)
        
        self.get_castle_moves(r,c,moves,piece_color)



    def get_castle_moves(self,r,c,moves,piece_color):

        in_check = self.sqaure_under_attack(r,c,piece_color)
        if in_check:
            return #append no moves as the king is in check
        
        if (self.white_move and self.current_castling_rights.wks) or (not self.white_move and self.current_castling_rights.bks):
            self.get_kingside_castle_moves(r,c,moves,piece_color)
        
        if (self.white_move and self.current_castling_rights.wqs) or (not self.white_move and self.current_castling_rights.bqs):
            self.get_queenside_castle_moves(r,c,moves,piece_color)

        
    
    def get_kingside_castle_moves(self,r,c,moves,piece_color):
        if self.board[r][c+1] == '__' and self.board[r][c+2] == "__":
            if not self.sqaure_under_attack(r,c+1,piece_color) and not self.sqaure_under_attack(r,c+2,piece_color):
                moves.append(Move((r,c),(r,c+2),self.board,is_castle_move = True))




    def get_queenside_castle_moves(self,r,c,moves,piece_color):
        if self.board[r][c-1] == '__' and self.board[r][c-2] == "__" and self.board[r][c-3] == "__":
            if not self.sqaure_under_attack(r,c-1,piece_color) and not self.sqaure_under_attack(r,c-2,piece_color):
                moves.append(Move((r,c),(r,c-2),self.board,is_castle_move = True))
    
        

class castling_rights():
    def __init__(self,wks,bks,wqs,bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs



class Move():
    rows_to_ranks = {0:"8", 1:"7", 2:"6", 3:"5", 4:"4", 5:"3",6:"2", 7:"1"}
    ranks_to_rows = {a:b for a,b in rows_to_ranks.items()}
    cols_to_files = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}
    files_to_cols = {a:b for a,b in cols_to_files.items()}

    def __init__(self, initial_sq, final_sq, board, is_castle_move= False, is_enpassant_move = False):
        self.initial_row = initial_sq[0]
        self.initial_col = initial_sq[1]
        self.final_row = final_sq[0]
        self.final_col = final_sq[1]
        self.piece_moved = board[self.initial_row][self.initial_col]
        self.piece_captured = board[self.final_row][self.final_col]
        self.move_id = self.initial_row*1000+self.initial_col*100+self.final_row*10+self.final_col
        
        #flag for castling move
        self.is_castle_move = is_castle_move

        #flag for pawn promotion move
        self.is_pawn_promotion = (self.piece_moved == "wP" and self.final_row == 0) or (self.piece_moved == "bP" and self.final_row == 7)

        #flag for en passant move
        self.is_enpassant_move = is_enpassant_move

        if self.is_enpassant_move:
            self.piece_captured = "wP" if self.piece_moved == "bP" else "bP"

    #operator overloading for equal to compare 2 moves
    def __eq__(self, other):
        if isinstance(other,Move):
            return self.move_id == other.move_id
        return False

    def get_chess_square(self,r,c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
        
    def get_chess_move(self):
        return self.get_chess_square(self.initial_row,self.initial_col) + " -> "+self.get_chess_square(self.final_row,self.final_col)