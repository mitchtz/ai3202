#Mitch Zinser
#CSCI 3202 Assignment 8
'''PIPE TO EXTERNAL FILE WITH > filename.txt'''
letters = 'abcdefghijklmnopqrstuvwxyz'

#Note:Space characters aren't corrupted, denominator is +26 for emission and +27 for transition

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
			
			#Check if this line is a separation between words ("_ _")
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
		#Remove 'tot' key from probability dict
		del emis_prob[i]["tot"]


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
		init_prob[i] = (init_freq[i]/tot)
	

	#Return both lists as and probability dtionary
	return first_col,second_col,emis_prob,tran_prob,init_prob

if __name__ == "__main__":
	#Set correct and actual as lists to hold words in each column
	correct,actual,conditional,transitional,initial = data_parser("typos20.data")
	#Print conditional
	print("----------------Condition----------------")
	#Iterate through keys of a sorted dictionary
	for i in sorted(conditional):
		print("--------Hidden(X):",i,"--------")
		#Iterate through keys of dict in dict (value dict to the key "i")
		for j in sorted(conditional[i]):
			#Print the number of occurances
			print(j, conditional[i][j])
	#Print transitional
	print("----------------Transition----------------")
	#Iterate through keys of a sorted dictionary
	for i in sorted(transitional):
		print("--------Hidden(X):",i,"--------")
		#Iterate through keys of dict in dict (value dict to the key "i")
		for j in sorted(transitional[i]):
			#Print the number of occurances
			print(j, transitional[i][j])


	#Print Initial
	print("----------------Initial (Using Hidden)----------------")
	#Iterate through key of sorted dict
	for i in sorted(initial):
		print(i, initial[i])

