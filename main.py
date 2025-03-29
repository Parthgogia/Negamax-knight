from engine import game_state
import pygame as p


BOARD_WIDTH = BOARD_HEIGHT = 512
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

LIGHT_SQUARE_COLOR = (237, 238, 209)
DARK_SQUARE_COLOR = (119, 153, 82)

def load_images():
    pieces = ["bR","bN","bB","bQ","bK","bP","wR","wN","wB","wQ","wK","wP"]
    for piece in pieces:
        image = p.image.load("images/"+piece+".png")
        IMAGES[piece] = p.transform.scale(image,(SQ_SIZE,SQ_SIZE))


#draws all the graphics in the current game state
def draw_game_state(screen,gs):
    draw_board(screen) 
    draw_pieces(screen,gs.board)

# draws the sqaures on the board
def draw_board(screen):
    colors = [p.Color(LIGHT_SQUARE_COLOR), p.Color(DARK_SQUARE_COLOR)]
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





def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH,BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color(LIGHT_SQUARE_COLOR))
    gs = game_state()
    load_images()
    running = True

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        draw_game_state(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__=="__main__":
    main()
         

