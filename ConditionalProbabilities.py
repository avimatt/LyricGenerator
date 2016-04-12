import os, sys
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

def getCounts(directory):
	bigrams = {}
	unigrams = {}
	for filename in os.listdir(directory):
		if filename.startswith("."):
			continue

		# Open File and get the Text
		infile = open(directory + filename)
		filetext = infile.read()

		lines = filetext.split("\n")
		for i in range(0, len(lines)):
			# Read line by line
			if i > 1:
				line = lines[i]
				# Add start tag for conditional probabilities
				line = "<start> " + line
				words = line.split(" ")

				# Sum up word freqs
				for word in words:
					unigrams.setdefault(word, 0)
					unigrams[word] += 1

				offset_word_list = words[1:len(words)]
				bigram_list = ['{} {}'.format(x, y) for x, y in zip(words, offset_word_list)]
				
				# Sum up bigram freqs
				for bigram in bigram_list:
					bigrams.setdefault(bigram, 0)
					bigrams[bigram] += 1

	return unigrams, bigrams

''' 
				 C(W_n-1 W_n)
P(W_1 | W_n-1) =  ---------- 
				   C(W_n-1)
'''
class WordProb(object):
    def __init__(self, probability, word):
        self.probability = probability
        self.word = word
        return
    def __cmp__(self, other):
        return -1 * cmp(self.probability, other.probability)

def getProbabilities(unigrams, bigrams):
	conditionalProbs = {}
	for bigram in bigrams:
		first_word, second_word = bigram.split(" ")
		prob = bigrams[bigram]/float(unigrams[first_word])
		# Add a priority queue to the dict
		conditionalProbs.setdefault(first_word, Q.PriorityQueue())
		# Add calculated element to the queue
		conditionalProbs[first_word].put(WordProb(prob, second_word))

	return conditionalProbs


'''**************************
	 Start Main Function
**************************'''
def CPmain():
	# Key = Word Unigram
	# Value = Word Unigram Frequency
	unigrams = {}
	# Key = Word Bigram
	# Value = Word Bigram Frequency
	bigrams = {}
	# Key = Word Unigram 1
	# Value = Priority Queue Q (Highest Probability at the top)
	# 	- Get Highest Probability: conditionalProbs[key].get().word
	conditionalProbs = {}

	directory = sys.argv[1]

	unigrams, bigrams = getCounts(directory)

	conditionalProbs = getProbabilities(unigrams, bigrams)

	# Test 
	n = 0
	string = ""
	prev_word = "<start>"
	while n < 60:
		new_word = conditionalProbs[prev_word].get().word
		while new_word not in conditionalProbs:
			new_word = conditionalProbs[prev_word].get().word
		string += " " + new_word
		prev_word = new_word
		n += 1
	print string
