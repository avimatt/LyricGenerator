"""
To run script: python WordDefine.py [path to folder of song files]
Song folders currently in google drive that Avi shared
Currently generates 
	1) list of song lengths 
	2) list of line lengths 
	3) counts of all sentence structure types
	4) Dictionary of word types(noun, verb, etc.) to (word to wordCount) ie dict inside of dict

"""
import nltk, os, sys, string, operator, random, ConditionalProbabilities
from nltk.corpus import wordnet as wn
from sets import Set
try:
	import Queue as Q
except:
	import queue as Q
class WordProb(object):
    def __init__(self, probability, word):
        self.probability = probability
        self.word = word
        return
    def __cmp__(self, other):
        return -1 * cmp(self.probability, other.probability)

def create_sentence_probs(sentenceStructures, sentenceStrctureBigram):
	probs = {}
	for key in sentenceStrctureBigram:
		bigram = key.split(",")
		prevBi = bigram[0]
		curBi = bigram[1]
		curProb = float(sentenceStrctureBigram[key]) / float(sentenceStructures[prevBi]) #count(cur-bi*prev-bi) / count (prev-bi)
		probs.setdefault(prevBi, Q.PriorityQueue())
		probs[prevBi].put(WordProb(curProb, curBi))
	return probs
def print_song(conditionalProbs, typeWordDict, sentenceStrctureProbs):
	print "----------"
	n = 0
	string = ""
	typestring = ""
	prev_word = "<start>"
	sent = "PRP VBP NN"
	try:
		while n < 10:
			typestring += sent + "\n"
			ss = sent.split()
			for tag in ss:
				new_word = conditionalProbs[prev_word].get().word
				while new_word not in typeWordDict[tag]:
					new_word = conditionalProbs[prev_word].get_nowait().word
				string += " " + new_word 
				prev_word = new_word
			sent = sentenceStrctureProbs[sent].get_nowait().word
			string += "\n"
			n += 1
	except:
		print string
		print typestring
		exit(1)
	print string
	print typestring
def main():
	path = sys.argv[1]
	unigrams = {}
	songLength = {}
	lineLength = {}
	typeWordDict = {} #key: word type, value: dictionary (key: word, value: word count)
	sentenceStructures = {}
	sentenceStrctureBigram = {}
	sentenceStrctureProbs = {}
	# Key = sent structure Unigram 1
	# Value = Priority Queue Q (Highest Probability at the top)
	# 	- Get Highest Probability: conditionalProbs[key].get().word
	songList = []
	lastLineStrcut = "NNP"
	#read in song files, get song length count and push all lines into songDict
	for filename in os.listdir(path):
		with open(path + "/" + filename, 'r') as myfile:
			songLines = myfile.readlines()
			songList.append(songLines)
			songLength.setdefault(len(songLines),0)
			songLength[len(songLines)] += 1
	for song in songList:
		#read through each line to get tag for each words
		for line in song:
			lineStructure = "" #string of all tags to see if same sentence structure repeats itself
			try:
				tagged = nltk.pos_tag(nltk.word_tokenize(line)) #tokenize line then get word tag for each word
			except:
				continue
			#lineLength.setdefault(len(tagged),0)
			#lineLength[len(tagged)] += 1
			for pair in tagged: #pair = (word, tag)
				if len(pair) == 2:
					(word, tag) = pair
					if word.isalpha() and tag.isalpha(): #will take out punctuation and song titles
						lineStructure += tag + " "
						typeWordDict.setdefault(tag, set()) #create key for tag with word if doesnt exist
						typeWordDict[tag].add(word)
						unigrams.setdefault(word, 0)
						unigrams[word] += 1
			# Create sentence structure, bigram dictionaries
			lineStructure = lineStructure[:-1]
			sentenceStructures.setdefault(lineStructure,0) 
			sentenceStructures[lineStructure] += 1
			#create bigram dict for sentence structure
			sentBigram = lastLineStrcut + "," + lineStructure 
			sentenceStrctureBigram.setdefault(sentBigram,0)
			sentenceStrctureBigram[sentBigram] += 1
			
			lastLineStrcut = lineStructure
	sorted_ss = sorted(sentenceStructures.items(), key=operator.itemgetter(1)) #to see most popular sentence types and line lengths
	sentenceStrctureProbs = create_sentence_probs(sentenceStructures, sentenceStrctureBigram)
	unigrams, bigrams = ConditionalProbabilities.getCounts(path)
	conditionalProbs = ConditionalProbabilities.getProbabilities(unigrams, bigrams) #Get conditional probs for words
	print_song(conditionalProbs, typeWordDict, sentenceStrctureProbs) #test
main()








