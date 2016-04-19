import nltk
from nltk.corpus import wordnet as wn

def trainGrams(lines, unigrams, bigrams):
	# Read line by line
	for i in range(2, len(lines)):
		# Add start tag for conditional probabilities
		line = lines[i]
		line = "<start> " + line
		words = line.split(" ")
		# Sum up word freqs
		for word in words:
			unigrams.setdefault(word, 0)
			unigrams[word] += 1

		# Sum up bigram freqs
		offset_word_list = words[1:len(words)]
		bigram_list = ['{} {}'.format(x, y) for x, y in zip(words, offset_word_list)]
		for bigram in bigram_list:
			bigrams.setdefault(bigram, 0)
			bigrams[bigram] += 1

def trainStructures(lines, typeWordDict, sentenceStructures, sentenceStrctureBigram):
	lastLineStrcut = "NNP"
	# Read line by line
	for i in range(2, len(lines)):
		# String of all tags to see if same sentence structure repeats itself
		lineStructure = ""
		line = lines[i]
		try:
			#tokenize line then get word tag for each word
			tagged = nltk.pos_tag(nltk.word_tokenize(line))
		except:
			continue
		#pair = (word, tag)
		for pair in tagged:
			if len(pair) == 2:
				(word, tag) = pair
				# Will take out punctuation and song titles
				if word.isalpha() and tag.isalpha():
					lineStructure += tag + " "
					
					# Map word types to words of that type
					typeWordDict.setdefault(tag, set()) 
					typeWordDict[tag].add(word)

		# Create sentence structure, bigram dictionaries
		lineStructure = lineStructure[:-1] 
		sentenceStructures.setdefault(lineStructure,0) 
		sentenceStructures[lineStructure] += 1

		# Create bigram dict for sentence structure
		sentBigram = lastLineStrcut + "," + lineStructure 
		sentenceStrctureBigram.setdefault(sentBigram,0)
		sentenceStrctureBigram[sentBigram] += 1
		lastLineStrcut = lineStructure

def findMostPopPOS(typeWordDict, unigrams):
	tagToWord = {}
	for tag in typeWordDict:
		for unigram in sorted(unigrams, key=unigrams.get, reverse=True):
			if unigram in typeWordDict[tag]:
				tagToWord[tag] = unigram
				break
	return tagToWord

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