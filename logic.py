from abc import ABC, abstractmethod
from typing import Literal
import math


# move(bool take, bool evolve, tuple(x,y)) note: not actually sure if it is xy or yx

Color = Literal['red', 'blue'] #blue down, red up

RED = "\033[31m" 
BLUE = "\033[34m" 
RESET = "\033[0m"

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def value(self):
        return (self.x,self.y)
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def set_y(self,y):
        self.y = y

    def set_x(self,x):
        self.x = x
 

class Move:
    def __init__(self, take: int, evolve: int, position: Position):
        self.take = take
        self.evolve = evolve
        self.position = position

    def value(self):
        return (self.take, self.evolve, self.position.value())


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

    def get_current_player(self):
        return self.players[self.current_turn]

    def switch_turn(self):
        self.current_turn = 1 - self.current_turn

    def is_current_player_piece(self, piece):
        return piece.get_color() == self.get_current_player().get_color()
    
    def check_victory(self, captured_piece):
        """Check if the captured piece is the opponent's Tortoise and declare a winner."""
        if isinstance(captured_piece, Tortoise):
            self.winner = self.get_current_player().get_color()
            print(f"{self.winner} wins by capturing the Tortoise!")


    def make_move(self, piece, position):
        """Move a piece to a new position and check for victory if any piece was captured."""
        captured_piece = self.board.move_piece(piece, position)
        
        if captured_piece != None:
            self.check_victory(captured_piece)
        
        if self.winner:
            return True  

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
    
    #Known bugs - Ape can randomly evolve, Crab can teleport, Sometimes makes really weird moves 
    def minimax(self, depth: int, alpha: int, beta: int, maximizing_player: bool):
        if depth == 0 or self.winner:
            return self.evaluate_board(), None

        best_move = None
        if maximizing_player:
            max_eval = -math.inf
            for piece, move in self.generate_moves("blue"):
                old_pos = piece.get_position()
                captured_piece = self.apply_move(piece, move[2])
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
                captured_piece = self.apply_move(piece, move[2])
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
    
    def apply_move(self, piece, position):
        """Apply a move and return any captured piece."""
        captured_piece = self.board.get_piece_at_pos(position)
        self.board.move_piece(piece, position)
        return captured_piece
    
    def undo_move(self, piece, new_position, captured_piece, evolved):
        """Undo a move by placing the piece back and restoring any captured piece."""
        old_position = piece.get_position()
        if(evolved):
            piece.devolve()
        self.board.move_piece(piece,new_position)
        if captured_piece:
            self.board.place_piece(captured_piece, old_position)

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]

    def setup(self):
        
        for col in range(8):
            self.grid[1][col] = Ape(color='red', initial_position=(1, col))
            
        self.grid[0][0] = Meerkat(color='red', initial_position=(0, 0))
        self.grid[0][1] = Snake(color='red', initial_position=(0, 1))
        self.grid[0][2] = Lynx(color='red', initial_position=(0, 2))
        self.grid[0][3] = Tortoise(color='red', initial_position=(0, 3))
        self.grid[0][4] = Crab(color='red', initial_position=(0, 4))
        self.grid[0][5] = Lynx(color='red', initial_position=(0, 5))
        self.grid[0][6] = Snake(color='red', initial_position=(0, 6))
        self.grid[0][7] = Meerkat(color='red', initial_position=(0, 7))


        
        for col in range(8):
            self.grid[6][col] = Ape(color='blue', initial_position=(6, col))
        
        self.grid[7][0] = Meerkat(color='blue', initial_position=(7, 0))
        self.grid[7][1] = Snake(color='blue', initial_position=(7, 1))
        self.grid[7][2] = Lynx(color='blue', initial_position=(7, 2))
        self.grid[7][3] = Crab(color='blue', initial_position=(7, 3))
        self.grid[7][4] = Tortoise(color='blue', initial_position=(7, 4))
        self.grid[7][5] = Lynx(color='blue', initial_position=(7, 5))
        self.grid[7][6] = Snake(color='blue', initial_position=(7, 6))
        self.grid[7][7] = Meerkat(color='blue', initial_position=(7, 7))
        

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

    def move_piece(self,piece,new_pos): 
        prev_pos = piece.get_position()
        captured_piece = self.get_piece_at_pos(new_pos)

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
    
    def add_eligble_move_ape(self,ape,new_pos,moves,own_color):
        if (self.pos_inside_board(new_pos)):
                if (self.pos_is_empty(new_pos)):
                    if(ape.will_evolve(new_pos)):
                        moves.append((0,1,new_pos))
                    moves.append((0,0,new_pos))
                    return True

                else:
                    piece = self.get_piece_at_pos(new_pos)
                    if(piece.get_color() != own_color):
                        if(ape.will_evolve(new_pos)):
                            moves.append((1,1,new_pos))
                        moves.append((1,0,new_pos))
                        return False
        return None
        



class Piece:
    piece_type = None
    piece_value = None
    def __init__(self,color: Color,position: tuple):
        self.__color = color
        self.__position = position
        if self.piece_type is None:
            raise NotImplementedError("Subclasses must define 'piece_type'.")


    @abstractmethod
    def get_possible_moves(self,position, board):
        pass

    def get_color(self) -> Color:
        return self.__color
    
    def get_position(self):
        return self.__position
    
    def move(self,new_position):
        self.__position = new_position

    def get_piece_type(self):
        return self.piece_type
    
    def get_piece_value(self):
        return self.piece_value
    
    def be_taken(self,board):
        board.grid[self.get_position()] = (0,0)

    @abstractmethod
    def get_representation(self):
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass



class Ape(Piece): 
    piece_type = "ape"
    piece_value = 1
    evolved = False
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)

    def get_possible_moves(self,position, board)->list:
        moves = []
        direction = 1
        color = self.get_color()
        steps = 1

        if (color =='blue'):
            direction = -1
        
        if (not self.evolved):


            if (position[0] == 6 and color == "blue" ) or (position[0]==1 and color == "red" ): #something weird with positition
                steps = 2
        
            for i in range(1, steps + 1):
                new_pos = (position[0]+direction*i,position[1])
                if (board.pos_inside_board(new_pos)):
                    if (board.pos_is_empty(new_pos)):
                        if(self.will_evolve(new_pos)):
                            moves.append((0,1,new_pos))
                        moves.append((0,0,new_pos))
                    else:
                        break
        
            r_pos = (position[0]+direction,position[1] - 1)
            board.add_eligble_move_ape(self,r_pos,moves,self.get_color())
            l_pos = (position[0]+direction,position[1] + 1)
            board.add_eligble_move_ape(self,l_pos,moves,self.get_color())

        else:
            directions = [(1,0),(0,1),(-1,0),(0,-1)]
            for d in directions:
                for i in range(1,8):

                    new_pos = (position[0]+ d[0]*i,position[1]+ d[1]*i)
                    if (board.add_eligble_move(new_pos,moves,color)!=True):
                        break
            
        return moves
    
    def evolve(self):
        self.evolved = True
        self.piece_value = 4

    def devolve(self):
        self.evolved = False
        self.piece_value = 1

    def will_evolve(self, position):
        """If an ape will evolve at a certain position, returns True if evolved else False"""
        if self.evolved== 0:
            if (position[0] == 0 and self.get_color() == "blue" ) or (position[0]==7 and self.get_color() == "red" ):
                return True
        return False
            
    def get_representation(self):
        if not self.evolved:
            return "A"
        else:
            return "EA"


    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} A {RESET}")
        else:
            return(f"{BLUE} A {RESET}")


class Snake(Piece):
    piece_type = "snake"
    piece_value = 5
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)
    
    def get_possible_moves(self,position, board)->list:
        moves = []
        directions = [(1,0),(0,1),(-1,0),(0,-1)]
        for d in directions:
            l_path = True
            r_path = True
            for x in range (1,6):
                if not l_path and not r_path:
                    break
                if (x%2 == 0):
                    new_pos = (position[0] + d[0]*x,position[1]+ d[1]*x)
                    if (board.add_eligble_move(new_pos,moves,self.get_color())!=True):
                        break

                else:
                    
                    if l_path:
                        l_pos = (position[0] + x * d[0] + d[1], position[1] + x * d[1] + d[0])
                        
                        if (board.add_eligble_move(l_pos,moves,self.get_color())!=True):
                            l_path = False
                    if r_path: 
                        r_pos = (position[0] + x * d[0] - d[1], position[1] + x * d[1] - d[0])
                        if (board.add_eligble_move(r_pos,moves,self.get_color())!=True):
                            r_path = False  
        moves = set(moves)
        return moves
    
    def get_representation(self):
        return "S"

            

    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} S {RESET}")
        else:
            return(f"{BLUE} S {RESET}")


class Crab(Piece):
    piece_type = "crab"
    piece_value = 2
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)
    
    def get_possible_moves(self,position, board):
        moves = []
        for i in range(-1,2):
            new_pos = (position + (i,0))
            new_pos = (position[0]+ i, position[1])
            board.add_eligble_move(new_pos,moves,self.get_color())
        l_path = True
        r_path = True
        for i in range(1,8):
            l_pos = (position[0], position[1]+i)
            r_pos = (position[0], position[1]-i)
            if (board.add_eligble_move(l_pos,moves,self.get_color())==False):
                l_pos = False

            if (board.add_eligble_move(r_pos,moves,self.get_color())==False):
                r_pos = False

            if (l_path == False and r_path == False):
                break

        return moves
            

    def get_representation(self):
        return "C"

    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} C {RESET}")
        else:
            return(f"{BLUE} C {RESET}")

class Meerkat(Piece): 
    piece_type = "meerkat"
    piece_value = 3
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)
    
    def get_possible_moves(self,position, board):
        moves = []
        directions = [(1,0),(0,1),(-1,0),(0,-1)]
        for d in directions:
            for i in range(1,3):
                new_pos = (position[0] + i *d[0], position[1] + i *d[1])
                board.add_eligble_move(new_pos,moves,self.get_color())
                
        return moves
            
    def get_representation(self):
        return "M"

    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} M {RESET}")
        else:
            return(f"{BLUE} M {RESET}")
        
class Tortoise(Piece): 
    piece_type = "Tortoise"
    piece_value = 100
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)
    
    def get_possible_moves(self,position, board):
        moves = []
        directions = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
        for d in directions:
            new_pos = (position[0] + d[0], position[1] + d[1])
            board.add_eligble_move(new_pos,moves,self.get_color())
                
        return moves
            
    def get_representation(self):
        return "T"

    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} T {RESET}")
        else:
            return(f"{BLUE} T {RESET}")

class Lynx(Piece):
    piece_type = "lynx"
    piece_value = 5
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)
    
    def get_possible_moves(self,position, board):
        moves = []
        directions = [(1,1),(-1,1),(1,-1),(-1,-1)]
        for d in directions:
            for i in range(1,8):
                new_pos = (position[0] + d[0]*i,position[1] + d[1]*i)
                if (board.add_eligble_move(new_pos,moves,self.get_color())!=True):
                    break

        directions = [(1,0),(0,1),(-1,0),(0,-1)]
        for d in directions:
            new_pos = position + d
            new_pos = (position[0] + d[0],position[1] + d[1])
            board.add_eligble_move(new_pos,moves,self.get_color())
        return moves
            
    def get_representation(self):
        return "L"

    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} L {RESET}")
        else:
            return(f"{BLUE} L {RESET}")






