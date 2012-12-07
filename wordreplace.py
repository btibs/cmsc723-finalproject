# find suitable words in a sentence to replace

import berkeleyParser
from MetaphorMapping import nounToNoun, nounToAdj#, nounToVerb
import re
import sys

"""
[NN] is a [NN] (Noun is metaphor)
[NN] [VV] (Verb is metaphor)
[JJ] [NN] or [NN] is [JJ] (Adjective is metaphor)
"""
# pattern types
#PATTERN_TYPES = [NN_NN, NN_VV, JJ_NN, NN_JJ] = range(4)
#WORD_TYPES = ["NOUN", "VERB", "ADJ", "IS"]
PATTERNS = {
    'NN_NN': 'NOUN IS NOUN',
    'NN_VV': 'NOUN VERB',
    'JJ_NN': 'NOUN ADJ',
    'NN_JJ': 'NOUN IS ADJ',
}
WORD_TYPES = {
    'ADJ':  ['ADJP', 'JJ', 'JJR', 'JJS'],
    'NOUN': ['NP', 'NN', 'NNS', 'NNP', 'NNPS', 'PRP'], # should proper nouns and pronouns actually be included?
    'VERB': ['VP', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
    'IS':   [' is', ' are', ' am', ' was', ' were'], # complex enough?
}

# make regexs
for p, pat in PATTERNS.iteritems():
    s = pat
    for w, wtags in WORD_TYPES.iteritems():
        if s.find(w) >= 0:
            s = s.replace(w, "(" + '|'.join(wtags) + ")")
    #print s

"""
(NP|NN|NNS|NNP|NNPS|PRP) (ADJP|JJ|JJR|JJS)
(NP|NN|NNS|NNP|NNPS|PRP) (VP|VB|VBD|VBG|VBN|VBP|VBZ)
(NP|NN|NNS|NNP|NNPS|PRP) (is|are|am|was|were) (NP|NN|NNS|NNP|NNPS|PRP)
(NP|NN|NNS|NNP|NNPS|PRP) (is|are|am|was|were) (ADJP|JJ|JJR|JJS)
"""
# example: {'S': [{'NP': [{'DT': 'This'}]}, {'VP': [{'VBZ': 'is'}]}, {'NP': [{'DT': 'a'}]}, {'NN': 'test'}]}
# parse: '( (S (NP (DT This)) (VP (VBZ is) (NP (DT a) (NN test)))) )'
# this is NN_NN (NP IS NP)

def findReplacements(tree, parse):
    print findWordTypeInTree(tree, 'VERB')
    """
    curTag = tree
    wordmatches = []
    for pname, pat in PATTERNS.iteritems():
        # given a pattern, find it in the tree
        wordindex = 0
        for pword in pat.split(" "):
            for tag in WORD_TYPES(pword):
                if curTag == tag:   # tag matches, now get the word
                    if curTag.word is not None:
                        wordmatches.append(wordindex)
                        wordindex += 1
                    else:   # this is a higher-level tag, we need to find the word
                        while (curTag.word is None):
                            curTag = curTag.children[0]
                        wordmatches.append(wordindex)
                        wordindex += 1
                    break
    """

# go through tree to find a word associated with a [wordType] tag
# if successful returns (wordindex, tag), else None
# this basically does a BFS but wants the lowest-level
def findWordTypeInTree(curTag, wordType):
    if curTag.word is not None and curTag.tag.strip() in WORD_TYPES[wordType]:
        # success
        return (curTag.wordIndex, curTag.tag.strip())
    elif curTag.word is None:
        # check children
        for c in curTag.children:
            result = findWordTypeInTree(c, wordType)
            if result is not None:
                # success
                return result
    return None
                

# find possible replacement locations given a parse tree and original parse
# return dictionary of PATTERN_TYPE: [loc, loc] ?
# exclude NN_VV is V = IS?
def findReplacementsFAIL(tree, parse):
    # first: find patterns matching the types
    # todo: this is pretty dumb and doesn't use the tree at all
    patmatches = []
    for p, pat in PATTERNS.iteritems():
        indices = []
        lastI = 0
        lastWord = ''
        matches = True
        for word in pat.split(" "):
            for tag in WORD_TYPES[word]:
                if parse.find(tag, lastI) > -1:
                    if lastI != 0 and lastWord != "IS":
                        indices.append(lastI)
                    lastI = parse.find(tag, lastI)
                    lastWord = word
                    break
                else:
                    matches = False
        if matches:
            indices.append(lastI)
            patmatches.append([p, indices])
    
    # second: return locations of the actual words in the sentence
    # actual words:
    wordsToRepl = []
    print "\n",parse,"\n",patmatches
    for p, indices in patmatches:
        print "\n",p
        for i in indices:
            opp = 0
            lastI = i-1
            for k in range(i-1, len(parse)):
                if parse[k] == '(':
                    opp += 1
                    lastI = k
                elif parse[k] == ')': opp -= 1
                if opp == 0:
                    break
            print parse[parse.find(" ",lastI)+1:k-1]
    
    return []

# recover sentence from a dictionary
def dictToSentence(d):
    s = ''
    for k,v in d.iteritems():
        if type(v) == type([]):
            for a in v:
                s = s.strip() + " " + dictToSentence(a)
        elif type(v) == type(d):
            s = s.strip() + " "  + dictToSentence(v)
        elif type(v) == type(''):
            s += s.strip() + " " + v
    return s.strip()
    
# command-line usage
if __name__ == "__main__":
    VERBOSE = True
    if len(sys.argv) < 2:
        print "Usage: wordreplace [parse]"
        sys.exit(0)
    else:
        phrase = ''
        for arg in sys.argv[1:]:
            phrase += arg + " "
        phrase = phrase[:-1]
        
        #parse = berkeleyParser.parsePhrase(phrase)
        #if VERBOSE: print parse
        parse = phrase
        
        tree = berkeleyParser.parseToTree(parse)
        if VERBOSE: print tree
        
        d = tree.toDict()
        if VERBOSE: print d
        
        replacements = findReplacements(tree, parse)
