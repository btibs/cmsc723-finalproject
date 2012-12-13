# Isaac Julien
# wn.py
# Python module for interfacing with WordNet SQLite

import re

class wn:

    # Argument is name of database
    # Creates <c>, a cursor for the db
    def __init__(self, db_name):
        import sqlite3
        conn = sqlite3.connect(db_name)
        self.c = conn.cursor()

    # BASIC ===================================================================

    # Return word id for lemma (long):
    def get_word_ids(self, lemma):
        arg = (lemma,)
        self.c.execute("SELECT wordid FROM WORDS WHERE lemma = ?", arg)
        res = self.c.fetchone()
        if res is None:
            return None
        return long(res[0])

    # Return list of synset ids for word id (list of longs):
    def get_synset_ids(self, word_id):
        arg = (word_id,)
        self.c.execute("SELECT synsetid FROM SENSES WHERE wordid = ?", arg)
        res = self.c.fetchall()
        synsetids = []
        for r in res:
            synsetids.append(long(r[0]))
        return synsetids

    # Return word form for word id:
    def get_word_form(self, wordid):
        arg = (wordid,)
        self.c.execute("SELECT lemma FROM WORDS WHERE wordid = ?", arg)
        res = self.c.fetchone()
        if res is None:
            return None
        return str(res[0])


    # SYNSET INFO ============================================================+

    # Return tag count of synset (int):
    def get_tagcount(self, synsetid):
        arg = (synsetid,)
        self.c.execute("SELECT tagcount FROM SENSES WHERE synsetid = ?", arg)
        res = self.c.fetchone()
        return int(res[0])

    # Return gloss (definition) of synset (string):
    def get_gloss(self, synsetid):
        arg = (synsetid,)
        self.c.execute("SELECT definition FROM SYNSETS WHERE synsetid = ?", arg)
        res = self.c.fetchone()
        return str(res[0])

    # Get example sentences of synset (string):
    def get_examples(self, synsetid):
        arg = (synsetid,)
        self.c.execute("SELECT sample FROM SAMPLES WHERE synsetid = ?", arg)
        res = self.c.fetchone()
        if res is None:
            return None
        return str(res[0])

    # Get example sentences of synset (string):
    def get_pos(self, synsetid):
        arg = (synsetid,)
        self.c.execute("SELECT pos FROM SYNSETS WHERE synsetid = ?", arg)
        res = self.c.fetchone()
        if res is None:
            return None
        return str(res[0])

    # Return string with info about synsets
    def synset_info(self, synsetid):
        lemma = self.get_lemma(synsetid)
        gloss = self.get_gloss(synsetid)
        ex = self.get_examples(synsetid)
        if ex is None:
            ex = ""
        return lemma + '\t' + gloss + "\t" + '\"' + ex + '\"'

    # Return string with more info about synset:
    def synset_more_info(self, synsetid):
        lemma = self.get_lemma(synsetid)
        tc = self.get_tagcount(synsetid)
        gloss = self.get_gloss(synsetid)
        ex = self.get_examples(synsetid)
        if ex is None:
            ex = ""
        return "SynsetID=" + str(synsetid) + ' TagCount=' + str(tc) + '\t' + lemma + '\t' + gloss + "\t" + '\"' + ex + '\"'


    # SYNSET RELATIONS ========================================================

    # Return hypernym synsetids (longs):
    def get_domain(self, synsetid):
        arg = (synsetid,)
        command = "SELECT synset2id FROM SEMLINKS WHERE synset1id = ? and linkid in (SELECT linkid FROM linktypes WHERE link='domain category')"
        self.c.execute(command, arg)
        res = self.c.fetchone()
        if res is None:
            return None
        return long(res[0])

    # Return hypernym synsetids (longs):
    def get_hypernyms(self, synsetid):
        arg = (synsetid,)
        command = "SELECT synset2id FROM SEMLINKS WHERE synset1id = ? and linkid in (SELECT linkid FROM linktypes WHERE link='hypernym')"
        self.c.execute(command, arg)
        res = self.c.fetchall()
        synsetids = []
        for r in res:
            synsetids.append(long(r[0]))
        return synsetids

    # Return hyponym synsetids (longs):
    def get_hyponyms(self, synsetid):
        arg = (synsetid,)
        command = "SELECT synset2id FROM SEMLINKS WHERE synset1id = ? and linkid in (SELECT linkid FROM linktypes WHERE link='hyponym')"
        self.c.execute(command, arg)
        res = self.c.fetchall()
        synsetids = []
        for r in res:
            synsetids.append(long(r[0]))
        return synsetids

    # SPECIAL =================================================================

    # Get all wordids:
    def get_all_wordids(self):
        self.c.execute("SELECT wordid FROM SENSES")
        res = self.c.fetchall()
        wordids = []
        for r in res:
            wordids.append(long(r[0]))
        return wordids


    # Get all synsets:
    def get_all_synsets(self):
        self.c.execute("SELECT synsetid FROM SYNSETS")
        res = self.c.fetchall()
        synsetids = []
        for r in res:
            synsetids.append(long(r[0]))
        return synsetids

    # Return lemma (string) of synset given id:
    def get_lemma(self, synsetid):
        arg = (synsetid,)
        command = "SELECT lemma FROM WORDS WHERE wordid in (SELECT wordid FROM SENSES WHERE synsetid = ?)"
        self.c.execute(command, arg)
        res = self.c.fetchone()
        return str(res[0])

    # Get all link names:
    def get_linknames(self):
        links = []
        self.c.execute("SELECT link FROM LINKTYPES")
        res = self.c.fetchall()
        for r in res:
            links.append(str(r[0]))
        return links


    # For a given gloss, return all associated domain categories of words in the gloss with same POS:
    def gloss_pos_finder(self, gloss, pos):

        dcs = []

        split = gloss.split("\W")
        for s in split:
            lemma = s.lower().strip()
            senses = self.get_synset_ids(lemma)
            # Use most common sense heuristic:
            best_sense = 0
            max_tags = 0
            for sense in senses:
                tags = self.get_tagcount(sense)
                if tags > max_tags:
                    max_tags = tags
                    best_sense = sense

            # Discard synsets with different POS
            best_pos = self.get_pos(best_sense)
            if best_pos != pos:
                continue

            # Get domain of best sense:
            dc = self.get_domain(best_sense)
            if dc is not None:
                dcs.append(dc)

        return dcs


    # MAPPING #########################################################################

    # Return sense with nonzero tag count and matching POS (basic disambiguation):
    def get_senses_pos(self, word, pos):
        wid = self.get_word_ids(word)
        sids = self.get_synset_ids(wid)

        same_pos = []
        for sid in sids:
            tc = self.get_tagcount(sid)
            if tc == 0:
                continue
            apos = self.get_pos(sid)
            if apos == pos:
                same_pos.append(sid)

        return same_pos


    # Return first hypernym of <first_sid> appearing in <list>:
    # Return -1 if no hypernym is in list
    def get_hypernym_in_list(self, first_sid, list):

        sids = [first_sid]

        while True:

            new_sids = []

            for sid in sids:
                if sid in list:
                    return sid

                hyps = self.get_hypernyms(sid)
                if len(hyps) < 1:
                    return -1
                for hyp in hyps:
                    new_sids.append(hyp)

            sids = new_sids

    # Return entire hyponym subtree, including root word:
    def get_all_hyponyms(self, first_sid):
        all = []

        sids = [first_sid]
        added = False
        while True:
            new_sids = []
            for sid in sids:
                all.append(sid)
                hypos = self.get_hyponyms(sid)
                if len(hypos) < 1:
                    added = False
                    continue
                added = True
                for hypo in hypos:
                    new_sids.append(hypo)
            if added is False:
                return all
            sids = new_sids

    # Return all text context of synset:
    def get_text(self, sid):
        gloss = self.get_gloss(sid)
        examples = self.get_examples(sid)
        both = gloss
        if examples is not None:
            both += " " + examples
        words = both.split(" ")
        for i, word in enumerate(words):
            words[i] = re.sub(r'\W+', '', word).lower()
        return words

    # Return shortest Ancestral Path between word1, word2:
    def SAP(self, word1, word2):
        set1 = self.get_synset_ids(self.get_word_ids(word1))
        set2 = self.get_synset_ids(self.get_word_ids(word2)) #TODO: could do by POS, for both.
        seen1 = {}
        seen2 = {}
        for s in set1:
            seen1[s] = 0
        for s in set2:
            seen2[s] = 0

        MAX = 5

        if len(set1) < 1 or len(set2) < 1:
            return 2*MAX

        level = 0
        while True:
            for s in set1:
                if s in seen2.keys():
                    return level + seen2[s]
            for s in set2:
                if s in seen1:
                    return level + seen1[s]

            new1 = []
            for s in set1:
                hypers = self.get_hypernyms(s)
                for h in hypers:
                    new1.append(h)
                seen1[s] = level
            set1 = new1

            new2 = []
            for s in set2:
                hypers = self.get_hypernyms(s)
                for h in hypers:
                    new2.append(h)
                seen2[s] = level
            set2 = new2

            level += 1

            if level >= MAX:
                return 2*MAX


    # Get adjectives related to noun:
    def get_related_adjs(self, sid):
        arg = (sid,)
        print sid
        command = "SELECT synset2id FROM LEXLINKS WHERE synset1id = ? "+\
                  "and linkid in (SELECT linkid FROM linktypes WHERE link='derivation')"+\
                  " and synset2id in (SELECT synsetid FROM SYNSETS WHERE pos='a')"
        self.c.execute(command, arg)
        res = self.c.fetchall()
        synsetids = []
        for r in res:
            print r
            synsetids.append(long(r[0]))
        return synsetids

    # Get nouns related to adjective:
    def get_related_noun(self, sid):
        arg = (sid,)
        print sid
        command = "SELECT synset2id FROM LEXLINKS WHERE synset1id = ? "+\
                  "and linkid in (SELECT linkid FROM linktypes WHERE link='derivation')"+\
                  " and synset2id in (SELECT synsetid FROM SYNSETS WHERE pos='n')"
        self.c.execute(command, arg)
        res = self.c.fetchall()
        synsetids = []
        for r in res:
            print r
            synsetids.append(long(r[0]))
        return synsetids







# Some simple test code - prints out some info about an input word
def main():

    print "this is a test of wn.py"
    wn = wn("wordnet.db")


    word = raw_input("Word?\t")
    res = wn.get_word_ids(word)

    if res is not None:

        print "word id = " + str(res)

        res = wn.get_synset_ids(res)
        for sid in res:

            print wn.synset_info(sid)

            print "\tHypernyms:"

            hypernyms = wn.get_hypernyms(sid)
            for hid in hypernyms:
                print "\t\t" + wn.synset_info(hid)

            print "\tHyponyms:"

            hyponyms = wn.get_hyponyms(sid)
            for hid in hyponyms:
                print "\t\t" + wn.synset_info(hid)