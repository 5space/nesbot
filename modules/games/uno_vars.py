import itertools

COLOR_WILD = 0
COLOR_RED = 1
COLOR_YELLOW = 2
COLOR_GREEN = 3
COLOR_BLUE = 4

CARD_0 = 0
CARD_1 = 1
CARD_2 = 2
CARD_3 = 3
CARD_4 = 4
CARD_5 = 5
CARD_6 = 6
CARD_7 = 7
CARD_8 = 8
CARD_9 = 9

CARD_SKIP = 10
CARD_REVERSE = 11
CARD_DRAWTWO = 12
CARD_WILD = 13
CARD_DRAWFOUR = 14
CARD_DRAWEIGHT = 15
CARD_SHUFFLEHANDS = 16

CARD_SPECIALS = [CARD_SKIP, CARD_REVERSE, CARD_DRAWTWO, CARD_DRAWFOUR, CARD_DRAWEIGHT]
CARD_WILDS = [CARD_WILD, CARD_DRAWFOUR, CARD_DRAWEIGHT, CARD_SHUFFLEHANDS]

COLOR_STRINGS = {COLOR_RED: "red",
                 COLOR_YELLOW: "yellow",
                 COLOR_GREEN: "green",
                 COLOR_BLUE: "blue"}

CARD_NONWILD_STRINGS = {CARD_0: "0",
                        CARD_1: "1",
                        CARD_2: "2",
                        CARD_3: "3",
                        CARD_4: "4",
                        CARD_5: "5",
                        CARD_6: "6",
                        CARD_7: "7",
                        CARD_8: "8",
                        CARD_9: "9",
                        CARD_SKIP: "skip",
                        CARD_REVERSE: "reverse",
                        CARD_DRAWTWO: "+2",
                        CARD_WILD: "wild",
                        CARD_DRAWFOUR: "wild +4",
                        CARD_DRAWEIGHT: "wild +8",
                        CARD_SHUFFLEHANDS: "shuffle hands"}

# CARDS = [tuple(x) for x in itertools.product(COLOR_STRINGS.keys(), range(13))]
# CARDS *= 2
# CARDS.remove((COLOR_RED, CARD_0))
# CARDS.remove((COLOR_YELLOW, CARD_0))
# CARDS.remove((COLOR_GREEN, CARD_0))
# CARDS.remove((COLOR_BLUE, CARD_0))
# CARDS += [
#     (COLOR_WILD, CARD_WILD),
#     (COLOR_WILD, CARD_WILD),
#     (COLOR_WILD, CARD_WILD),
#     (COLOR_WILD, CARD_WILD),
#     (COLOR_WILD, CARD_DRAWFOUR),
#     (COLOR_WILD, CARD_DRAWFOUR),
#     (COLOR_WILD, CARD_DRAWFOUR),
#     (COLOR_WILD, CARD_DRAWFOUR),
#     (COLOR_WILD, CARD_DRAWEIGHT)
# ]

CARDS = [(COLOR_RED, CARD_0),
         (COLOR_RED, CARD_1),
         (COLOR_RED, CARD_1),
         (COLOR_RED, CARD_2),
         (COLOR_RED, CARD_2),
         (COLOR_RED, CARD_3),
         (COLOR_RED, CARD_3),
         (COLOR_RED, CARD_4),
         (COLOR_RED, CARD_4),
         (COLOR_RED, CARD_5),
         (COLOR_RED, CARD_5),
         (COLOR_RED, CARD_6),
         (COLOR_RED, CARD_6),
         (COLOR_RED, CARD_7),
         (COLOR_RED, CARD_7),
         (COLOR_RED, CARD_8),
         (COLOR_RED, CARD_8),
         (COLOR_RED, CARD_9),
         (COLOR_RED, CARD_9),
         (COLOR_RED, CARD_SKIP),
         (COLOR_RED, CARD_SKIP),
         (COLOR_RED, CARD_REVERSE),
         (COLOR_RED, CARD_REVERSE),
         (COLOR_RED, CARD_DRAWTWO),
         (COLOR_RED, CARD_DRAWTWO),
         (COLOR_YELLOW, CARD_0),
         (COLOR_YELLOW, CARD_1),
         (COLOR_YELLOW, CARD_1),
         (COLOR_YELLOW, CARD_2),
         (COLOR_YELLOW, CARD_2),
         (COLOR_YELLOW, CARD_3),
         (COLOR_YELLOW, CARD_3),
         (COLOR_YELLOW, CARD_4),
         (COLOR_YELLOW, CARD_4),
         (COLOR_YELLOW, CARD_5),
         (COLOR_YELLOW, CARD_5),
         (COLOR_YELLOW, CARD_6),
         (COLOR_YELLOW, CARD_6),
         (COLOR_YELLOW, CARD_7),
         (COLOR_YELLOW, CARD_7),
         (COLOR_YELLOW, CARD_8),
         (COLOR_YELLOW, CARD_8),
         (COLOR_YELLOW, CARD_9),
         (COLOR_YELLOW, CARD_9),
         (COLOR_YELLOW, CARD_SKIP),
         (COLOR_YELLOW, CARD_SKIP),
         (COLOR_YELLOW, CARD_REVERSE),
         (COLOR_YELLOW, CARD_REVERSE),
         (COLOR_YELLOW, CARD_DRAWTWO),
         (COLOR_YELLOW, CARD_DRAWTWO),
         (COLOR_GREEN, CARD_0),
         (COLOR_GREEN, CARD_1),
         (COLOR_GREEN, CARD_1),
         (COLOR_GREEN, CARD_2),
         (COLOR_GREEN, CARD_2),
         (COLOR_GREEN, CARD_3),
         (COLOR_GREEN, CARD_3),
         (COLOR_GREEN, CARD_4),
         (COLOR_GREEN, CARD_4),
         (COLOR_GREEN, CARD_5),
         (COLOR_GREEN, CARD_5),
         (COLOR_GREEN, CARD_6),
         (COLOR_GREEN, CARD_6),
         (COLOR_GREEN, CARD_7),
         (COLOR_GREEN, CARD_7),
         (COLOR_GREEN, CARD_8),
         (COLOR_GREEN, CARD_8),
         (COLOR_GREEN, CARD_9),
         (COLOR_GREEN, CARD_9),
         (COLOR_GREEN, CARD_SKIP),
         (COLOR_GREEN, CARD_SKIP),
         (COLOR_GREEN, CARD_REVERSE),
         (COLOR_GREEN, CARD_REVERSE),
         (COLOR_GREEN, CARD_DRAWTWO),
         (COLOR_GREEN, CARD_DRAWTWO),
         (COLOR_BLUE, CARD_0),
         (COLOR_BLUE, CARD_1),
         (COLOR_BLUE, CARD_1),
         (COLOR_BLUE, CARD_2),
         (COLOR_BLUE, CARD_2),
         (COLOR_BLUE, CARD_3),
         (COLOR_BLUE, CARD_3),
         (COLOR_BLUE, CARD_4),
         (COLOR_BLUE, CARD_4),
         (COLOR_BLUE, CARD_5),
         (COLOR_BLUE, CARD_5),
         (COLOR_BLUE, CARD_6),
         (COLOR_BLUE, CARD_6),
         (COLOR_BLUE, CARD_7),
         (COLOR_BLUE, CARD_7),
         (COLOR_BLUE, CARD_8),
         (COLOR_BLUE, CARD_8),
         (COLOR_BLUE, CARD_9),
         (COLOR_BLUE, CARD_9),
         (COLOR_BLUE, CARD_SKIP),
         (COLOR_BLUE, CARD_SKIP),
         (COLOR_BLUE, CARD_REVERSE),
         (COLOR_BLUE, CARD_REVERSE),
         (COLOR_BLUE, CARD_DRAWTWO),
         (COLOR_BLUE, CARD_DRAWTWO),
         (COLOR_WILD, CARD_WILD),
         (COLOR_WILD, CARD_WILD),
         (COLOR_WILD, CARD_WILD),
         (COLOR_WILD, CARD_WILD),
         (COLOR_WILD, CARD_DRAWFOUR),
         (COLOR_WILD, CARD_DRAWFOUR),
         (COLOR_WILD, CARD_DRAWFOUR),
         (COLOR_WILD, CARD_DRAWFOUR),
         (COLOR_WILD, CARD_DRAWEIGHT)]

CARD_EMOJIS = {(COLOR_RED, CARD_0): "<:red0:642807175865040925>",
               (COLOR_RED, CARD_1): "<:red1:642807175378632745>",
               (COLOR_RED, CARD_2): "<:red2:642807176070561852>",
               (COLOR_RED, CARD_3): "<:red3:642807175911047179>",
               (COLOR_RED, CARD_4): "<:red4:642807175533559811>",
               (COLOR_RED, CARD_5): "<:red5:642807175906852874>",
               (COLOR_RED, CARD_6): "<:red6:642807176045395979>",
               (COLOR_RED, CARD_7): "<:red7:642807175734886413>",
               (COLOR_RED, CARD_8): "<:red8:642807176041070592>",
               (COLOR_RED, CARD_9): "<:red9:642807176158773258>",
               (COLOR_RED, CARD_SKIP): "<:redskip:642806932528169002>",
               (COLOR_RED, CARD_REVERSE): "<:redreverse:642806932285030401>",
               (COLOR_RED, CARD_DRAWTWO): "<:reddraw2:642806932591083530>",
               (COLOR_RED, CARD_WILD): "<:redwild:643174385234083842>",
               (COLOR_RED, CARD_DRAWFOUR): "<:redwilddraw4:643482873940148264>",
               (COLOR_RED, CARD_DRAWEIGHT): "<:redwilddraw8:654772088258822175>",
               (COLOR_RED, CARD_SHUFFLEHANDS): "<:redshufflehands:643995233645887499>",
               (COLOR_YELLOW, CARD_0): "<:yellow0:642807176062304256>",
               (COLOR_YELLOW, CARD_1): "<:yellow1:642807175584153600>",
               (COLOR_YELLOW, CARD_2): "<:yellow2:642807175932018709>",
               (COLOR_YELLOW, CARD_3): "<:yellow3:642807176188133386>",
               (COLOR_YELLOW, CARD_4): "<:yellow4:642807175902658575>",
               (COLOR_YELLOW, CARD_5): "<:yellow5:642807176410431568>",
               (COLOR_YELLOW, CARD_6): "<:yellow6:642807176540323840>",
               (COLOR_YELLOW, CARD_7): "<:yellow7:642807176120893451>",
               (COLOR_YELLOW, CARD_8): "<:yellow8:642807176330608641>",
               (COLOR_YELLOW, CARD_9): "<:yellow9:642807176485928971>",
               (COLOR_YELLOW, CARD_SKIP): "<:yellowskip:642806933367291913>",
               (COLOR_YELLOW, CARD_REVERSE): "<:yellowreverse:642806933136605184>",
               (COLOR_YELLOW, CARD_DRAWTWO): "<:yellowdraw2:642806933358903326>",
               (COLOR_YELLOW, CARD_WILD): "<:yellowwild:643174385607376946>",
               (COLOR_YELLOW, CARD_DRAWFOUR): "<:yellowwilddraw4:643482874041073712>",
               (COLOR_YELLOW, CARD_DRAWEIGHT): "<:yellowwilddraw8:654772088439177217>",
               (COLOR_YELLOW, CARD_SHUFFLEHANDS): "<:yellowshufflehands:643992482883043348>",
               (COLOR_GREEN, CARD_0): "<:green0:642807173658837043>",
               (COLOR_GREEN, CARD_1): "<:green1:642807173881135151>",
               (COLOR_GREEN, CARD_2): "<:green2:642807173927272492>",
               (COLOR_GREEN, CARD_3): "<:green3:642807174476726312>",
               (COLOR_GREEN, CARD_4): "<:green4:642807174409748510>",
               (COLOR_GREEN, CARD_5): "<:green5:642807174514343946>",
               (COLOR_GREEN, CARD_6): "<:green6:642807174610944029>",
               (COLOR_GREEN, CARD_7): "<:green7:642807174422200340>",
               (COLOR_GREEN, CARD_8): "<:green8:642807174602686464>",
               (COLOR_GREEN, CARD_9): "<:green9:642807176171094035>",
               (COLOR_GREEN, CARD_SKIP): "<:greenskip:642806932486225920>",
               (COLOR_GREEN, CARD_REVERSE): "<:greenreverse:642806932310065182>",
               (COLOR_GREEN, CARD_DRAWTWO): "<:greendraw2:642806932016594955>",
               (COLOR_GREEN, CARD_WILD): "<:greenwild:643174385414438924>",
               (COLOR_GREEN, CARD_DRAWFOUR): "<:greenwilddraw4:643482874007257112>",
               (COLOR_GREEN, CARD_DRAWEIGHT): "<:greenwilddraw8:654772088078598155>",
               (COLOR_GREEN, CARD_SHUFFLEHANDS): "<:greenshufflehands:643992482442510337>",
               (COLOR_BLUE, CARD_0): "<:blue0:642807172765450280>",
               (COLOR_BLUE, CARD_1): "<:blue1:642807172513660977>",
               (COLOR_BLUE, CARD_2): "<:blue2:642807174317342754>",
               (COLOR_BLUE, CARD_3): "<:blue3:642807172920770561>",
               (COLOR_BLUE, CARD_4): "<:blue4:642807172815650858>",
               (COLOR_BLUE, CARD_5): "<:blue5:642807173176492032>",
               (COLOR_BLUE, CARD_6): "<:blue6:642807173503647745>",
               (COLOR_BLUE, CARD_7): "<:blue7:642807173570887681>",
               (COLOR_BLUE, CARD_8): "<:blue8:642807173599985664>",
               (COLOR_BLUE, CARD_9): "<:blue9:642807173574819860>",
               (COLOR_BLUE, CARD_SKIP): "<:blueskip:642806932045955073>",
               (COLOR_BLUE, CARD_REVERSE): "<:bluereverse:642806931647627266>",
               (COLOR_BLUE, CARD_DRAWTWO): "<:bluedraw2:642806931332792339>",
               (COLOR_BLUE, CARD_WILD): "<:bluewild:643174385213112349>",
               (COLOR_BLUE, CARD_DRAWFOUR): "<:bluewilddraw4:643482873717850128>",
               (COLOR_BLUE, CARD_DRAWEIGHT): "<:bluewilddraw8:654772088288313394>",
               (COLOR_BLUE, CARD_SHUFFLEHANDS): "<:blueshufflehands:643992482610282518>",
               (COLOR_WILD, CARD_WILD): "<:wild:642806933383806976>",
               (COLOR_WILD, CARD_DRAWFOUR): "<:wilddraw4:642806933065039903>",
               (COLOR_WILD, CARD_DRAWEIGHT): "<:wilddraw8:654772088451891220>",
               (COLOR_WILD, CARD_SHUFFLEHANDS): "<:shufflehands:642803897961938987>"}

CARD_STRINGS = {(color, card): COLOR_STRINGS[color] + " " + CARD_NONWILD_STRINGS[card]
                for (color, card) in itertools.product(COLOR_STRINGS.keys(), CARD_NONWILD_STRINGS.keys())}

CARD_STRINGS.update({(COLOR_WILD, CARD_WILD): "wild",
                     (COLOR_WILD, CARD_DRAWFOUR): "wild +4",
                     (COLOR_WILD, CARD_DRAWEIGHT): "wild +8",
                     (COLOR_WILD, CARD_SHUFFLEHANDS): "shuffle hands"})

CARD_STRINGS_REVERSED = {v: k for k, v in CARD_STRINGS.items()}
