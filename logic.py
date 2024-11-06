from abc import ABC, abstractmethod
from typing import Literal


Color = Literal['red', 'blue'] #blue down, red up

RED = "\033[31m" 
BLUE = "\033[34m" 
RESET = "\033[0m"


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

    def get_current_player(self):
        return self.players[self.current_turn]

    def switch_turn(self):
        self.current_turn = 1 - self.current_turn

    def is_current_player_piece(self, piece):
        return piece.get_color() == self.get_current_player().get_color()

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]

    def setup(self):
        
        for col in range(8):
            self.grid[1][col] = Ape(color='red', initial_position=(1, col))
            
        self.grid[0][0] = Meerkat(color='red', initial_position=(0, 0))
        self.grid[0][1] = Snake(color='red', initial_position=(0, 1))
        self.grid[0][2] = Lynx(color='red', initial_position=(0, 2))
        self.grid[0][3] = Meerkat(color='red', initial_position=(0, 3))
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
        self.grid[7][4] = Meerkat(color='blue', initial_position=(7, 4))
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

    def place_piece(self,Piece,position):
        assert(self.pos_is_empty(position))
        self.grid[position[0]][position[1]]=Piece

    def move_piece(self,Piece,position):
        prev_pos = Piece.get_position()
        if (self.pos_is_empty(position)):
            self.grid[position[0]][position[1]]=Piece
            self.grid[prev_pos[0]][prev_pos[1]]=None
            Piece.move(position)

        else:
            opp_piece = self.get_piece_at_pos(position)
            opp_piece.kill()
            self.grid[position[0]][position[1]]=Piece
            self.grid[prev_pos[0]][prev_pos[1]]=None
            Piece.move(position)

    def get_piece_at_pos(self,position):
        return self.grid[position[0]][position[1]]

    def pos_inside_board(self,position)-> bool:
        return (0 <= position[0] < 8) and (0 <= position[1] < 8)
    
    def add_eligble_move(self,new_pos,moves,own_color):
        """Returns: None if place is not eligeble, True if place is empty, False if place is opponent piece"""
        if (self.pos_inside_board(new_pos)):
                if (self.pos_is_empty(new_pos)):
                    moves.append(new_pos)
                    return True

                else:
                    piece = self.get_piece_at_pos(new_pos)
                    if(piece.get_color() != own_color):
                        moves.append(new_pos)
                        return False
        return None
        



class Piece:
    piece_type = None
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

    def piece_type(self):
        return self.piece_type
    
    def be_taken(self,board):
        board.grid[self.position] = (0,0)

    def kill(self):
        pass #TODO

    @abstractmethod
    def get_representation(self):
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass



class Ape(Piece): 
    piece_type = "ape"
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)

    def get_possible_moves(self,position, board)->list:
        moves = []
        direction = 1
        color = self.get_color()
        steps = 1

        if (color =='blue'):
            direction = -1
        
        if (position[0] == 6 and color == "blue" ) or (position[0]==1 and color == "red" ): #something weird with positition
            steps = 2

        for i in range(1, steps + 1):
            mid_pos = (position[0]+direction*i,position[1])
            if (board.pos_inside_board(mid_pos)):
                if (board.pos_is_empty(mid_pos)):
                    moves.append(mid_pos)
                else:
                    break
        
        r_pos = (position[0]+direction,position[1] - 1)
        board.add_eligble_move(r_pos,moves,self.get_color())
        l_pos = (position[0]+direction,position[1] + 1)
        board.add_eligble_move(l_pos,moves,self.get_color())
            
        return moves
    
    def get_representation(self):
        return "A"

    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} A {RESET}")
        else:
            return(f"{BLUE} A {RESET}")


class Snake(Piece): #TODO does not work when at (7,a), also can go through opponent pieces
    piece_type = "snake"
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

class Lynx(Piece):
    piece_type = "lynx"
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






