# Berkeley Parser interface
# requires:
# berkeleyParser.jar (in same folder)
# java installed

#example BerkeleyParser command-line usage:
#echo %s | java -jar berkeleyParser.jar -gr eng_sm6.gr"

import subprocess
import os
import sys

VERBOSE = True

class ParseTree:
    def __init__(self, tag=None, parent=None, children=[], word=None):
        self.tag = tag
        self.parent = parent
        self.children = children
        self.word = word
    
    def __str__(self):
        if self.word is not None:
            return "%s: %s" % (self.tag, self.word)
        else:
            return "%s: %s" % (self.tag, self.children)
        
    def toDict(self):
        # convert tree to dictionary
        d = {}
        if self.word is None:
            d[self.tag] = []
            for c in self.children:
                d[self.tag].append(c.toDict())
        else:
            d[self.tag] = self.word
        return d

def parsePhrase(phrase):
    # get parse from BerkeleyParser
    # python 2.7+
    #parse = subprocess.check_output(['echo %s'%phrase, '| java', '-jar', 'berkeleyParser.jar', '-gr', 'eng_sm6.gr'])
    # python < 2.7
    process = os.popen("echo %s | java -jar berkeleyParser.jar -gr eng_sm6.gr" % phrase)
    parse = process.read()
    process.close()
    return parse

def parseToTree(parse):
    # example parse: '( (S (NP (DT This)) (VP (VBZ is) (NP (DT a) (NN test)))) )'
    
    # parser always has extra layer of parens, remove those
    parse = parse.strip()
    if parse.startswith("( "):
        if parse.endswith(" )"):
            parse = parse[2:-2]
    
    curTag = None
    arr = [s.strip() for s in parse.split('(') if s != '']
    for a in arr:
        if a.endswith(")"):
            # we are closing tags
            parts = [s.strip() for s in a.split(" ")]
            tagname = parts[0]
            wordstr = parts[1].strip(")")
            newTag = ParseTree(tag=tagname, parent=curTag, word=wordstr)
            curTag.children.append(newTag)
            newTag.children = []
            for i in range(a.count(")")):
                # close tag - go up the tree
                if curTag.parent is not None:
                    curTag = curTag.parent
        else:
            newTag = ParseTree(tag=a, parent=curTag)
            if curTag is not None:
                curTag.children.append(newTag)
                newTag.children = []
            curTag = newTag
    return curTag
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: berkeleyParser [phrase]"
        sys.exit(0)
    else:
        phrase = ''
        for arg in sys.argv[1:]:
            phrase += arg + " "
        phrase = phrase[:-1]

        if sys.argv[1] == "-p":
            parse = phrase[2:]
        else:
            parse = parsePhrase(phrase)

        if VERBOSE: print parse
        tree = parseToTree(parse)
        if VERBOSE: print tree
        d = tree.toDict()
        if VERBOSE: print d
