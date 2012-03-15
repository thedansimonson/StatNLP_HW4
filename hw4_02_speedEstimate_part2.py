from pickle import load
from nltk import tokenize
from datetime import datetime

def histogram(stuff):
	dagram = [0]*(max(stuff)+1)
	for each in stuff: dagram[each]+=1
	return dagram
	

print "Loading sentences..."
sentences = map(lambda x: x.leaves(), load(open("hw4_testTrees.pkl", "r")))
sentLengths = map(lambda x: len(x), sentences)
print max(sentLengths)
countsOfLengths = histogram(sentLengths)

for each, i in zip(countsOfLengths, range(0, len(countsOfLengths))): 
	print str(i)+": "+str(each)

#duration in vitParse.pkl parser according to speedEstimate part1,
# and a spreadsheet
durationFormula = lambda x: 4.47*1.50**x
duration = reduce(lambda eax,x: eax+durationFormula(x[0])*x[1], \
		[0]+zip(range(0,len(countsOfLengths)), countsOfLengths))

print "x: duration for one sentence of length x"
for each in range(0,58): print str(each)+": "+str(durationFormula(each))

print "Estimated total duration"
print duration

"""
RESULTS
Loading sentences...
58
0: 0
1: 0
2: 1
3: 0
4: 0
5: 1
6: 6
7: 6
8: 0
9: 6
10: 8
11: 4
12: 8
13: 6
14: 6
15: 11
16: 15
17: 10
18: 20
19: 14
20: 13
21: 15
22: 16
23: 16
24: 14
25: 16
26: 16
27: 14
28: 13
29: 14
30: 13
31: 11
32: 12
33: 8
34: 13
35: 6
36: 14
37: 8
38: 5
39: 3
40: 3
41: 5
42: 1
43: 2
44: 6
45: 4
46: 1
47: 0
48: 1
49: 1
50: 0
51: 1
52: 0
53: 0
54: 1
55: 2
56: 0
57: 1
58: 1
x: duration for one sentence of length x
0: 4.47
1: 6.705
2: 10.0575
3: 15.08625
4: 22.629375
5: 33.9440625
6: 50.91609375
7: 76.374140625
8: 114.561210937
9: 171.841816406
10: 257.762724609
11: 386.644086914
12: 579.966130371
13: 869.949195557
14: 1304.92379333
15: 1957.38569
16: 2936.078535
17: 4404.11780251
18: 6606.17670376
19: 9909.26505564
20: 14863.8975835
21: 22295.8463752
22: 33443.7695628
23: 50165.6543442
24: 75248.4815162
25: 112872.722274
26: 169309.083412
27: 253963.625117
28: 380945.437676
29: 571418.156514
30: 857127.234771
31: 1285690.85216
32: 1928536.27823
33: 2892804.41735
34: 4339206.62603
35: 6508809.93904
36: 9763214.90856
37: 14644822.3628
38: 21967233.5443
39: 32950850.3164
40: 49426275.4746
41: 74139413.2119
42: 111209119.818
43: 166813679.727
44: 250220519.59
45: 375330779.385
46: 562996169.078
47: 844494253.617
48: 1266741380.43
49: 1900112070.64
50: 2850168105.96
51: 4275252158.94
52: 6412878238.4
53: 9619317357.6
54: 14428976036.4
55: 21643464054.6
56: 32465196081.9
57: 48697794122.9
Estimated total duration
1.92085859861e+11
beauty:HW04 EmperorOfTheMoon$ 

The final date estimate is roughly six thousand YEARS.

"""

