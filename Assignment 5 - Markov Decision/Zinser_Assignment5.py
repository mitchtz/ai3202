#Mitch Zinser
#CSCI 3202 Assignment 5
import sys #For getting command line arguments
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
				#Store new line with rewards
				new_line = []
				#Assign reward value for each square
				for i in line:
					#If empty
					if i == "0":
						new_line.append(0.0)
					#If mountain
					elif i == "1":
						new_line.append(-1.0)
					#Wall, set to -inf
					elif i == "2":
						new_line.append(float("-inf"))
					#Snake
					elif i == "3":
						new_line.append(-2.0)
					#Barn
					elif i == "4":
						new_line.append(1.0)

					#If anything else
					else:
						new_line.append(float(i))


				#Iterate through list and convert list of strings to list of ints (list comprehension)
				graph.append(new_line)
	#Return the graph
	return graph

'''
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
'''
#Function that constructs the path from the mdp using the direction dictionary
#Takes in the direction dictionary, the start point coordinates, and the end point coordinates
#Returns list that is the path
def construct_path(dir_dict,start,end,util):
	
	#Set current square as start
	cur = start
	#Store path in list
	path = [cur]
	#Iterate until goal is reached
	##print(cur,dir_dict[cur])
	#Limit the number of times the loop can run in case path is never found
	loop_i = 0
	#Total utility of the path
	tot_util = util[cur]
	while cur != end:
		#Check if we are stuck in a loop, limit iterations of loop
		if loop_i > 100:
			break
		#Check direction and go that way
		#North
		if dir_dict[cur] == 0:
			#cur[0] = cur[0]-1
			cur = (cur[0]-1,cur[1])
			#Add square to path
			##print(cur,"0")
			path.append(cur)
		#East
		elif dir_dict[cur] == 1:
			cur = (cur[0],cur[1]+1)
			#Add square to path
			##print(cur,"1")
			path.append(cur)
		#South
		elif dir_dict[cur] == 2:
			cur = (cur[0]+1,cur[1])
			#Add square to path
			##print(cur,"2")
			path.append(cur)
		#West
		else:
			cur = (cur[0],cur[1]-1)
			#Add square to path
			##print(cur,"3")
			path.append(cur)
		tot_util += util[cur]
		loop_i += 1
	print("--------Total utility--------")
	print(tot_util)
	return path
#Function that calculates the utility of going in each direction from the passed in
#coordinates and finds the direction that yields the most utility
#Takes in coordinates to find best direction to go, graph, dictionary of utility values,discount factor
#Reuturns tuple of best utility and direction to go to get it
def calc_util(row_y,col_x,graph,util_dict,discount_rate):
	if graph[row_y][col_x] == 50:
		return 50,0
	else:
		'''
		utility of each direction
		0 = north
		1 = East
		2 = South
		3 = West
		'''
		#If not valid, assign as float("-inf")
		'''Get neighbors utility'''
		#Check all neighbors, get utility from them
		neighbor_util = []
		#North
		#Check if is out of bounds
		if (row_y-1) < 0:
			neighbor_util.append(0)
		else:
			neighbor_util.append(util_dict[(row_y-1,col_x)])
		#East
		#Check if is out of bounds
		if (col_x+1) >= len(graph[row_y]):
			neighbor_util.append(0)
		else:
			neighbor_util.append(util_dict[(row_y,col_x+1)])
		#South
		#Check if is out of bounds
		if (row_y+1) >= len(graph):
			neighbor_util.append(0)
		else:
			neighbor_util.append(util_dict[(row_y+1,col_x)])
		#West
		#Check if is out of bounds
		if (col_x-1) < 0:
			neighbor_util.append(0)
		else:
			neighbor_util.append(util_dict[(row_y,col_x-1)])
		'''Calculate the utility for each direction, including uncertainty'''
		#Holds the utility for each direction with uncertainty
		#0.8 chance to go where intended
		#0.1 chance to go right or left of intended
		dir_util = []
		#North
		dir_util.append((0.8*neighbor_util[0])+(0.1*neighbor_util[1])+(0.1*neighbor_util[3]))
		#East
		dir_util.append((0.8*neighbor_util[1])+(0.1*neighbor_util[2])+(0.1*neighbor_util[0]))
		#South
		dir_util.append((0.8*neighbor_util[2])+(0.1*neighbor_util[3])+(0.1*neighbor_util[1]))
		#West
		dir_util.append((0.8*neighbor_util[3])+(0.1*neighbor_util[2])+(0.1*neighbor_util[0]))
		max_util = max(dir_util)
		max_util_index = dir_util.index(max_util)
		#Calculate total utility of going this direction
		total_util = graph[row_y][col_x] + (discount_rate*max_util)
		return (total_util,max_util_index)
#Function that calculates the best route using markov decision process
#Takes in the graph to evaluate, the discount facotr, and the epsilon value
#Returns a 3-tuple of the util dictionary, the util_direction dictionary, and the path list of coordinates
def mdp(graph,discount,epsilon,start_coord,end_coord):
	#Dictionary to hold utility of each square
	util = {}
	#Set all utility values to 0
	for row,i in enumerate(graph):
		for col,j in enumerate(i):
			util[(row,col)] = 0
	#Dictionary that tells the direction of best direction to move
	util_direction = {}
	#U, the old utility of a square
	u = 0.0
	#U prime, next utility of a square
	u_prime = 0.0
	#Delta
	d = float("inf")
	#Direction to move
	#0 = north
	#1 = East
	#2 = South
	#3 = West
	direction = 0
	#Keep track of loop iterations
	iterations = 0
	#Value iteration loop
	while (d > epsilon*((1-discount)/discount)):
		#Reset delta
		d = 0
		#Iterate through whole board
		#Iterate through rows
		for row,i in enumerate(graph):
			#Iterate through items of a row
			for col,j in enumerate(i):
				#Check to make sure we are not evualuating a wall
				if (graph[row][col] != float("-inf")):
					#Set the old value of the squares utility (u)
					u = util[(row,col)]
					#Calculate the next value of the square (u prime), and the direction
					u_prime,direction = calc_util(row,col,graph,util,discount)
					#Check if the delta is greater than the previous greatest in this board state
					if (abs(u-u_prime) > d):
						d = abs(u-u_prime)
					#Update utility in dictionary
					util[(row,col)] = u_prime
					#Update directino to go to get best utility
					util_direction[(row,col)] = direction
		iterations += 1
		#print("D = " + str(d))
	#Construct the best path
	
	'''
	print("--------Util dict--------")
	#print(util)
	for i in range(len(graph)):
		for j in range(len(graph[i])):
			try:
				print("("+str(i)+","+str(j)+")",util[(i,j)])
			except:
				print("("+str(i)+","+str(j)+") None")
	print("--------Direction--------")
	
	for i in range(len(graph)):
		for j in range(len(graph[i])):
			try:
				print("("+str(i)+","+str(j)+")",util_direction[(i,j)])
			except:
				print("("+str(i)+","+str(j)+") None")
	'''
	print("--------Constructing path--------")
	best_path = construct_path(util_direction,start_coord,end_coord,util)
	#best_path = []
	return (util,util_direction,best_path,iterations)
#Pretty print graph out
def print_graph(start,end,graph):
	print("Start = S\nEnd = E\nMountain = ^\nWall = @\nSnake = %\nBarn = B")
	graph[start[0]][start[1]] = "S"
	graph[end[0]][end[1]] = "E"
	border = "|"
	border += ("-"*len(graph[0]))+"|"
	print(border)
	for i in graph:
		line = "|"
		for j in i:
			if j == 0.0:
				line += " "
			#Mountain
			elif j == -1.0:
				line += "^"
			#Wall
			elif j == float("-inf"):
				line += "@"
			#Snake
			elif j == -2.0:
				line += "%"
			#Barn
			elif j == 1.0:
				line += "B"
			else:
				line += str(j)
		print(line+"|")
	print(border)


#Only run this if file is being run directly
if __name__ == "__main__":
	#Get command line arguments
	#If user only calls script, use default heuristic
	if len(sys.argv) == 1:
		#Default heuristic is Manhattan distance (heuristic number 0)
		map_name = "World1MDP.txt"
		print("Using default map (World1MDP.txt)")
		ep = 0.5
		print("Using default epsilon")
	#Check that user only input 1 or 0 command line argument
	elif len(sys.argv) > 3:
		print("Too many command line arguments input")
		print("Valid command line arguments: None or the name of the input file and the epsilon")
		print("No command line arguments: Use default map world and epsilon")
	#Else user has input 3 arguments. Set heuristic to users choice
	else:
		#Set map name
		map_name = sys.argv[1]
		#Set epsilon
		ep = float(sys.argv[2])
	'''Set the discount factor'''
	disc = 0.9
	#Read World1.txt and create graph
	graph = create_graph(map_name)
	#[print(x) for x in graph] #Print graph

	#Start is at the bottom left corner
	start_square = (len(graph)-1, 0)
	#End is at top right corner
	end_square = (0, len(graph[0])-1)
	print("================Calculating MDP for graph================")
	#Start path finding for graph, calculate board squares
	utility,utility_direction,path,iters = mdp(graph,disc,ep,start_square,end_square)
	print("--------Iterations--------")
	print(iters)
	print_graph(start_square, end_square, graph)
	print("--------Graph with path marked with X--------")
	solved = graph
	for i in path:
		solved[i[0]][i[1]] = "X"
	print_graph(start_square, end_square, solved)
	print("--------Printed path and Utility--------")
	for i in path:
		print(i, "--", utility[i])

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