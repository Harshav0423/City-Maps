#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by:
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#

# !/usr/bin/env python3
import sys
import math

# Main heuristic. This calculates Euclidean difference between the city in a given state
# and the destination city. Returns Euclidean distance or -1 if the "city" has no known
# latitude and longitude, IE not in cities list.
def euclidean(state, end_coords, cities):
    latitude,longitude = 200,200
    end_lat,end_long = end_coords[0],end_coords[1]
    for entry in cities:
        match = entry.split()
        if state[1] in match:
            latitude,longitude = match[1],match[2]
    if latitude == 200 or longitude == 200:
        return -1
    max_lat = max(float(latitude),float(end_lat))
    delta_x = abs(float(latitude)-float(end_lat))*math.cos(max_lat*math.pi/180)*69.172
    delta_y = abs(float(longitude)-float(end_long))*68.703
    euc_dist = math.sqrt((delta_x)**2+(delta_y)**2)
    return euc_dist

# Gets route and returns all the necessary intel for main.
def get_route(start, end, cost):
    cities = []
    for line in open("city-gps.txt","r"):
        cities.append(line)
        if end in line:
            end_coords = line.split()[-2:]
    roads = []
    max_length = 0
    max_speed = 0
    for line in open("road-segments.txt", "r"):
        roads.append(line)  
        travel_plan = line.split()
        if float(travel_plan[2]) > max_length:
            max_length = float(travel_plan[2])
        if float(travel_plan[3]) > max_speed:
            max_speed = float(travel_plan[3])
    state = [0., start, 0., 0., 0., []]
    fringe = []
    best_list = []
    while True:
        for i in range(len(roads)):
            travel_plan = roads[i].split()
            if state[1] in travel_plan:
                new_state = [0.]
                if travel_plan[0] == state[1]:
                    new_state.append(travel_plan[1])
                    destination = travel_plan[1]
                elif travel_plan[1] == state[1]:
                    new_state.append(travel_plan[0])
                    destination = travel_plan[0]
                new_state.append(state[2]+float(travel_plan[2]))
                new_state.append(state[3]+float(travel_plan[2])/float(travel_plan[3]))
                if float(travel_plan[3]) >= 50:
                    p = math.tanh(float(travel_plan[2])/1000)
                else: p = 0
                new_state.append(state[4]+float(travel_plan[2])/float(travel_plan[3])
                                 +p*2*(float(travel_plan[2])/float(travel_plan[3])+state[4]))
                no_backtracking = True
                route_so_far = []
                route_to_add = (destination,str(travel_plan[4])+" for "
                                     +str(travel_plan[2])+" miles")
                for route in state[5]:
                    route_so_far.append(route)
                    if route_to_add in route:
                        no_backtracking = False            
                route_so_far.append(route_to_add)
                new_state.append(route_so_far)
                #calculation for f(x) = g(x) + h(x)
                euc_dist = euclidean(new_state, end_coords, cities)
                cost_methods = ["segments", "distance", "time", "delivery"]
                hx = 0
                if cost_methods.index(cost) == 0:
                    gx = len(new_state[5])
                    if euc_dist != -1:
                        hx = euc_dist/max_length
                elif cost_methods.index(cost) == 1:
                    gx = new_state[2]
                    if euc_dist != -1:
                        hx = euc_dist
                elif cost_methods.index(cost) == 2:
                    gx = new_state[3]
                    if euc_dist != -1:
                        hx = euc_dist/max_speed
                elif cost_methods.index(cost) == 3:
                    gx = new_state[4]
                    if euc_dist != -1:
                        hx = euc_dist/max_speed
                new_state[0] = gx + hx
                
                for item in best_list:
                    if item[0]==(travel_plan[0],travel_plan[1]):
                        if item[1] <= new_state[0]:
                            no_backtracking = False
                if no_backtracking:
                    fringe.append(new_state)
                    best_list.append([(travel_plan[0],travel_plan[1]),new_state[0]])
        state = min(fringe)
        if state[1]==end:
            end_state = state
            break
        else:
            fringe.remove(state)
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    route_taken = end_state[5]
    
    return {"total-segments" : len(route_taken), 
            "total-miles" : end_state[2], 
            "total-hours" : end_state[3],
            "total-delivery-hours" : end_state[4], 
            "route-taken" : route_taken}

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


