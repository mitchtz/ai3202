#Mitch Zinser
#CSCI 3202 Assignment 6
import getopt, sys

#Node class that stores its parents, its conditional probability
class B_Node:
	def __init__(self):
		self.parents = []
		self.conditionals = {}
	#Takes in a list of parents to the node, adds them to the parent list
	def set_parents(self, parent_list):
		for i in parent_list:
			self.parents.append(i)
	#Takes in the condition and probability and adds them to the conditional probability table for the node
	def set_conditional(self, condition, prob):
		self.conditionals[condition] = prob
	#Returns a list of the nodes parents
	def get_parents(self):
		return self.parents
	#Returns the conditional dict
	def get_conditional(self):
		return self.conditionals
#Function to calculate the marginal probabillity of the passed in node
def marginal(graph, args):
	#Check for tilde (reverses true/false)
	if args[0] == "~":
		#Call marginal on the letter
		marg = marginal(graph, args[1])
		return ("Not " + marg[0], 1-marg[1])
	#Else the cmd line arg is a single letter
	#Pollution
	elif args.upper() == "P":
		return ("Pollution", graph["Pollution"].get_conditional()["p"])
	#Smoker
	elif args.upper() == "S":
		return ("Smoker", graph["Smoker"].get_conditional()["s"])
	#Cancer
	elif args.upper() == "C":
		#Get conditional dict from cancer node
		cond_dict = graph["Cancer"].get_conditional()
		#Get marginal probabilities for pollution and smoker
		pollution_marg = graph["Pollution"].get_conditional()["p"]
		smoker_marg = graph["Smoker"].get_conditional()["s"]
		#Calculate part of tree that assumes p
		p = (cond_dict["ps"]*smoker_marg) + (cond_dict["p~s"]*(1-smoker_marg))
		#Calculate part of tree that assumes ~p
		not_p = (cond_dict["~ps"]*smoker_marg)+ (cond_dict["~p~s"]*(1-smoker_marg))
		#Add parts of tree together and multiply by prob of p or ~p
		marg = (pollution_marg*p) + ((1-pollution_marg)*not_p)
		return ("Cancer", marg)
	#XRay
	elif args.upper() == "X":
		#Get conditional dict ffor xray node
		cond_dict = graph["XRay"].get_conditional()
		#Calculate marginal probability for cancer
		cancer_marg = marginal(graph, "C")[1]
		#Calculate marginal of XRay using conditional table and marginal prob
		marg = (cond_dict["c"]*cancer_marg) + (cond_dict["~c"]*(1-cancer_marg))
		return ("XRay", marg)
	#Dyspnoea
	elif args.upper() == "D":
		#Get conditional dict ffor xray node
		cond_dict = graph["Dyspnoea"].get_conditional()
		#Calculate marginal probability for cancer
		cancer_marg = marginal(graph, "C")[1]
		#Calculate marginal of XRay using conditional table and marginal prob
		marg = (cond_dict["c"]*cancer_marg) + (cond_dict["~c"]*(1-cancer_marg))
		return ("Dyspnoea", marg)
#Function to calculate the conditional probability of the first arg (before) given the second arg(s) (after)
def conditional(graph, before, after):
	pass
#Function to calculate the joint probability
def joint(graph, args):
	var_list = parse_string(args)
	print(var_list)
#Helper functino to return a list of variables from a string
def parse_string(args):
	#Store if the last character was a ~
	skip = False
	#List to store the individual args
	arg_list = []
	#Iterate through the characters of the args string
	for i in args:
		#If the last char was ~, reset skip and add ~ + current char to args list
		if skip:
			skip = False
			arg_list.append("~"+i)
		#Otherwise, last char was not ~
		else:
			#If current char is ~, set skip to true for next loop
			if i == "~":
				skip = True
			#Otherwise add char to arg list
			else:
				arg_list.append(i)
	return arg_list

#Only run this if file is beng run directly
if __name__ == "__main__":
	'''Create the Bayes Net and insert probability tables'''
	#Dictionary to store nodes
	b_network = {}
	#Create nodes
	b_network["Pollution"] = B_Node()
	b_network["Smoker"] = B_Node()
	b_network["Cancer"] = B_Node()
	b_network["XRay"] = B_Node()
	b_network["Dyspnoea"] = B_Node()
	#Set parents for nodes
	b_network["Cancer"].set_parents([b_network["Pollution"],b_network["Smoker"]])
	b_network["XRay"].set_parents([b_network["Cancer"]])
	b_network["Dyspnoea"].set_parents([b_network["Cancer"]])
	#Set conditional probabilities for each node
	#Pollution
	b_network["Pollution"].set_conditional("p",0.9) #Low pol
	#Smoker
	b_network["Smoker"].set_conditional("s",0.3) #Smoker
	#Cancer
	b_network["Cancer"].set_conditional("~ps",0.05) #High pol, smoker
	b_network["Cancer"].set_conditional("~p~s",0.02) #High pol, not smoker
	b_network["Cancer"].set_conditional("ps",0.03) #Low pol, smoker
	b_network["Cancer"].set_conditional("p~s",0.001) #Low pol, not smoker
	#Account for the input being backwards
	b_network["Cancer"].set_conditional("s~p",0.05) #High pol, smoker
	b_network["Cancer"].set_conditional("~s~p",0.02) #High pol, not smoker
	b_network["Cancer"].set_conditional("sp",0.03) #Low pol, smoker
	b_network["Cancer"].set_conditional("~sp",0.001) #Low pol, not smoker
	#XRay
	b_network["XRay"].set_conditional("c",0.9) #Cancer
	b_network["XRay"].set_conditional("~c",0.2) #Not cancer
	#Dyspnoea
	b_network["Dyspnoea"].set_conditional("c",0.65) #Cancer
	b_network["Dyspnoea"].set_conditional("~c",0.3)
	'''Parse for input and start calculations'''
	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
	except getopt.GetoptError as err:
		# print help information and exit:
		print(str(err)) # will printsomething like "option -a not recognized"
		sys.exit(2)
	for o, a in opts:
		if o in ("-p"):
			print("flag", o)
			print("args", a)
			#print(a[0]) #Variable to change prior
			#print(float(a[1:])) #Value to change prior to
			#Check which variable to change prior
			#If pollution
			if a[0] == "P":
				#Change prior
				b_network["Pollution"].set_conditional("p",float(a[1:]))
			#If Smoker
			elif a[0] == "S":
				#Change prior
				b_network["Smoker"].set_conditional("s",float(a[1:]))
		elif o in ("-m"):
			#print("flag", o)
			#print("args", a)
			#print(type(a))
			marg = marginal(b_network, a)
			print("Marginal of", marg[0], "=", marg[1])
		elif o in ("-g"): #TODO
			#print("flag", o)
			#print("args", a)
			#print(type(a))
			'''you may want to parse a here and pass the left of |
			and right of l as arguments to calcConditional
			'''
			p = a.find("l")
			print(a[:p])
			print(a[p+1:])
			cond = conditional(b_network,a[:p],a[p+1:])
		elif o in ("-j"):
			print("flag", o)
			print("args", a)
			joint(b_network, a)
		else:
			assert False, "unhandled option"