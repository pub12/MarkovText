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
	maxWordInSentence = 20
	genNSentences = 5
	fileList = []

	if len(sys.argv) < 3:
		print( "Usage: " + sys.argv[0] + " -w <sentence word length> -n <sentences to generate> -d <dictionary file> ")
		exit(0)
	else:
		arg = {}
		options = getopt.getopt(sys.argv[1:], 'k:w:n:d:')
		for item in options[0]:
			if(item):
				arg[ item[0] ] = item[1]
		# pprint.pprint(arg)

		maxWordInSentence = int(arg[ '-w'])
		genNSentences = int(arg[ '-n' ])
		dictFile = arg['-d']

	return( maxWordInSentence, genNSentences, dictFile)
 

def main(maxWordInSentence, dictFile, genNSentences=50):

	#Create new Markov class
	markovObj = markov.Markov(dictFile=dictFile, maxWordInSentence= maxWordInSentence)

	twitterText = []

	for _ in range( genNSentences ):
		text = markovObj.genText() 
		print( text )
		if len(text) <= 140 and text.endswith('.'):
			twitterText.append(text)

	print("\n\n")
	pprint.pprint(twitterText)

if __name__ == "__main__":
	(maxWordInSentence, genNSentences, dictFile) = checkargs()

	main(maxWordInSentence, dictFile, genNSentences)