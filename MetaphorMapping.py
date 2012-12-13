# master list of metaphor mappings

from wn import *

class Mapping:



    def map(self, word):

        senses = self.wn.get_senses_pos(word, 'n')

        if len(senses) < 1:
            return []

        possible = []

        for sense in senses:

            #print self.wn.synset_info(sense)
            #print "========================"

            left = self.wn.get_hypernym_in_list(sense, self.NounToNoun)
            if left == -1:
                continue

            right = self.NounToNoun[left]


            #print "\t"+self.wn.synset_info(left)+" -> "
            #for r in right:
                #print "\t\t" + self.wn.synset_info(r)


            for r in right:

                temp = self.wn.get_all_hyponyms(r)
                for t in temp:
                    possible.append(t)


        return possible








    def __init__(self):

        self.wn = wn("wordnet.db")

        nounToNoun = {}
        nounToAdj = {}

        nounToAdj = {
        105611302: [300708498], # mind is brittle
        107480068: [302091020], # emotion is blinding->concealing?
        107541053: [300269989], # hope is light
        107511733: [300269989], # (specific) hope is light
        104846770: [300417413, 302314584], # morality is clean
        104849241: [400096333, 300269989, 300393105], # good is up, white
        105144079: [400095320, 300273082, 300392812], # bad is down, black

        }

        nounToNoun = {
        107480068: [302261386, 111458624, 105194578, 111466043, 100027167, 107309781, 201206218, 114395018], # emotions are liquids (in a person, in the eyes), forces
        100007846: [102810471, 100015388, 100017222, 102913152, 103699975], # people are batteries
        107516354: [111466043, 114686186], # anger is heat
        201188485: [111466043], # lust is heat
        107544647: [105725527], # affection is warmth
        100759335: [114395018], # lust is madness
        107543288: [114395018, 113742573, 100306426, 105967977], # love is madness
        114379501: [202743020, 104738641], # emotional stability->sanity is balance
        107541053: [100032613, 109918248, 111473954], # hope is a possession
        107511733: [100032613, 109918248, 111473954], # (specific) hope is a possession
        113928388: [100015388, 104194289, 104468005, 102958343], # relationship is an animal
        104655442: [105085572], # emotional intimacy is physical closeness
        113781820: [100148653], # emotional bonding is physical bonding
        109622928: [100032613], # loved one is a possession
        201776727: [301251128], # dislike is cold
        107484265: [111458624, 105194578, 114039534], # desires are physical forces
        107519253: [301251128], # fear is cold
        104713118: [107027180], # emotional harmony is musical harmony
        107503260: [114359952], # disgust is nausea
        104887129: [100367280], # conceit is inflation
        107508486: [113501548], # pride is swelling
        100027807: [107309781, 103094503], # form is motion
        109387222: [110151570], # paths are guides
        104673965: [104151940], # appearance is a cover
        101072402: [100019613], # laughter is a substance
        100658082: [100973077], # treating illness is fighting a war
        103740161: [104565375], # medicine is a weapon
        114018567: [107334490], # intoxication is destruction
        111473954: [114939900, 302261386], # light is a fluid
        113983515: [115046900], # darkness is a solid
        103699975: [100007846], # machines are people
        113384557: [302261386], # money is a liquid
        113333237: [103094503], # investments are containers
        104846770: [104896161], # morality is cleanliness
        106784003: [108630039, 109225146], # problems are regions
        101129920: [100032613, 103679986, 103094503], # obligation is a possession
        103094503: [105194578], # obligation is force
        107966140: [105216365], # society is a body
        }



        # love is a journey
        nounToNoun[107543288] = [100306426]
        # career is a journey
        nounToNoun[100282613] = [100306426]
        # vehicle and person
        nounToNoun[104524313] = [100007846]
        # body and air
        nounToNoun[108436288] = [108653314]
        # harm is physical injury
        nounToNoun[107420770] = [114285662]
        # competition is a race
        nounToNoun[101168569] = [107472657]


        nounToNoun[long(105770926)] = [long(101170962)]
        nounToNoun[long(105805475)] = [long(100803617), long(113465809), long(105710860)] # understanding
        nounToNoun[long(105770926)] = [long(100243918), long(100278810)]
        nounToNoun[long(106252138)] = [long(101057759)]
        nounToNoun[long(100636921)] = [long(100310063)]
        nounToNoun[long(105611302)] = [long(103094503), long(103699975)] # mind
        nounToNoun[long(105833840)] = [long(106362953), long(109917593), long(109918248), long(105750657), long(105154676)] #idea
        nounToNoun[long(105941423)] = [long(103051540), long(109622302), long(110151570), long(114070360)] # belief
        nounToNoun[long(106283764)] = [long(104565375)]

        self.NounToNoun = nounToNoun
        self.NounToAdj = nounToAdj



def main():
    map = Mapping()
    input = raw_input()
    result = map.map(input)



if __name__ == "__main__":
    main()