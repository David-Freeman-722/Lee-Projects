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
    for row in w:
        for col in row:
            if col=='b':
                col_index = row.index(col)
                row_index = w.index(row)
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
            cell_node = Node(h(node, goal), g, cell_pos, node)
            node.child = cell_node
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
    
    for index, box in enumerate(box_coords):
        start_node = Node(h(original_fork_position, box), 0, original_fork_position, None)
        frontier = Frontier(start_node)
        adj_cell_nodes = check_adjacent_cells(start_node, box, directions, grid_dims)
        box_node = frontier.expand_frontier(adj_cell_nodes, box)
        while box_node is None:
            box_node = expand_smallest_frontier_neighbor(frontier, box, directions, grid_dims)
            print(box.position)
            print("IM STUCK IN BOX NODE LOOP")
            print(len(frontier.queue))
            print(index)
            # print(frontier.reached)
        
        opt_path_coordinates = []
        current_node = box_node
        
        while current_node.parent is not None:
            opt_path_coordinates.append(current_node.position)
            current_node = current_node.parent
            print("IM STUCK IN CURRENT NODE LOOP")

        opt_path_coordinates.reverse() # Reverses order to get the direction
        to_box_moves = generate_movements(opt_path_coordinates.copy(), directions)
        # Generates movement directions to get to the box
        forklift_movements = to_box_moves.copy()
        
        # Adds lift command to pick up the box
        forklift_movements.append(['lift', index])
        print(forklift_movements)
        # Reverses coordinates to get the inverse directions
        opt_path_coordinates.reverse()
        back_to_unload = generate_movements(opt_path_coordinates.copy(), directions)
        
        backtrack_movements = back_to_unload.copy()
        last_move = backtrack_movements.pop()
        backtrack_movements.append(['drop', last_move[1]])
        backtrack_movements.append(last_move)
        
        forklift_movements.extend(backtrack_movements)
        
        total_movements.extend(forklift_movements)
        backtrack_movements.clear()
        forklift_movements.clear()
        
        print(forklift_movements)
        
    print(total_movements)
    breakpoint()
    return total_movements

if __name__ == 'main':
    main()