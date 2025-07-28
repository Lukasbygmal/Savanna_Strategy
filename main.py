import pygame
from logic import Game
from menu import GameMenu, GameState
import time
import colors

SCREEN_SIZE = 640
TILE_COUNT = 8
TILE_SIZE = SCREEN_SIZE // 8

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Savanna Strategy")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

font = pygame.font.SysFont(None, 44)


def get_board_position(x, y):
    """Convert screen coordinates to board position for detecting clicks.
    Returns: Tuple[int, int] - Row and column on the board."""
    return (y // TILE_SIZE, x // TILE_SIZE)


def draw_board():
    """Draw the checker game board grid.
    Returns: None."""
    screen.fill(colors.WHITE)
    for row in range(TILE_COUNT):
        for col in range(TILE_COUNT):
            color = (
                colors.TILE_COLORS["light"]
                if (row + col) % 2 == 0
                else colors.TILE_COLORS["dark"]
            )
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
            )


def draw_piece(piece, row, col, sprites):
    """Render a piece at a specific board position, perfectly centered in the tile."""
    piece_type = piece.piece_type
    if piece.get_color() == "White":
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
            colors.HIGHLIGHT,
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


def handle_menu_state(menu, screen, sprites):
    menu.draw_menu(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return None, GameState.MENU, True

        action = menu.handle_menu_events(event)
        if action == "play":
            settings = menu.get_settings()
            game = Game(sprites)
            return (game, settings), GameState.PLAYING, False

    return None, GameState.MENU, False


def handle_playing_state(
    game, selected_piece, possible_moves, settings, sprites, screen, menu
):
    draw_board()
    draw_pieces(game.board, sprites)

    if possible_moves:
        draw_possible_moves(possible_moves)

    if game.winner:
        return selected_piece, possible_moves, GameState.GAME_OVER, False

    if (
        game.get_current_player().get_color() == settings["ai_color"]
        and not game.viewing_mode
    ):
        pygame.display.flip()

        game.step_to_front()
        start_time = time.time()
        if game.get_current_player().get_color() == "Black":
            maximizing_player = True
        else:
            maximizing_player = False

        best_score, best_move = game.minimax(
            settings["ai_depth"], -float("inf"), float("inf"), maximizing_player
        )
        end_time = time.time()
        elapsed_time = end_time - start_time

        if best_move:
            piece_to_move, move = best_move
            game.make_move(piece_to_move, move)
        else:
            return selected_piece, possible_moves, GameState.GAME_OVER, False
    else:
        selected_piece, possible_moves, game_state, should_quit = handle_game_events(
            game, selected_piece, possible_moves, menu
        )
        if should_quit:
            return selected_piece, possible_moves, game_state, True

        if game_state != GameState.PLAYING:
            return selected_piece, possible_moves, game_state, False

        pygame.display.flip()

    return selected_piece, possible_moves, GameState.PLAYING, False


def handle_game_over_state(game, menu, sprites, screen):
    """Handle the game over state with proper event handling."""
    draw_board()
    draw_pieces(game.board, sprites)
    menu.draw_game_over(screen, game.winner)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return GameState.GAME_OVER, True

        # Use the new event handler method
        action = menu.handle_game_over_events(event)
        if action == "menu":
            return GameState.MENU, False

    return GameState.GAME_OVER, False


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
            result, game_state, should_quit = handle_menu_state(menu, screen, sprites)
            if should_quit:
                running = False
            elif result:
                game, settings = result
                selected_piece = None
                possible_moves = []

        elif game_state == GameState.PLAYING:
            selected_piece, possible_moves, game_state, should_quit = (
                handle_playing_state(
                    game,
                    selected_piece,
                    possible_moves,
                    settings,
                    sprites,
                    screen,
                    menu,
                )
            )
            if should_quit:
                running = False

        elif game_state == GameState.GAME_OVER:
            game_state, should_quit = handle_game_over_state(
                game, menu, sprites, screen
            )
            if should_quit:
                running = False

        if game_state != GameState.PLAYING:
            pygame.display.flip()

        clock.tick(120)

    pygame.quit()


if __name__ == "__main__":
    main()
