from wn import *

wn = wn('wordnet.db')


while True:

    lemma = str(raw_input())

    wid = wn.get_word_ids(lemma)
    sids = wn.get_synset_ids(wid)

    for sid in sids:
        info = wn.synset_more_info(sid)
        print info

    print