import pygame
from screeninfo import get_monitors


class Settings:
    def __init__(self):
        """
        Settings of the maze
        """
        # get screen
        self.screen = pygame.display.get_surface()

        # activate shader
        self.SHADERON = True

        # set size of screen
        self.WIDTH, self.HEIGHT = get_monitors()[0].width, get_monitors()[0].height

        # set size of maze for each level
        self.NUMLEVELS = 3
        self.MAZEWIDTHS, self.MAZEHEIGHTS = [0] * self.NUMLEVELS, [0] * self.NUMLEVELS
        for i in range(self.NUMLEVELS):
            self.MAZEWIDTHS[i], self.MAZEHEIGHTS[i] = (i+1) * 3200, (i+1) * 2000

        self.CURRENTLEVEL = 0

        # set the resolution for the screen and the maze
        self.RESOLUTION = self.WIDTH, self.HEIGHT
        self.MAZERESOLUTION = self.MAZEWIDTHS[self.CURRENTLEVEL], self.MAZEHEIGHTS[self.CURRENTLEVEL]

        # set the tilesize in the maze (larger ones means smaller maze)
        self.TILESIZE = 120

        # randomness of the maze
        self.TURNFACTOR = 5

        # difficulty of the maze 0=easy 1=medium 2=hard
        self.DIFFICULTY = 0

        # proportion of enemies for a 1000*1000 maze
        self.WOLFPROPORTION = 0.125
        self.SPIDERPROPORTION = 0.375
        self.SLIMEPROPORTION = 0.5
        self.RABBITPROPORTION = 0.2

        # initialize font
        self.FONT = pygame.font.Font('../font/Pixeltype.ttf', self.HEIGHT // 10)
        self.SMALLFONT = pygame.font.Font('../font/Pixeltype.ttf', self.HEIGHT // 17)
        self.BIGCREEPYFONT = pygame.font.Font('../font/HelpMe.ttf', self.HEIGHT // 10)
        self.SMALLCREEPYFONT = pygame.font.Font('../font/HelpMe.ttf', self.HEIGHT // 13)

        # controls
        self.K_UP = pygame.K_z
        self.K_DOWN = pygame.K_s
        self.K_LEFT = pygame.K_q
        self.K_RIGHT = pygame.K_d
        self.K_MAP = pygame.K_m

        # colors
        self.MENUBACKGROUNDCOLOR = pygame.Color(46, 60, 87)
        self.TEXTCOLOR = 'darkgray'
        self.DARKTEXTCOLOR = 'goldenrod3'
        self.HOVERINGCOLOR = 'gray'
        self.DARKHOVERINGCOLOR = 'goldenrod2'
        self.SLIDEREXTCOLOR = 'gray28'
        self.SLIDERINTCOLOR = 'black'
        self.FAILCOLOR = 'darkred'
        self.SUCCESSCOLOR = 'gold'

        self.WALLCOLOR = 'gold4' if self.SHADERON else pygame.Color(163, 128, 83)  # color of the wall on the map
        self.PATHCOLOR = 'goldenrod4' if self.SHADERON else 'burlywood'  # color of the path on the map
        self.PLAYERCOLOR = 'blue'  # color of the player on the map
        self.ENDCOLOR = 'gold'  # color of the end on the map
        self.CHESTCOLOR = 'chocolate4' if self.SHADERON else pygame.Color(117, 79, 46)  # color of chests on the map

        # lighting
        self.LIGHTCOLOR = (255, 255, 200)  # color of the light
        self.LIGHTRADIUS = 250 * self.TILESIZE//60  # size of the light
        self.LIGHTINTENSITY = 10  # intensity of the light

        # toggle heart beat effect in shaders
        self.SHOWHEARTBEATEFFECT = True

        # shaders
        self.GAMMA = 12  # default gamma value

        # set FPS
        self.GAMEFPS = 60

        # initialize music and sound effects
        self.MUSICCHANNEL = pygame.mixer.Channel(0)
        self.MUSIC = pygame.mixer.Sound('../sound/Horror.mp3')
        self.SOUNDEFFECTCHANNEL = pygame.mixer.Channel(1)
        self.FOOTSTEPSOUNDEFFECTS = list(pygame.mixer.Sound(f'../sound/effects/walking/footstep{i}.mp3') for i in range(6))

        self.VOLUME = 1.00  # default volume

        # type of the player, either boy or girl
        self.TYPE = 'girl'

        # translations of the texts
        self.LANGUAGE = 'FR'
        self.TEXTS = {
            'FR': {'The Maze Of Shadows': 'Le Labyrinthe Des Ombres',
                   'START': 'COMMENCER',
                   'PARAMETERS': 'PARAMETRES',
                   'RESTART': 'RECOMMENCER',
                   'RETRY': 'REESAYER',
                   'QUIT GAME': 'QUITTER LE JEU',
                   'QUIT': 'QUITTER',
                   'DIFFICULTY': 'DIFFICULTEE',
                   'EASY': 'FACILE',
                   'MEDIUM': 'MOYEN',
                   'HARD': 'DIFFICILE',
                   'HEART BEAT EFFECT': 'EFFET BATTEMENTS DE COEUR',
                   'GAMMA': 'GAMMA',
                   'VOLUME': 'VOLUME',
                   'FPS': 'FPS',
                   'CONTROLS': 'CONTROLES',
                   'UP': 'HAUT',
                   'DOWN': 'BAS',
                   'LEFT': 'GAUCHE',
                   'RIGHT': 'DROITE',
                   'MAP': 'CARTE',
                   'Waiting for input...': 'Appuyez sur une touche...',
                   'CONTINUE': 'CONTINUER',
                   'MAIN MENU': 'MENU PRINCIPAL',
                   'BOY': 'GARCON',
                   'GIRL': 'FILLE',
                   'CANCEL': 'ANNULER',
                   'YOU HAVE FOUND': 'VOUS AVEZ TROUVE',
                   'YOU HAVE USED': 'VOUS AVEZ UTILISE',
                   'YOU HAVE REFOUND': 'VOUS AVEZ RETROUVE',
                   'YOUR BROTHER': 'VOTRE FRERE',
                   'YOUR SISTER': 'VOTRE SOEUR',
                   'YOU DIED': 'VOUS ETES MORT',
                   'LIVES': 'VIES',
                   'A PIECE OF MAP': 'UN BOUT DE CARTE',
                   'A FREEZE ITEM': 'UN GEL',
                   'AN EXTRA LIFE': 'UNE VIE EN PLUS',
                   'HELP': 'AIDE',
                   'ENEMIES': 'ENNEMIS',
                   'WOLF DESCRIPTION': "LOUP AVEUGLE : COURT VITE MAIS NE VOUS VOIT PAS SI",
                   'WOLF DESCRIPTION 2': "VOUS NE BOUGEZ PAS",
                   'SPIDER DESCRIPTION': "ARAIGNEE-SOURIS : VITESSE NORMALE MAIS PEUT PLACER",
                   'SPIDER DESCRIPTION 2': "DES TOILES D'ARAIGNEE SUR VOTRE CHEMIN",
                   'SLIME DESCRIPTION': "SLIME : EST LENT ET BETE, IL NE VOUS POURSUIVERA PAS",
                   'SLIME DESCRIPTION 2': "MAIS IL Y EN A BEAUCOUP",
                   'RABBIT DESCRIPTION': "LAPIN : IL A L'AIR MIGNON N'EST-CE PAS ?",
                   'ITEM USE DESCRIPTION': "UTILISEZ LE CLIC-GAUCHE POUR UTILISER",
                   'ITEM USE DESCRIPTION 2': "L'OBJET SELECTIONNE",
                   'ITEM CHANGE DESCRIPTION': "UTILISEZ LA MOLETTE DE LA SOURIS",
                   'ITEM CHANGE DESCRIPTION 2': "POUR CHANGER D'OBJET",
                   'ITEM DISPLAY DESCRIPTION': "VOUS POUVEZ VOIR L'OBJET SELECTIONNE ICI",
                   'ITEMS': "OBJETS",
                   'MAP DESCRIPTION': "CARTE : UN BOUT DE CARTE, IL VOUS PERMET DE REVELER",
                   'MAP DESCRIPTION 2': "UNE PARTIE DE LA CARTE",
                   'FREEZE DESCRIPTION': "GEL : CE GEL VOUS PERMET DE RALENTIR L'ENNEMI",
                   'FREEZE DESCRIPTION 2': "QUE VOUS TOUCHEZ PENDENT 5s",
                   'HEAL DESCRIPTION': "SOIN : CE KIT DE SOIN VOUS PERMET D'AVOIR",
                   'HEAL DESCRIPTION 2': "UNE VIE EN PLUS"},

            'EN': {'The Maze Of Shadows': 'The Maze Of Shadows',
                   'START': 'START',
                   'PARAMETERS': 'PARAMETERS',
                   'RESTART': 'RESTART',
                   'RETRY': 'RETRY',
                   'QUIT GAME': 'QUIT GAME',
                   'QUIT': 'QUIT',
                   'DIFFICULTY': 'DIFFICULTY',
                   'EASY': 'EASY',
                   'MEDIUM': 'MEDIUM',
                   'HARD': 'HARD',
                   'HEART BEAT EFFECT': 'HEART BEAT EFFECT',
                   'GAMMA': 'GAMMA',
                   'VOLUME': 'VOLUME',
                   'FPS': 'FPS',
                   'CONTROLS': 'CONTROLS',
                   'UP': 'UP',
                   'DOWN': 'DOWN',
                   'LEFT': 'LEFT',
                   'RIGHT': 'RIGHT',
                   'MAP': 'MAP',
                   'Waiting for input...': 'Waiting for input...',
                   'CONTINUE': 'CONTINUE',
                   'MAIN MENU': 'MAIN MENU',
                   'BOY': 'BOY',
                   'GIRL': 'GIRL',
                   'CANCEL': 'CANCEL',
                   'YOU HAVE FOUND': 'YOU FOUND',
                   'YOU HAVE USED': 'YOU USED',
                   'YOU HAVE REFOUND': 'YOU FOUND',
                   'YOUR BROTHER': 'YOUR BROTHER',
                   'YOUR SISTER': 'YOUR SISTER',
                   'YOU DIED': 'YOU DIED',
                   'LIVES': 'LIVES',
                   'A PIECE OF MAP': 'A PIECE OF MAP',
                   'A FREEZE ITEM': 'A FREEZE ITEM',
                   'AN EXTRA LIFE': 'AN EXTRA LIFE',
                   'HELP': 'HELP',
                   'ENEMIES': 'ENEMIES',
                   'WOLF DESCRIPTION': "BLIND WOLF : RUNS FAST BUT DOESN'T SEE YOU",
                   'WOLF DESCRIPTION 2': "IF YOU DON'T MOVE",
                   'SPIDER DESCRIPTION': "SPIDER-MOUSE : NORMAL SPEED BUT CAN PLACE",
                   'SPIDER DESCRIPTION 2': "COBWEBS IN YOUR WAY",
                   'SLIME DESCRIPTION': "SLIME : IS SLOW AND DUMB, WON'T FOLLOW YOU",
                   'SLIME DESCRIPTION 2': "BUT THERE'S A LOT OF THEM",
                   'RABBIT DESCRIPTION': "RABBIT : IT LOOKS CUTE DOESN'T IT ?",
                   'ITEM USE DESCRIPTION': "USE LEFT-CLICK TO USE",
                   'ITEM USE DESCRIPTION 2': "CURRENTLY SELECTED ITEM",
                   'ITEM CHANGE DESCRIPTION': "USE THE MOUSE WHEEL",
                   'ITEM CHANGE DESCRIPTION 2': "TO CHANGE SELECTED OBJECT",
                   'ITEM DISPLAY DESCRIPTION': "YOU CAN SEE THE CURRENTLY SELECTED ITEM HERE",
                   'ITEMS': "ITEMS",
                   'MAP DESCRIPTION': "MAP : A PIECE OF MAP THAT CAN REVEAL",
                   'MAP DESCRIPTION 2': "A PORTION OF THE MAP",
                   'FREEZE DESCRIPTION': "FREEZE : THIS FREEZE CAN SLOW DOWN",
                   'FREEZE DESCRIPTION 2': "THE ENEMY YOU TOUCH FOR 5s",
                   'HEAL DESCRIPTION': "HEAL : THIS MEDKIT ALLOWS YOU TO GET",
                   'HEAL DESCRIPTION 2': "ONE EXTRA LIFE"},

            'DE': {'The Maze Of Shadows': 'Das Schattenlabyrinth',
                   'START': 'BEGINN',
                   'PARAMETERS': 'EINSTELLUNGEN',
                   'RESTART': 'NEU ANFANGEN',
                   'RETRY': 'WIEDERVERSUCHEN',
                   'QUIT GAME': 'SPIEL VERLASSEN',
                   'QUIT': 'VERLASSEN',
                   'DIFFICULTY': 'SCHWIERIGKEITENGRAD',
                   'EASY': 'EINFACH',
                   'MEDIUM': 'MITTEL',
                   'HARD': 'SCHWER',
                   'HEART BEAT EFFECT': 'HERZSCHLAG-EFFEKT',
                   'GAMMA': 'GAMMA',
                   'VOLUME': 'LAUTSTARKE',
                   'FPS': 'FPS',
                   'CONTROLS': 'KONTROLLEN',
                   'UP': 'OBEN',
                   'DOWN': 'UNTEN',
                   'LEFT': 'LINKS',
                   'RIGHT': 'RECHTS',
                   'MAP': 'KARTE',
                   'Waiting for input...': 'Warten auf Eingabe...',
                   'CONTINUE': 'FORTSETZEN',
                   'MAIN MENU': 'HAUPTMENU',
                   'BOY': 'JUNGE',
                   'GIRL': 'MADCHEN',
                   'CANCEL': 'STORNIEREN',
                   'YOU HAVE FOUND': 'SIE HABEN GEFUNDEN',
                   'YOU HAVE USED': 'SIE HABEN BENUTZT',
                   'YOU HAVE REFOUND': 'SIE HABEN',
                   'YOUR BROTHER': 'IHREN BRUDER WIEDERGEFUNDEN',
                   'YOUR SISTER': 'IHRE SCHWESTER WIEDERGEFUNDEN',
                   'YOU DIED': 'SIE SIND GETOTET',
                   'LIVES': 'LEBEN',
                   'A PIECE OF MAP': 'EIN KARTESTUCK',
                   'A FREEZE ITEM': 'EIN SPERRVERMERK',
                   'AN EXTRA LIFE': 'EIN EXTRA-LEBEN',
                   'HELP': 'HILFE',
                   'ENEMIES': 'FEINDE',
                   'WOLF DESCRIPTION': "BLINDE WOLF : LAUFT SCHNELL ABER SIEHT NICHT SIE, WENN",
                   'WOLF DESCRIPTION 2': "SIE NICHT BEWEGEN",
                   'SPIDER DESCRIPTION': "SPINNE-MAUS : NORMALE GESCHWINDICHKEIT ABER KANN",
                   'SPIDER DESCRIPTION 2': "SPINNENNETZ AUF IHREN WEG STELLEN",
                   'SLIME DESCRIPTION': "SLIME : IST LANGSAM UND BLOD, ER WIRD NICHT IHNEN VERFOLGEN",
                   'SLIME DESCRIPTION 2': "ABER ES GIBT VIELE",
                   'RABBIT DESCRIPTION': "KANINCHEN : ES SIEHT NIEDLICH AUS, NE ?",
                   'ITEM USE DESCRIPTION': "BENUTZEN SIE DEN RECHTEN MAUSKLICK",
                   'ITEM USE DESCRIPTION 2': "UM DAS GEWAHLT OBJEKT ZU BENUTZEN",
                   'ITEM CHANGE DESCRIPTION': "BENUTZEN SIE DIE MAUSRADCHEN",
                   'ITEM CHANGE DESCRIPTION 2': "UM OBJEKTE ZU ANDERN",
                   'ITEM DISPLAY DESCRIPTION': "SIE KONNEN DAS GEWAHLT OBJEKT DA",
                   'ITEMS': "OBJEKTE",
                   'MAP DESCRIPTION': "KARTE : EIN KARTESTUCK, ES ERMOGLICHT IHNEN",
                   'MAP DESCRIPTION 2': "EIN KARTETEIL ZU ZEIGEN",
                   'FREEZE DESCRIPTION': "GEL : MIT DIESEM GEL KONNEN SIE DIE FEINDE",
                   'FREEZE DESCRIPTION 2': "DIE SIE BERUHREN, WAHREND 5 SEKUNDE VERLANGSAMEN",
                   'HEAL DESCRIPTION': "HILFE : DIESES HILFSET ERMOGLICHT IHNEN",
                   'HEAL DESCRIPTION 2': "EIN EXTRA-LEBEN ZU HABEN"}
        }

        # keep track of distance to the closest enemy
        self.dstToClosestEnemy = 1000000
