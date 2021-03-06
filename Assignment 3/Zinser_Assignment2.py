#Mitch Zinser
#CSCI 3202 Assignment 2
import sys #For getting command line arguments
import queue #For Priority Queues
import math

#Function to create list of lists that holds a graph
#Takes in name of text file
#Returns list of lists that is 2d graph
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
#Takes in the heuristic number to use, and the two coordinates to calculate
#Returns heuristic cost to get to end (int)
def heuristic(coord1, coord2, heur_num):
	#Use Manhattan distance
	if heur_num == 0:
		return (abs(coord1[0] + coord2[0]) + abs(coord1[1] + coord2[1]))
	#Use custom heuristic
	elif heur_num == 1:
		x = abs(coord1[1] - coord2[1])
		y = abs(coord1[0] - coord2[0])
		#Calculate the manhattan distance (uses right angles to get to goal, meaning all horizontal or vertical moves)
		#Calculate the linear distance (Probably more diagonal moves rather than horizontal or vertical)
		#Multiply Manhattan distance by 10 (mostly 10 cost moves)
		#Multiply the linear distance by 14 (mostly diagonal moves)
		#Return the minimum of the 2 costs
		return int(min((10 * (x + y)),(14*math.sqrt(pow(x, 2) + pow(y, 2)))))

#Function that takes in coordinates and the graph, and returns a list of the coordinates of the non-wall adjacent squares
#Returns list of of coordinates that are adjacent squares
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
#Returns cost to move into square (int)
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
#Function that reconstructs the most efficient path from the a_star analysis using prev_square dict and cost dict
#Takes in prev_square dict, start and end coordinates
#Returns list that is path
def reconstruct_path(coord_start, coord_end, prev_square):
	#Set current square as goal
	cur = coord_end
	#Store path to finish backwards, add end to path
	path = [cur]
	#Loop until we reach the start
	while cur != coord_start:
		#Set current square as the square that leads to it
		cur = prev_square[cur]
		#Add square to path
		path.append(cur)
	#Reverse path so it reads forwards and return it
	return path[::-1]


#Function that finds most efficient path by evaluating graph using a* method
#Takes in start coordinates, end coordinates, heuristic number, and graph to evaluate
#Returns list that is the most efficient path, cost to get there, and number of square explored
def a_star(start, end, heur_num, graph):
	squares_eval = 0
	#Priority queue for evaluating border in order
	border = queue.PriorityQueue()
	#Put the first point int eh queue
	border.put((0, start))
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
		#Get next grid squrae to evaluate from queue
		cur = border.get()[1]
		#Check to see if we have reached our goal
		if cur == end:
			#break
			done = True

		#If we aren't at goal, evaluate square
		if not done:
			#Iterate through the neightbors of the current square
			for next in get_adjacent(cur, graph):
				#Calculate new cost for getting to this square and getting to the next
				new_cost = cost[cur] + get_cost(cur, next, graph)
				#If the square has not been cost calcuated yet or the new cost is less than previous evaluations
				if ((next not in cost) or (new_cost < cost[next])):
					#Update cost to this square
					cost[next] = new_cost
					#Set priority by adding cost to get her + hueristic cost to goal
					priority = new_cost + heuristic(cur, next, heur_num)
					
					#Add square to the priority queue to evaluate
					border.put((priority, next))
					#Update previous square
					prev_square[next] = cur
					squares_eval += 1
	#Return the two dictionaries (previous square dict and cost dict)
	##return (prev_square, cost)
	#Return most efficient path, cost to get there, and number of squares that have been explored
	return reconstruct_path(start, end, prev_square), cost[(end[0], end[1])], squares_eval

#Prett print graph out
def print_graph(start, end, graph):
	print("Start = S\nEnd = E")
	graph[start[0]][start[1]] = "S"
	graph[end[0]][end[1]] = "E"
	border = "|"
	border += ("-"*len(graph[0]))+"|"
	print(border)
	for i in graph:
		line = "|"
		for j in i:
			if j == 0:
				line += " "
			elif j == 1:
				line += "^"
			elif j == 2:
				line += "@"
			else:
				line += j
		print(line+"|")
	print(border)


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
		print("1: Custom heuristic")
	#Else user has input 2 arguments. Set heuristic to users choice
	else:
		#Check that user is only using valid heuristic choices
		if sys.argv[1] == "0":
			heur = 0
			print("Using Manhattan distance")
		elif sys.argv[1] == "1":
			heur = 1
			print("Using Custom heuristic")
		else:
			print("Invalid command line argument")
			print("Valid command line arguments: None or numbers 0 or 1")
			print("No command line arguments: Use default heuristic (Manhattan distance)")
			print("0: Manhattan distance")
			print("1: Custom heuristic")
	#Variables that hold the names of the worlds
	world1 = "World1.txt"
	world2 = "World2.txt"
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
	print("================Calculating A* for graph1================")
	#Start path finding for graph1, calculate board squares
	path, path_cost, evaluated = a_star(start_square, end_square, heur, graph1)
	print("--------Path--------")
	print(path)
	print("--------Path Cost--------")
	print(path_cost)
	print("--------Squares Evaluated--------")
	print(evaluated)
	print("--------Graph1--------")
	print_graph(start_square, end_square, graph1)
	print("--------Graph1 with path marked with X--------")
	graph1_solved = graph1
	for i in path:
		graph1_solved[i[0]][i[1]] = "X"
	print_graph(start_square, end_square, graph1_solved)

	#Start is at the bottom left corner
	start_square = (len(graph2)-1, 0)
	#Endis at top right corner
	end_square = (0, len(graph2[0])-1)
	print("================Calculating A* for graph2================")
	#Start path finding for graph1, calculate board squares
	path, path_cost, evaluated = a_star(start_square, end_square, heur, graph2)
	print("--------Path--------")
	print(path)
	print("--------Path Cost--------")
	print(path_cost)
	print("--------Squares Evaluated--------")
	print(evaluated)
	print("--------Graph2--------")
	print_graph(start_square, end_square, graph2)
	print("--------Graph2 with path marked with X--------")
	graph2_solved = graph2
	for i in path:
		graph2_solved[i[0]][i[1]] = "X"
	print_graph(start_square, end_square, graph2_solved)

	'''Test Area'''
	'''
	cust_graph = create_graph("Custom_graph.txt")
	#Start is at the bottom left corner
	start_square = (len(cust_graph)-1, 0)
	#Endis at top right corner
	end_square = (0, len(cust_graph[0])-1)
	print("================Calculating A* for custom graph================")
	#Start path finding for graph1, calculate board squares
	path, path_cost, evaluated = a_star(start_square, end_square, heur, cust_graph)
	print("--------Path--------")
	print(path)
	print("--------Path Cost--------")
	print(path_cost)
	print("--------Squares Evaluated--------")
	print(evaluated)
	print("--------Graph2--------")
	print_graph(start_square, end_square, cust_graph)
	print("--------Graph2 with path marked with X--------")
	cust_graph_solved = cust_graph
	for i in path:
		cust_graph_solved[i[0]][i[1]] = "X"
	print_graph(start_square, end_square, cust_graph_solved)
	'''