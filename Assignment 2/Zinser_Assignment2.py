#Mitch Zinser
#CSCI 3202 Assignment 2

#Variables that hold the names of the worlds
world1 = "World1.txt"
world2 = "World2.txt"

#Manhattan is |x1-x2| + |y1-y2|
#def hueristic

def a_star(start, graph):
	#Keep track of how many squares are evaluated
	square_eval = 0
	#Priority queue for evaluating border in order
	border = PriorityQueue()
	#Put the first point int eh queue
	border.put(start, 0)
	#Dictionary to store where each square in the grid comes from when traversing
	prev_square = {}
	#Cost to get to a square from the start
	cost = {}
	#Enter start point as having no previous square
	prev_square[start] = None
	#Enter the cost of getting to start, which is 0
	cost[start] = 0
	done = False
	while ((not border.empty()) and (not done)):
		#Get next grid square to evaluate from queue
		cur = border.get()
		#Check to see if we have reached our goal
		if cur == goal:
			done = True
		#If we aren't at goal, evaluate square
		if not done:
			#Iterate through the neightbors of the current square
			for next in #graph.neightbors '''TODO make function''':
				#Calculate new cost for 
				new_cost = cost[cur] + #Calculate cost from this square to next '''TODO'''
				#If the square has not been cost calcuated yet or the new cost is less than previous evaluations
				if ((next not in cost) or (new_cost < cost[next])):
					#Update cost to this square
					cost[next]= new_cost
					#Set priority by adding cost to get her + hueristic cost to goal
					prior = new_cost + #heuristic
					#Add square to the priority queue to evaluate
					border.put(#Next coords, prior)
					#Update previous square
					prev_square[#next coords] = cur coords
					#Increment squares evaluated
					square_eval += 1