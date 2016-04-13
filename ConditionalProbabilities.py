import os, sys
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
		conditionalProbs.setdefault(first_word, Q.PriorityQueue())
		# Add calculated element to the queue
		conditionalProbs[first_word].put(WordProb(prob, second_word))

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