from nltk.corpus import treebank
from nltk import Tree, Nonterminal
from nltk.parse.viterbi import ViterbiParser
from nltk.grammar import induce_pcfg
from os import getcwd, walk
from pickle import dump

###############################
# 2) Remove numerical indices #
###############################

print "Loading treebank."
sentenceStrings = map(lambda x: x.pprint(), treebank.parsed_sents())

#these are various things we want to remove (indices) or replace
indexStrings = map(str, range(166,0,-1))

#things that come before values and what should be left behind after
#the index is removed
indexPrefixes = [("-",""), ("=","")]
indiceRemedy = lambda n: map(lambda x: (n[0]+x,n[1]), indexStrings)
fixingTuples = reduce(lambda x,y: x+indiceRemedy(y), [[]]+indexPrefixes)

#this is where the removing takes place
print "Cleaning POS tags."
removeTargets = lambda x: reduce(lambda y,z: y.replace(z[0],z[1]), \
		[x]+fixingTuples)
sentenceStrings = map(removeTargets, sentenceStrings)
sentenceTrees = map(lambda x: Tree(x), sentenceStrings)

###################################################
# 1) Reserve 10% of the parsed trees for testing. #
###################################################

print "Storing test set of parsed trees for review."
numTrainTrees = int(len(sentenceTrees)*0.9)
trainTrees = sentenceTrees[:numTrainTrees]
testTrees = sentenceTrees[numTrainTrees:]

print "Number of Training Trees: "+str(len(trainTrees))
print "Number of Test Trees: "+str(len(testTrees))
print ""

#########################
# 3) Extend the lexicon #
#########################

extendedPOS = ["JJ","JJR","JJS","NN","NNS","NNP","NNPS","RB","RBR",
	"RBS","VB","VBD","VBG","VBN","VBP","VBZ"]

#PTB POS-tagged files are assumed located in a subdirectory /POS
#if this is not the case, please update it.
PTBdir = getcwd()+"/POS/"

print "Getting paths from operating system."
getPaths = lambda x: map(lambda y: x[0]+"/"+y, x[2])
complexPaths = map(lambda x: x, walk(PTBdir))
paths = reduce(lambda x,y: x+getPaths(y), [[]]+complexPaths)

print "Generating extended rule set..."

print "Loading all files from PTB and turning into superstring."
everything = reduce(lambda x,y: "".join([x,y]), map(lambda p: \
	open(p, "r").read(), paths))

print "Breaking into words."
everything = everything.split()
print "Only retaining tagged words."
everything = filter(lambda x: "/" in x, everything)
print "Only retaining tagged words in extended POS set."
everything = filter(lambda x: x.split("/")[1] in extendedPOS, everything)

print "Transforming PTB tags into production rules."
tagToTree = lambda x: "("+x.split("/")[1]+" "+x.split("/")[0]+")"
tagToProd = lambda x: Tree(tagToTree(x)).productions()

extraLexicals = []
for each in everything:
	try:
		extraLexicals.extend(tagToProd(each))
	except:
		print "    "+each+" failed to form object of type Tree()"

#########################
# Let's build a parser! #
#########################

print "Combining extended lexicon with the training trees and "
print "building grammar."

#trainTrees currently has the productions in a list of lists
#this turns them into a list
trainProds = reduce(lambda x,y: x+y,\
		map(lambda x: x.productions(), trainTrees))
parserProds = trainProds+extraLexicals

#remove duplicates
print "Removing duplicates from productions."
parserProds = list(set(parserProds))

for each in parserProds: print each

parser = ViterbiParser(induce_pcfg(Nonterminal("S"),parserProds))

#I've got this thing somewhat working. I'm tired of running it over
# and over. I think it's taking nearly 10 minutes.
# PICKLE AND EXPORT TIME
prsFilename = "hw4_vitParser.pkl"
print "Saving parser to " + prsFilename
dump(parser, open(prsFilename, "w"))
dump(testTrees, open("hw4_testTrees.pkl","w"))




