from engine import game_state,Move
import pygame as p
from algorithms import get_random_move,find_alpha_beta_best_move

BOARD_WIDTH = BOARD_HEIGHT = 672
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 30
IMAGES = {}

#Green board
LIGHT_SQUARE_COLOR = (237, 238, 209)
DARK_SQUARE_COLOR = (119, 153, 82)
PIECE_SELECTED_COLOR = (180, 10, 60)
PIECE_MOVES_COLOR = (100, 149, 237)

"""
# Brown board
LIGHT_SQUARE_COLOR = (240, 217, 181)
DARK_SQUARE_COLOR = (181, 136, 99)
PIECE_SELECETED_COLOR = (84, 115, 161)
PIECE_MOVES_COLOR = (100, 149, 237)
"""

"""
#Gray board
LIGHT_SQUARE_COLOR = (220, 220, 220)
DARK_SQUARE_COLOR = (130, 130, 130)
PIECE_SELECETED_COLOR = (84, 115, 161)
PIECE_MOVES_COLOR = (100, 149, 237)
"""

colors = [p.Color(LIGHT_SQUARE_COLOR), p.Color(DARK_SQUARE_COLOR)]


def load_images():
    pieces = ["bR","bN","bB","bQ","bK","bP","wR","wN","wB","wQ","wK","wP"]
    for piece in pieces:
        image = p.image.load("images/"+piece+".png")
        IMAGES[piece] = p.transform.smoothscale(image,(SQ_SIZE,SQ_SIZE))

#draws all the graphics in the current game state
def draw_game_state(screen,gs,legal_moves,sq_selected):
    draw_board(screen) 
    highlight_squares(screen,gs,legal_moves,sq_selected)
    draw_pieces(screen,gs.board)

# draws the sqaures on the board
def draw_board(screen):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color_number = (r+c)%2 #even is always light and odd is always dark
            color = colors[color_number]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

# draws the pieces on  the board using current game state
def draw_pieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "__":
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def highlight_squares(screen,gs,legal_moves, sq_selected):
    if sq_selected!=():
        r,c = sq_selected
        if gs.board[r][c][0] == ('w' if gs.white_move else 'b'): #sq selected should have a piece color same as whose turn it is
            #highlight selected square
            s = p.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(150) #transparency value (0-225)
            s.fill(p.Color(PIECE_SELECTED_COLOR))
            screen.blit(s,(c*SQ_SIZE,r*SQ_SIZE))

            #highlight moves
            s.fill(p.Color(PIECE_MOVES_COLOR))
            for move in legal_moves:
                if move.initial_row == r and move.initial_col == c:
                    screen.blit(s,(move.final_col*SQ_SIZE,move.final_row*SQ_SIZE))

def animate_move(move,screen,board,clock):
    drow = move.final_row - move.initial_row
    dcol = move.final_col - move.initial_col
    frames_per_square = 5 #frames moving per square
    frame_count = (abs(drow)+abs(dcol)) * frames_per_square

    for frame in range (frame_count+1):
        r,c = (move.initial_row + drow*frame/frame_count, move.initial_col + dcol*frame/frame_count)
        draw_board(screen)
        draw_pieces(screen,board)

        #erase the piece from ending square
        color_number = (move.final_row + move.final_col)%2 #even is always light and odd is always dark
        color = colors[color_number]
        final_square = p.Rect(move.final_col*SQ_SIZE, move.final_row*SQ_SIZE, SQ_SIZE,SQ_SIZE)
        p.draw.rect(screen,color,final_square)

        #draw captured piece onto final square
        if move.piece_captured != "__":
            if move.is_enpassant_move:
                enpassant_row = move.final_row+1 if move.piece_captured[0] == 'b' else move.final_row-1
                final_square = p.Rect(move.final_col*SQ_SIZE, enpassant_row*SQ_SIZE, SQ_SIZE,SQ_SIZE)

            screen.blit(IMAGES[move.piece_captured],final_square)

        #draw moving piece
        screen.blit(IMAGES[move.piece_moved],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(120)

def draw_endgame_text(screen, text):
    font = p.font.SysFont("Arial", 48, True)
    
    # Render the text surfaces: one for the shadow and one for the main text
    text_surface = font.render(text, True, p.Color('Black'))
    shadow_surface = font.render(text, True, p.Color('Gray'))
    
    # Center the text
    text_rect = text_surface.get_rect(center=(BOARD_WIDTH/2, BOARD_HEIGHT/2))
    
    # Create a semi-transparent background rectangle that has a bit of padding
    padding = 20
    background_rect = text_rect.inflate(padding, padding)
    background_surface = p.Surface((background_rect.width, background_rect.height))
    background_surface.set_alpha(220) 
    background_surface.fill(p.Color(255, 255, 255))  
    
    # Draw a border around the background rectangle for extra definition
    border_color = p.Color('Black')
    border_thickness = 5
    p.draw.rect(screen, border_color, background_rect.inflate(border_thickness, border_thickness), border_thickness, border_radius=8)
    
    # Blit the background, then the text shadow, then the main text
    screen.blit(background_surface, background_rect)
    # Offset shadow for a subtle depth effect
    shadow_offset = (3, 3)
    screen.blit(shadow_surface, text_rect.move(*shadow_offset))
    screen.blit(text_surface, text_rect)

def load_sounds():
    p.mixer.init()
    global default_sound,capture_sound,check_sound,castle_sound,promotion_sound
    default_sound = p.mixer.Sound("sounds/default.mp3")
    capture_sound = p.mixer.Sound("sounds/capture.mp3")
    check_sound = p.mixer.Sound("sounds/check.mp3")
    castle_sound =  p.mixer.Sound("sounds/castle.mp3")
    promotion_sound = p.mixer.Sound("sounds/promote.mp3")

def play_sound(move,in_check):
    if in_check:
        check_sound.play()
    elif move.is_castle_move:
        castle_sound.play()
    elif move.is_pawn_promotion:
        promotion_sound.play()
    elif move.piece_captured !="__":
        capture_sound.play()
    else:
        default_sound.play()


def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH,BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color(LIGHT_SQUARE_COLOR))
    gs = game_state()
    load_images()
    load_sounds()
    legal_moves = gs.get_legal_moves()
    move_made = False  #flag variable to track if the move is made
    animate = False #flag variable for when to animate a move 
    running = True
    square_selected = ()
    squares_clicked = []
    game_over = False
    player_one = True #player one is white
    player_two = False #player two is black


    while running:
        human_turn = (gs.white_move and player_one) or (not gs.white_move and player_two)
        
        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over and human_turn:
                    loc = p.mouse.get_pos()
                    row = loc[1]//SQ_SIZE
                    col = loc[0]//SQ_SIZE
                    if square_selected == (row,col):
                        #user clicked same square --> deselected the current square
                        square_selected = ()
                        squares_clicked = []
                    else:
                        square_selected = (row,col)
                        squares_clicked.append(square_selected)
                    
                    if len(squares_clicked) ==2:
                        move = Move(squares_clicked[0],squares_clicked[1],gs.board)
                        for i in range(len(legal_moves)):
                            if move == legal_moves[i]:                              
                                gs.make_move(legal_moves[i])
                                print(move.get_chess_move())
                                move_made =True
                                animate = True
                                #reset the move to allow user to make further moves
                                square_selected = ()
                                squares_clicked = []
                        if not move_made:
                            squares_clicked = [square_selected]                        

            elif e.type == p.KEYDOWN:
                    if e.key == p.K_z:
                        if player_one!=player_two: #when playing against AI undo move will undo AI's move plus human's move
                            gs.undo_move()
                            gs.undo_move()
                            human_turn = True  
                        else:
                            gs.undo_move()
                        game_over = False
                        move_made = True #undo move is also considered as a move to generate legal moves 
                        animate = False 
                    if e.key == p.K_r: #reset the board
                        gs = game_state()
                        legal_moves = gs.get_legal_moves()
                        square_selected = ()
                        squares_clicked = []
                        move_made = False
                        animate = False
                        game_over = False

        #AI moves
        if not game_over and not human_turn:
            AI_move = find_alpha_beta_best_move(gs,legal_moves)
            if AI_move is None:
                AI_move = get_random_move(legal_moves)
            gs.make_move(AI_move)
            move_made = True
            animate = True


        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock)
            legal_moves=gs.get_legal_moves() #only generate legal moves if the move was made
            if len(gs.move_log)>0:
                play_sound(gs.move_log[-1],gs.in_check)
            move_made = False
            animate = False

        draw_game_state(screen,gs,legal_moves,square_selected)

        if gs.checkmate:
            game_over = True
            if gs.white_move:
                draw_endgame_text(screen, "Black wins by checkmate")
            else:
                draw_endgame_text(screen, "White wins by checkmate")
        elif gs.stalemate:
            game_over = True
            draw_endgame_text(screen, "Game draw by stalemate")
        
              
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__=="__main__":
    main()
         