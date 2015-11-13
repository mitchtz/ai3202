#Mitch Zinser
#CSCI 3202 Assignment 8
'''PIPE TO EXTERNAL FILE IN WINDOWS WITH > filename.txt'''
letters = 'abcdefghijklmnopqrstuvwxyz'

'''
Need to consider keeping spaces in dict
Not returning lists of words
Removing 'tot' from final dict
Adding all letters to each dict (since it is 1/(total number of occurances of letter))
Note:Space characters aren't corrupted, denominator is +26 for emission and +27 for transition
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
	emiss_freq = {}
	#Fill dictionary with dictionaries, and those with letter entries (init to 0)
	for i in letters:
		emiss_freq[i] = {}
		for j in letters:
			emiss_freq[i][j] = 0

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
	#Fill dictionary with dictionaries, and those with letter entries (init to 0)
	for i in (letters):
		init_freq[i] = 0


	#Open the file
	with open(name,"r") as data_in:
		#Save the last letter
		last_let = ""
		#Don't run the loop the same the first time to account for no starting place in the transition dict
		first_run = True
		#Iterate through the file line by line
		for i in data_in.readlines():

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


				if i[2] in emiss_freq[i[0]]:
					emiss_freq[i[0]][i[2]] += 1
				else:
					emiss_freq[i[0]][i[2]] = 1
	#Cleanup since data file doesn't end in a "_ _" line
	first_col.append(word1)
	second_col.append(word2)

	'''Emission Calulations'''
	#Add entry to dict 'tot' that holds the total number of times the letter appears
	#Iterate through keys (actual letters)
	for i in emiss_freq:
		#Reset total
		tot = 0
		#Iterate through evidence keys for letter i
		for j in emiss_freq[i]:
			tot += emiss_freq[i][j]
		#Add 'tot' entry to dict
		emiss_freq[i]["tot"] = tot
	#Now take this data (total) and create a probability dictionary
	emiss_prob = {}
	#Iterate through keys (actual letters)
	for i in emiss_freq:
		#Create dictionary for this actual letter in new dict
		emiss_prob[i] = {}
		#Iterate through evidence keys for letter i
		for j in emiss_freq[i]:
			#Add one to the numerator and 26 (num of letters + '_') to the denominator
			emiss_prob[i][j] = (emiss_freq[i][j]+1)/(emiss_freq[i]["tot"]+26)

	'''Transition Calulations'''
	#Dictionary that stores the first letter (t) as the key, and second letter (t+1) as the second key with frequencies as value
	tran_freq = {}
	#Fill dictionary with dictionaries, and those with letter entries (init to 0)
	for i in (letters+"_"):
		tran_freq[i] = {}
		for j in (letters+"_"):
			tran_freq[i][j] = 0
	#Iterate through list of hidden (state, left col) and calculate transitional frequencies
	#Iterate through words
	for i in first_col:
		#Iterate through letters of word
		for j in i:
			#Add entry with 
			pass

	'''Initial Calculations'''
	#Dictionary to store frequency that a letter occurs in the first col (hidden, actual)
	init_freq = {}
	#Fill dictionary with dictionaries, and those with letter entries (init to 0)
	for i in (letters):
		init_freq[i] = 0
	#Freq of "_" is 1 less than the number of the words (one less b/c no space at beginning or end)
	init_freq["_"] = len(first_col)-1
	#Total number of chars in the hidden (actual, first col), starts at len of "_"
	init_tot = init_freq["_"]
	#Iterate through 

	#Return both lists as and probability dtionary
	return first_col,second_col,emiss_prob

if __name__ == "__main__":
	#Set correct and actual as lists to hold words in each column
	correct, actual,dict_let = data_parser("typos20.data")
	#Iterate through keys of a sorted dictionary
	for i in sorted(dict_let):
		print("--------Intended:",i,"--------")
		#Iterate through keys of dict in dict (value dict to the key "i")
		for j in sorted(dict_let[i]):
			#Print the number of occurances
			print(j, dict_let[i][j])

	'''ANY VALUE NOT IN THE DICT IS AUTOMATICALLY 1/27'''
	'''
	print(correct[1])
	print(actual[1])
	'''
