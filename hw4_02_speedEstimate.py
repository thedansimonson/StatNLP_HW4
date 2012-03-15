from pickle import load
from nltk import tokenize
from datetime import datetime

print "Loading parser..."
parser = load(open("hw4_vitParser.pkl", "r"))

userIn = ""
sentences=["Go .",
			"A bike .",
			"Ride a bike .",
			"I ride a bike .",
			"I ride a bike slowly .",
			"I ride a bike up there .",
			"I ride a bike up a hill .",
			"I ride a bike up a hill slowly .",
			"I ride a bike up a big hill slowly ."]

times = []
for each in sentences:
	start = datetime.now()
	print parser.parse(each.split())
	times.append(datetime.now()-start)
	for each in times:
		print each.total_seconds()

for each in zip(times, range(2, len(times)+2)):
	delta, length = each
	print str(length) +": "+str(delta.total_seconds())
