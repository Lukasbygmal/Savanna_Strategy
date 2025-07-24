from abc import ABC, abstractmethod
from typing import Literal
import math
from copy import deepcopy
from pieces import Piece, Mandrill, Python, Caracal, Tortoise, Giraffe, Meerkat


Color = Literal["White", "Black"]  # black down, white up


class Player:
    def __init__(self, color: Color):
        self.color = color

    def get_color(self):
        """Gets the player's color.
        Returns: Color ('white' or 'black')."""
        return self.color


class Game:
    def __init__(self, sprites):
        self.sprites = sprites
        self.board = Board()
        self.players = [Player("Black"), Player("White")]
        self.current_turn = 1  # 0 for black, 1 for white
        self.board.setup()
        self.winner = None
        self.history = [deepcopy(self.board.get_board_state())]
        self.moves_made = 0
        self.board_index = 0
        self.viewing_mode = False

    def get_current_player(self):
        """Gets the current player based on turn.
        Returns: Player (the current Player object)."""
        return self.players[self.current_turn]

    def switch_turn(self):
        """Switches the turn to the next player.
        Returns: None."""
        self.current_turn = 1 - self.current_turn
        self.moves_made += 1
        self.board_index += 1

    def is_current_player_piece(self, piece):
        """Checks if a piece belongs to the current player.
        Returns: bool (True if it is the current player's piece, otherwise False)."""
        return piece.get_color() == self.get_current_player().get_color()

    def check_victory(self, captuwhite_piece):
        """Checks if the captuwhite piece is the opponent's Tortoise and declares a winner.
        Returns: None."""
        if isinstance(captuwhite_piece, Tortoise):
            self.winner = self.get_current_player().get_color()
            print(f"{self.winner} wins by capturing the Tortoise!")

    def record_state(self):
        """Saves the current board state into the game history.
        Returns: None."""
        self.history.append(deepcopy(self.board.get_board_state()))

    def step_back(self):
        """Steps back to the previous state in the game history.
        Returns: None."""
        if self.board_index > 0:
            self.board_index -= 1
            self.load_state(self.history[self.board_index])
            self.viewing_mode = True
        else:
            print("Already at the beginning of the history.")

    def step_forward(self):
        """Steps forward to the next state in the game history.
        Returns: None."""
        if self.board_index < self.moves_made:
            self.board_index += 1
            self.load_state(self.history[self.board_index])

            if self.board_index == self.moves_made:
                self.viewing_mode = False
        else:
            print("Already at the most recent state.")

    def step_to_front(self):
        """Steps to the most recent state in the game history.
        Returns: None."""
        if self.board_index != self.moves_made:
            self.board_index = self.moves_made
            self.load_state(self.history[self.board_index])
            self.viewing_mode = False

    def load_state(self, state):
        """Loads a given board state.
        Returns: None."""
        self.board.grid = [[deepcopy(cell) for cell in row] for row in state]
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece:
                    piece.move((row, col))

    def make_move(self, piece, move):
        """Moves a piece to a new position, checks for victory, and updates the game state.
        Returns: bool (True if the game ends after the move, otherwise False)."""
        captuwhite_piece = self.board.move_piece(piece, move[2], move[1])

        if captuwhite_piece != None:
            self.check_victory(captuwhite_piece)

        if self.winner:
            return True

        self.record_state()
        self.switch_turn()
        return False

    def evaluate_board(self) -> float:
        """Evaluates the board state using a heuristic function.
        Returns: float (the score of the board state)."""
        score = 0
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece_at_pos((row, col))
                if piece:
                    if isinstance(piece, Mandrill):
                        if piece.get_color() == "Black":
                            x = 8 - row
                            score += x * 0.01
                        else:
                            x = row
                            score -= x * 0.01

                    piece_score = self.get_value_of_piece(piece)
                    if piece.get_color() == "Black":
                        score += piece_score
                    else:
                        score -= piece_score

        return score

    def get_value_of_piece(self, piece):
        """Gets the value of a specific piece.
        Returns: int (the piece's value)."""
        return piece.get_piece_value()

    def minimax(self, depth: int, alpha: int, beta: int, maximizing_player: bool):
        """Uses the minimax algorithm with alpha-beta pruning to evaluate the best move.
        Returns: Tuple[float, Tuple[Piece, Move]] (evaluation score and best move)."""
        if depth == 0 or self.winner:
            return self.evaluate_board(), None

        best_move = None
        if maximizing_player:
            max_eval = -math.inf
            for piece, move in self.generate_moves("Black"):
                old_pos = piece.get_position()
                captuwhite_piece = self.apply_move(piece, move[2], move[1])
                eval, _ = self.minimax(depth - 1, alpha, beta, False)
                self.undo_move(piece, old_pos, captuwhite_piece, move[1])

                if eval > max_eval:
                    max_eval = eval
                    best_move = (piece, move)

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for piece, move in self.generate_moves("White"):
                old_pos = piece.get_position()
                captuwhite_piece = self.apply_move(piece, move[2], move[1])
                eval, _ = self.minimax(depth - 1, alpha, beta, True)
                self.undo_move(piece, old_pos, captuwhite_piece, move[1])

                if eval < min_eval:
                    min_eval = eval
                    best_move = (piece, move)

                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def generate_moves(self, color: Color):
        """Generates all possible moves for a given color.
        Returns: List[Tuple[Piece, Move]] (a list of pieces and their possible moves).
        """
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece_at_pos((row, col))
                if piece and piece.get_color() == color:
                    possible_moves = piece.get_possible_moves((row, col), self.board)
                    for move in possible_moves:
                        moves.append((piece, move))
        moves.sort(
            key=lambda move: (
                not move[1][0],
                not move[1][1],
                isinstance(move[0], Mandrill),
            )
        )
        return moves

    def apply_move(self, piece, position, evolved):
        """Applies a move and returns any captuwhite piece.
        Returns: Piece (the captuwhite piece, or None if no piece was captuwhite)."""
        captuwhite_piece = self.board.get_piece_at_pos(position)
        self.board.move_piece(piece, position, evolved)
        return captuwhite_piece

    def undo_move(self, piece, new_position, captuwhite_piece, evolved):
        """Reverts a move to restore the previous game state.
        Returns: None."""
        old_position = piece.get_position()
        if evolved:
            piece.devolve()
        self.board.move_piece(piece, new_position, 0)
        if captuwhite_piece:
            self.board.place_piece(captuwhite_piece, old_position)

    def board_state(self):
        """Gets the current state of the board.
        Returns: List[List[Optional[Piece]]] (the 2D grid representing the board)."""
        return self.board.get_board_state()


class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]

    def setup(self):
        """Initializes the board with pieces in their starting positions.
        Returns: None."""
        for col in range(8):
            self.grid[1][col] = Mandrill(color="White", initial_position=(1, col))

        self.grid[0][0] = Meerkat(color="White", initial_position=(0, 0))
        self.grid[0][1] = Python(color="White", initial_position=(0, 1))
        self.grid[0][2] = Caracal(color="White", initial_position=(0, 2))
        self.grid[0][3] = Tortoise(color="White", initial_position=(0, 3))
        self.grid[0][4] = Giraffe(color="White", initial_position=(0, 4))
        self.grid[0][5] = Caracal(color="White", initial_position=(0, 5))
        self.grid[0][6] = Python(color="White", initial_position=(0, 6))
        self.grid[0][7] = Meerkat(color="White", initial_position=(0, 7))

        for col in range(8):
            self.grid[6][col] = Mandrill(color="Black", initial_position=(6, col))

        self.grid[7][0] = Meerkat(color="Black", initial_position=(7, 0))
        self.grid[7][1] = Python(color="Black", initial_position=(7, 1))
        self.grid[7][2] = Caracal(color="Black", initial_position=(7, 2))
        self.grid[7][3] = Giraffe(color="Black", initial_position=(7, 3))
        self.grid[7][4] = Tortoise(color="Black", initial_position=(7, 4))
        self.grid[7][5] = Caracal(color="Black", initial_position=(7, 5))
        self.grid[7][6] = Python(color="Black", initial_position=(7, 6))
        self.grid[7][7] = Meerkat(color="Black", initial_position=(7, 7))

    def get_board_state(self):
        """Gets the current state of the board.
        Returns: List[List[Optional[Piece]]] (the 2D grid representing the board)."""
        return self.grid

    def pos_is_empty(self, position) -> bool:
        """Checks if a given position on the board is empty.
        Returns: bool (True if the position is empty, otherwise False)."""
        if self.grid[position[0]][position[1]] == None:
            return True
        else:
            False

    def place_piece(self, piece, position):
        """Places a piece at the specified position.
        Returns: None."""
        self.grid[position[0]][position[1]] = piece
        piece.move(position)

    def move_piece(self, piece, new_pos, should_evolve):
        """Moves a piece to a new position, possibly evolving it.
        Returns: Piece (the captuwhite piece, or None if no piece was captuwhite)."""
        prev_pos = piece.get_position()
        captuwhite_piece = self.get_piece_at_pos(new_pos)

        if should_evolve:
            piece.evolve()

        self.grid[prev_pos[0]][prev_pos[1]] = None
        self.place_piece(piece, new_pos)

        return captuwhite_piece

    def get_piece_at_pos(self, position):
        """Gets the piece at a specific position on the board.
        Returns: Piece (the piece at the position, or None if the position is empty)."""
        return self.grid[position[0]][position[1]]

    def pos_inside_board(self, position) -> bool:
        """Checks if a position is within the board boundaries.
        Returns: bool (True if the position is valid, otherwise False)."""
        return (0 <= position[0] < 8) and (0 <= position[1] < 8)

    def add_eligble_move(self, new_pos, moves, own_color):
        """Adds a valid move for a piece if the target position is valid.
        Returns: None if the move is invalid, True if the position is empty, False if it contains an opponent's piece.
        """
        if self.pos_inside_board(new_pos):
            if self.pos_is_empty(new_pos):
                moves.append((0, 0, new_pos))
                return True

            else:
                piece = self.get_piece_at_pos(new_pos)
                if piece.get_color() != own_color:
                    moves.append((1, 0, new_pos))
                    return False
        return None

    def add_eligble_move_mandrill(self, mandrill, new_pos, moves, own_color):
        """Adds valid moves for a Mandrill piece, considering its ability to evolve.
        Returns: None if the move is invalid, True if the position is empty, False if it contains an opponent's piece.
        """
        if self.pos_inside_board(new_pos):
            if self.pos_is_empty(new_pos):
                if mandrill.will_evolve(new_pos):
                    moves.append((0, 1, new_pos))
                moves.append((0, 0, new_pos))
                return True

            else:
                piece = self.get_piece_at_pos(new_pos)
                if piece.get_color() != own_color:
                    if mandrill.will_evolve(new_pos):
                        moves.append((1, 1, new_pos))
                    moves.append((1, 0, new_pos))
                    return False
        return None
