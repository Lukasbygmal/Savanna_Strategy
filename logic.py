from abc import ABC, abstractmethod
from typing import Literal
import math
from copy import deepcopy
from pieces import Piece,Mandrill,Python,Caracal,Tortoise,Giraffe,Meerkat


Color = Literal['red', 'blue'] #blue down, red up


class Player:
    def __init__(self, color: Color):
        self.color = color

    def get_color(self):
        return self.color


class Game:
    def __init__(self):
        self.board = Board()
        self.players = [ Player("blue"),Player("red")]
        self.current_turn = 0  # 0 for blue, 1 for red
        self.board.setup()
        self.winner = None
        self.history = [deepcopy(self.board.get_board_state())]
        self.moves_made = 0
        self.board_index = 0
        self.viewing_mode = False
        

    def get_current_player(self):
        return self.players[self.current_turn]

    def switch_turn(self):
        self.current_turn = 1 - self.current_turn
        self.moves_made += 1
        self.board_index += 1

    def is_current_player_piece(self, piece):
        return piece.get_color() == self.get_current_player().get_color()
    
    def check_victory(self, captured_piece):
        """Check if the captured piece is the opponent's Tortoise and declare a winner."""
        if isinstance(captured_piece, Tortoise):
            self.winner = self.get_current_player().get_color()
            print(f"{self.winner} wins by capturing the Tortoise!")
    
    def record_state(self):

        self.history.append(deepcopy(self.board.get_board_state()))


    def step_back(self):
        if self.board_index > 0:  
            self.board_index -= 1
            self.load_state(self.history[self.board_index])
            self.viewing_mode = True 
        else:
            print("Already at the beginning of the history.") 
        

    def step_forward(self):
        if self.board_index < self.moves_made:  
            self.board_index += 1
            self.load_state(self.history[self.board_index])

            if self.board_index == self.moves_made:
                self.viewing_mode = False
        else:
            print("Already at the most recent state.")

    def step_to_front(self):
        """Go to the latest state in the history."""
        if self.board_index != self.moves_made:
            self.board_index = self.moves_made
            self.load_state(self.history[self.board_index])
            self.viewing_mode = False

    def load_state(self,state):
        self.board.grid = [[deepcopy(cell) for cell in row] for row in state]
        for row in range(8):
            for col in range(8):
                piece = self.board.grid[row][col]
                if piece:
                    piece.move((row, col))


    def make_move(self, piece, move):
        """Move a piece to a new position and check for victory if any piece was captured."""
        captured_piece = self.board.move_piece(piece, move[2],move[1])
        
        if captured_piece != None:
            self.check_victory(captured_piece)
        
        if self.winner:
            return True  

        self.record_state()
        self.switch_turn()
        return False  

    def evaluate_board(self) -> int:
        """A heuristic function to evaluate the board position."""
        score = 0
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece_at_pos((row, col))
                if piece:
                    piece_score = self.get_value_of_piece(piece)
                    if piece.get_color() == "blue":
                        score += piece_score
                    else:
                        score -= piece_score
        return score
    
    def get_value_of_piece(self, piece):
        return piece.get_piece_value()
    
    def minimax(self, depth: int, alpha: int, beta: int, maximizing_player: bool):
        if depth == 0 or self.winner:
            return self.evaluate_board(), None

        best_move = None
        if maximizing_player:
            max_eval = -math.inf
            for piece, move in self.generate_moves("blue"):
                old_pos = piece.get_position()
                captured_piece = self.apply_move(piece, move[2], move[1])
                eval, _ = self.minimax(depth - 1, alpha, beta, False)
                self.undo_move(piece, old_pos, captured_piece, move[1])

                if eval > max_eval:
                    max_eval = eval
                    best_move = (piece, move)

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for piece, move in self.generate_moves("red"):
                old_pos = piece.get_position()
                captured_piece = self.apply_move(piece, move[2], move[1])
                eval, _ = self.minimax(depth - 1, alpha, beta, True)
                self.undo_move(piece, old_pos, captured_piece, move[1])

                if eval < min_eval:
                    min_eval = eval
                    best_move = (piece, move)

                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
        
    def generate_moves(self, color: Color):
        """Generates all possible moves for the current player color."""
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece_at_pos((row, col))
                if piece and piece.get_color() == color:
                    possible_moves = piece.get_possible_moves((row, col), self.board)
                    for move in possible_moves:
                        moves.append((piece, move))
        return moves
    
    def apply_move(self, piece, position, evolved):
        """Apply a move and return any captured piece."""
        captured_piece = self.board.get_piece_at_pos(position)
        self.board.move_piece(piece, position, evolved)
        return captured_piece
    
    def undo_move(self, piece, new_position, captured_piece, evolved):
        """Undo a move by placing the piece back and restoring any captured piece."""
        old_position = piece.get_position()
        if evolved:
            piece.devolve()
        self.board.move_piece(piece,new_position,0)
        if captured_piece:
            self.board.place_piece(captured_piece, old_position)

    def board_state(self):
        return self.board.get_board_state()

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]

    def setup(self):
        
        for col in range(8):
            self.grid[1][col] = Mandrill(color='red', initial_position=(1, col))
            
        self.grid[0][0] = Meerkat(color='red', initial_position=(0, 0))
        self.grid[0][1] = Python(color='red', initial_position=(0, 1))
        self.grid[0][2] = Caracal(color='red', initial_position=(0, 2))
        self.grid[0][3] = Tortoise(color='red', initial_position=(0, 3))
        self.grid[0][4] = Giraffe(color='red', initial_position=(0, 4))
        self.grid[0][5] = Caracal(color='red', initial_position=(0, 5))
        self.grid[0][6] = Python(color='red', initial_position=(0, 6))
        self.grid[0][7] = Meerkat(color='red', initial_position=(0, 7))


        
        for col in range(8):
            self.grid[6][col] = Mandrill(color='blue', initial_position=(6, col))
        
        self.grid[7][0] = Meerkat(color='blue', initial_position=(7, 0))
        self.grid[7][1] = Python(color='blue', initial_position=(7, 1))
        self.grid[7][2] = Caracal(color='blue', initial_position=(7, 2))
        self.grid[7][3] = Giraffe(color='blue', initial_position=(7, 3))
        self.grid[7][4] = Tortoise(color='blue', initial_position=(7, 4))
        self.grid[7][5] = Caracal(color='blue', initial_position=(7, 5))
        self.grid[7][6] = Python(color='blue', initial_position=(7, 6))
        self.grid[7][7] = Meerkat(color='blue', initial_position=(7, 7))


    def get_board_state(self):
        return self.grid
        

    def pos_is_empty(self,position)-> bool:
        if (self.grid[position[0]][position[1]]==None):
            return True
        else:
            False

    def place_has_piece_of_color(self,position,color)-> bool:
        if (self.pos_is_empty(position)==False):
            piece = self.get_piece_at_pos()
            if(piece.get_color()==color):
                return True
        return False

    def place_piece(self,piece,position):
        self.grid[position[0]][position[1]]=piece
        piece.move(position)

    def move_piece(self,piece,new_pos, should_evolve):
        prev_pos = piece.get_position()
        captured_piece = self.get_piece_at_pos(new_pos)

        if should_evolve:
            piece.evolve()

        self.grid[prev_pos[0]][prev_pos[1]] = None
        self.place_piece(piece, new_pos)

        return captured_piece
            

    def get_piece_at_pos(self,position):
        return self.grid[position[0]][position[1]]

    def pos_inside_board(self,position)-> bool:
        return (0 <= position[0] < 8) and (0 <= position[1] < 8)
    
    def add_eligble_move(self,new_pos,moves,own_color):
        """Returns: None if place is not eligeble, True if place is empty, False if place is opponent piece"""
        if (self.pos_inside_board(new_pos)):
                if (self.pos_is_empty(new_pos)):
                    moves.append((0,0,new_pos))
                    return True

                else:
                    piece = self.get_piece_at_pos(new_pos)
                    if(piece.get_color() != own_color):
                        moves.append((1,0,new_pos))
                        return False
        return None
    
    def add_eligble_move_mandrill(self,mandrill,new_pos,moves,own_color):
        if (self.pos_inside_board(new_pos)):
                if (self.pos_is_empty(new_pos)):
                    if(mandrill.will_evolve(new_pos)):
                        moves.append((0,1,new_pos))
                    moves.append((0,0,new_pos))
                    return True

                else:
                    piece = self.get_piece_at_pos(new_pos)
                    if(piece.get_color() != own_color):
                        if(mandrill.will_evolve(new_pos)):
                            moves.append((1,1,new_pos))
                        moves.append((1,0,new_pos))
                        return False
        return None
        









