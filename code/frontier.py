# Contains the frontier for the A* search.  Stores nodes which are tuples of grid locations 
# along with their individual cost from the starting node

from node import Node, Position

class Frontier:
    def __init__(self, start_node: Node):
        self.queue: list[Node] = [start_node] # Holds a queue of nodes
        self.size: int = 1
        self.reached = {start_node.position: start_node.f_cost}
    
    # Adds a node to the priority queue frontier
    def add_node(self, node: Node):
        self.queue.append(node)
        self.queue.sort(key=lambda n: n.f_cost) # Sorts list based on cost
        if node.position not in self.reached.keys() or self.reached[node.position] < node.f_cost:
            self.reached[node.position] = node.f_cost

    # Removes node from frontier priority queue (occurs when the node is chosen)
    def pop_node(self):
        node: Node = self.queue.pop(0)
        self.size -= 1
        return node
    
    # Expands frontier to include the nodes
    def expand_frontier(self, neighbors: list[Node], goal: Position):
        # breakpoint()
        chosen_node = self.pop_node()
        if chosen_node.position == goal.position:
            return chosen_node
        else:
            for neighbor in neighbors:
                if neighbor.position not in self.reached.keys() or self.reached[neighbor.position] < neighbor.f_cost:
                    #  Add accessible adjecent nodes to the frontier.  Check to see if you can move in them first
                    self.add_node(neighbor)
            
    # Returns size of the queue
    def get_queue_size(self):
        return len(self.queue)
        
    # Returns the queue of neighbors
    def get_frontier_queue(self):
        return self.queue
    
    # Adds entries to reached dict
    def add_to_reached_dictionary(self, dict):
        self.reached.update(dict)
    
    # Returns the reached dictionary storing all the visited nodes
    def get_reached_dictionary(self):
        return self.reached
    
    # Returns the first node in the queue
    def get_first_node(self):
        return self.queue[0]
    
    # Returns list of the costs for each node in the frontier
    def get_frontier_node_costs(self):
        costs = [i.cost for i in self.queue]
        return costs
    
    def empty_queue(self):
        self.queue.clear()
    
    