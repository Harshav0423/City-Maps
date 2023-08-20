# This is EAI Assignment @ IUB MSCS

(1) Preliminary Information:

   - State Space: {All states such that there is a current city location that is reachable from the start city by some set of roads}
   - In the format f(x) = g(x) + h(x), my cost functions f and heuristics h were:
      - Cost Function 1 (Segments) = (total segments traveled so far) + (Euclidean distance from current position to goal state)/(maximum possible segment length)
      - Cost Function 2 (Distance) = (total distance traveled so far) + (Euclidean distance from current position to goal state)
      - Cost Function 3 (Time) = (total time traveled so far) + (Euclidean distance from current position to goal state)/(maximum possible speed limit)
      - Cost Function 4 (Delivery) = (total delivery time traveled so far) + (Euclidean distance from current position to goal state)/(maximum possible speed limit)
   - Since the euclidean distance between any two points in the shortest possible distance, heuristic 2 is less than or equal to the actual distance remaining. Additionally, since the fewest segments on that route would be the shorted possible distance divided by the largest segment possible from out dataset, heuristic 1 must be less than or equal to the true number of segments remaining. Similarly, since the quickest possible time between two points is the shortest distance divided by the maximum speed in our dataset, heuristic 3 and 4 must be less than or equal to the remaining time to the goal. Thus, all 4 heuristics are admissible.
   - Successor Function: searches the road list for matches with the current location to consider all possible next locations (connected by a road) and generates a new state for the fringe if the new state does not visit any place twice and is the lowest-cost option to get to the next location in question.
   - Edge Weights: if our cost is segments, edge weight is always 1. For distance, edge weight is the length of the road represented by the edge. If our cost is time, the edge weight is the time to drive that road segment. If our cost is delivery, the edge weight is the delivery time on the road, established by the problem to add a bit of extra time to account for the possibility that a package may fall off on faster roads.
   - Goal State: {State with path from start to end with minimal cost}


(2) Code Description:

   - This code converts "road-segments.txt" and "city-gps.txt" to lists and uses a function called euclidean to determine the straight line distance from any given city to the goal city in miles. The states are lists of length 6, and the structure of the state is: 
   
         {state = [fx, current location, distance so far, time so far, delivery time so far, [route so far]]} 

   - From the initial state, the program checks for the goal state, runs the successor function, and then chooses the next state from the fringe with minimum estimated cost. If the cost of interest is segments, distance, time, or delivery, the program estimates the cost function 1, 2, 3, or 4, respectively. It stores the relevant data in the state list prior to adding each new state to the fringe. The code uses search algorithm #2.
   
(3) Assumptions, Challenges, & Design Choices

   - The problem we encountered with search algorithm #3 was that the datasets are highly flawed. Some cities have gps coordinates and connecting roads that are not possible, such as Augusta, GA, and Gracewood, GA, which have a road distance of 4 miles and a Euclidean distance (calculated by gps coordinates) of over 137 miles. Additionally, city coordinates appeared to be focused on the city-center, while roads leading to them appeared to stop short of the center. This made consistency very challenging.
   - Instead, we used search algorithm #2, limiting the state space contextually. For instance, we assumed that no single trip would need to visit the same location twice. Additionally, we assumed that if we arrived at a location multiple times during our search, only the time with the minimum cost value could possibly be on the optimal solution to the goal state. These two assumptions greatly limited the state space and made search algorithm #2 viable. We maintain that this is not technically search algorithm #3, as previously explored nodes can still be expanded if they have a lower cost value that prior visits to that node.
   - Prior iterations of this program included versions with a separate successor definition, but the runtime for repeatedly passing large lists through the function’s arguments appeared to slow down the program. Another version included breaking apart the cities and roads by state, to give a smaller set of options to search through given any current city. This also increased runtime noticeably and was discarded. To account for impossible routes, such as trips to or from Newfoundland, we added in a return option with an empty set of directions and infinite costs when possible.