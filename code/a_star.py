# Has code for the A* algorithm to run

import warehouse
import stringParser
from node import Node, Position
from frontier import Frontier

# Creates warehouse as a list of chars
def createListOfCharsWarehouse(warehouse):
    return stringParser.splitTemplateRowsIntoDistinctListsOfSingleCharacters(warehouse)

# Gets the coordinates of where the forklift starts
def getInitialForkliftCoordinates(warehouse: list[list]):
    for row in warehouse:
        for col in row:
            if col=='f':
                col_index = row.index(col)
                row_index = warehouse.index(row)
                return Position(row_index, col_index)

# gets the coordinates of the boxes inside of the grid
def getBoxCoordinates(w):
    boxes = []
    for index, row in enumerate(w):
        for i, col in enumerate(row):
            if col=='b':
                col_index = i
                row_index = index
                box = Position(row_index, col_index)
                boxes.append(box)
    return boxes

# Calculates heuristic distance between current node position and the goal position
def h(node: Node, goal: Position):
    # g for first node would be 0
    manhattan_row_dist = abs(node.row-goal.row)
    manhattan_col_dist = abs(node.col-goal.col)
    diagonal_dist = 0
    smaller_manhattan_dist = manhattan_row_dist if manhattan_row_dist < manhattan_col_dist else manhattan_col_dist
    bigger_manhattan_dist = manhattan_row_dist if manhattan_row_dist > manhattan_col_dist else manhattan_col_dist
    bigger_manhattan_dist = bigger_manhattan_dist - smaller_manhattan_dist
    diagonal_dist = smaller_manhattan_dist*3
    orthogonal_dist = bigger_manhattan_dist*2
    return abs(orthogonal_dist + diagonal_dist)

# Expand the frontier with adjacent nodes.  Looks to see if there are walls around it.
def check_adjacent_cells(node: Node, goal: Position, directions: dict[str, Position], dims: tuple[int, int]):
    valid_types = ['e', 'b']
    valid_cells = []
    for direction in directions.values():
        checked_row = direction.row + node.row
        checked_col = direction.col + node.col
        if checked_row < 0 or checked_col < 0: # Funnels out negative indeces
            continue
        elif(checked_row > dims[0] - 1 or checked_col > dims[1] - 1):
            continue
        cell_type = stringParser.queryWarehouse(checked_row, checked_col)    
        if cell_type in valid_types:
            cell_pos = Position(checked_row, checked_col)
            if abs(direction.row) + abs(direction.col) > 1:
                g = 3
            else:
                g = 2
            # if cell_type == 'b':
            #     breakpoint()
            cell_node = Node(h(node, goal), g, cell_pos, node)
            node.child = cell_node
            # if cell_type == 'b':
            #     return [cell_node]
            # else:
            #     valid_cells.append(cell_node)
            valid_cells.append(cell_node)
    return valid_cells


# Function looks thru frontier nodes and expands the node with the smallest cost
def expand_smallest_frontier_neighbor(frontier: Frontier, goal: Position, directions: dict[str, Position], dims: tuple[int, int]):
    # breakpoint()
    first_node = frontier.get_first_node()
    adj_nodes = check_adjacent_cells(first_node, goal, directions, dims)
    goal_node = frontier.expand_frontier(adj_nodes, goal)
    return goal_node

def generate_movements(path_coords: list, directions: dict[str, Position]):
    movements = []
    for i in range(1, len(path_coords)):
        start = path_coords[i-1]
        end = path_coords[i]
        row_diff = end[0] - start[0]
        col_diff = end[1] - start[1]
        direction_diff = Position(row_diff, col_diff)
        for direction, value in directions.items():
            if direction_diff.position == value.position:
                movements.append(['move',direction])
    return movements

def main():
    w = warehouse.w
    w_char_list = createListOfCharsWarehouse(w)
    original_fork_position = getInitialForkliftCoordinates(w_char_list)
    box_coords = getBoxCoordinates(w_char_list)
    num_grid_rows = len(w_char_list)
    num_grid_cols = len(w_char_list[0])
    grid_dims = (num_grid_rows, num_grid_cols)
    directions = {"N": Position(-1, 0), "S": Position(1,0), "E": Position(0,1), "W": Position(0,-1),
                "NW": Position(-1,-1), "NE": Position(-1,1), "SW": Position(1,-1), "SE": Position(1,1)}
    forklift_movements = []
    total_movements = []
    current_forklift_position = 0
    start_nodes = []
    reached = {}
    
    for index, box in enumerate(box_coords):
        if index == 0:
            start_node = Node(h(original_fork_position, box), 0, original_fork_position, None)
            # start_nodes.append(start_node)
        else:
            start_node = Node(h(current_forklift_position, box), reached[original_fork_position.position], current_forklift_position, None)
            start_nodes.append(start_node)
        frontier = Frontier(start_node)
        adj_cell_nodes = check_adjacent_cells(start_node, box, directions, grid_dims)
        box_node = frontier.expand_frontier(adj_cell_nodes, box)
        
        # Expands the frontier until the box_node is found
        while box_node is None:
            box_node = expand_smallest_frontier_neighbor(frontier, box, directions, grid_dims)
        
        opt_path_coordinates = []
        current_node = box_node
        
        # Backtracks adding the coordinates of every node in the optimal path to a list
        while current_node.parent is not None:
            opt_path_coordinates.append(current_node.position)
            current_node = current_node.parent

        opt_path_coordinates.reverse() # Reverses order to get the direction
        # Generates the directions for the robot to reach the cell before the box
        to_box_moves = generate_movements(opt_path_coordinates.copy(), directions)
        
        # Copies over the movements to a master list of commands
        forklift_movements = to_box_moves.copy()
        
        # Adds lift command to pick up the box
        forklift_movements.append(['lift', index])
      
        # Reverses coordinates to get the inverse directions
        opt_path_coordinates.reverse()
        
        # Adds a path through the previous starting nodes to get to the cell to drop off the box
        for node in start_nodes:
            opt_path_coordinates.append(node.position)
        
        # Generates commands to get the forklift back next to the dropoff point
        back_to_unload = generate_movements(opt_path_coordinates.copy(), directions)
        

        backtrack_movements = back_to_unload.copy()
        
        # Removes the final command as that command moves onto the drop zone tile
        backtrack_movements.pop()
        
        # Gets current forklift coordinates
        current_forklift_coords = opt_path_coordinates[len(opt_path_coordinates)-1]
        # Gets current forklift position
        current_forklift_position = Position(current_forklift_coords[0], current_forklift_coords[1])
        
        # Set drop direction so that the forklift can drop off the box in the drop zone
        dropzone_delta_coords = Position(original_fork_position.row - current_forklift_position.row, original_fork_position.col - current_forklift_position.col)

        # Finds the direction the forklift should drop its box
        drop_dir= [k for k, v in directions.items() if v.position == dropzone_delta_coords.position]
        
        # Adds drop command to master list of commands
        backtrack_movements.append(['drop', drop_dir[0]])
        
        # Adds backtracking movements to the forklift movements for the current box
        forklift_movements.extend(backtrack_movements)
        
        # Adds commands for current box to master list of commands
        total_movements.extend(forklift_movements)
        
        # Resets the commands for the new box
        backtrack_movements.clear()
        forklift_movements.clear()
    
        # Updates the reached dictionary with the values from the current frontier
        reached.update(frontier.get_reached_dictionary())
    
    print(reached)
    return total_movements

if __name__ == 'main':
    main()