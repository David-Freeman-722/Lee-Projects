
# Position class that holds row and column coordinates in an object
class Position():
    def __init__(self, row, col, type=None):
        self.row: int = row
        self.col: int = col
        self.position: tuple = (self.row, self.col)
        self.type: str = type
        
    def get_coordinates(self):
        return (self.row, self.col)
    
    def get_row(self):
        return self.row
    
    def get_col(self):
        return self.col
    
    def set_row(self, row):
        self.row = row
        
    def set_col(self, col):
        self.col = col
        

# Code to create node objects that contain a grid position and cost

class Node(Position):
    def __init__(self, h_cost: int, g_cost: int, position: Position, parent, type='e'):
        super().__init__(position.row, position.col)
        self.h_cost: int = h_cost
        self.g_cost: int = g_cost
        self.f_cost: int = h_cost + g_cost
        self.parent: Node = parent
        self.child: Node = None
        
    def get_f_cost(self):
        return self.f_cost
    
    def get_g_cost(self):
        return self.g_cost
    
    def get_h_cost(self):
        return self.h_cost
        
