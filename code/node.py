
# Position class that holds row and column coordinates in an object
class Position():
    def __init__(self, row, col):
        self.row = row
        self.col = col

# Code to create node objects that contain a grid position and cost

class Node(Position):
    def __init__(self, cost: int, position: Position):
        super().__init__(position.row, position.col)
        self.cost = cost
        
