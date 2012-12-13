# find suitable words in a sentence to replace, given the parse of the sentence

from berkeleyParser import parseToTree
from MetaphorMapping import nounToNoun, nounToAdj#, nounToVerb
import re
import sys

PATTERNS = {
    'NN_NN': 'NOUN IS NOUN',    # noun2 is metaphor
    'NN_VV': 'NOUN VERB',       # verb is metaphor
    'JJ_NN': 'ADJ NOUN',        # adjective is metaphor
    'NN_JJ': 'NOUN IS ADJ',     # adjective is metaphor
}
WORD_TYPES = {
    'ADJ':  ['ADJP', 'JJ', 'JJR', 'JJS'],
    'NOUN': ['NP', 'NN', 'NNS', 'NNP', 'NNPS', 'PRP'], # should proper nouns and pronouns actually be included?
    'VERB': ['VP', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'],
    'IS':   [' is', ' are', ' am', ' was', ' were'], # complex enough?
}

"""
# make regexs?
for p, pat in PATTERNS.iteritems():
    s = pat
    for w, wtags in WORD_TYPES.iteritems():
        if s.find(w) >= 0:
            s = s.replace(w, "(" + '|'.join(wtags) + ")")
    #print s
"""

# return a dictionary of PATTERN_TYPE: [wordloc, wordloc, ..]
def findReplacements(tree, parse):
    '''
    Find candidates for replacement based on give patterns and word types
    Returns a dictionary of {PATTERN_TYPE: [wordloc, wordloc, ...], ...}
    '''
    repls = {}
    for pname, pat in PATTERNS.iteritems():
        # for each pattern, try to find it in the tree
        repls[pname] = []
        wi = -1
        for pword in pat.split(" "):
            loc = findWordTypeInTree(tree, pword)
            if len(loc) > 0:
                for l in loc:
                    if l[0] > wi:
                        wi = l[0]
                        repls[pname].append(wi)
                        break
                        
        if len(repls[pname]) != len([p for p in pat.split(" ") if p != "IS"]):
            # did not find as many words as required by pattern
            repls.pop(pname)
            
    return repls

def findWordTypeInTree(curTag, wordType):
    '''
    Find a word of given wordType in a parse tree, starting at the current tag, similar to BFS
    If successful, returns [(wordindex, tag),...], else []
    '''
    locs = []
    if curTag.tag.strip() in WORD_TYPES[wordType]:
        if curTag.word is not None and curTag.word.strip() != '': # success
            locs.append((curTag.wordIndex, curTag.tag.strip()))
        else: # try to find more specific child
            for c in curTag.children:
                result = findWordTypeInTree(c, wordType)
                if len(result) > 0: # success
                    locs += result
            if len(locs) == 0:  # i.e. finding child failed; just try to find a word below this tag
                # TODO this may be dumb; just goes down through first child
                temptag = curTag
                while temptag.word is None or temptag.word.strip() == '':
                    temptag = temptag.children[0]
                locs.append((temptag.wordIndex, curTag.tag.strip()))
    elif curTag.word is None or curTag.word.strip() == '':
        # curTag does not match - but children might
        for c in curTag.children:
            result = findWordTypeInTree(c, wordType)
            if len(result) > 0: # success
                locs += result
    return locs
                
def dictToSentence(d):
    '''Recover original sentence from parse dictionary'''
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
    
# command-line demo
if __name__ == "__main__":
    VERBOSE = True
    if len(sys.argv) < 2:
        print "Usage: wordreplace [parse]"
        sys.exit(0)
    else:
        phrase = ''
        for arg in sys.argv[1:]:
            phrase += arg + " "
        parse = phrase[:-1]
        
        tree = parseToTree(parse)
        if VERBOSE: print tree
        
        d = tree.toDict()
        if VERBOSE: print d
        
        replacements = findReplacements(tree, parse)
        print "found replacements:",replacements