# from nltk.tokenize import RegexpTokenizer
import nltk
import re
import pprint
import random
import sys
import getopt
import glob
import markov


def checkargs():
	keyLen = 1
	fileList = []

	if len(sys.argv) < 3:
		print( "Usage: " + sys.argv[0] + " -k <Key lenth> -i <input files> -d <dictionary file> ")
		exit(0)
	else:
		arg = {}
		options = getopt.getopt(sys.argv[1:], 'k:i:d:')
		for item in options[0]:
			if(item):
				arg[ item[0] ] = item[1]
		# pprint.pprint(arg)

		keyLen = int(arg[ '-k'])
		dictFile = arg['-d']

		wildcardFileList = arg[ '-i'].split(",")
		for filePattern in wildcardFileList:
			fileList = fileList + glob.glob(filePattern) 


	return(keyLen, fileList, dictFile)

def main():

	(keyLen, fileList, dictFile) = checkargs()

	#Create new Markov class
	markovObj = markov.Markov(keyLen)

	# print(fileList)
	for file in fileList:	
		try:
			markovObj.readFile(file, "utf-8")
		except:
			markovObj.readFile(file, "windows-1252")
	
	markovObj.outputDict(dictFile)

	print( "Generated Markov dictionary %s with processing %s input lines and %s input words " % ( dictFile, str(markovObj.getLineCount()), str(markovObj.getWordCount()) ) )
	
if __name__ == "__main__":
    main()