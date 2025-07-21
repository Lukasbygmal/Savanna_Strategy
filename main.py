import pygame
from logic import Game
from menu import GameMenu, GameState
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

white = (255, 0, 0)
black = (0, 0, 255)
HIGHLIGHT = (173, 216, 230)
SCREEN_SIZE = 640
TILE_COUNT = 8
TILE_SIZE = SCREEN_SIZE // 8

PIECE_COLORS = {
    "white": white,
    "black": black,
}  # this is never used?! but will keep here until refactor colors! TODO

TILE_COLORS = {"light": (209, 219, 183), "dark": (128, 128, 128)}

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Savanna")

font = pygame.font.SysFont(None, 44)


def get_board_position(x, y):
    """Convert screen coordinates to board position for detecting clicks.
    Returns: Tuple[int, int] - Row and column on the board."""
    return (y // TILE_SIZE, x // TILE_SIZE)


def draw_board():
    """Draw the checker game board grid.
    Returns: None."""
    screen.fill(WHITE)
    for row in range(TILE_COUNT):
        for col in range(TILE_COUNT):
            color = (
                TILE_COLORS["light"] if (row + col) % 2 == 0 else TILE_COLORS["dark"]
            )
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
            )


def draw_piece(piece, row, col, sprites):
    """Render a piece at a specific board position, perfectly centered in the tile."""
    piece_type = piece.piece_type
    if piece.get_color() == "white":
        piece_type = "w_" + piece_type
    else:
        piece_type = "b_" + piece_type
    sprite = sprites[piece_type]
    sprite_width, sprite_height = sprite.get_size()

    x_offset = (TILE_SIZE - sprite_width) // 2
    y_offset = (TILE_SIZE - sprite_height) // 2

    x_position = col * TILE_SIZE + x_offset
    y_position = row * TILE_SIZE + y_offset

    screen.blit(sprite, (x_position, y_position))


def load_sprites(sprite_sheet_path):
    """Load sprites for pieces from a sprite sheet and scale them."""
    sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
    SPRITE_ROWS = 4
    SPRITE_COLUMNS = 4
    sprite_width = sprite_sheet.get_width() // SPRITE_COLUMNS
    sprite_height = sprite_sheet.get_height() // SPRITE_ROWS

    scaled_size = (int(TILE_SIZE * 0.75), int(TILE_SIZE * 0.75))

    sprites = {}
    piece_names = [
        "w_giraffe",
        "b_giraffe",
        "w_tortoise",
        "b_tortoise",
        "w_python",
        "b_python",
        "w_caracal",
        "b_caracal",
        "w_meerkat",
        "b_meerkat",
        "w_mandrill",
        "b_mandrill",
        "w_baboon",
        "b_baboon",
    ]
    index = 0
    for row in range(SPRITE_ROWS):
        for col in range(SPRITE_COLUMNS):
            if index < len(piece_names):
                sprite = sprite_sheet.subsurface(
                    (
                        col * sprite_width,
                        row * sprite_height,
                        sprite_width,
                        sprite_height,
                    )
                )
                scaled_sprite = pygame.transform.scale(sprite, scaled_size)
                sprites[piece_names[index]] = scaled_sprite
                index += 1
    return sprites


def draw_pieces(board, sprites):
    """Draw all pieces on the board from its current state.
    Returns: None."""
    for row in range(8):
        for col in range(8):
            piece = board.get_piece_at_pos((row, col))
            if piece:
                draw_piece(piece, row, col, sprites)


def draw_possible_moves(possible_moves):
    """Highlight tiles for valid moves of the selected piece.
    Returns: None."""
    for move in possible_moves:
        pygame.draw.rect(
            screen,
            HIGHLIGHT,
            (move[2][1] * TILE_SIZE, move[2][0] * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )


def handle_game_events(game, selected_piece, possible_moves, menu):
    """Handle all pygame events during gameplay and return updated selected_piece, possible_moves and game state"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return None, None, GameState.MENU, True  # quit = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                game.step_forward()
            elif event.key == pygame.K_LEFT:
                game.step_back()
            elif event.key == pygame.K_SPACE:
                game.step_to_front()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game.viewing_mode:
                print("You cannot make moves while viewing previous states.")
                continue

            x, y = pygame.mouse.get_pos()
            position = get_board_position(x, y)

            if selected_piece:
                for move in possible_moves:
                    if_capture, if_evolution, pos = move
                    if pos == position:
                        game.make_move(selected_piece, move)
                        break

                selected_piece = None
                possible_moves = []

            else:
                piece = game.board.get_piece_at_pos(position)
                if piece and game.is_current_player_piece(piece):
                    selected_piece = piece
                    possible_moves = piece.get_possible_moves(position, game.board)

    return selected_piece, possible_moves, GameState.PLAYING, False


def main():
    sprites = load_sprites("pieces.png")
    menu = GameMenu(SCREEN_SIZE)
    game_state = GameState.MENU

    game = None
    selected_piece = None
    possible_moves = []
    settings = None

    running = True
    while running:
        if game_state == GameState.MENU:
            menu.draw_menu(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                action = menu.handle_menu_events(event)
                if action == "play":
                    settings = menu.get_settings()
                    game = Game(sprites)
                    selected_piece = None
                    possible_moves = []
                    game_state = GameState.PLAYING

        elif game_state == GameState.PLAYING:
            draw_board()
            draw_pieces(game.board, sprites)

            if possible_moves:
                draw_possible_moves(possible_moves)

            if game.winner:
                game_state = GameState.GAME_OVER

            elif (
                game.get_current_player().get_color() == settings["ai_color"]
                and not game.viewing_mode
            ):
                game.step_to_front()
                start_time = time.time()
                best_score, best_move = game.minimax(
                    settings["ai_depth"], -float("inf"), float("inf"), True
                )
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Function runtime: {elapsed_time:.4f} seconds")

                if best_move:
                    piece_to_move, move = best_move
                    print("-------Piece to move:", piece_to_move)
                    print("Move", move)
                    game.make_move(piece_to_move, move)
                else:
                    print("No valid moves available for AI player.")
                    game_state = GameState.GAME_OVER
            else:
                selected_piece, possible_moves, game_state, should_quit = (
                    handle_game_events(game, selected_piece, possible_moves, menu)
                )
                if should_quit:
                    running = False

        elif game_state == GameState.GAME_OVER:
            draw_board()
            draw_pieces(game.board, sprites)

            back_button = menu.draw_game_over(screen, game.winner)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif back_button.handle_event(event):
                    game_state = GameState.MENU

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
