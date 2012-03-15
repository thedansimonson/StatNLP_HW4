from pickle import load
from nltk import tokenize

print "Loading parser..."
parser = load(open("hw4_vitParser.pkl", "r"))

userIn = ""
while userIn != "q":
	userIn = raw_input("Give me a sentence to parse: ")
	try:
		print parser.parse(userIn.split())
	except:
		print "Whoops!"
