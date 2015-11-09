#Converts input file in format of columns 1 = correct word, columns 2 = space, column 3 = wrong word. One letter column, words separated by "_ _"
#Retuns two lists, first list is words in first column, second list is words in second column
def data_parser(name):
	#Store columns
	first_col = []
	second_col = []
	#Temporarily store words as they are built
	word1 = ""
	word2 = ""
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
	#Cleanup since data file doesn't end in a "_ _" line
	first_col.append(word1)
	second_col.append(word2)
	#Retusn both lists as tuple
	return first_col,second_col

if __name__ == "__main__":
	#Set first and second as lists to hold words in each column
	first, second = data_parser("typos20.data")
	print(first[1])
	print(second[1])

