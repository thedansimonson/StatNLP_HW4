#!/usr/bin/env python

"""
Calculates parsing evaluation metrics: precision, recall, labeled precision and
labeled recall.

Depends on nltk (developed with version 2.05b)

Alex Rudnick (alex.rudnick@gmail.com)

modified for loading pickled NLTK trees by Dan Simonson
"""

from nltk.tree import *
from os import walk, getcwd
import sys
from pickle import load
import copy

def precision(gold, parse, ignore_labels=True):
    """Return the proportion of brackets in the suggested parse tree that are
    in the gold standard."""

    parsebrackets = list_brackets(parse)
    goldbrackets = list_brackets(gold)

    parsebrackets_u = list_brackets(parse, ignore_labels=True)
    goldbrackets_u = list_brackets(gold, ignore_labels=True)

    if ignore_labels:
        candidate = parsebrackets_u
        gold = goldbrackets_u
    else:
        candidate = parsebrackets
        gold = goldbrackets

    total = len(candidate)
    successes = 0
    for bracket in candidate:
        if bracket in gold:
            successes += 1
    return float(successes) / float(total)

def recall(gold, parse, ignore_labels=True):
    """Return the proportion of brackets in the gold standard that are in the
    suggested parse tree."""

    parsebrackets = list_brackets(parse)
    goldbrackets = list_brackets(gold)

    parsebrackets_u = list_brackets(parse, ignore_labels=True)
    goldbrackets_u = list_brackets(gold, ignore_labels=True)

    if ignore_labels:
        candidate = parsebrackets_u
        gold = goldbrackets_u
    else:
        candidate = parsebrackets
        gold = goldbrackets

    total = len(gold)
    successes = 0
    for bracket in gold:
        if bracket in candidate:
            successes += 1
    return float(successes) / float(total)

def labeled_precision(gold, parse):
    return precision(gold, parse, ignore_labels=False)

def labeled_recall(gold, parse):
    return recall(gold, parse, ignore_labels=False)

def words_to_indexes(tree):
    """Return a new tree based on the original tree, such that the leaf values
    are replaced by their indexs."""

    out = copy.deepcopy(tree)

    leaves = out.leaves()
    for index in range(0, len(leaves)):
        path = out.leaf_treeposition(index)

        out[path] = index + 1
    return out

def firstleaf(tr):
    return tr.leaves()[0]

def lastleaf(tr):
    return tr.leaves()[-1]

def list_brackets(tree, ignore_labels=False):
    tree = words_to_indexes(tree)

    def not_pos_tag(tr):
        return tr.height() > 2

    def label(tr):
        if ignore_labels:
            return "ignore"
        else:
            return tr.node

    out = []
    subtrees = tree.subtrees(filter=not_pos_tag)
    return [(firstleaf(sub), lastleaf(sub), label(sub)) for sub in subtrees]

def calculatePR(goldS, parseS):
    gold = Tree.parse(goldS)
    parse = Tree.parse(parseS)

    return (precision(gold,parse), recall(gold,parse))

#FIRST, load MY parses
PTBdir = getcwd()+"/hw4_vitParses/"

print "Getting paths from operating system."
getPaths = lambda x: map(lambda y: x[0]+y, x[2])
complexPaths = map(lambda x: x, walk(PTBdir))
paths = reduce(lambda x,y: x+getPaths(y), [[]]+complexPaths)

print "Loading completed parses."
parseIndex = lambda s: int(s.split("/")[-1].split("_")[0])
parses = []
for each in paths: 
	try:
		parses.append((parseIndex(each), load(open(each, "r")).pprint()))
	except:
		print each
		print sys.exc_info()
		print "failed!"

for each in parses: print each
raw_input()

#NOW, load gold parses
print "Loading gold parses..."
testTrees = load(open("hw4_testTrees.pkl", "r"))
testSents = map(lambda x: map(lambda y: y[0], x.pos()), testTrees)
testUnit = zip(range(0,len(testTrees)), map(lambda x: x.pprint(), testTrees))

goldDict = dict(testUnit)
prnums = []
for index, sTree in parses:
	#try:
	print sTree
	sGold = goldDict[index]
	prnums.append(calculatePR(sGold, sTree))
	"""
	except:
		print "Index"
		print index
		print "Bombed!"
		print sys.exc_info()
"""

print str(len(prnums)) + " sentences evaluated. "
precisions,recalls = (map(lambda x: x[0], prnums),map(lambda x: x[1], prnums))
avgPrecision = sum(precisions)/len(precisions)
avgRecall = sum(recalls)/len(recalls)
print "Average precision: " + str(avgPrecision)
print "Average recall: " + str(avgRecall)




