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
	#Returns the probability for the given conditional
	def get_conditional(self, condition):
		if condition in self.conditionals:
			return self.conditionals[condition]
		else:
			return None

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
	#XRay
	b_network["XRay"].set_conditional("c",0.9) #Cancer
	b_network["XRay"].set_conditional("~c",0.2) #Not cancer
	#Dyspnoea
	b_network["Dyspnoea"].set_conditional("c",0.65) #Cancer
	b_network["Dyspnoea"].set_conditional("~c",0.3)
	'''Parse for input and start calculations'''
	print("Pollution Low prob: ", b_network["Pollution"].get_conditional("p"))
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
			print(a[0]) #Variable to change prior
			print(float(a[1:])) #Value to change prior to
			#Check which variable to change prior
			#If for pollution
			if a[0] == "P":
				#Change prior
				b_network["Pollution"].set_conditional("p",float(a[1:]))
				print("Pollution Low prob: ", b_network["Pollution"].get_conditional("p"))
				#Set prior for P to a[1:]
			#setting the prior here works if the Bayes net is already built
			#setPrior(a[0], float(a[1:])
		elif o in ("-m"):
			print("flag", o)
			print("args", a)
			print(type(a))
			#calcMarginal(a)
		elif o in ("-g"):
			print("flag", o)
			print("args", a)
			print(type(a))
			'''you may want to parse a here and pass the left of |
			and right of | as arguments to calcConditional
			'''
			p = a.find("|")
			print(a[:p])
			print(a[p+1:])
			#calcConditional(a[:p], a[p+1:])
		elif o in ("-j"):
			print("flag", o)
			print("args", a)
		else:
			assert False, "unhandled option"