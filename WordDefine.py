"""
To run script: python WordDefine.py [path to folder of song files]
Song folders currently in google drive that Avi shared
Currently generates 
	1) list of song lengths 
	2) list of line lengths 
	3) counts of all sentence structure types
	4) Dictionary of word types(noun, verb, etc.) to (word to wordCount) ie dict inside of dict

"""
import nltk, os, sys, string, operator, random
path = sys.argv[1]
songLength = {}
lineLength = {}
typeWordDict = {} #key: word type, value: dictionary (key: word, value: word count)
sentenceStructures = {}
songList = []
#read in song files, get song length count and push all lines into songDict
for filename in os.listdir(path):
	with open(path + "/" + filename, 'r') as myfile:
		songLines = myfile.readlines()
		songList.append(songLines)
		if len(songLines) not in songLength:
			songLength[len(songLines)] = 1
		else:
			songLength[len(songLines)] += 1
#read through each line and get tags
for song in songList:
	for line in song:
		lineStructure = "" #string of all tags to see if same sentence structure repeats itself
		try:
			tagged = nltk.pos_tag(nltk.word_tokenize(line)) #tokenize line then get word tag for each word
		except:
			continue
		if len(tagged) not in lineLength:
			lineLength[len(tagged)] = 1
		else:
			lineLength[len(tagged)] += 1
		for pair in tagged:
			if len(pair) == 2:
				(word, tag) = pair
				if word.isalpha() and tag.isalpha(): #will take out punctuation and song titles
					lineStructure += tag + " "
					if tag not in typeWordDict:
						typeWordDict[tag] = {word: 1}
					else:
						if word not in typeWordDict[tag]:
							typeWordDict[tag][word] = 1
						else:
							typeWordDict[tag][word] += 1
					if lineStructure not in sentenceStructures: #get count of all sent strcture types
						sentenceStructures[lineStructure] = 1
					else:
						sentenceStructures[lineStructure] += 1
sorted_ss = sorted(sentenceStructures.items(), key=operator.itemgetter(1)) #to see most popular sentence types and line lengths
sorted_ll = sorted(lineLength.items(), key=operator.itemgetter(1))
