import os, sys, nltk
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

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
		conditionalProbs.setdefault(first_word, [])
		# Add calculated element to the queue
		conditionalProbs[first_word].append(WordProb(prob, second_word))

	return conditionalProbs

def createSentenceProbs(sentenceStructures, sentenceStrctureBigram):
	probs = {}
	for key in sentenceStrctureBigram:
		bigram = key.split(",")
		prevBi = bigram[0]
		curBi = bigram[1]
		# count(cur-bi*prev-bi) / count (prev-bi)
		curProb = float(sentenceStrctureBigram[key]) / float(sentenceStructures[prevBi]) 
		probs.setdefault(prevBi, Q.PriorityQueue())
		probs[prevBi].put(WordProb(curProb, curBi))
	return probs

def sortConditionalProbs(conditionalProbs):
	for key in conditionalProbs:
		sort_list = conditionalProbs[key]
		conditionalProbs[key] = sorted(sort_list, key=lambda x: x.probability, reverse=True)

''' TO BE MOVED '''

def getFirstPrevWord(seedLine, conditionalProbs):
	seedList = seedLine.split(" ")
	seedList.reverse()
	for word in seedList:
		if word in conditionalProbs:
			return word

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

def findMostPopPOS(typeWordDict, unigrams):
	tagToWord = {}
	for tag in typeWordDict:
		for unigram in sorted(unigrams, key=unigrams.get, reverse=True):
			if unigram in typeWordDict[tag]:
				tagToWord[tag] = unigram
				break
	return tagToWord