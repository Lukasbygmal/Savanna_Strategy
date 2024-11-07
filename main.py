import pygame
from logic import Game, Board

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
HIGHLIGHT = (173, 216, 230)
SCREEN_SIZE = 640
TILE_COUNT = 8
TILE_SIZE = SCREEN_SIZE // 8

PIECE_COLORS = {
    'red': RED,
    'blue': BLUE
}

pygame.init()

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Savanna")

font = pygame.font.SysFont(None, 44)

def get_board_position(x,y):
    return (y // TILE_SIZE, x // TILE_SIZE)

def draw_board():
    screen.fill(WHITE)
    for row in range(TILE_COUNT):
        for col in range(TILE_COUNT):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_piece(piece, row, col):
    piece_color = PIECE_COLORS[piece.get_color()]
    text_surface = font.render(str(piece.get_representation()), True, piece_color)
    screen.blit(text_surface, (col * TILE_SIZE + TILE_SIZE // 3, row * TILE_SIZE + TILE_SIZE // 4))


def draw_pieces(board):
    for row in range(8):
        for col in range(8):
            piece = board.get_piece_at_pos((row, col))
            if piece:
                draw_piece(piece, row, col)

def draw_possible_moves(possible_moves):
    for move in possible_moves:
        pygame.draw.rect(screen, HIGHLIGHT, (move[1] * TILE_SIZE, move[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def main():
    game = Game()
    selected_piece = None
    possible_moves = []

    running = True
    while running:
        draw_board() #maybe doesn't need to be in loop?
        draw_pieces(game.board)
        
        if possible_moves:
            draw_possible_moves(possible_moves)
        
        pygame.display.flip()
        if game.winner:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                position = get_board_position(x,y)
                
                if selected_piece:
                    if position in possible_moves:
                        game.board.move_piece(selected_piece, position)
                        if game.winner:
                            running = False
                            break
                        game.switch_turn()
                    selected_piece = None
                    possible_moves = []
                
                else:
                    piece = game.board.get_piece_at_pos(position)
                    if piece and game.is_current_player_piece(piece):
                        selected_piece = piece
                        possible_moves = piece.get_possible_moves(position, game.board)

    pygame.quit()

if __name__ == "__main__":
    main()
