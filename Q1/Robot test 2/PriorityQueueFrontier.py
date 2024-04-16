import heapq

class PriorityQueueFrontier():
    def __init__(self):
        self.frontier = []            # Priority queue
        self.states = set()           

    def add(self, node):
        heapq.heappush(self.frontier, (node.f_cost, node))  
        self.states.add(node.state)                        

    def contains_state(self, state):
        return state in self.states                       

    def empty(self):
        return len(self.frontier) == 0                    

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = heapq.heappop(self.frontier)[1]      
            self.states.remove(node.state)                
            return node