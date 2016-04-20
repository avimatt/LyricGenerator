"""
To run script: python Generator.py "seed_sent" [path to folder of song files] [path to most important words]|NONE
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

def getFirstPrevWord(seedLine, conditionalProbs):
	seedList = seedLine.split(" ")
	seedList.reverse()
	for word in seedList:
		if word in conditionalProbs:
			return word
	return "<start>"

def getFirstSentStructure(seedStruct, sentenceStrctureProbs):
	if seedStruct in sentenceStrctureProbs:
		return seedStruct
	else:
		return "PRP VBP NN"

def getLineTag(line):
	taggedLineString = ""

	tagged = nltk.pos_tag(nltk.word_tokenize(line))
	for pair in tagged:
		if len(pair) == 2:
			(word, tag) = pair
			taggedLineString += tag + " "
	return taggedLineString[:-1]

def generateSong(seed, conditionalProbs, sentenceStrctureProbs, typeWordDict, tagToWord, tagToWordImp):
	print "----------"
	print seed
	numLines = 10
	curLine = 0
	string = ""
	typestring = ""
	seedStruct = getLineTag(seed)
	prev_word = getFirstPrevWord(seed, conditionalProbs)
	sent = getFirstSentStructure(seedStruct, sentenceStrctureProbs)
	try:
		while curLine < numLines:
			typestring += sent + "\n"
			ss = sent.split()
			# Loops over a line
			for tag in ss:
				# Get the next word
				wordObject = conditionalProbs[prev_word].pop(0)
				new_word = wordObject.word
				conditionalProbs[prev_word].append(wordObject)
				# Make sure that the next word is of the correct POS and has possible next words
				i = 0
				while (new_word not in typeWordDict[tag]) and (new_word not in conditionalProbs) and (i < len(conditionalProbs[prev_word])):
					wordObject = conditionalProbs[prev_word].pop(0)
					new_word = wordObject.word
					conditionalProbs[prev_word].append(wordObject)
					i += 1
				# If could not find a probable next word of correct POS
				if i >= len(conditionalProbs[prev_word]):
					# If there is a good textRank value use it other use the most popular word for the POS
					new_word = tagToWordImp[tag] if tagToWordImp[tag] in conditionalProbs else tagToWord[tag]
					i = 0

				# Add the word to the lyrics
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
	# print typestring

def trainSystem(directory, unigrams, bigrams, twd, ss, ssb, akw, flag):
	allText = ""
	for filename in os.listdir(directory):
		if filename.startswith(".") or filename.startswith("_"):
			continue
		# Open File and get the Text
		infile = open(directory + filename)
		filetext = infile.read()
		newfiletext = re.sub("_"," ",filetext)
		allText += re.sub("\n", ". ", newfiletext) + " "

		lines = filetext.split("\n")

		T.trainGrams(lines, unigrams, bigrams)
		T.trainStructures(lines, twd, ss, ssb)
	# Get TextRank Keywords
	if flag:
		keywords = tr.main(allText)
		for key in keywords:
			if " " not in key.encode('ascii', 'ignore'):
				akw.append(key.encode('ascii', 'ignore'))

		'''# Uncomment to use for making a most important words file
		for word in akw:
			print word
		exit(1)'''
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
	tagToWord = T.findMostPopPOS(typeWordDict, unigrams)	
	if not flag:
		keywords = T.getListFromFile(keywordsPath)
		tagToWordImp = T.getKeywordsForTag(keywords, tagToWord)

	# Generate the song
	generateSong(seed, wordConditionalProbs, sentenceStructureProbs, typeWordDict, tagToWord, tagToWordImp)

main()
