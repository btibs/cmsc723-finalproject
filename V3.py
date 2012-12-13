from wn import *
import berkeleyParser as parser
from wordreplace import *
import re
from MetaphorMapping import *
import fileinput

import operator


def get_stop_words():
    stop_words = []
    f = open("stop.txt",'r')
    for word in fileinput.input("stop.txt"):
        stop_words.append(word.strip())
    return stop_words


# Remove stopwords from <words>:
def remove_stopwords(words, stopwords):
    ret = []
    for w in words:
        if w not in stopwords:
            ret.append(w)
    return ret

# Jaccard similarity:
def jaccard(words1, words2):
    shared = 0
    total = len(words1) + len(words2)
    for word in words1:
        if word in words2:
            #print "\t\t" + word
            shared += 1
    return float(shared) / float(total)


def SAP_distance(words1, words2, wordnet):
    sum = 0
    tots = len(words1) * len(words2)
    for word1 in words1:
        for word2 in words2:
            sap = wordnet.SAP(word1, word2)
            sum += sap
    #print words1
    #print words2
    #print float(tots) / float(sum)
    #print
    #print
    return float(tots) / float(sum)




def adj_test():
    w = wn("wordnet.db")
    adj = raw_input()
    wid = w.get_word_ids(adj)
    sids = w.get_synset_ids(wid)
    for sid in sids:
        print w.synset_info(sid)

        rel = w.get_related_adjs(sid)
        for r in rel:
            print '\t'+w.synset_info(r)




def generate_noun_metaphors(sentence, parse, place):
    wordnet = wn("wordnet.db")
    stop_words = get_stop_words()


    words = sentence.split(" ")
    for i, word in enumerate(words):
        words[i] = re.sub(r'\W+', '', word).lower()

    noun = words[place[0]] # word to metaphorize
    replace = words[place[1]] # word to replace

    metmap = Mapping()

    context = remove_stopwords(words, stop_words)

    # Find metaphors ##########
    possible = metmap.map(noun)
    have_overlap = {}
    overlap = {}
    for sid in possible:
        text = wordnet.get_text(sid)
        text = remove_stopwords(text, stop_words)
        sim = jaccard(text, context)
        #print sim
        if sim > 0.0:
            have_overlap[sid] = text
            overlap[sid] = sim

    # Limit number of synsets by overlap
    MAX = 5
    keys = []
    overlap = sorted(overlap.iteritems(), key=operator.itemgetter(1))
    overlap = overlap[-1*MAX:]
    for pair in overlap:
        keys.append(pair[0])

    max_similarity = -1.0
    max_sid = None
    for sid in keys:
        text = have_overlap[sid]

        # TODO - CAN USE JACCARD OR SAP ------------------------------------------------^^^^^^^
        #sim = SAP_distance(text, context, wordnet)
        sim = jaccard(text, context)

        if sim >  max_similarity:
            max_sid = sid
            max_similarity = sim

    if max_sid is None:
        return False, sentence

    lemma = wordnet.get_lemma(max_sid)

    #metaphor = wordnet.synset_info(max_sid)
    #print "Found mapping from '%s' to: %s" % (word, metaphor)

    return True, sentence.replace(replace, lemma)






def main():

    input_file = "input.txt"

    originals = []
    for text in fileinput.input(input_file):
        originals.append(text.strip())

    output_file = "output.txt"
    parser.parseFile(input_file, output_file)

    parses = []

    for parse in fileinput.input(output_file):
        parses.append(parse.strip())

    for i in range(len(parses)):

        parse = parses[i]
        original = originals[i]

        try:
            tree = parser.parseToTree(parse)
        except:
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            continue

        reps = findReplacements(tree, parse)


        if "NN_NN" in reps.keys():

            changed, result = generate_noun_metaphors(original, parse, reps["NN_NN"])


            if changed:
                print original
                print result
                print
                print














if __name__ == "__main__":
    main()
