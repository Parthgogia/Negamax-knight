import random

piece_value = {'K':0, 'Q':9, 'N':3, 'B':3, 'R':5, 'P':1}
CHECKMATE = 10000
STALEMATE = 0
DEPTH = 3

#piece positional scores

knight_scores = [[1, 1, 1, 1, 1, 1, 1, 1],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1, 1, 1, 1, 1, 1, 1, 1]]

bishop_scores = [[4, 3, 2, 1, 1, 2, 3, 4],
                 [3, 4, 3, 2, 2, 3, 4, 3],
                 [2, 3, 4, 3, 3, 4, 3, 2],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [2, 3, 4, 3, 3, 4, 3, 2],
                 [3, 4, 3, 2, 2, 3, 4, 3],
                 [4, 3, 2, 1, 1, 2, 3, 4]]

rook_scores =  [[4, 3, 4, 4, 4, 4, 3, 4],
                [4, 4, 4, 4, 4, 4, 4, 4],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [4, 4, 4, 4, 4, 4, 4, 4],
                [4, 3, 4, 4, 4, 4, 3, 4]]

queen_scores =  [[1, 1, 1, 3, 1, 1, 1, 1],
                 [1, 2, 3, 3, 3, 1, 1, 1],
                 [1, 4, 3, 3, 3, 4, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 4, 3, 3, 3, 4, 2, 1],
                 [1, 1, 2, 3, 3, 1, 1, 1],
                 [1, 1, 1, 3, 1, 1, 1, 1]]

king_scores = [[1, 1, 5, 1, 1, 1, 5, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 1, 1, 1, 1, 1, 1],
               [1, 1, 5, 1, 1, 1, 5, 1]]

white_pawn_scores = [[9, 9, 9, 9, 9, 9, 9, 9],
                     [8, 8, 8, 8, 8, 8, 8, 8],
                     [5, 6, 6, 7, 7, 6, 6, 5],
                     [3, 4, 4, 5, 5, 4, 4, 3],
                     [1, 2, 3, 4, 4, 3, 2, 1],
                     [1, 1, 2, 3, 3, 2, 1, 1],
                     [1, 1, 1, 0, 0, 1, 1, 1],
                     [0, 0, 0, 0, 0, 0, 0, 0]]

black_pawn_scores = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [1, 1, 1, 0, 0, 1, 1, 1],
                     [1, 1, 2, 3, 3, 2, 1, 1],
                     [1, 2, 3, 4, 4, 3, 2, 1],
                     [3, 4, 4, 5, 5, 4, 4, 3],
                     [5, 6, 6, 7, 7, 6, 6, 5],
                     [8, 8, 8, 8, 8, 8, 8, 8],
                     [9, 9, 9, 9, 9, 9, 9, 9]]

piece_positional_value = {'K':king_scores, 'Q':queen_scores, 'N':knight_scores, 'B':bishop_scores, 'R':rook_scores, 'wP':white_pawn_scores, 'bP':black_pawn_scores}


def get_random_move(legal_moves):
    return random.choice(legal_moves)


def get_material_value(board):
    score =0
    for i in range(8):
        for j in range(8):
            color = board[i][j][0]
            piece = board[i][j][1]
            if color == 'w':
                score+= piece_value[piece]
            elif color == 'b':
                score-= piece_value[piece]
    return score


#positive is good for white, negative is good for black
def score_board(gs):
    if gs.checkmate:
        if gs.white_move:
            return -CHECKMATE
        else:
            return CHECKMATE
        
    elif gs.stalemate:
        return STALEMATE

    score =0
    for row in range(8):
        for col in range(8):
            square = gs.board[row][col]
            color = square[0]
            piece = square[1]
            if square != "__":
                #score on the basis of position
                piece_positional_score = 0
                if piece == 'P':
                    piece_positional_score = piece_positional_value[square][row][col]
                else:
                    piece_positional_score = piece_positional_value[piece][row][col]
                
                #score on the basis of material
                if color == 'w':
                    score += piece_value[piece] + piece_positional_score*0.1
                elif color == 'b':
                    score -= piece_value[piece] + piece_positional_score*0.1
    
    #score on the basis of number of legal moves,checks and pins
    if gs.white_move:
        score += gs.no_of_legal_moves * 0.01
        if gs.in_check:
            score-=1
        if len(gs.pins)>0:
            score-= len(gs.pins)*0.1
    else:
        score -= gs.no_of_legal_moves * 0.01
        if gs.in_check:
            score+=1
        if len(gs.pins)>0:
            score+= len(gs.pins)*0.1

    
    
    return score


def find_best_move(gs,legal_moves):
    turn_multiplier = 1 if gs.white_move else -1
    opponent_minmax_score = CHECKMATE
    best_player_move = None
    random.shuffle(legal_moves)
    for player_move in legal_moves:
        gs.make_move(player_move)
        opponent_moves = gs.get_legal_moves()
        if gs.stalemate:
            opponent_max_score = STALEMATE
        elif gs.checkmate:
            opponent_max_score = -CHECKMATE
        else:
            opponent_max_score = - CHECKMATE
            for opponent_move in opponent_moves:
                gs.make_move(opponent_move)
                gs.get_legal_moves()
                if gs.checkmate:
                    score = CHECKMATE
                elif gs.stalemate:
                    score = STALEMATE
                else:
                    score = -turn_multiplier*get_material_value(gs.board)

                if score>opponent_max_score:
                    opponent_max_score = score
                gs.undo_move()

        if opponent_max_score < opponent_minmax_score :
            opponent_minmax_score = opponent_max_score
            best_player_move = player_move        
            
        gs.undo_move()

    return best_player_move

#helper function to make first recursive call
def find_minmax_best_move(gs,legal_moves):
    global next_move
    next_move = None
    random.shuffle(legal_moves)
    get_minmax_move(gs,legal_moves,DEPTH,gs.white_move)
    return next_move


def get_minmax_move(gs,legal_moves,depth,white_to_move):
    global next_move

    if depth ==0:
        return score_board(gs)
    
    if white_to_move:
        max_score = -CHECKMATE #start at minimum score
        for move in legal_moves:
            gs.make_move(move)
            next_moves = gs.get_legal_moves()
            score = get_minmax_move(gs,next_moves,depth-1,False)
            if score>max_score:
                max_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return max_score


    else:
        min_score = CHECKMATE #start at the maximum score
        for move in legal_moves:
            gs.make_move(move)
            next_moves = gs.get_legal_moves()
            score = get_minmax_move(gs,next_moves,depth-1,True)
            if score<min_score:
                min_score = score
                if depth == DEPTH:
                    next_move = move
            gs.undo_move()
        return min_score


def find_negamax_best_move(gs,legal_moves):
    global next_move,counter
    next_move = None
    random.shuffle(legal_moves)
    counter=0
    get_negamax_move(gs,legal_moves,DEPTH, 1 if gs.white_move else -1)
    print(counter)
    return next_move


def get_negamax_move(gs,legal_moves,depth,turn_multiplier):
    global next_move,counter
    counter+=1
    if depth ==0:
        return turn_multiplier*score_board(gs)
    
    max_score = -CHECKMATE
    for move in legal_moves:
        gs.make_move(move)
        next_moves = gs.get_legal_moves()
        score = -get_negamax_move(gs,next_moves,depth-1,-turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        gs.undo_move()

    return max_score


def find_alpha_beta_best_move(gs,legal_moves):
    global next_move,counter
    next_move = None
    random.shuffle(legal_moves)
    counter=0
    get_alpha_beta_move(gs,legal_moves,DEPTH,-CHECKMATE,CHECKMATE, 1 if gs.white_move else -1)
    print(counter)
    return next_move

def get_alpha_beta_move(gs,legal_moves,depth,alpha,beta,turn_multiplier):
    global next_move,counter
    counter+=1
    if depth ==0:
        return turn_multiplier*score_board(gs)
    
    max_score = -CHECKMATE
    for move in legal_moves:
        gs.make_move(move)
        next_moves = gs.get_legal_moves()
        score = -get_alpha_beta_move(gs,next_moves,depth-1,-beta,-alpha,-turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
                print(move.get_chess_move(),score)
        gs.undo_move()

        if max_score>alpha: #pruning
            alpha = max_score
        if alpha>=beta:
            break

    return max_score