from abc import ABC, abstractmethod
from typing import Literal
import math

Color = Literal['red', 'blue']

RED = "\033[31m" 
BLUE = "\033[34m" 
RESET = "\033[0m"

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


class Mandrill(Piece): 
    piece_type = "mandrill"
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


            if (position[0] == 6 and color == "blue" ) or (position[0]==1 and color == "red" ):
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
            board.add_eligble_move_mandrill(self,r_pos,moves,self.get_color())
            l_pos = (position[0]+direction,position[1] + 1)
            board.add_eligble_move_mandrill(self,l_pos,moves,self.get_color())

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
        self.piece_value = 5

    def devolve(self):
        self.evolved = False
        self.piece_value = 1

    def will_evolve(self, position):
        """If an mandrill will evolve at a certain position, returns True if evolved else False"""
        if not self.evolved:
            if (position[0] == 0 and self.get_color() == "blue" ) or (position[0]==7 and self.get_color() == "red" ):
                return True
        return False
            
    def get_representation(self):
        if not self.evolved:
            return "M"
        else:
            return "B"


    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} M {RESET}")
        else:
            return(f"{BLUE} M {RESET}")


class Python(Piece):
    piece_type = "python"
    piece_value = 5
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)
    
    def get_possible_moves(self,position, board)->list:
        moves = []
        directions = [(1,0),(0,1),(-1,0),(0,-1)]
        for d in directions:
            l_path = True
            r_path = True
            for x in range (1,4):
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


class Giraffe(Piece):
    piece_type = "giraffe"
    piece_value = 3
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)
    
    def get_possible_moves(self,position, board):
        moves = []
        for d in range(-1,2):
            for i in range(1,3):
                new_pos = (position + (i,0))
                new_pos = (position[0]+ i, position[1])
                if (board.add_eligble_move(new_pos,moves,self.get_color())!= True):
                    break
        
        #TODO should probably check whether i really should do it like this with for loop
        for d in range(-1,2):
            for i in range(1,8):
                new_pos = (position[0], position[1]+i*d)
                if (board.add_eligble_move(new_pos,moves,self.get_color())!=True):
                    break

        return moves
            

    def get_representation(self):
        return "G"

    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} G {RESET}")
        else:
            return(f"{BLUE} G {RESET}")

class Meerkat(Piece): 
    piece_type = "meerkat"
    piece_value = 3
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)
    
    def get_possible_moves(self,position, board):
        moves = []
        directions = [(1,0),(0,1),(-1,0),(0,-1)]
        for d in directions:
            for i in range(1,4):
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

class Caracal(Piece):
    piece_type = "caracal"
    piece_value = 6
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
        return "C"

    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} C {RESET}")
        else:
            return(f"{BLUE} C {RESET}")
