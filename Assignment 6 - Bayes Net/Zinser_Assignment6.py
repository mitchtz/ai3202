#Mitch Zinser
#CSCI 3202 Assignment 6
import getopt, sys

#Only run this if file is beng run directly
if __name__ == "__main__":
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
			print(a[0])
			print(float(a[1:]))
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