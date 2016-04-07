import sys, os, re

num_lines = 0
num_words = 0
bigrams = set()
unique_words = set()
words_per_line = []
lines_per_song = []

def countLines(filetext):
	global num_lines
	lines = filetext.split("\n")
	if len(lines) <= 3:
		print re.sub(r"_",r" ",lines[0])
	else:
		num_lines += (len(lines) - 2)
		lines_per_song.append((len(lines) - 2))
	infile.close()

def getWordStats(filetext):
	global bigrams, unique_words, num_words
	lines = filetext.split("\n")
	for i in range(0, len(lines)):
		if i > 1:
			line = lines[i]
			words = line.split(" ")

			num_words += len(words)

			words_per_line.append(len(words))

			unique_words = unique_words | set(words)

			offset_word_list = words[1:len(words)]
			bigram_list = zip(words, offset_word_list)
			bigrams = bigrams | set(bigram_list)


''' START MAIN '''
directory = sys.argv[1]

for filename in os.listdir(directory):
	if filename.startswith("."):
		continue
	
	# Open File and get the Text
	infile = open(directory + filename)
	filetext = infile.read()

	# Collect Statistics
	countLines(filetext)
	getWordStats(filetext)

	# Close File
	infile.close()

# Output Statistics
print "Number of lines:", num_lines
print "Number of words:", num_words
print "Number of unique words:", len(unique_words)
print "Number of unique bigrams", len(bigrams)
print "Average lines per song:", sum(lines_per_song)/len(lines_per_song)
print "Average words per line:", sum(words_per_line)/len(words_per_line)