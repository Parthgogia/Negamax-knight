import random

piece_value = {'K':0, 'Q':9, 'N':3, 'B':3, 'R':5, 'P':1}
CHECKMATE = 10000
STALEMATE = 0
DEPTH = 3


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
    for i in range(8):
        for j in range(8):
            color = gs.board[i][j][0]
            piece = gs.board[i][j][1]
            if color == 'w':
                score+= piece_value[piece]
            elif color == 'b':
                score-= piece_value[piece]
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
        gs.undo_move()

        if max_score>alpha: #pruning
            alpha = max_score
        if alpha>=beta:
            break

    return max_score