nounToNoun = {}
nounToAdj = {}
nounToVerb = {}

# change is relative motion
nounToNoun[100191142] = 114004317

# causation is control over relative location
nounToNoun[100042311] = 100027167

# properties are possessions
nounToNoun[104916342] = 100032613

# attributes are entities
nounToNoun[100002684] = 100024264

# entities are attributes
nounToNoun[100001740] = 105849040

# well-being is wealth
nounToNoun[114447525] = 105116128

# motion is change
nounToNoun[107309781] = 113859043

# action is motion
nounToNoun[100037396] = 107309781

# active is alive
nounToAdj[114776804] = 300094448

# longterm purposeful activity is a journey
nounToNoun[100407535] = 100306426

# love is a journey
nounToNoun[107543288] = 100306426

# career is a journey
nounToNoun[100282613] = 100306426

# vehicle and person
nounToNoun[104524313] = 100007846

# person and person
nounToNoun[100007846] = 100007846

# body and air
nounToNoun[108436288] = 108653314

# harm is physical injury
nounToNoun[107420770] = 114285662

# status is position (comparison)
nounToNoun[113920835] = 113945919

# importance is precendence (comparison)
nounToNoun[105168261] = 113949802

# competition is a race
nounToNoun[101168569] = 107472657

# competition is a war

# opportunities are objects
nounToNoun[114483917] = 100002684

# creating is giving an object
nounToVerb[100908492] = 202316868

# time is something moving toward you
nounToNoun[115122231] = 201835496


nounToNoun[long(105770926)] = [long(101170962)]
nounToNoun[long(105805475)] = [long(100803617), long(113465809), long(105710860)] # understanding
nounToNoun[long(105770926)] = [long(100243918), long(100278810)]
nounToNoun[long(106252138)] = [long(101057759)]
nounToNoun[long(100636921)] = [long(100310063)]
nounToNoun[long(105611302)] = [long(103094503), long(103699975)] # mind
nounToNoun[long(105833840)] = [long(106362953), long(109917593), long(109918248), long(105750657), long(105154676)] #idea
nounToNoun[long(105941423)] = [long(103051540), long(109622302), long(110151570), long(114070360)] # belief
nounToNoun[long(106283764)] = [long(104565375)]


nounToAdj = {
105611302: 300708498, # mind is brittle
107480068: 302091020, # emotion is blinding->concealing?
107541053: 300269989, # hope is light
107511733: 300269989, # (specific) hope is light
104846770: 300417413, # morality is clean
104846770: 302314584, # morality is straight
104849241: 400096333, # good is up
105144079: 400095320, # bad is down
104849241: 300269989, # good is light
105144079: 300273082, # bad is dark
104849241: 300393105, # good is white
105144079: 300392812, # bad is black
}

nounToNoun = {
107480068: 302261386, # emotions are liquids (in a person, in the eyes)
107480068: 111458624, # emotions are physical forces
107480068: 105194578, # emotions are forces
100007846: 102810471, # people are batteries
107480068: 111466043, # emotions are heat
107516354: 111466043, # anger is heat
201188485: 111466043, # lust is heat
107544647: 105725527, # affection is warmth
107480068: 100027167, # emotions are locations
107480068: 107309781, # emotion is motion
107480068: 201206218, # "effect on emotionounToAdjl self is physical contact" -> emotion is physical contact ?
107480068: 114395018, # emotion is madness
100759335: 114395018, # lust is madness
107543288: 114395018, # love is madness
114379501: 202743020, # emotional stability->sanity is balance
114379501: 104738641, # emotional stability->sanity is maintaining position->stability
107516354: 114686186, # anger is fire
107541053: 100032613, # hope is a possession
107511733: 100032613, # (specific) hope is a possession
107541053: 109918248, # hope is a child
107511733: 109918248, # (specific) hope is a child
107541053: 111473954, # hope is light
107511733: 111473954, # (specific) hope is light
107543288: 100306426, # love is a journey
113928388: 100015388, # relationship is an animal
113928388: 104194289, # relationship is a ship
113928388: 104468005, # relationship is a train
113928388: 102958343, # relationship is a car
107543288: 113742573, # love is unity
104655442: 105085572, # emotional intimacy is physical closeness
113781820: 100148653, # emotional bonding is physical bonding
109622928: 100032613, # loved one is a possession
201776727: 301251128, # dislike is cold
107543288: 105967977, # love is magic
107484265: 111458624, # desires are physical forces
107484265: 105194578, # desires are forces
107484265: 114039534, # desire is hunger
100007846: 100015388, # people are animals
107519253: 301251128, # fear is cold
104713118: 107027180, # emotional harmony is musical harmony
107503260: 114359952, # disgust is nausea
104887129: 100367280, # conceit is inflation
107508486: 113501548, # pride is swelling
100027807: 107309781, # form is motion
109387222: 110151570, # paths are guides
100027807: 103094503, # shapes are containers
104673965: 104151940, # appearance is a cover
101072402: 100019613, # laughter is a substance
100658082: 100973077, # treating illness is fighting a war
103740161: 104565375, # medicine is a weapon
114018567: 107334490, # intoxication is destruction
111473954: 114939900, # light is a fluid
111473954: 302261386, # light is a liquid
113983515: 115046900, # darkness is a solid
103699975: 100007846, # machines are people
113384557: 302261386, # money is a liquid
113333237: 103094503, # investments are containers
104846770: 104896161, # morality is cleanliness
100007846: 103699975, # people are machines
100007846: 100017222, # people are plants
100007846: 102913152, # people are buildings
106784003: 108630039, # problems are regions
106784003: 109225146, # problems are bodies of water
101129920: 100032613, # obligation is a possession
101129920: 103679986, # obligation is a burden
101129920: 103094503, # obligation is container
103094503: 105194578, # obligation is force
107966140: 105216365, # society is a body
}