#Mitch Zinser
#CSCI 3202 Assignment 2
import sys #For getting command line arguments
#Variables that hold the names of the worlds
world1 = "World1.txt"
world2 = "World2.txt"

def create_graph(text_file):
	#List to hold lists for each line of graph input file
	graph = []
	#Open file as file
	with open(text_file) as file:
		#Iterate through lines of file
		for i in file.readlines():
			#Split lines of file at default (split at spaces and remove spaces)
			line = i.split()
			#Make sure line isn't empty
			if len(line) > 0:
				#If line isn't empty, append line to graph, which is a list of lists
				#Iterate through list and convert list of strings to list of ints (list comprehension)
				graph.append([int(x) for x in line])
	#Return the graph
	return graph
#Manhattan is |x1-x2| + |y1-y2|
#Takes in the heuristic number to use, and the two coordinates to calculate
def hueristic(heur_num, coord1, coord2):
	#Use Manhattan distance
	if heur_num == 0:
		return (abs(coord1[0] + coord2[1]) + abs(coord1[1] + coord2[1]))
		#TODO create second heuristic
	elif heur_num == 1:
		pass
'''
#Function that takes in coordinates and the graph, and returns a list of the coordinates of the non-wall adjacent squares
def get_adjacent(coord, graph):
	#List of adjacent coordinates
	adj = []
	#Check 9 adjacent squares
	#Up Left
	if graph[coord[0]-1][coord[1]-1] != "2"
	#Up
	#Up Right
	#Left
	#Right
	#Down Left
	#Down
	#Down Right

def a_star(start, end, heur_num, graph):
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
			for next in get_adjacent(cur, graph) #TODO make function:
				#Calculate new cost for 
				new_cost = cost[cur] + #Calculate cost from this square to next #TODO
				#If the square has not been cost calcuated yet or the new cost is less than previous evaluations
				if ((next not in cost) or (new_cost < cost[next])):
					#Update cost to this square
					cost[next]= new_cost
					#Set priority by adding cost to get her + hueristic cost to goal
					prior = new_cost + #heuristic TODO
					#Add square to the priority queue to evaluate
					border.put(#Next coords, prior) #TODO
					#Update previous square
					prev_square[#next coords] = cur coords TODO
					#Increment squares evaluated
					square_eval += 1

'''
#Only run this if file is being run directly
if __name__ == "__main__":
	#Get command line arguments
	#If user only calls script, use default heuristic
	if len(sys.argv) == 1:
		#Default heuristic is Manhattan distance (heuristic number 0)
		heur = 0
		print("Using default heuristic (Manhattan distance)")
	#Check that user only input 1 or 0 command line argument
	elif len(sys.argv) > 2:
		print("Too many command line arguments input")
		print("Valid command line arguments: None or numbers 0 or 1")
		print("No command line arguments: Use default heuristic (Manhattan distance)")
		print("0: Manhattan distance")
		print("1: (Fill in with heuristic)") #TODO
	#Else user has input 2 arguments. Set heuristic to users choice
	else:
		#Check that user is only using valid heuristic choices
		if sys.argv[1] == "0":
			heur = 0
			print("Using Manhattan distance")
		elif sys.argv[1] == "1":
			heur = 1
			print("Using (Fill in heuristic)") #TODO
		else:
			print("Invalid command line argument")
			print("Valid command line arguments: None or numbers 0 or 1")
			print("No command line arguments: Use default heuristic (Manhattan distance)")
			print("0: Manhattan distance")
			print("1: (Fill in with heuristic)") #TODO
	#Read World1.txt and create graph
	graph1 = create_graph(world1)
	#[print(x) for x in graph1] #Print graph
	#Read World2.txt and create graph
	graph2 = create_graph(world2)
	#Define the starting and ending goals for graph1 (-1 to account for 0 indexing)
	#Start is at the bottom left corner
	start_square = (len(graph1)-1, 0)
	#Endis at top right corner
	end_square = (0, len(graph1[0])-1)
	#Start path finding for graph1, calculate board squares
	#a_star(start_square, end_square, graph1)
	#Recreate path for graph1