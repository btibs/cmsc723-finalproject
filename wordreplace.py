# find suitable words in a sentence to replace

import berkeleyParser
from MetaphorMapping import nounToNoun, nounToAdj#, nounToVerb
import re

'''
“[NN] is a [NN]” (Noun is metaphor)
“[NN] [VV]” (Verb is metaphor)
“[JJ] [NN]” or “[NN] is [JJ]” (Adjective is metaphor)
'''
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
    'IS':   ['is', 'are', 'am', 'was', 'were'], # complex enough?
}

# make regexs
for p, pat in PATTERNS.iteritems():
    s = pat
    for w, wtags in WORD_TYPES.iteritems():
        if s.find(w) >= 0:
            s = s.replace(w, "(" + '|'.join(wtags) + ")")
    print s

'''
(NP|NN|NNS|NNP|NNPS|PRP) (ADJP|JJ|JJR|JJS)
(NP|NN|NNS|NNP|NNPS|PRP) (VP|VB|VBD|VBG|VBN|VBP|VBZ)
(NP|NN|NNS|NNP|NNPS|PRP) (is|are|am|was|were) (NP|NN|NNS|NNP|NNPS|PRP)
(NP|NN|NNS|NNP|NNPS|PRP) (is|are|am|was|were) (ADJP|JJ|JJR|JJS)
'''
# example: {'S': [{'NP': [{'DT': 'This'}]}, {'VP': [{'VBZ': 'is'}]}, {'NP': [{'DT': 'a'}]}, {'NN': 'test'}]}
# parse: '( (S (NP (DT This)) (VP (VBZ is) (NP (DT a) (NN test)))) )'
# this is NN_NN (NP IS NP)

# find possible replacement locations given a parse tree and original parse
# return dictionary of PATTERN_TYPE: [loc, loc] ?
# exclude NN_VV is V = IS?
def findReplacements(parse):
    # first: find patterns matching the types
    patmatches = []
    for p, pat in PATTERNS.iteritems():
        lastI = 0
        matches = True
        for word in pat.split(" "):
            for tag in WORD_TYPES[word]:
                if parse.find(tag, lastI) > -1:
                    lastI = parse.find(tag, lastI)
                    break
                else:
                    matches = False
        if matches:
            patmatches.append(p)
    
    # second: return locations of those in the sentence
    print patmatches
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
    if len(sys.argv) < 2:
        print "Usage: wordreplace [phrase]"
        sys.exit(0)
    else:
        phrase = ''
        for arg in sys.argv[1:]:
            phrase += arg + " "
        phrase = phrase[:-1]
        
        parse = berkeleyParser.parsePhrase(phrase)
        if VERBOSE: print parse
        
        tree = berkeleyParser.parseToTree(parse)
        if VERBOSE: print tree
        
        d = tree.toDict()
        if VERBOSE: print d
        
        replacements = findReplacements(tree, parse)
