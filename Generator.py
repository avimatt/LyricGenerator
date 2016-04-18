"""
To run script: python Generator.py [path to folder of song files]
Song folders currently in google drive that Avi shared
"""

import os, sys, string, operator, random, re
import ConditionalProbabilities as CP
import Train as T
import textrank as tr
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
				wordObject = conditionalProbs[prev_word].pop(0)
				new_word = wordObject.word
				conditionalProbs[prev_word].append(wordObject)
				i = 0
				while (new_word not in typeWordDict[tag]) and (i < len(conditionalProbs[prev_word])):
					wordObject = conditionalProbs[prev_word].pop(0)
					new_word = wordObject.word
					conditionalProbs[prev_word].append(wordObject)
					i += 1
				if i >= len(conditionalProbs[prev_word]):
					# sterling function
					string += "->"
					new_word = "is"
					i = 0
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
	allText = ""
	for filename in os.listdir(directory):
		if filename.startswith("."):
			continue

		# Open File and get the Text
		infile = open(directory + filename)
		filetext = infile.read()
		filetext = re.sub("_"," ",filetext)
		allText += re.sub("\n", ". ", filetext) + " "
		T.trainGrams(lines, unigrams, bigrams)
		T.trainStructures(lines, twd, ss, ssb)
	keywords = tr.main(allText)
	aKeywords = []
	for key in keywords:
		aKeywords.append(key.encode('ascii', 'ignore'))
	print aKeywords
	exit(1)
	#sorted_keywords = sorted(keywords.items(), key=operator.itemgetter(1))
	#print sorted_keywords
	# Get Conditional Probabilities
	sentenceStructureProbs = CP.createSentenceProbs(ss, ssb)
	wordConditionalProbs = CP.getProbabilities(unigrams, bigrams) 
	CP.sortConditionalProbs(wordConditionalProbs)

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
