import nltk
import re
import pprint
import random


class Markov(object):
	def __init__(self, order=2, dictFile="", maxWordInSentence=20):
		self.table = {}
		self.inputLineCount = 0
		self.inputWordCount = 0
		self.setOrder( order )
		self.setMaxWordInSentence(maxWordInSentence)
		if dictFile:
			self.loadDictionary(dictFile)


	def setOrder(self, order=2):
		self.order = order

	def loadDictionary(self, dictFile):
		with open(dictFile, 'r') as inf:
			self.table = eval(inf.read())
		# print("Loaded dictionary file:"+dictFile)
		# pprint.pprint(self.table)

	def readFile(self, filename, fileEncoding="utf-8"):
		with  open(filename, "r", encoding=fileEncoding) as file:
			strLine = " ".join(file)
			self.processSection(strLine)

	def processSection(self,line ):
	# global lineCount, wordCount, table, keyLen
		sent_text = nltk.sent_tokenize(line) # this gives us a list of sentences

		for sentence in sent_text:
			self.inputLineCount = self.inputLineCount  + 1

			tokens = sentence.split()
			keyList = [ ];
			
			#Add a special key with just beginning words
			self.table.setdefault( '#BEGIN#', []).append(tokens[0:self.order ]);

			#loop through each word, and if we have enough to add dictionary item, then add
			for item in tokens:
				if len(keyList) < self.order :  #not enough items
					keyList.append(item)
					continue
				
				#If we already have the item, then add it, otherwise add to empty list
				self.table.setdefault( tuple(keyList), []).append(item)

				#Remove the first word and push last word on to it
				keyList.pop(0)
				keyList.append(item)
				self.inputWordCount = self.inputWordCount + 1

	def setMaxWordInSentence(self, maxWordInSentence):
		self.maxWordInSentence = maxWordInSentence

	def genText(self):	
		key = list(random.choice(  self.table['#BEGIN#'] ))
		genStr = " ".join( key )
		for _ in range( self.maxWordInSentence ):
			newKey = self.table.setdefault( tuple(key), "") 
			if(newKey == ""):
				break
			newVal = random.choice( newKey )
			genStr = genStr + " " + newVal

			key.pop(0)
			key.append(newVal)

		return genStr

	def getLineCount(self):
		return self.inputLineCount

	def getWordCount(self):
		return self.inputWordCount
  
	def outputDict(self, filename):
		markovDictFile=open(filename, 'w')
		pprint.pprint(self.table,markovDictFile)
