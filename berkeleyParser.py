# Berkeley Parser interface
# requires:
# - berkeleyParser.jar (in same folder)
# - java installed

import subprocess
import os
import sys
from optparse import OptionParser

VERBOSE = True

class ParseTree:
    '''class to hold parse information'''
    def __init__(self, tag=None, parent=None, word=None, wordIndex=0):
        self.tag = tag
        self.parent = parent
        self.word = word
        self.wordIndex = wordIndex
        self.children = []
    
    def __str__(self):
        if self.word is not None:
            return "%s: %s" % (self.tag, self.word)
        else:
            return "%s: [%s]" % (self.tag, ", ".join([str(c) for c in self.children]))
        
    def toDict(self):
        '''convert tree to dictionary'''
        d = {}
        if self.word is None:
            d[self.tag] = []
            for c in self.children:
                d[self.tag].append(c.toDict())
        else:
            d[self.tag] = self.word
        return d

def parsePhrase(phrase):
    '''Returns a parse of a phrase'''
    # python 2.7+
    #parse = subprocess.check_output(['echo %s'%phrase, '| java', '-jar', 'berkeleyParser.jar', '-gr', 'eng_sm6.gr'])
    # python < 2.7
    process = os.popen("echo %s | java -jar berkeleyParser.jar -gr eng_sm6.gr" % phrase)
    parse = process.read()
    process.close()
    return parse

def parseFile(inputfile, outputFile=None):
    '''Parse sentences in a file, optionally writing output to another file'''
    pstr = "java -jar berkeleyParser.jar -gr eng_sm6.gr -inputFile %s" % inputfile
    if outputFile is not None:
        pstr += " -outputFile %s" % outputFile
    process = os.popen(pstr)
    result = process.read()
    process.close()
    return result
    
def parseToTree(parse):
    '''Convert a parse to a ParseTree'''
    # parser always has extra layer of parens, remove those
    parse = parse.strip()
    if parse.startswith("( ") and parse.endswith(" )"):
        parse = parse[2:-2]
    
    curTag = None
    temp = ''
    i = 0
    wi = 0
    while (i < len(parse)):
        c = parse[i]
        if c == "(":    # opening tag
            tn = ''
            while (parse[i] != ' '):
                i += 1
                tn += parse[i]  # index error sometimes: expecting (TAG word) not (TAG (word)) format
            newTag = ParseTree(tag=tn, parent=curTag)
            if curTag is not None:
                curTag.children.append(newTag)
            curTag = newTag
        elif c == ")":  # closing tag
            if temp != '':
                curTag.word = temp
                curTag.wordIndex = wi
                wi += 1
                temp = ''
            if curTag.parent is not None:
                curTag = curTag.parent
        else:   temp += c
        i += 1
        
    return curTag
    
# command-line entry
if __name__ == "__main__":
    op = OptionParser()
    op.add_option("-p", "--phrase", dest="phrase", help="simple phrase to parse")
    op.add_option("-i", "--input",  dest="inputfile", help="file containing sentences to parse")
    op.add_option("-o", "--output", dest="outputfile", help="file to store parse output")
    op.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False, help="print result to stdout")
    (options, args) = op.parse_args()
    
    if not options.phrase and not options.inputfile:
        print op.print_help()
        sys.exit(0)
    
    if options.phrase:
        result = parsePhrase(options.phrase)
        print result
        if options.verbose:
            tree = parseToTree(result)
            print "Tree:", tree
            d = tree.toDict()
            print "Dict:", d
    
    if options.inputfile:
        result = parseFile(options.inputfile, options.outputfile)
        if options.verbose and options.outputfile:
            print "wrote parse to %s" % options.outputfile
        else:
            print result
