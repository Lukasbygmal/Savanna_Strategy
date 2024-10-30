from abc import ABC, abstractmethod
from typing import Literal


Color = Literal['red', 'blue']

RED = "\033[31m" 
BLUE = "\033[34m" 
RESET = "\033[0m"


class Game:
    def __init__(self):
        pass

class Board:
    def __init__(self):
        self.grid = [[' ' for _ in range(8)] for _ in range(8)]

    def display(self):
        print("  A B C D E F G H")
        for i, row in enumerate(self.grid):
            print(f"{8 - i} " + " ".join(row) + f" {8 - i}")
        print("  A B C D E F G H")

    def setup(self):
        pass

class Piece:
    def __init__(self,color: Color,position: tuple):
        self.__color = color
        self.__position = position


    @abstractmethod
    def get_possible_moves(self,position, board):
        pass

    def get_color(self) -> Color:
        return self.__color
    
    def get_position(self):
        return self.__position
    
    def move(self,new_position):
        self.__position = new_position
    
    @abstractmethod
    def __str__(self) -> str:
        pass



class Ape(Piece):
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)

    def get_possible_moves(self,position, board):
        pass

    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} A {RESET}")
        else:
            return(f"{BLUE} A {RESET}")


class Snake(Piece):
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)
    
    def get_possible_moves(self,position, board):
        pass
            

    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} S {RESET}")
        else:
            return(f"{BLUE} S {RESET}")


class Crab(Piece):
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)
    
    def get_possible_moves(self,position, board):
        pass
            

    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} C {RESET}")
        else:
            return(f"{BLUE} C {RESET}")

class Meerkat(Piece):
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)
    
    def get_possible_moves(self,position, board):
        pass
            

    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} M {RESET}")
        else:
            return(f"{BLUE} M {RESET}")

class Lynx(Piece):
    def __init__(self, color, initial_position):
        super().__init__(color,initial_position)
    
    def get_possible_moves(self,position, board):
        pass
            

    def __str__(self) -> str:
        if (self.get_color()== 'red'):
            return(f"{RED} L {RESET}")
        else:
            return(f"{BLUE} L {RESET}")






