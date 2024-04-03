#These libraries are used for generating random numbers, visualization, and numerical operations, respectively.
import random
import matplotlib.pyplot as plt
import numpy as np

#This defines a class TSPSolver that represents a solver for the Traveling Salesman Problem (TSP). It has an initializer method __init__ that takes places and distances as input parameters.
# places is a list of place names, and distances is a dictionary containing distances between places.
class TSPSolver:
    def __init__(self, places, distances):
        self.places = places
        self.distances = distances

 #This method calculates the total distance of a given route (visiting order) for all the places. 
#It iterates over the given route and sums up the distances between consecutive cities, including the distance from the last city back to the starting city.   
    def calculate_total_distance(self, route):
        total_distance = 0
        for i in range(len(route) - 1):
            current_city = route[i]
            next_city = route[i + 1]
            total_distance += self.distances[current_city][next_city]
        total_distance += self.distances[route[-1]][route[0]]  # Return to starting point
        return total_distance

#This defines a class HillClimbingTSP that represents a solver using the hill climbing algorithm for the TSP.
# It has an initializer method __init__ that takes a solver object as input parameter
class HillClimbingTSP:
    def __init__(self, solver):
        self.solver = solver

    #This method generates a random initial route visiting all places.
   # It converts the set of places into a list, then uses random.sample() to shuffle the list and return a random route.
    def generate_random_route(self):
           return random.sample(list(self.solver.places), len(self.solver.places))

    #This method explores neighboring solutions by swapping the order of two randomly chosen places in the current route. 
    #It makes a copy of the current route, selects two random indices, and swaps the places at those indices.
    def explore_neighbours(self, route):
        new_route = route[:]
        idx1, idx2 = random.sample(range(len(new_route)), 2)
        new_route[idx1], new_route[idx2] = new_route[idx2], new_route[idx1]
        return new_route

 #This method implements the core logic of hill climbing for the TSP. 
#It starts with a random initial route and iteratively explores neighboring solutions. If a neighboring route has a shorter total distance, it replaces the current route with the neighbor.   
    def hill_climbing(self, max_iterations):
        current_route = self.generate_random_route()
        current_distance = self.solver.calculate_total_distance(current_route)

        for _ in range(max_iterations):
            neighbour_route = self.explore_neighbours(current_route)
            neighbour_distance = self.solver.calculate_total_distance(neighbour_route)

            if neighbour_distance < current_distance:
                current_route = neighbour_route
                current_distance = neighbour_distance

        return current_route, current_distance

#This function visualizes a route on a scatter plot. It takes places, a dictionary of place names and their coordinates, and route, a list representing the route. 
#It plots the places as blue dots, the starting place as a green dot, and the route as black lines connecting the places. Finally, it adds titles, labels, and grid to the plot and displays it using plt.show().
def visualize_route(places, route):
    x_coords = [place[0] for place in places.values()]
    y_coords = [place[1] for place in places.values()]

    plt.figure(figsize=(8, 6))
    plt.plot(x_coords, y_coords, 'bo')  # Plot cities
    plt.plot(x_coords[0], y_coords[0], 'go')  # Plot starting city
    for i in range(len(route) - 1):
        city1 = route[i]
        city2 = route[i + 1]
        plt.plot([places[city1][0], places[city2][0]], [places[city1][1], places[city2][1]], 'k-')  # Plot route
    plt.plot([places[route[-1]][0], places[route[0]][0]], [places[route[-1]][1], places[route[0]][1]], 'k-')  # Return to starting point
    plt.title('TSP Route')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.show()

# It defines the places and distances, creates instances of the TSP solver and hill climbing solver, runs the hill climbing algorithm to find the final route, prints the final route 
#and its total distance, and visualizes the route using the visualize_route() function.
places = {'Dorado Park': (0, 0), 'Khomasdal': (3, 1), 'Katutura': (1, 3), 'Eros': (4, 3), 'Klein Windhoek': (2, 0)}
distances = {
    'Dorado Park': {'Dorado Park': 0, 'Khomasdal': 7, 'Katutura': 20, 'Eros': 15, 'Klein Windhoek': 12},
    'Khomasdal': {'Dorado Park': 10, 'Khomasdal': 0, 'Katutura': 6, 'Eros': 14, 'Klein Windhoek': 18},
    'Katutura': {'Dorado Park': 20, 'Khomasdal': 6, 'Katutura': 0, 'Eros': 15, 'Klein Windhoek': 30},
    'Eros': {'Dorado Park': 15, 'Khomasdal': 14, 'Katutura': 25, 'Eros': 0, 'Klein Windhoek': 2},
    'Klein Windhoek': {'Dorado Park': 12, 'Khomasdal': 18, 'Katutura': 30, 'Eros': 2, 'Klein Windhoek': 0}
}

tsp_solver = TSPSolver(places.keys(), distances)
hill_climbing_solver = HillClimbingTSP(tsp_solver)
final_route, total_distance = hill_climbing_solver.hill_climbing(1000)
print("Final route found by hill climbing:", final_route)
print("Total distance of the final route:", total_distance)

visualize_route(places, final_route)
