#Mitch Zinser
#CSCI 3202 Assignment 2
import sys #For getting command line arguments
import queue #For Priority Queues
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
def heuristic(coord1, coord2, heur_num):
	#Use Manhattan distance
	if heur_num == 0:
		return (abs(coord1[0] + coord2[1]) + abs(coord1[1] + coord2[1]))
		#TODO create second heuristic
	elif heur_num == 1:
		pass

#Function that takes in coordinates and the graph, and returns a list of the coordinates of the non-wall adjacent squares
def get_adjacent(coord, graph):
	#Check if passed in coordinates are out of range
	if (coord[0] >= len(graph)) or (coord[0] < 0):
		return [None]
	if (coord[1] >= len(graph[coord[0]])) or (coord[1] < 0):
		return [None]
	#Store input coordinates as y and x for easier reading of the code
	y = coord[0]
	x = coord[1]
	#Max value that y and x can be (-1 to account for 0 indexing)
	y_max = len(graph)-1
	x_max = len(graph[y])-1
	#List of adjacent coordinates
	adj = []
	#Check 8 adjacent squares
	#Up Left
	#If not wall or out of index range for graph, add to adjacent list
	if ((y>0) and (x>0)) and (graph[y-1][x-1] != 2):
		adj.append((y-1,x-1))
	#Up
	#If not wall or out of index range for graph, add to adjacent list
	if (y>0) and (graph[y-1][x] != 2):
		adj.append((y-1,x))
	#Up Right
	#If not wall or out of index range for graph, add to adjacent list
	if ((y>0) and (x<x_max)) and (graph[y-1][x+1] != 2):
		adj.append((y-1,x+1))
	#Left
	#If not wall or out of index range for graph, add to adjacent list
	if (x>0) and (graph[y][x-1] != 2):
		adj.append((y,x-1))
	#Right
	#If not wall or out of index range for graph, add to adjacent list
	if (x<x_max) and (graph[y][x+1] != 2):
		adj.append((y,x+1))
	#Down Left
	#If not wall or out of index range for graph, add to adjacent list
	if ((y<y_max) and (x>0)) and (graph[y+1][x-1] != 2):
		adj.append((y+1,x-1))
	#Down
	#If not wall or out of index range for graph, add to adjacent list
	if (y<y_max) and (graph[y+1][x] != 2):
		adj.append((y+1,x))
	#Down Right
	#If not wall or out of index range for graph, add to adjacent list
	if ((y<y_max) and (x<x_max)) and (graph[y+1][x+1] != 2):
		adj.append((y+1,x+1))
	return adj
#Function that calculates the cost to go from one square to another adjacent square
#Takes in the current coordinates and the coordinates of the square to move to
def get_cost(cur_coord, next_coord, graph):
	#Check if move is horizontal or vertical by seeing if one axis doesn't change
	if (cur_coord[0] == next_coord[0]) or (cur_coord[1] == next_coord[1]):
		#Horizontal or vertical moves cost 10
		#Check if moving into mountain
		if graph[next_coord[0]][next_coord[1]] == 1:
			#Moving into a mountain costs 10 extra
			return 20
		#Return cost to move horizontally or vertically
		return 10

	#Else move is diagonal
	else:
		#Diagonal moves cost 14
		#Check if moving into mountain
		if graph[next_coord[0]][next_coord[1]] == 1:
			#Moving into a mountain costs 10 extra
			return 24
		#Return cost to move diagonally
		return 14

def a_star(start, end, heur_num, graph):
	#Keep track of how many squares are evaluated
	square_eval = 0
	#Priority queue for evaluating border in order
	border = queue.PriorityQueue()
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
		if cur == end:
			done = True
		#If we aren't at goal, evaluate square
		if not done:
			#Iterate through the neightbors of the current square
			for next in get_adjacent(cur, graph): #TODO make function DONE
				#Calculate new cost for 
				new_cost = cost[cur] + get_cost(cur, next, graph) #Calculate cost from this square to next #TODO DONE
				#If the square has not been cost calcuated yet or the new cost is less than previous evaluations
				if ((next not in cost) or (new_cost < cost[next])):
					#Update cost to this square
					cost[next]= new_cost
					#Set priority by adding cost to get her + hueristic cost to goal
					priority = new_cost + heuristic(cur, next, heur_num) #heuristic TODO DONE
					#Add square to the priority queue to evaluate
					border.put(next, priority) #TODO DONE
					#Update previous square
					prev_square[next] = cur #TODO DONE
					#Increment squares evaluated
					square_eval += 1
	#Return the two dictionaries (previous square dict and cost dict)
	return (prev_square, cost)


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
	came_from, square_cost = a_star(start_square, end_square, heur, graph1)
	'''
	print("--------Came From--------")
	[print(i, came_from[i]) for i in came_from]
	print("--------Square Cost--------")
	[print(i, square_cost[i]) for i in square_cost]
	'''
	#Recreate path for graph1
	'''Test Area'''
	##print(get_cost((0,1), (1,2), graph1))