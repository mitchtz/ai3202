#Mitch Zinser
#CSCI 3202 Assignment 8
'''ANY VALUE NOT IN THE DICT IS AUTOMATICALLY 1/27'''
not_in_dict = 1/27

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
	let_freq = {}
	#Open the file
	with open(name,"r") as data_in:
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

				#Add to letter frequency dict
				if i[0] in let_freq:
					if i[2] in let_freq[i[0]]:
						let_freq[i[0]][i[2]] += 1
					else:
						let_freq[i[0]][i[2]] = 1
				else:
					let_freq[i[0]] = {}
					let_freq[i[0]][i[2]] = 1
	#Cleanup since data file doesn't end in a "_ _" line
	first_col.append(word1)
	second_col.append(word2)

	#Add entry to dict 'tot' that holds the total number of times the letter appears
	#Iterate through keys (actual letters)
	for i in let_freq:
		#Reset total
		tot = 0
		#Iterate through evidence keys for letter i
		for j in let_freq[i]:
			tot += let_freq[i][j]
		#Add 'tot' entry to dict
		let_freq[i]["tot"] = tot
	#Now take this data (total) and create a probability dictionary
	let_prob = {}
	#Iterate through keys (actual letters)
	for i in let_freq:
		#Create dictionary for this actual letter in new dict
		let_prob[i] = {}
		#Iterate through evidence keys for letter i
		for j in let_freq[i]:
			#Add one to the numerator and 27 (num of letters + '_') to the denominator
			let_prob[i][j] = (let_freq[i][j]+1)/(let_freq[i]["tot"]+27)

	#Return both lists as and probability dtionary
	return first_col,second_col,let_prob

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
