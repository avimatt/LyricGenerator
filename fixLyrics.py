import sys, os, re

def doFix(filename):
	infile = open(filename)
	filetext = infile.read()
	title = filetext.split("\n")[0]
	lyrics = filetext.split("\n")[2]
	infile.close()

	infile = open(filename, "w")
	infile.write(title + "\n\n")
	lines = lyrics.split(". ")
	if len(lines) <= 1:
		prev_char = " "
		for char in lyrics:
			if char.isupper() and prev_char != " ":
				infile.write("\n" + char)
			else:
				infile.write(char)
			prev_char = char
	else:
		infile.write(lyrics)

	infile.close()

def findBadFormatting(filename):
	infile = open(filename)
	filetext = infile.read()
	infile.close()

	if len(filetext.split("\n")) <= 3:
		print filename

''' START MAIN '''
directory = sys.argv[1]

for filename in os.listdir(directory):
	if filename.startswith("."):
		continue
	#doFix(directory + filename)
	findBadFormatting(directory + filename)

# average number of lines per song
# average number of words per line
# number of lines that repeat
# average number times a line repeats