###############################################
#	Name: 		Jacob Stants
#	uniqname:	jmstants	
#	Date:		Feb 25, 2016
#	File:		lryicsnaivebayes.py
###############################################

import re
import os
import sys
import operator
from operator import itemgetter
from os import path

import porterStemmer
from porterStemmer import PorterStemmer

#List of common contractions
#This list was found on the web
#SOURCE:http://www.softschools.com/language_arts/grammar/contractions/contractions_list/
common_contractions = ["aren't", "can't", "couldn't", "didn't", "doesn't", "don't", "hadn't", "hasn't", "haven't", "isn't", "let's", "shouldn't", "that's", "there's", "they'd", "they'll", "they're", "they've", "we'd", "we're", "we've", "weren't", "what'll", "what're", "what's", "what've", "where's", "who's", "who've", "won't", "wouldn't", "you'd", "you'll", "you've", "you're"]
fixes = [["are", "not",],["can", "not"], ["could", "not"], ["did", "not"], ["does", "not"], ["do", "not"], ["had", "not"], ["has", "not"], ["have", "not"], ["is", "not"], ["let", "us"], ["should", "not"], ["that", "is"], ["there", "is"], ["they", "had"], ["they", "will"], ["they", "are"], ["they", "have"], ["we", "did"], ["we", "are"], ["we", "have"], ["were", "not"], ["what", "will"], ["what", "are"], ["what", "is"], ["what", "have"], ["where", "is"], ["who", "is"], ["who", "have"], ["will", "not"], ["would", "not"], ["you", "did"], ["you", "will"], ["you", "have"], ["you", "are"]]

#This function tokenizes the text
def tokenizeText(input_string):
	input_string.strip()	#Remove leading and trailing whitespace characters
	tokens = re.split('\s+', input_string)	#Create list of words in document
	new_list = []
	for x in tokens:
		#get rid of token if token is a period
		if x == '.':
			continue
		#handle common contractions
		for k in range(0,len(common_contractions)):
			if x == common_contractions[k]:
				new_list.append(fixes[k][0])
				new_list.append(fixes[k][1])
				continue
		new_list.append(x)
	return new_list

#This is the list of stopwords found on the class website
stopwords = ["a", "all", "an", "and", "any", "are", "as", "at", "be", "been", "but", "by", "few", "from", "for", "have", "he", "her", "here", "him", "his", "how", "i", "in", "is", "it", "its", "many", "me", "my", "none", "of", "on", "or", "our", "she", "some", "the", "their", "them", "there", "they", "that", "this", "to", "us", "was", "what", "when", "where", "which", "who", "why", "will", "with", "you", "your"]

#This function removes stopwords
def removeStopwords(tokens):
	for i in range(0, len(tokens)):
		for j in range(0, len(stopwords)):
			if tokens[i] == stopwords[j]:
				tokens[i] = ""
	tokens = [x for x in tokens if x != ""]
	return tokens

#This function stems the tokens
def stemWords(tokens):
	for i in range(0,len(tokens)):
		stemmer = PorterStemmer()
		tokens[i] = stemmer.stem(tokens[i], 0, len(tokens[i])-1)
	return tokens

#This function trains a Naive Bayes classifier
def trainNaiveBayes(traininglist1, traininglist2, truthwords, liewords, beatles_folder, marley_folder):
	for doc in traininglist2:
		extension = marley_folder + '/' + doc
		current_path = path.relpath(extension)
		with open(current_path, 'r') as f:
			read_data = f.read()
			tokens = tokenizeText(read_data)
			#Depending on the implementation, perform the next two functions:
			#tokens = removeStopwords(tokens)
			#tokens = stemWords(tokens)
			if (True):	#doc is a bob marley song
				for word in tokens:
					if word in liewords:
						liewords[word] = liewords[word] + 1
					else:
						liewords[word] = 1
	for doc in traininglist1:
		extension = beatles_folder + '/' + doc
		current_path = path.relpath(extension)
		with open(current_path, 'r') as f:
			read_data = f.read()
			tokens = tokenizeText(read_data)
			#Depending on the implementation, perform the next two functions:
			#tokens = removeStopwords(tokens)
			#tokens = stemWords(tokens)
			if (True):				#doc is a beatles song
				for word in tokens:
					if word in truthwords:
						truthwords[word] = truthwords[word] + 1
					else:
						truthwords[word] = 1
	return

#This function predicts the class (truth or lie) of an unseen document
def testNaiveBayes (testfile, truthwords, liewords, folder, answers):
	truthchance = 1.0
	liechance = 1.0

	#Subset of documents for which target class is truth or lie
	problie = float(0)
	probtruth = float(0)
	problie = 0.5
	probtruth = 0.5
	
	#Process the testfile
	extension = test_folder + '/' + testfile
	current_path = path.relpath(extension)
	with open(current_path, 'r') as f:
		read_data = f.read()
		tokens = tokenizeText(read_data)
		#Depending on the implementation do 1 or more of the following
		tokens = removeStopwords(tokens)
		tokens = stemWords(tokens)

	vocabulary = len(truthwords) + len(liewords)

	#Calculate chance the testfile is a beatles song
	n = len(truthwords)
	for word in tokens:
		n_k = 1.0
		if word in truthwords:
			n_k = n_k + truthwords[word]
		truthchance = truthchance * (n_k / (n + vocabulary))
	truthchance = truthchance * probtruth

	#Caluclate chance the testfile is a bob marley song
	n = len(liewords)
	for word in tokens:
		n_k = 1.0
		if word in liewords:
			n_k = n_k + liewords[word]
		liechance = liechance * (n_k / (n + vocabulary))
	liechance = liechance * problie
	

	if (truthchance > liechance):
		#print testfile, "beatles"
		answers.append([testfile, "beatles"])
	else:
		#print testfile, "bob marley"
		answers.append([testfile, "marley"])


#Main Function

#One arguement from the command line: name of the folder containing the beatles lyrics
beatles_folder = sys.argv[1]

#beatles_songs = list containing all the file names of the beatles songs
beatles_songs = os.listdir(beatles_folder)

#One arguement from the command line: name of the folder containing the beatles lyrics
marley_folder = sys.argv[2]

#beatles_songs = list containing all the file names of the beatles songs
marley_songs = os.listdir(marley_folder)

#Third argument from the command line: name of the folder containing the testing songs
test_folder = sys.argv[3]
test_songs = os.listdir(test_folder)


answers = [] #holds pairs of [testfile, prediction]


traininglist1 = []		#traininglist contains all the file names to be used for training
for song in beatles_songs:
	traininglist1.append(song)
traininglist2 = []
for song in marley_songs:
	traininglist2.append(song)

for song in test_songs:
	#Create data structures necessary for various Bayes parameters
	truthwords = {}
	liewords = {}
	trainNaiveBayes(traininglist1, traininglist2, truthwords, liewords, beatles_folder, marley_folder) 
	testNaiveBayes(song, truthwords, liewords, test_folder, answers)

#Calculate accuracy
count = 0
for x in range(0,len(answers)):
	print answers[x][0], answers[x][1]
	if answers[x][0][0] == answers[x][1][0]:
		count = count + 1
print "accuracy:", float(count)/len(answers)

'''#Sort toptruthwords and topliewords
toptruthwords = sorted(toptruthwords, key=itemgetter(1), reverse=True)
topliewords = sorted(topliewords, key=itemgetter(1), reverse=True)
'''

'''print "truthwords"
for i in range(0,100):
	print toptruthwords[i]
print "liewords"
for i in range(0,100):	
	print topliewords[i]
'''