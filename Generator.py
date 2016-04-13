"""
To run script: python Generator.py [path to folder of song files]
Song folders currently in google drive that Avi shared
"""

import os, sys, string, operator, random
import ConditionalProbabilities as CP
import Train as T
try:
	import Queue as Q
except:
	import queue as Q

def generateSong(conditionalProbs, sentenceStrctureProbs, typeWordDict):
	print "----------"
	numLines = 10
	curLine = 0
	string = ""
	typestring = ""
	prev_word = "<start>"
	sent = "PRP VBP NN"
	try:
		while curLine < numLines:
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
			curLine += 1
	except:
		print string
		print typestring
		print "exit in exception:", sys.exc_info()[0]
		exit(1)
	print string
	print typestring

def trainSystem(directory, unigrams, bigrams, twd, ss, ssb):
	for filename in os.listdir(directory):
		if filename.startswith("."):
			continue

		# Open File and get the Text
		infile = open(directory + filename)
		filetext = infile.read()

		lines = filetext.split("\n")

		T.trainGrams(lines, unigrams, bigrams)
		T.trainStructures(lines, twd, ss, ssb)

	# Get Conditional Probabilities
	sentenceStructureProbs = CP.createSentenceProbs(ss, ssb)
	wordConditionalProbs = CP.getProbabilities(unigrams, bigrams) #Get conditional probs for words

	return wordConditionalProbs, sentenceStructureProbs

def main():
	# Directory that the lyrics are in
	directory = sys.argv[1]
	# Key = Word Unigram
	# Value = Word Unigram Frequency
	unigrams = {}
	# Key = Word Bigram
	# Value = Word Bigram Frequency
	bigrams = {}
	# Key: Word Type, t
	# Value: Set() of words of type t
	typeWordDict = {} 
	# Key: Structure of a line (ex: "PRP VBP NN")
	# Value: Frequency of the key
	sentenceStructures = {}
	# Key: Structure of 2 consecutive lines separated by a comma 
	# 	- (ex: "PRP VBP NN,NNP IN DT NN")
	# Value: Frequency of the key
	sentenceStrctureBigram = {}
	# Key = Word Unigram
	# Value = Priority Queue Q (Highest Probability at the top)
	# 	- Get Highest Probability: wordConditionalProbs[key].get().word
	wordConditionalProbs = {}
	# Key = Sentence Structure
	# Value = Priority Queue Q (Highest Probability at the top)
	# 	- Get Highest Probability: sentenceStructureProbs[key].get().word
	sentenceStructureProbs = {}


	# Train on the data
	wordConditionalProbs, sentenceStructureProbs = trainSystem(directory, unigrams, bigrams, typeWordDict, sentenceStructures, sentenceStrctureBigram)

	# Generate the song
	generateSong(wordConditionalProbs, sentenceStructureProbs, typeWordDict)

main()
