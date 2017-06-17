import re
import sys
import getopt
import glob
import pprint

inputFilesList = []
outputFileName = ""

def checkargs():
	global outputFileName, inputFilesList
	if len(sys.argv) < 3:
		print( "Usage: " + sys.argv[0] + " -i <input files as wildcard> -o <output filename>")
		exit(0)
	else:
		arg = {}
		options = getopt.getopt(sys.argv[1:], 'i:o:')
		for item in options[0]:
			if(item):
				arg[ item[0] ] = item[1]
		# pprint.pprint(arg)

		outputFileName = arg[ '-o']
		wildcardFileList = arg[ '-i'].split(",")
		for filePattern in wildcardFileList:
			inputFilesList = inputFilesList + glob.glob(filePattern) 


#Read a westwing script which has a character name in CAPS and then the text below with a line break afterwards
def readWestWingFile(filename,  inputFileEncoding, outFile):
	lineCount = 0;
	prevword = "";
	fullline = ""

	with  open(filename, "r", encoding=inputFileEncoding) as file:
		bartletLineActive = False

		for line in file:
			if not line.strip():
				bartletLineActive = False
				if fullline:
					outFile.write( re.sub(r"\[.+\]","",fullline ) )
					lineCount = lineCount + 1
					fullline = ""
				continue
			elif "BARTLET" in line: 
				bartletLineActive = True
				fullline = ""
			elif bartletLineActive:
				fullline = fullline + " " + line.strip()
		if fullline:
			outFile.write( re.sub(r"\[.+\]","",fullline ) )
			lineCount = lineCount + 1
	return lineCount

def main():
	global outputFileName, inputFilesList
	totalLineCount = 0
	checkargs()

	outFile=open(outputFileName, 'w')
	for file in inputFilesList:
		totalLineCount = totalLineCount + readWestWingFile(file, "windows-1252", outFile)

	print("Generated file:"+ outputFileName + " with %s lines" % totalLineCount)
if __name__ == "__main__":
    main()