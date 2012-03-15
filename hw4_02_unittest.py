from pickle import load
import sys

print "Loading parser..."
parser = load(open("hw4_vitParser.pkl", "r"))
testTrees = load(open("hw4_testTrees.pkl", "r"))
testSents = map(lambda x: map(lambda y: y[0], x.pos()), testTrees)

testPairs = zip(testSents, testTrees)
testPairs.sort(key = lambda x: len(x[0]))


for each in testPairs:
	rawSent, ideal = each
	print rawSent
	
	parsed = parser.parse(rawSent)

	print ideal
	print parsed
	try:
		print ideal == parsed
	except:
		print "!!!!!Error during comparison!!!!!!"
		print sys.exc_info()
		print ideal
		print parsed
		print "!!!!!Error during comparison!!!!!!"
	print ""

