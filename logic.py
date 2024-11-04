from abc import ABC, abstractmethod
from typing import Literal


Color = Literal['red', 'blue'] #blue down, red up

RED = "\033[31m" 
BLUE = "\033[34m" 
RESET = "\033[0m"


class Game:
    
    def __init__(self):
        pass

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]

    def display(self):
        print("  A B C D E F G H")
        for i, row in enumerate(self.grid):
            print(f"{8 - i} " + " ".join(row) + f" {8 - i}")
        print("  A B C D E F G H")

    def setup(self):
        pass

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

    def get_piece_at_pos(self,position):
        return self.grid[position[0]][position[1]]

    def pos_inside_board(self,position)-> bool:
        return 0 <= position[0] < 8 and 0 <= position[1] < 8
    
    def add_eligble_move(self,new_pos,moves,own_color) ->bool:
        result = False
        if (self.pos_inside_board(new_pos)):
                if (self.pos_is_empty(new_pos)):
                    moves.append(new_pos)
                    result = True

                else:
                    piece = self.get_piece_at_pos(new_pos)
                    if(piece.get_color() != own_color):
                        moves.append(new_pos)
                        result = True
        return result
        



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
    
    def move(self,new_position,board):
        self.__position = new_position

    def piece_type(self):
        return self.piece_type
    
    def be_taken(self,board):
        board.grid[self.position] = (0,0)

    
    @abstractmethod
    def __str__(self) -> str:
        pass



class Ape(Piece): ##TODO checck if actually cheks bounds
    piece_type = "ape"
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)

    def get_possible_moves(self,position, board)->list:
        moves = []
        direction = 1
        if (self.get_color()=='blue'):
            direction = -1
        for i in range(1,3):
            new_pos = (position[0]+direction*i,position[1])
            if (board.pos_inside_board(new_pos)):
                if (board.pos_is_empty):
                    moves.append(new_pos)
                else:
                    piece = board.get_piece_at_pos(new_pos)
                    if(piece.color == self.get_color() or piece.piece_type == "ape"):
                        ()
                    else:
                        moves.append(new_pos)
            
        return moves

    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} A {RESET}")
        else:
            return(f"{BLUE} A {RESET}")


class Snake(Piece):
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
                if (x%2 == 0):
                    new_pos = (position[0] + d[0]*x,position[1]+ d[1]*x)
                    if (board.add_eligble_move(new_pos,moves,self.get_color())==False):
                        break

                else:
                    
                    if l_path:
                        l_pos = (position[0] + x * d[0] + d[1], position[1] + x * d[1] + d[0])
                        if (board.add_eligble_move(l_pos,moves,self.get_color())==False):
                            l_path = False
                
                    if r_path:
                        r_pos = (position[0] + x * d[0] - d[1], position[1] + x * d[1] - d[0])
                        if (board.add_eligble_move(r_pos,moves,self.get_color())==False):
                            r_path = False
        moves = set(moves)
        return moves
        

            

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
                board.add_eligble_move(new_pos,moves,self.get_color())

        directions = [(1,0),(0,1),(-1,0),(0,-1)]
        for d in directions:
            new_pos = position + d
            new_pos = (position[0] + d[0],position[1] + d[1])
            board.add_eligble_move(new_pos,moves,self.get_color())
        return moves
            

    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} L {RESET}")
        else:
            return(f"{BLUE} L {RESET}")






