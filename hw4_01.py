from string import rjust

#provided a list of tuples
#calculate probability of x[1] given x[0]
def probabilities(tuples):
	counts = {}
	rowTotal = {}
	for each in tuples:
		try:
			#both x|y have been seen before
			counts[each[1]][each[0]]+=1
			rowTotal[each[0]] += 1
		except KeyError: 
			try:
				#this y in x|y has never been seen before
				counts[each[1]][each[0]] = 1
				rowTotal[each[0]] += 1
			except KeyError:
				#this x in x|y has never been seen before
				counts[each[1]] = {each[0]: 1}
				rowTotal[each[0]] = 1
	
	#now use the counts to calculate the probabilities
	probs = {}
	for each in counts:
		probs[each] = {}
		print rowTotal
		for more in counts[each]:
			probs[each][more]=float(counts[each][more])/rowTotal[more]
	
	return probs

def prettyTable(dictOfDicts, numLen = 5, default = 0.0, colW = 10):
	columns = list(dictOfDicts)
	columns.sort()
	rows = set(reduce(lambda x,y: x + list(dictOfDicts[y]), [[]] + columns))
	rows = list(rows)
	rows.sort()
	
	rowReduc = lambda x: "".join(map(lambda y: rjust(str(y), colW),x))

	header = [rowReduc([""]+columns)]

	finalTable = []
	for more in rows: 
		rowContent = []
		for each in columns:
			try:
				stuff = dictOfDicts[each][more]
				if numLen >= 0: 
					stuff = round(stuff, numLen)
				rowContent.append(stuff)
			except: 
				rowContent.append(default)
		finalTable.append([more]+rowContent)
	
	finalTable = map(rowReduc, finalTable)
	finalTable = header+finalTable

	return "\n".join(finalTable)


data = open("tagseq.txt", "r").read().split("\n")

dataTuples = map(lambda x: x.split(" "), data)
transitions = map(lambda x,y: (x[0], y[0]), dataTuples[:-1], dataTuples[1:])
transP = probabilities(transitions[:-1])

wordTuples = filter(lambda x: len(x) == 2, dataTuples)
emissionP = probabilities(wordTuples)

print "   Transition Probabilities (column given row)"
print prettyTable(transP)
print "\n   Emission Probabilities (column given row)"
print prettyTable(emissionP)
