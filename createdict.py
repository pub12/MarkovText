# from nltk.tokenize import RegexpTokenizer
import nltk
import re
import pprint
import random
import sys
import getopt
import glob

table = {}
lineCount = 0;
wordCount = 0;
keyLen = 1
maxWordInSentence = 20
genNSentences = 5

arg = {}

def checkargs():
	global keyLen, maxWordInSentence, genNSentences
	if len(sys.argv) < 3:
		print( "Usage: " + sys.argv[0] + " -k <Key lenth> -w <sentence word length> -n <sentences to generate> -f <files>")
		exit(0)
	else:
		arg = {}
		options = getopt.getopt(sys.argv[1:], 'k:w:n:f:')
		for item in options[0]:
			if(item):
				arg[ item[0] ] = item[1]
		pprint.pprint(arg)

		keyLen = int(arg[ '-k'])
		maxWordInSentence = int(arg[ '-w'])
		genNSentences = int(arg[ '-n' ])
		print(arg['-f'])



#Read a westwing script which has a character name in CAPS and then the text below with a line break afterwards
def readWestWingFile(filename,  fileEncoding="utf-8"):
	prevword = "";
	fullline = ""

	with  open(filename, "r", encoding=fileEncoding) as file:
		bartletLineActive = False
		# strData = str(file)
		# file = strData.decode("utf-8")

		for line in file:
			if not line.strip():
				bartletLineActive = False
				if fullline:
					processSection( re.sub(r"\[.+\]","",fullline ) )
					fullline = ""
				continue
			elif "BARTLET" in line: 
				bartletLineActive = True
				fullline = ""
			elif bartletLineActive:
				fullline = fullline + " " + line.strip()
		if fullline:
			processSection( re.sub(r"\[.+\]","",fullline ) )

#Text is just the one person
def readGenericFile(filename, fileEncoding="utf-8"):
	with  open(filename, "r", encoding=fileEncoding) as file:
		strLine = " ".join(file)
		processSection(strLine)


def processSection(line ):
	global lineCount, wordCount, table, keyLen
	
	sent_text = nltk.sent_tokenize(line) # this gives us a list of sentences
		# now loop over each sentence and tokenize it separately
	# pprint.pprint(sent_text)

	for sentence in sent_text:
		lineCount = lineCount  + 1
		cleanStr = sentence
		# cleanStr = re.sub('[^ A-Za-z0-9]+', ' ', sentence)

		# outputFile.write(cleanStr)	
		tokens = cleanStr.split()

		keyList = [ ];
		
		#print()
		table.setdefault( '#BEGIN#', []).append(tokens[0:keyLen]);

		for item in tokens:
			if len(keyList) < keyLen:  #not enough items
				keyList.append(item)
				#if len(keyList) < keyLen:	#If still too short, go to next iteration
				continue
			
			table.setdefault( tuple(keyList), []).append(item)
			keyList.pop(0)
			keyList.append(item)
			wordCount = wordCount + 1
		#if lineCount > 1:
		#	break
		# table.setdefault( tuple(keyList), []).append('#END#')


def generate():
	global table, maxWordInSentence

	key = list(random.choice(  table['#BEGIN#'] ))
	#print("starting on:"+str(key))
	genStr = " ".join( key )
	# print("start key:" + str(key) )

	for _ in range( maxWordInSentence ):
		newKey = table.setdefault( tuple(key), "") 
		if(newKey == ""):
			break
		newVal = random.choice( newKey )
		genStr = genStr + " " + newVal
		#print( "BEFORE:" + str( table['#BEGIN#'] ))
		key.pop(0)
		key.append(newVal)
		#print( "AFTER:" + str( table['#BEGIN#'] ))
		# print("new key:" + str(key) )

	print("::"+ genStr)

def main():
	global lineCount, wordCount, genNSentences
	checkargs()
	#nltk.download('all')
    # my code here

	#cleanInputFile=open('cleaninputfile.txt', 'w')


	seasonList = ( [1, 22], [2, 22], [3, 21], [4, 22] )
	for season in seasonList:
		seasonNo = season[0]
		for episodeNo in range(1, season[1]+1):
			filename = "tww-" + str(seasonNo) + "-" + str(episodeNo).zfill(2) + ".txt"
			#readWestWingFile( filename, cleanInputFile, "windows-1252")

	fileList = [];
	fileList = glob.glob("eddie*.txt")
	fileList = fileList + glob.glob("Obama*.txt") 

	print(fileList)
	for file in fileList:
		readGenericFile(file, "utf-8")
	

	print( "lines: " + str(lineCount) )
	print( "total words: " + str(wordCount) )
	
	markovDictFile=open('markovdictfile.txt', 'w')
	pprint.pprint(table,markovDictFile)

	for _ in range( genNSentences ):
		generate()

	
if __name__ == "__main__":
    main()