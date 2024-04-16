class Node():
    def __init__(self, state, parent, action, cost, f_cost):
        self.state = state            
        self.parent = parent          
        self.action = action          
        self.cost = cost              
        self.f_cost = f_cost

    def __lt__(self,other):
           return self.f_cost < other.f_cost