#Mitch Zinser
#CSCI 3202 Assignment 8
#Worked with the Wikipedia Example and Brady Auen
from math import log2 #For converting numbers to log base 2
'''PIPE TO EXTERNAL FILE WITH > filename.txt'''
letters = 'abcdefghijklmnopqrstuvwxyz'
'''File to read in data from, change this name to read from other files'''
file_name = "typos20.data"
test_file = "typos20Test.data"
'''
NOTE: Spaces are uncorrupted. Words always have the same number of letters and transition to spaces at the end of the word
'''
#Converts input file in format of columns 1 = correct word, columns 2 = space, column 3 = wrong word. One letter column, words separated by "_ _"
#Retuns two lists, first list is words in first column, second list is words in second column
def data_parser(name):
	#Store columns
	first_col = []
	second_col = []
	#Temporarily store words as they are built
	word1 = ""
	word2 = ""

	#Emission dict
	#Dictionary that stores the intended letter as key, and observed letters with frequencies as value
	emis_freq = {}
	#Fill dictionary with dictionaries, and those with letter entries (init to 0)
	for i in letters:
		emis_freq[i] = {}
		for j in letters:
			emis_freq[i][j] = 0

	#Transition dictionary
	#Dictionary that stores the first letter (t) as the key, and second letter (t+1) as the second key with frequencies as value
	tran_freq = {}
	#Fill dictionary with dictionaries, and those with letter entries (init to 0)
	for i in (letters+"_"):
		tran_freq[i] = {}
		for j in (letters+"_"):
			tran_freq[i][j] = 0

	#Initial dictionary
	#Dictionary to store frequency that a letter occurs in the first col (hidden, actual)
	init_freq = {}
	#Fill dictionary with letter entries (init to 0)
	for i in (letters+"_"):
		init_freq[i] = 0


	#Open the file
	with open(name,"r") as data_in:
		#Store the last char
		last_char = ""
		#Bool to see if this is the rist char
		first_char = True
		#Iterate through the file line by line
		for i in data_in.readlines():
			#Initial
			#Increment the first col characters frequency in the intial dict
			init_freq[i[0]] += 1
			#Transition
			#Make sure this isn't the first
			if first_char:
				first_char = False
			#Otherwise add to the transition frequency dict
			else:
				tran_freq[last_char][i[0]] += 1
			#Set the last char to be the current first col char that we have added to the dict
			last_char = i[0]
			
			#Check if this line is a separation between words ("_")
			if i[0] == "_":
				#Append word to list of words
				first_col.append(word1)
				second_col.append(word2)
				#Reset temperary word storage
				word1 = ""
				word2 = ""
			#Otherwise line is letter
			else:
				#Append letters to their temporary storage containers
				word1 += i[0]
				word2 += i[2]


				if i[2] in emis_freq[i[0]]:
					emis_freq[i[0]][i[2]] += 1
				else:
					emis_freq[i[0]][i[2]] = 1
	#Cleanup since data file doesn't end in a "_ _" line
	first_col.append(word1)
	second_col.append(word2)

	'''Emission Calulations'''
	#Add entry to dict 'tot' that holds the total number of times the letter appears
	#Iterate through keys (actual letters)
	for i in emis_freq:
		#Reset total
		tot = 0
		#Iterate through evidence keys for letter i
		for j in emis_freq[i]:
			tot += emis_freq[i][j]
		#Add 'tot' entry to dict
		emis_freq[i]["tot"] = tot
	#Now take this data (total) and create a probability dictionary
	emis_prob = {}
	#Iterate through keys (actual letters)
	for i in emis_freq:
		#Create dictionary for this actual letter in new dict
		emis_prob[i] = {}
		#Iterate through evidence keys for letter i
		for j in emis_freq[i]:
			#Add one to the numerator and 26 (num of letters) to the denominator
			emis_prob[i][j] = (emis_freq[i][j]+1)/(emis_freq[i]["tot"]+26)
		#Add the very small, basically 0 chance of a "_" getting in the mix (chance is 0 in reality)
		emis_prob[i]["_"] = 1/(emis_freq[i]["tot"]+26)
		#Remove 'tot' key from probability dict
		del emis_prob[i]["tot"]
	'''Spaces are immutable, uncorruptable beasts, and have an emission probability of 1. They are not counted'''
	emis_prob['_'] = {}
	emis_prob['_']['_'] = 0.9999999999999999
	for i in letters:
		emis_prob['_'][i] = 0.0000000000000001



	'''Transition Calulations'''
	#Add entry to dict 'tot' that holds the total number of times the letter appears
	#Iterate through keys (actual letters)
	for i in tran_freq:
		#Reset total
		tot = 0
		#Iterate through evidence keys for letter i
		for j in tran_freq[i]:
			tot += tran_freq[i][j]
		#Add 'tot' entry to dict
		tran_freq[i]["tot"] = tot
	#Now take this data (total) and create a probability dictionary
	tran_prob = {}
	#Iterate through keys (actual letters)
	for i in tran_freq:
		#Create dictionary for this actual letter in new dict
		tran_prob[i] = {}
		#Iterate through evidence keys for letter i
		for j in tran_freq[i]:
			#Add one to the numerator and 27 (num of letters + '_') to the denominator
			tran_prob[i][j] = (tran_freq[i][j]+1)/(tran_freq[i]["tot"]+27)
		#Remove 'tot' key from probability dict
		del tran_prob[i]["tot"]

	'''Initial Calculations'''
	#Count the total number of characters in the first col (hidden)
	tot = 0
	for i in init_freq:
		tot += init_freq[i]
	#Dict that stores the probabilities of each letter
	init_prob = {}
	for i in init_freq:
		init_prob[i] = (init_freq[i]/tot)#(init_freq[i]/len("_".join(first_col)))
	
	#Return both lists as and probability dtionary
	return first_col,second_col,emis_prob,tran_prob,init_prob

#Viterbi algorithm, returns final prob of getting to end and likely route (sequence of letters)
#Takes in: Evid (observed state sequence, one giant string with underscores for spaces), hidd (list of hidden states, eg. list of possible letters), star (dict of starting probabilities), tran (transition probability dict), emis (emission probability dict)
#Tran must be in format tran[prev][cur]
#Emis must be in format emis[hidden][observed]
def furby(evid, hidd, star, tran, emis):
	'''Spaces have a 1.0 emission prob, since they are uncorrupted'''
	'''Use math libraries log2 to convert to log base 2 for math. Convert back with math libraries pow(2, num) if desired'''
	'''Log2 can still use max. log2(0.8) > log2(0.2)'''

	#Create list that uses the time as the index and the value is a dict to store probability
	P = [{}]
	#Create a dict for the path
	path = {}
	#Create dict for t(0) (seed dict with inital entries)
	#Iterate through start dict (Contains all states that sequence can start with)
	for i in star:
		#Calculate probability with start[letter]*emission (add instead of multiply with log numbers)
		P[0][i] = log2(star[i])+log2(emis[i][evid[0]])
		path[i] = [i]

	#Run for t > 1, start at second letter
	for i in range(1,len(evid)):
		#Create new dict at end of list of dicts (dict for each time value)
		P.append({})
		#Dict to temporarily store path for this iteration
		temp_path = {}

		#Iterate through all possible states that are connected to the previous state chosen
		for j in hidd:
			#Use list comprehension to iterate through states, calculate trans*emis*P[t-1] for each possible state, find max and store that in path
			(prob, state) = max((P[i-1][k] + log2(tran[k][j]) + log2(emis[j][evid[i]]), k) for k in hidd)

			P[i][j] = prob
			temp_path[j] = path[state] + [j]
		# Don't need to remember the old paths
		path = temp_path
	#Find max prob in the last iteration of the list of dicts (P)
	n = len(evid)-1
	(prob, state) = max((P[n][y], y) for y in hidd)
	#Return the probability for the best last state and the path for it as a list of 1 char strings
	return prob,path[state]
	


#Function that takes in 2 strings of equal length and returns the error percent. String 1 is the correct string, string 2 is checked for errors
def error_rate(correct, check):
	errors = 0
	for i in range(0,len(correct)):
		if correct[i] != check[i]:
			errors += 1
	return errors/len(correct)

if __name__ == "__main__":
	
	#Set correct and actual as lists to hold words in each column
	correct,actual,conditional,transitional,initial = data_parser(file_name)
	#Get the data from another file to run the algorithm on. Get the 1st and 3rd column as strings
	#String that had the hidden state sequence (1st column)
	test_hidden = ""
	#String that stores the observed column (3rd column)
	test_observed = ""
	#Open file to get data from
	with open(test_file,"r") as test_in:
		#Iterate through lines of file
		for i in test_in.readlines():
			#Store first column letter
			test_hidden += i[0]
			#Store third column letter
			test_observed += i[2]
			
	#Run Viterbi
	prob, path = furby(test_observed, letters+"_", initial, transitional, conditional)
	#Calculate error rates
	print("Error rate of", test_file, "before Viterbi:",error_rate(test_hidden,test_observed)*100,"%")
	print("Error rate of", test_file, "after Viterbi:",error_rate(test_hidden,path)*100,"%")
	print("--------State Sequence--------")
	#Print final sequence in more readable format by joining list
	print("".join(path))
	#Print the probability of the final state for fun
	print("--------Final State Probability--------")
	print("In Log2:", prob)
	print("In Decimal:", pow(2,prob))
	

	''' Part 1
	#Print conditional
	print("----------------Condition----------------")
	#Iterate through keys of a sorted dictionary
	for i in sorted(conditional):
		print("--------Hidden:",i,"--------")
		#Iterate through keys of dict in dict (value dict to the key "i")
		for j in sorted(conditional[i]):
			#Print the number of occurances
			print(j, conditional[i][j])
	#Print transitional
	print("----------------Transition----------------")
	#Iterate through keys of a sorted dictionary
	for i in sorted(transitional):
		print("--------Previous:",i,"--------")
		#Iterate through keys of dict in dict (value dict to the key "i")
		for j in sorted(transitional[i]):
			#Print the number of occurances
			print(j, transitional[i][j])
	#Print Initial
	print("----------------Initial (Using Hidden)----------------")
	#Iterate through key of sorted dict
	for i in sorted(initial):
		print(i, initial[i])
	'''
