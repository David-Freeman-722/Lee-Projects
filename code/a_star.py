# Has code for the A* algorithm to run

import warehouse
import stringParser
from node import Node, Position
from frontier import Frontier

w = warehouse.w
w_char_list = stringParser.splitTemplateRowsIntoDistinctListsOfSingleCharacters(w)

# Gets the coordinates of where the forklift starts
def getInitialForkliftCoordinates():
    for row in w_char_list:
        for col in row:
            if col=='f':
                col_index = row.index(col)
                row_index = w_char_list.index(row)
                return Position(row_index, col_index)
            
original_fork_position = getInitialForkliftCoordinates()
# original_starting_node = Node()
# gets the coordinates of the boxes inside of the grid
def getBoxCoordinates():
    boxes = []
    for row in w_char_list:
        for col in row:
            if col=='b':
                col_index = row.index(col)
                row_index = w_char_list.index(row)
                box = Position(row_index, col_index)
                boxes.append(box)
    return boxes

box_coords = getBoxCoordinates()
# print(box_coords)

## TEMP COORDS  WILL LOOP THRU BOX COORDINATES NEXT
pos1 = Position(0,2)
goal1 = Position(1, 13)

bumpers = {'North': False, 'South': False, 'East': False, 'West': False}

# Calculates Manhattan distance between input node positions and the goal position
def h(node_position: Position, goal: Position):
    node_row = node_position.row
    node_col = node_position.col
    goal_row = goal.row
    goal_col = goal.col
    manhattan_row_dist = abs(goal_row-node_row)
    manhattan_col_dist = abs(goal_col-node_col)
    total_cost = manhattan_row_dist+manhattan_col_dist
    return total_cost

# Calculates the total cost to get from the initial start to the current node
def g(initial_position: Position, node_position: Position):
    i_row = initial_position.row # Gets the row coordinate
    i_col = initial_position.col
    node_row = node_position.row # Row coordinate
    node_col = node_position.col
    current_cost_row = abs(i_row-node_row)
    current_cost_col = abs(i_col-node_col)
    total_cost = current_cost_row+current_cost_col
    return total_cost

def f(starting_position: Position, node_position: Position, goal_position: Position):
    h_cost = h(node_position, goal_position) # Holds row and col cost for h
    g_cost = g(starting_position, node_position) # Holds row and col cost for g
    print(f"H cost {h_cost}")
    print(f"G cost {g_cost}")
    cost = h_cost+g_cost
    return cost

start_node = Node(f(original_fork_position, original_fork_position, goal1), original_fork_position)

# # Expand the frontier with adjacent nodes.  Looks to see if there are walls around it.
def check_adjacent_cells(node: Node):
    directions = {"N": Position(-1, 0), "S": Position(1,0), "E": Position(0,1), "W": Position(0,-1),
                "NW": Position(-1,-1), "NE": Position(-1,1), "SW": Position(1,-1), "SE": Position(1,1)}
    valid_types = ['e', 'b']
    valid_cells = []
    for direction in directions.values():
        checked_row = direction.row + node.row
        checked_col = direction.col + node.col
        cell_type = stringParser.queryWarehouse(checked_row, checked_col)
        if cell_type in valid_types:
            valid_cells.append(Position(checked_row, checked_col))
            
    return valid_cells

adj_cells = check_adjacent_cells(start_node)
frontier = Frontier(start_node)
def expand_frontier(frontier: Frontier, neighbors: list[Position]):
    for neighbor_position in neighbors:
        #  Add accessible adjecent nodes to the frontier.  Check to see if you can move in them first
        cost = f(original_fork_position, neighbor_position, goal1)
        print(f"Cost is {cost}")
        neighbor = Node(cost, neighbor_position)
        frontier.add_node(neighbor)
    
expand_frontier(frontier, adj_cells)
frontier_nodes = frontier.getFrontier()