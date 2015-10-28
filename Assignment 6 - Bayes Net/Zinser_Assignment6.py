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
	tilde = False
	#Check for tilde
	if before[0] == "~":
		tilde = True
		before = before[1]
	#Check if the before is in the after
	if before in after:
		return 1
	#Get conditional dictionaries for each node
	pol_cond = graph["Pollution"].get_conditional()
	smoke_cond = graph["Smoker"].get_conditional()
	canc_cond = graph["Cancer"].get_conditional()
	xray_cond = graph["XRay"].get_conditional()
	dys_cond = graph["Dyspnoea"].get_conditional()
	#Check for the before condition
	#Pollution
	if before.upper() == "P":
		#Check if the probability is already calculated
		if after in pol_cond:
			return pol_cond[after]
		#Otherwise start case matching
		elif tilde:
			#If ~p|d
			if after == "d":
				return (conditional(graph,"d","~p")*pol_cond["~p"])/marginal(graph,"D")[1]
			#If ~p|c
			elif after == "c":
				return (conditional(graph,"c","~p")*pol_cond["~p"])/marginal(graph,"c")[1]
			#~p|cs
			elif (after == "cs") or (after == "sc"):
				#Numerator
				numer = canc_cond["~ps"]*smoke_cond["s"]*pol_cond["~p"]
				#Denominator
				denom = canc_cond["~ps"]*smoke_cond["s"]*pol_cond["~p"]+canc_cond["ps"]*smoke_cond["s"]*pol_cond["p"]
				return numer/denom
			#~p|ds
			elif (after == "ds") or (after == "sd"):
				#Store Numerator and Denomerator
				numer = []
				denom = []
				#Calculate numerators
				numer.append(dys_cond["c"]*canc_cond["~ps"]*pol_cond["~p"]*smoke_cond["s"])
				numer.append(dys_cond["~c"]*(1-canc_cond["~ps"])*pol_cond["~p"]*smoke_cond["s"])
				denom.append(dys_cond["c"]*canc_cond["~ps"]*pol_cond["~p"]*smoke_cond["s"])
				denom.append(dys_cond["c"]*canc_cond["ps"]*pol_cond["p"]*smoke_cond["s"])
				denom.append(dys_cond["~c"]*(1-canc_cond["~ps"])*pol_cond["~p"]*smoke_cond["s"])
				denom.append(dys_cond["~c"]*(1-canc_cond["ps"])*pol_cond["p"]*smoke_cond["s"])
				#Calculate denominators
				return sum(numer)/sum(denom)
	#Smoking
	elif before.upper() == "S":
		#Check if the probability is already calculated
		if after in smoke_cond:
			return smoke_cond[after]
		#Otherwise start case matching
		elif not tilde:
			#s|c
			if after == "c":
				return (conditional(graph,"c","s")*smoke_cond["s"])/marginal(graph,"c")[1]
			#s|d
			elif after == "d":
				return (conditional(graph,"d","s")*smoke_cond["s"])/marginal(graph,"d")[1]
	#Cancer
	elif before.upper() == "C":
		#Check if the probability is already calculated
		if after in canc_cond:
			return canc_cond[after]
		#Otherwise start case matching
		elif not tilde:
			#c|s
			if after == "s":
				return ((canc_cond["ps"]*pol_cond["p"]*smoke_cond["s"])+(canc_cond["~ps"]*pol_cond["~p"]*smoke_cond["s"]))/smoke_cond["s"]
			#c|ds
			elif (after == "ds") or (after =="sd"):
				#Store Numerator and Denomerator
				numer = []
				denom = []
				#Calculate numerators
				numer.append(dys_cond["c"]*canc_cond["ps"]*pol_cond["p"]*smoke_cond["s"])
				numer.append(dys_cond["c"]*canc_cond["~ps"]*pol_cond["~p"]*smoke_cond["s"])
				#Calculate denominators
				denom.append(dys_cond["c"]*canc_cond["ps"]*pol_cond["p"]*smoke_cond["s"])
				denom.append(dys_cond["c"]*canc_cond["~ps"]*pol_cond["~p"]*smoke_cond["s"])
				denom.append(dys_cond["~c"]*(1-canc_cond["ps"])*pol_cond["p"]*smoke_cond["s"])
				denom.append(dys_cond["~c"]*(1-canc_cond["~ps"])*pol_cond["~p"]*smoke_cond["s"])
				return sum(numer)/sum(denom)
			#c|d
			elif after == "d":
				return (dys_cond["c"]*marginal(graph,"c")[1])/marginal(graph,"d")[1]
			#c|~p
			elif after == "~p":
				#Store Numerator
				numer = []
				#Calculate numerator
				numer.append(canc_cond["~ps"]*pol_cond["~p"]*smoke_cond["s"])
				numer.append(canc_cond["~p~s"]*pol_cond["~p"]*smoke_cond["~s"])
				return sum(numer)/pol_cond["~p"]
			#c|p
			elif after == "p":
				#Store Numerator
				numer = []
				#Calculate numerator
				numer.append(canc_cond["ps"]*pol_cond["p"]*smoke_cond["s"])
				numer.append(canc_cond["p~s"]*pol_cond["p"]*smoke_cond["~s"])
				return sum(numer)/pol_cond["p"]
	#XRay
	elif before.upper() == "X":
		#Check if the probability is already calculated
		if after in xray_cond:
			return xray_cond[after]
		#Otherwise start case matching
		elif not tilde:
			#x|s
			if after == "s":
				#Store Numerator and Denomerator
				numer = []
				denom = []
				#Calculate numerators
				numer.append(xray_cond["c"]*(canc_cond["ps"]*smoke_cond["s"]*pol_cond["p"]))
				numer.append(xray_cond["c"]*(canc_cond["~ps"]*smoke_cond["s"]*pol_cond["~p"]))
				numer.append(xray_cond["~c"]*((1-canc_cond["ps"])*smoke_cond["s"]*pol_cond["p"]))
				numer.append(xray_cond["~c"]*((1-canc_cond["~ps"])*smoke_cond["s"]*pol_cond["~p"]))
				#Calculate denominators
				denom.append(canc_cond["ps"]*pol_cond["p"]*smoke_cond["s"])
				denom.append(canc_cond["~ps"]*pol_cond["~p"]*smoke_cond["s"])
				denom.append((1-canc_cond["ps"])*pol_cond["p"]*smoke_cond["s"])
				denom.append((1-canc_cond["~ps"])*pol_cond["~p"]*smoke_cond["s"])
				return sum(numer)/sum(denom)
			#x|d
			elif after == "d":
				return (((xray_cond["c"]*marginal(graph,"c")[1]*dys_cond["c"])+(xray_cond["~c"]*marginal(graph,"~c")[1]*dys_cond["~c"]))/marginal(graph,"d")[1])
			#x|ds
			elif (after == "ds") or (after == "sd"):
				#Store Numerator and Denomerator
				numer = []
				denom = []
				#Calculate numerators
				numer.append(xray_cond["c"]*dys_cond["c"]*canc_cond["~ps"]*pol_cond["~p"]*smoke_cond["s"])
				numer.append(xray_cond["~c"]*dys_cond["~c"]*(1-canc_cond["~ps"])*pol_cond["~p"]*smoke_cond["s"])
				numer.append(xray_cond["c"]*dys_cond["c"]*canc_cond["ps"]*pol_cond["p"]*smoke_cond["s"])
				numer.append(xray_cond["~c"]*dys_cond["~c"]*(1-canc_cond["ps"])*pol_cond["p"]*smoke_cond["s"])
				#Calculate denominators
				denom.append(dys_cond["c"]*canc_cond["~ps"]*pol_cond["~p"]*smoke_cond["s"])
				denom.append(dys_cond["~c"]*(1-canc_cond["~ps"])*pol_cond["~p"]*smoke_cond["s"])
				denom.append(dys_cond["c"]*canc_cond["ps"]*pol_cond["p"]*smoke_cond["s"])
				denom.append(dys_cond["~c"]*(1-canc_cond["ps"])*pol_cond["p"]*smoke_cond["s"])
				return sum(numer)/sum(denom)
	#Dyspnoea
	elif before.upper() == "D":
		#Check if the probability is already calculated
		if after in dys_cond:
			return dys_cond[after]
		#Otherwise start case matching
		elif not tilde:
			#d|~p
			if after == "~p":
				#Store Numerator and Denomerator
				numer = []
				denom = []
				#Calculate numerators
				numer.append(dys_cond["c"]*(canc_cond["~ps"]*smoke_cond["s"]*pol_cond["~p"]))
				numer.append(dys_cond["c"]*(canc_cond["~p~s"]*smoke_cond["~s"]*pol_cond["~p"]))
				numer.append(dys_cond["~c"]*((1-canc_cond["~ps"])*smoke_cond["s"]*pol_cond["~p"]))
				numer.append(dys_cond["~c"]*((1-canc_cond["~p~s"])*smoke_cond["~s"]*pol_cond["~p"]))
				#Calculate denominators
				denom.append(canc_cond["~ps"]*pol_cond["~p"]*smoke_cond["s"])
				denom.append(canc_cond["~p~s"]*pol_cond["~p"]*smoke_cond["~s"])
				denom.append((1-canc_cond["~ps"])*pol_cond["~p"]*smoke_cond["s"])
				denom.append((1-canc_cond["~p~s"])*pol_cond["~p"]*smoke_cond["~s"])
				return sum(numer)/sum(denom)
			#d|s
			elif after == "s":
				#Store Numerator and Denomerator
				numer = []
				denom = []
				#Calculate numerators
				numer.append(dys_cond["c"]*(canc_cond["ps"]*smoke_cond["s"]*pol_cond["p"]))
				numer.append(dys_cond["c"]*(canc_cond["~ps"]*smoke_cond["s"]*pol_cond["~p"]))
				numer.append(dys_cond["~c"]*((1-canc_cond["ps"])*smoke_cond["s"]*pol_cond["p"]))
				numer.append(dys_cond["~c"]*((1-canc_cond["~ps"])*smoke_cond["s"]*pol_cond["~p"]))
				#Calculate denominators
				denom.append(canc_cond["ps"]*pol_cond["p"]*smoke_cond["s"])
				denom.append(canc_cond["~ps"]*pol_cond["~p"]*smoke_cond["s"])
				denom.append((1-canc_cond["ps"])*pol_cond["p"]*smoke_cond["s"])
				denom.append((1-canc_cond["~ps"])*pol_cond["~p"]*smoke_cond["s"])
				return sum(numer)/sum(denom)
			#d|c
			elif after == "c":
				return (conditional(graph,"c","d")*marginal(graph,"d")[1])/marginal(graph)[1]

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
	b_network["Pollution"].set_conditional("~p",0.1) #High pol
	#Smoker
	b_network["Smoker"].set_conditional("s",0.3) #Smoker
	b_network["Smoker"].set_conditional("~s",0.7) #Not smoker
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
				b_network["Pollution"].set_conditional("~p",1-float(a[1:]))
			#If Smoker
			elif a[0] == "S":
				#Change prior
				b_network["Smoker"].set_conditional("s",float(a[1:]))
				b_network["Smoker"].set_conditional("~s",1-float(a[1:]))
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
			print(a[:p],"given",a[p+1:])
			#print(a[p+1:])
			cond = conditional(b_network,a[:p],a[p+1:])
			print(cond)
		elif o in ("-j"):
			print("flag", o)
			print("args", a)
			joint(b_network, a)
		else:
			assert False, "unhandled option"