from pickle import load, dump
import sys
from os import getcwd, walk

print "Loading parser..."
parser = load(open("hw4_vitParser.pkl", "r"))
testTrees = load(open("hw4_testTrees.pkl", "r"))
testSents = map(lambda x: map(lambda y: y[0], x.pos()), testTrees)

#prepare all data for the loop
testPairs = zip(testSents, testTrees, range(0, len(testTrees)))
testPairs.sort(key = lambda x: len(x[0]))

#determine where parsing should continue based on the saved parse files
parseFolder = getcwd()+"/hw4_vitParses"
getPaths = lambda x: map(lambda y: x[0]+"/"+y, x[2])
complexPaths = map(lambda x: x, walk(parseFolder))
paths = reduce(lambda x,y: x+getPaths(y), [[]]+complexPaths)

for each in paths: print each
raw_input("ANYKEY BROW")

for each in testPairs:
	rawSent, ideal, index = each
	print "Working on "+str(index)+":\n"+" ".join(rawSent)
	
	try:
		parsed = parser.parse(rawSent)
		print ideal
		print parsed
		print ideal == parsed

	except:
		print "!!!!!Error during comparison!!!!!!"
		print sys.exc_info()
		print "Index: "+str(index)
		print ideal
		print "!!!!!Error during comparison!!!!!!"
		parsed = "Fail\n"+ideal+"\n\n"+str(sys.exc_info())
	
	#save parse to accumulate for later evaluation
	#and in case script crashes
	filename = str(index)+"_"+rawSent[0]+".pkl"
	dump(parsed, open(parseFolder+"/"+filename, "r"))
	print "Writing "+filename

	print ""

