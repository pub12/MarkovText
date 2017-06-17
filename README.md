# MarkovText
Text Generation through Markov Chains

SO this is my Markov text generator - I wrote this to learn about Markov Chains and to create a twitter bot at a later stage.  Here's how to use the code.

<H1> Training Data </H1>
There are some data sets that have been provided in there which have been scoured from the web.  What's included:
1. Script files from the West Wing with just Jed Bartlet quotes in a single file (there's a python script that pulls that out)
2. Eddie Murphy scripts - cleaned up
3. Obama Speeches
4. Donald Trumps Tweets

<H1> Generating a Dictionary </H1>
To generate a dictionary file, you'll need to run the genMarkovDict.py script as follows:

<code>python genMarkovDict.py -k (the order of the markov chain; i.e. do you generate one word at a time or pairs of words) -i (input file with wild card) -d (output dictionary file) </code>

For example, the following generates a dictionary of order 2 where the text was generated using two words at a time:
<code>python genMarkovDict.py -k 2 -i "Data - Obama\*.*" -d obamadict.txt </code>

<H1> Generating Text </H1>
To generate the actual text, you'll need to run the genMarkovText.py script as follows:

<code>python genMarkovText.py -w (maximum number of words in sentence) -n (number of sentences to generate) -d (source dictionary file) </code>

For example, the following creates 5 generated text sentences with each one having a maximum of 20 words (if the end of sentence is found, then it will only go up to that last word)
<code>python genMarkovText.py -w 20 -n 5 -d obamadict.txt </code>
