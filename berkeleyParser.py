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
    def __init__(self, tag=None, parent=None, word=None):
        self.tag = tag
        self.parent = parent
        self.word = word
        self.children = []
    
    def __str__(self):
        if self.word is not None:
            return "%s: %s" % (self.tag, self.word)
        else:
            return "%s: %s" % (self.tag, [c.__str__() for c in self.children])
        
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
    if parse.startswith("( ") and parse.endswith(" )"):
        parse = parse[2:-2]
    
    curTag = None
    temp = ''
    i = 0
    while (i < len(parse)):
        c = parse[i]
        if c == "(":    # opening tag
            tn = ''
            while (parse[i] != ' '):
                i += 1
                tn += parse[i]
            newTag = ParseTree(tag=tn, parent=curTag)
            if curTag is not None:
                curTag.children.append(newTag)
            curTag = newTag
        elif c == ")":  # closing tag
            if temp != '':
                curTag.word = temp
                temp = ''
            if curTag.parent is not None:
                curTag = curTag.parent
        else:   temp += c
        i += 1
        
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
