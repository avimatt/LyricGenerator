"""
To run script: python Generator.py "seed_sent" [path to folder of song files] [path to most important words]
Song folders currently in google drive that Avi shared
"""

import os, sys, string, operator, random, re, nltk
import ConditionalProbabilities as CP
import Train as T
import textrank as tr
try:
	import Queue as Q
except:
	import queue as Q

def generateSong(seed, conditionalProbs, sentenceStrctureProbs, typeWordDict, tagToWord, tagToWordImp):
	print "----------"
	print seed
	numLines = 10
	curLine = 0
	string = ""
	typestring = ""
	seedStruct = CP.getLineTag(seed)
	prev_word = CP.getFirstPrevWord(seed, conditionalProbs)
	sent = CP.getFirstSentStructure(seedStruct, sentenceStrctureProbs)
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
					string += "->"
					new_word = tagToWordImp[tag] if tagToWordImp[tag] in conditionalProbs else tagToWord[tag]
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

def trainSystem(directory, unigrams, bigrams, twd, ss, ssb, akw, flag):
	allText = ""
	for filename in os.listdir(directory):
		if filename.startswith("."):
			continue

		# Open File and get the Text
		infile = open(directory + filename)
		filetext = infile.read()
		newfiletext = re.sub("_"," ",filetext)
		allText += re.sub("\n", ". ", newfiletext) + " "

		lines = filetext.split("\n")

		T.trainGrams(lines, unigrams, bigrams)
		T.trainStructures(lines, twd, ss, ssb)
	if flag:
		keywords = tr.main(allText)
		for key in keywords:
			akw.append(key.encode('ascii', 'ignore'))

	# Get Conditional Probabilities
	sentenceStructureProbs = CP.createSentenceProbs(ss, ssb)
	wordConditionalProbs = CP.getProbabilities(unigrams, bigrams) 
	CP.sortConditionalProbs(wordConditionalProbs)

	return wordConditionalProbs, sentenceStructureProbs, akw

def main():
	# Seed Sentence
	seed = sys.argv[1]
	# Directory that the lyrics are in
	directory = sys.argv[2]
	# Path to most important words file, NONE if you don't have one
	keywordsPath = sys.argv[3]
	# Optional
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
	# List of most important words
	keywords = []
	# Key = Part of speech tag
	# Value = Most frequent unigram of that POS
	tagToWord = {}
	# Key = Part of speech tag
	# Value = Most important unigram of that POS
	tagToWordImp = {}


	flag = True if keywordsPath == "NONE" else False
	# Train on the data
	wordConditionalProbs, sentenceStructureProbs, keywords = trainSystem(directory, unigrams, bigrams, typeWordDict, sentenceStructures, sentenceStrctureBigram, keywords, flag)
	tagToWord = CP.findMostPopPOS(typeWordDict, unigrams)	
	if not flag:
		keywords = getListFromFile(keywordsPath)
		tagToWordImp = getKeywordsForTag(keywords, tagToWord)
	# Generate the song
	generateSong(seed, wordConditionalProbs, sentenceStructureProbs, typeWordDict, tagToWord, tagToWordImp)

def getListFromFile(path):
	# Open File and get the Text
	infile = open(path)
	filetext = infile.read()
	lines = filetext.split("\n")

	keywords = []
	for line in lines:
		keywords.append(line)

	return keywords

def getKeywordsForTag(keywords, tagToWord):
	tagged = nltk.pos_tag(keywords)
	tagToWordImp = {}
	for tag in tagToWord:
		for pair in tagged:
			tagToWordImp[tag] = tagToWord[tag]
			(word, wordTag) = pair
			if wordTag == tag:
				tagToWordImp[tag] = word
				break

	return tagToWordImp
main()
