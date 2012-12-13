from wn import *
import re

w = wn("wordnet.db")

out = open("input.txt", 'w')


dets = ["the", "an", "a"]

all_sids = w.get_all_synsets()

for sid in all_sids:

    tc = w.get_tagcount(sid)
    if tc > 5:




        gloss = w.get_gloss(sid).lower().strip()
        lemma = w.get_lemma(sid).lower().strip()

        words = gloss.split(" ")
        first = words[0]

        if first not in dets:
            continue

        sentence = "A %s is %s.\n" % (lemma, gloss)

        out.write(sentence)
