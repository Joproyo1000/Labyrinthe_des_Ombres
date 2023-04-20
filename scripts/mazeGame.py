import time

from sys import exit

from mazeLevel import Maze, Corridor
from settings import Settings
from shaders import Shader
from support import *


class MazeGame:
    def __init__(self):

        # initialize settings
        self.settings = Settings()

        # initialize pygame and mixer
        pygame.init()
        pygame.mixer.init()

        # start music playback
        self.settings.MUSICCHANNEL.play(self.settings.MUSIC, loops=-1)
        self.settings.MUSICCHANNEL.set_volume(self.settings.VOLUME)
        self.settings.SOUNDEFFECTCHANNEL.set_volume(self.settings.VOLUME / 8)

        # changes screen mode to adapt if shaders are activated or not
        if self.settings.SHADERON:
            self.screen = pygame.display.set_mode(self.settings.RESOLUTION, pygame.OPENGL | pygame.DOUBLEBUF)
        else:
            self.screen = pygame.display.set_mode(self.settings.RESOLUTION)

        self.menuBackground = pygame.image.load('../graphics/menu_background.png').convert()
        self.menuBackground = pygame.transform.scale(self.menuBackground, (self.screen.get_size()))
        self.endingBackground = pygame.image.load('../graphics/ending_background.png').convert()
        self.endingBackground = pygame.transform.scale(self.endingBackground, (self.screen.get_size()))
        self.background = self.menuBackground

        # initialize maze
        self.maze = Maze(self.settings)

        # initialize the render menus
        self.buttons = []
        if self.settings.SHADERON:
            self.shader = Shader(self.screen.get_size(), self.settings)

        pygame.display.set_caption(self.settings.TEXTS[self.settings.LANGUAGE]['The Maze Of Shadows'])
        self.clock = pygame.time.Clock()

    def main_menu(self):
        """
        Main menu, runs at start
        """
        self.buttons = [Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 2.3), self.settings.TEXTS[self.settings.LANGUAGE]['START'],
                               self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.87), self.settings.TEXTS[self.settings.LANGUAGE]['PARAMETERS'],
                               self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.57), self.settings.TEXTS[self.settings.LANGUAGE]['HELP'],
                               self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.3), self.settings.TEXTS[self.settings.LANGUAGE]['QUIT GAME'],
                               self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR)]

        self.drawScreen()

        titleText = pygame.font.Font('../font/Pixeltype.ttf', self.settings.HEIGHT // 8).render(self.settings.TEXTS[self.settings.LANGUAGE]['The Maze Of Shadows'].upper(), True, self.settings.TEXTCOLOR)
        titleTextRect = titleText.get_rect(center=(self.settings.WIDTH/2, self.settings.HEIGHT/3.5))
        self.screen.blit(titleText, titleTextRect)

        fadeTransitionEnd(self.screen, self.shader if self.settings.SHADERON else None)

        while True:
            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if button.checkForInput():
                            if i == 0:
                                if self.chooseType():
                                    fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                    self.maze.reset()
                                    self.corridor('down', 10, (56, 27, 24), self.game)
                            if i == 1:
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                self.settings_menu(self.main_menu)
                            if i == 2:
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                self.help_menu(self.main_menu)
                            if i == 3:
                                pygame.quit()
                                exit()

            self.drawScreen()
            self.screen.blit(titleText, titleTextRect)

            if not self.settings.SHADERON:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def settings_menu(self, start: classmethod, dotransition: bool=True):
        """
        Settings menu to change game settings
        """
        sliderSize = self.settings.HEIGHT//230

        self.buttons = [Slider((self.settings.WIDTH // 2, self.settings.HEIGHT // 4), self.settings.TEXTS[self.settings.LANGUAGE]['DIFFICULTY'],
                               (0, 2), self.settings.FONT, self.settings.TEXTCOLOR, self.settings.SLIDEREXTCOLOR, self.settings.SLIDERINTCOLOR, self.settings.HOVERINGCOLOR, self.settings.TEXTCOLOR,
                               sliderSize, 0, custom={0: self.settings.TEXTS[self.settings.LANGUAGE]['EASY'], 1: self.settings.TEXTS[self.settings.LANGUAGE]['MEDIUM'], 2: self.settings.TEXTS[self.settings.LANGUAGE]['HARD']}),

                        CheckButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 3.0), self.settings.TEXTS[self.settings.LANGUAGE]['HEART BEAT EFFECT'],
                                    self.settings.SHOWHEARTBEATEFFECT, self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),

                        Slider((self.settings.WIDTH // 2, self.settings.HEIGHT // 2.2), self.settings.TEXTS[self.settings.LANGUAGE]['GAMMA'],
                               (5, 30), self.settings.FONT, self.settings.TEXTCOLOR, self.settings.SLIDEREXTCOLOR, self.settings.SLIDERINTCOLOR, self.settings.HOVERINGCOLOR, self.settings.TEXTCOLOR,
                               sliderSize, self.settings.GAMMA),

                        Slider((self.settings.WIDTH // 2, self.settings.HEIGHT // 1.7), self.settings.TEXTS[self.settings.LANGUAGE]['VOLUME'],
                               (0, 100), self.settings.FONT, self.settings.TEXTCOLOR, self.settings.SLIDEREXTCOLOR, self.settings.SLIDERINTCOLOR, self.settings.HOVERINGCOLOR, self.settings.TEXTCOLOR,
                               sliderSize, self.settings.VOLUME*100),

                        Slider((self.settings.WIDTH // 2, self.settings.HEIGHT // 1.4), self.settings.TEXTS[self.settings.LANGUAGE]['FPS'],
                               (30, 120), self.settings.FONT, self.settings.TEXTCOLOR, self.settings.SLIDEREXTCOLOR, self.settings.SLIDERINTCOLOR, self.settings.HOVERINGCOLOR, self.settings.TEXTCOLOR,
                               sliderSize, 60),

                        Button(pygame.transform.scale(pygame.image.load('../graphics/flags/FR.png').convert_alpha(), (100, 100)), (self.settings.WIDTH // 6, self.settings.HEIGHT // 1.3),
                               '', self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        Button(pygame.transform.scale(pygame.image.load('../graphics/flags/EN.png').convert_alpha(), (100, 100)), (self.settings.WIDTH // 4.42, self.settings.HEIGHT // 1.3),
                               '', self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        Button(pygame.transform.scale(pygame.image.load('../graphics/flags/DE.png').convert_alpha(), (100, 100)), (self.settings.WIDTH // 3.5, self.settings.HEIGHT // 1.3),
                               '', self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),

                        Button(None, (self.settings.WIDTH // 1.3, self.settings.HEIGHT // 1.25), self.settings.TEXTS[self.settings.LANGUAGE]['CONTROLS'],
                               self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),

                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.25), self.settings.TEXTS[self.settings.LANGUAGE]['QUIT'],
                               self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR)]

        self.drawScreen(getInput=False)

        if dotransition:
            fadeTransitionEnd(self.screen, self.shader if self.settings.SHADERON else None)

        while True:
            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if button.checkForInput():
                            # language change
                            if i == 5:
                                self.settings.LANGUAGE = 'FR'
                                self.settings_menu(start, dotransition=False)
                            if i == 6:
                                self.settings.LANGUAGE = 'EN'
                                self.settings_menu(start, dotransition=False)
                            if i == 7:
                                self.settings.LANGUAGE = 'DE'
                                self.settings_menu(start, dotransition=False)

                            # quit settings
                            if i == len(self.buttons)-1:
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                self.settings.DIFFICULTY = int(self.buttons[0].value)
                                self.maze.FPS = self.buttons[4].value
                                start()
                            # go to controls
                            if i == len(self.buttons)-2:
                                self.settings.DIFFICULTY = int(self.buttons[0].value)
                                self.maze.FPS = self.buttons[4].value
                                self.controls_menu(start)

            self.settings.SHOWHEARTBEATEFFECT = self.buttons[1].value
            self.settings.GAMMA = self.buttons[2].value
            self.settings.VOLUME = self.buttons[3].value / 100
            self.settings.MUSICCHANNEL.set_volume(self.settings.VOLUME)
            self.settings.SOUNDEFFECTCHANNEL.set_volume(self.settings.VOLUME / 8)

            self.drawScreen()

            if not self.settings.SHADERON:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def controls_menu(self, start: classmethod):
        """
        Settings menu to change game controls
        """

        self.buttons = [InputButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 4.5), self.settings.TEXTS[self.settings.LANGUAGE]['UP'] + ': ',
                                    self.settings.K_UP, self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        InputButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 3), self.settings.TEXTS[self.settings.LANGUAGE]['DOWN'] + ': ',
                                    self.settings.K_DOWN, self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        InputButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 2.2), self.settings.TEXTS[self.settings.LANGUAGE]['LEFT'] + ': ',
                                    self.settings.K_LEFT, self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        InputButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.7), self.settings.TEXTS[self.settings.LANGUAGE]['RIGHT'] + ': ',
                                    self.settings.K_RIGHT, self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        InputButton(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.4), self.settings.TEXTS[self.settings.LANGUAGE]['MAP'] + ': ',
                                    self.settings.K_MAP, self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        Button(None, (self.settings.WIDTH // 4, self.settings.HEIGHT // 1.25), self.settings.TEXTS[self.settings.LANGUAGE]['PARAMETERS'],
                               self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.25), self.settings.TEXTS[self.settings.LANGUAGE]['QUIT'],
                               self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR)]

        self.drawScreen()

        while True:
            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        # if an input button is pressed, show a 'waiting for input' screen
                        if isinstance(button, InputButton):
                            if button.isHovered():
                                self.screen.fill(self.settings.MENUBACKGROUNDCOLOR)
                                waitText = self.settings.FONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['Waiting for input...'], True, self.settings.HOVERINGCOLOR)
                                self.screen.blit(waitText, waitText.get_rect(center=(self.settings.WIDTH/2, self.settings.HEIGHT/2)))
                                button.exitInputButton.update(self.screen)
                                if self.settings.SHADERON:
                                    self.shader.render(self.screen)
                                pygame.display.update()
                        # check every button for input
                        if button.checkForInput():
                            if i == len(self.buttons) - 1:
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                start()
                            if i == len(self.buttons) - 2:
                                self.settings_menu(start, dotransition=False)


            self.updateKeys()
            self.drawScreen()

            if not self.settings.SHADERON:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def help_menu(self, start: classmethod):
        """
        Help menu gives information about enemies, controls and items
        """

        self.buttons = [Button(None, (self.settings.WIDTH // 3.9, self.settings.HEIGHT // 1.3), '<---',
                                      self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        Button(None, (self.settings.WIDTH // 1.3, self.settings.HEIGHT // 1.3), '--->',
                                      self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.25), self.settings.TEXTS[self.settings.LANGUAGE]['QUIT'],
                                      self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR)]

        currentPage = 1
        pages = [
            # page 1
            [pygame.transform.scale_by(pygame.image.load('../graphics/mouseHelp.png').convert_alpha(), 5),
             pygame.transform.scale_by(pygame.image.load('../graphics/objectHelp.png').convert_alpha(), 5),
             self.settings.FONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['CONTROLS'], True, 'gray'),

             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['ITEM DISPLAY DESCRIPTION'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['ITEM CHANGE DESCRIPTION'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['ITEM CHANGE DESCRIPTION 2'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['ITEM USE DESCRIPTION'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['ITEM USE DESCRIPTION 2'], True, 'gray')
             ],
            # page 2
            [pygame.transform.scale_by(pygame.image.load('../graphics/enemies/wolf/right_idle/blind_wolf_right_idle1.png').convert_alpha(), 2),
             pygame.transform.scale_by(pygame.image.load('../graphics/enemies/spider/right_idle/spider_mouse_right_idle1.png').convert_alpha(), 3),
             pygame.transform.scale_by(pygame.image.load('../graphics/enemies/slime/right_idle/slime_right_idle1.png').convert_alpha(), 3),
             pygame.transform.scale_by(pygame.image.load('../graphics/enemies/rabbit/right_idle/cute_bunny_right_idle1.png').convert_alpha(), 3),

             self.settings.FONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['ENEMIES'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['WOLF DESCRIPTION'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['WOLF DESCRIPTION 2'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['SPIDER DESCRIPTION'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['SPIDER DESCRIPTION 2'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['SLIME DESCRIPTION'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['SLIME DESCRIPTION 2'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['RABBIT DESCRIPTION'], True, 'gray')],
            # page 3
            [pygame.transform.scale_by(pygame.image.load('../graphics/special/objects/map.png').convert_alpha(), 3),
             pygame.transform.scale_by(pygame.image.load('../graphics/special/objects/freeze.png').convert_alpha(), 3),
             pygame.transform.scale_by(pygame.image.load('../graphics/special/objects/heal.png').convert_alpha(), 3),

             self.settings.FONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['ITEMS'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['MAP DESCRIPTION'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['MAP DESCRIPTION 2'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['FREEZE DESCRIPTION'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['FREEZE DESCRIPTION 2'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['HEAL DESCRIPTION'], True, 'gray'),
             self.settings.SMALLFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['HEAL DESCRIPTION 2'], True, 'gray')]
        ]

        pagesRect = [
            # page 1:
            [pages[0][0].get_rect(center=(self.settings.WIDTH // 1.8, self.settings.HEIGHT // 1.7)),  # mouse image
             pages[0][0].get_rect(topright=(self.settings.WIDTH // 1.3, self.settings.HEIGHT // 4)),  # item selection image

             pages[0][2].get_rect(center=(self.settings.WIDTH // 2, self.settings.HEIGHT // 5)),  # title

             pages[0][3].get_rect(topright=(self.settings.WIDTH // 1.5, self.settings.HEIGHT // 3.22)),  # item selection description

             pages[0][4].get_rect(topright=(self.settings.WIDTH // 1.7, self.settings.HEIGHT // 2.4)),  # item change description
             pages[0][5].get_rect(topright=(self.settings.WIDTH // 1.7, self.settings.HEIGHT // 2.18)),

             pages[0][6].get_rect(topright=(self.settings.WIDTH // 1.7, self.settings.HEIGHT // 1.92)),  # item use description
             pages[0][7].get_rect(topright=(self.settings.WIDTH // 1.7, self.settings.HEIGHT // 1.78))
             ],
            # page 2:
            [pages[1][0].get_rect(center=(self.settings.WIDTH // 4.8, self.settings.HEIGHT // 3.6)),  # wolf image
             pages[1][1].get_rect(center=(self.settings.WIDTH // 4.8, self.settings.HEIGHT // 2.7)),  # spider image
             pages[1][2].get_rect(center=(self.settings.WIDTH // 4.8, self.settings.HEIGHT // 2.07)),  # slime image
             pages[1][3].get_rect(center=(self.settings.WIDTH // 4.8, self.settings.HEIGHT // 1.6)),  # rabbit image
             # texts
             pages[1][4].get_rect(center=(self.settings.WIDTH // 2, self.settings.HEIGHT // 5)),  # title

             pages[1][5].get_rect(topleft=(self.settings.WIDTH // 3.83, self.settings.HEIGHT // 3.98)),  # wolf description
             pages[1][6].get_rect(topleft=(self.settings.WIDTH // 3.83, self.settings.HEIGHT // 3.41)),

             pages[1][7].get_rect(topleft=(self.settings.WIDTH // 3.83, self.settings.HEIGHT // 2.55)),  # spider description
             pages[1][8].get_rect(topleft=(self.settings.WIDTH // 3.83, self.settings.HEIGHT // 2.31)),

             pages[1][9].get_rect(topleft=(self.settings.WIDTH // 3.83, self.settings.HEIGHT // 1.95)),  # slime description
             pages[1][10].get_rect(topleft=(self.settings.WIDTH // 3.83, self.settings.HEIGHT // 1.82)),

             pages[1][11].get_rect(topleft=(self.settings.WIDTH // 3.83, self.settings.HEIGHT // 1.53))  # rabbit description
             ],
            # page 3
            [pages[2][0].get_rect(center=(self.settings.WIDTH // 4.2, self.settings.HEIGHT // 3.15)),  # map image
             pages[2][1].get_rect(center=(self.settings.WIDTH // 4.2, self.settings.HEIGHT // 2.2)),  # freeze image
             pages[2][2].get_rect(center=(self.settings.WIDTH // 4.2, self.settings.HEIGHT // 1.7)),  # heal image

             pages[2][3].get_rect(center=(self.settings.WIDTH // 2, self.settings.HEIGHT // 5)),  # title

             pages[2][4].get_rect(topleft=(self.settings.WIDTH // 3.6, self.settings.HEIGHT // 3.38)),  # map description
             pages[2][5].get_rect(topleft=(self.settings.WIDTH // 3.6, self.settings.HEIGHT // 2.9)),

             pages[2][6].get_rect(topleft=(self.settings.WIDTH // 3.6, self.settings.HEIGHT // 2.31)),  # freeze description
             pages[2][7].get_rect(topleft=(self.settings.WIDTH // 3.6, self.settings.HEIGHT // 2.1)),

             pages[2][8].get_rect(topleft=(self.settings.WIDTH // 3.6, self.settings.HEIGHT // 1.8)),  # heal description
             pages[2][9].get_rect(topleft=(self.settings.WIDTH // 3.6, self.settings.HEIGHT // 1.67))
             ]
        ]

        self.drawScreen()
        for image, rect in zip(pages[currentPage % len(pages)], pagesRect[currentPage % len(pages)]):
            self.screen.blit(image, rect)

        fadeTransitionEnd(self.screen, self.shader if self.settings.SHADERON else None)

        while True:
            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        # check every button for input
                        if button.checkForInput():
                            if i == 0:
                                currentPage += 1
                            if i == 1:
                                currentPage -= 1
                            if i == len(self.buttons) - 1:
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                start()

            self.drawScreen()

            for image, rect in zip(pages[currentPage % len(pages)], pagesRect[currentPage % len(pages)]):
                self.screen.blit(image, rect)

            if not self.settings.SHADERON:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def corridor(self, direction: str, length: int, lightColor: (int, int, int), end: classmethod):
        """
        :param direction:
        :param length:
        :param lightColor:
        """
        corridor = Corridor(direction, length, lightColor, self.settings)

        currentTime = time.time()

        while True:
            # calculate deltaTime to make the speed go at the same rate regardless of FPS
            deltaTime = time.time() - currentTime
            currentTime = time.time()

            # set background color
            self.screen.fill('black')

            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if corridor.check_end():
                    end()

            # run the level
            corridor.run(deltaTime)

            if not self.settings.SHADERON:
                pygame.display.update()

            # set FPS
            self.clock.tick(self.maze.FPS)

    def game(self, doTransition: bool=True):
        """
        Main game loop
        """
        if doTransition:
            self.maze.run(0)
            fadeTransitionEnd(self.screen, self.shader if self.settings.SHADERON else None)

        currentTime = time.time()

        while True:
            # calculate deltaTime to make the speed go at the same rate regardless of FPS
            deltaTime = time.time() - currentTime
            currentTime = time.time()

            # set background color
            self.screen.fill('black')

            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # inventory
                if event.type == pygame.MOUSEWHEEL:
                    self.maze.player.currentItemIndex = (self.maze.player.currentItemIndex + event.y) % len(self.maze.player.inventory)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.maze.playerUse()

                # menus
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[self.settings.K_MAP]:
                        self.map()
                    if key[pygame.K_ESCAPE]:
                        self.pause_menu()

                # if maze level isn't finished, update all enemies
                if self.maze.status != 'finished':
                    # get player pos
                    playerPos = self.maze.check_tile(self.maze.player.rect.centerx // self.settings.TILESIZE,
                                                     self.maze.player.rect.centery // self.settings.TILESIZE)
                    for i, enemyEvent in enumerate(self.maze.enemyEvents):
                        if event.type == enemyEvent and playerPos:
                            self.maze.enemyBehavior(i, playerPos)

            if self.maze.status == 'success':
                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                self.corridor('up', 10, (99, 99, 76), self.end_menu)
            elif self.maze.status == 'fail':
                self.end_menu()

            # run the level
            self.maze.run(deltaTime)

            if not self.settings.SHADERON:
                pygame.display.update()

            # set FPS
            self.clock.tick(self.maze.FPS)

    def map(self):
        """
        Map display
        """
        currentTime = time.time()

        mapSurf = pygame.transform.scale(pygame.image.load('../graphics/special/objects/bigMap.png').convert_alpha(),
                                              (self.screen.get_size()))
        self.maze.run(0, getInput=False)
        mapImg = self.maze.bake_map()
        mapSurf.blit(mapImg, mapImg.get_rect(center=(self.settings.WIDTH/2, self.settings.HEIGHT/2)))
        slideTransitionStart(self.screen, mapSurf, self.shader if self.settings.SHADERON else None)

        while True:
            # calculate deltaTime to make the speed go at the same rate regardless of the FPS
            deltaTime = time.time() - currentTime
            currentTime = time.time()

            # set background color
            self.screen.fill(pygame.Color(46, 60, 87))

            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_ESCAPE]:
                        self.maze.run(0, getInput=False)
                        slideTransitionEnd(self.screen, mapSurf, self.shader if self.settings.SHADERON else None)
                        self.game(doTransition=False)
                    if key[self.settings.K_MAP]:
                        self.maze.run(0, getInput=False)
                        slideTransitionEnd(self.screen, mapSurf, self.shader if self.settings.SHADERON else None)
                        self.game(doTransition=False)

            # run the level
            mazeScreen = self.maze.run(deltaTime, getInput=False)
            self.screen.blit(mazeScreen, mazeScreen.get_rect())
            self.screen.blit(mapSurf, (0, 0))

            if self.settings.SHADERON:
                self.shader.render(self.screen)
            else:
                pygame.display.update()

            # set FPS
            self.clock.tick(self.maze.FPS)

    def pause_menu(self):
        """
        Pause menu, runs when escape is pressed
        """
        self.buttons = [Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 2.7), self.settings.TEXTS[self.settings.LANGUAGE]['CONTINUE'],
                                      self.settings.FONT, self.settings.TEXTCOLOR, self.settings.TEXTCOLOR),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.87), self.settings.TEXTS[self.settings.LANGUAGE]['PARAMETERS'],
                                      self.settings.FONT, self.settings.TEXTCOLOR, self.settings.TEXTCOLOR),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.57), self.settings.TEXTS[self.settings.LANGUAGE]['HELP'],
                                      self.settings.FONT, self.settings.TEXTCOLOR, self.settings.TEXTCOLOR),
                        Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.3), self.settings.TEXTS[self.settings.LANGUAGE]['MAIN MENU'],
                                      self.settings.FONT, self.settings.TEXTCOLOR, self.settings.TEXTCOLOR)]

        self.drawScreen()

        fadeTransitionEnd(self.screen, self.shader if self.settings.SHADERON else None)

        while True:
            # set background color
            self.screen.fill(pygame.Color(46, 60, 87))

            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_ESCAPE]:
                        self.game()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if button.checkForInput():
                            if i == 0:
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                self.maze.transition = 200
                                self.game()
                            elif i == 1:
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                self.settings_menu(self.pause_menu)
                            elif i == 2:
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                self.help_menu(self.pause_menu)
                            elif i == 3:
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                self.main_menu()

            self.drawScreen()

            if not self.settings.SHADERON:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def end_menu(self):
        """
        Menu that shows either when you die or when you succeed
        """
        if self.maze.status == 'success':
            # end background
            self.background = self.endingBackground

        self.buttons = []
        self.drawScreen()

        # if success
        if self.maze.status == 'success':
            # buttons
            self.buttons = [Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.6), self.settings.TEXTS[self.settings.LANGUAGE]['RETRY'],
                                                self.settings.SMALLCREEPYFONT, self.settings.DARKTEXTCOLOR, self.settings.DARKHOVERINGCOLOR),
                            Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.3), self.settings.TEXTS[self.settings.LANGUAGE]['QUIT'],
                                            self.settings.SMALLCREEPYFONT, self.settings.DARKTEXTCOLOR, self.settings.DARKHOVERINGCOLOR)]

            # end texts
            endTextUp = self.settings.BIGCREEPYFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['YOU HAVE REFOUND'], True, self.settings.SUCCESSCOLOR)
            endTextUpRect = endTextUp.get_rect(center=(self.settings.WIDTH / 2, self.settings.HEIGHT / 3))

            endTextDown = self.settings.BIGCREEPYFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['YOUR BROTHER'] if self.settings.TYPE == 'girl' else self.settings.TEXTS[self.settings.LANGUAGE]['YOUR SISTER'], True, self.settings.SUCCESSCOLOR)
            endTextDownRect = endTextDown.get_rect(center=(self.settings.WIDTH / 2, self.settings.HEIGHT / 2.2))

        # if fail
        else:
            # buttons
            self.buttons = [Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.6), self.settings.TEXTS[self.settings.LANGUAGE]['RESTART'],
                                   self.settings.SMALLCREEPYFONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR),
                            Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.3), self.settings.TEXTS[self.settings.LANGUAGE]['QUIT'],
                                   self.settings.SMALLCREEPYFONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR)]

            # end texts
            endTextUp = self.settings.BIGCREEPYFONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['YOU DIED'], True, self.settings.FAILCOLOR)
            endTextUpRect = endTextUp.get_rect(center=(self.settings.WIDTH / 2, self.settings.HEIGHT / 2.2))

            # placeholder text
            endTextDown = self.settings.BIGCREEPYFONT.render('', True, 'white')
            endTextDownRect = endTextDown.get_rect()

        fadeTransitionEnd(self.screen, self.shader if self.settings.SHADERON else None, duration=300)

        while True:
            # set background color
            self.screen.fill(pygame.Color(46, 60, 87))

            # used for taking inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, button in enumerate(self.buttons):
                        if button.checkForInput():
                            if i == 0:  # retry/restart button
                                self.background = self.menuBackground
                                self.maze.status = 'running'
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                self.maze.reset()
                                self.maze.transition = 200
                                self.game(doTransition=False)
                            elif i == 1:  # quit button
                                self.background = self.menuBackground
                                self.settings.dstToClosestEnemy = 1000000
                                self.maze.status = 'running'
                                fadeTransitionStart(self.screen, self.shader if self.settings.SHADERON else None)
                                self.main_menu()

            self.drawScreen()

            self.screen.blit(endTextUp, endTextUpRect)
            self.screen.blit(endTextDown, endTextDownRect)

            if not self.settings.SHADERON:
                pygame.display.update()
            else:
                self.shader.render(self.screen)

            # set FPS
            self.clock.tick(self.maze.FPS)

    def updateKeys(self):
        """
        Updates key in settings
        """
        self.settings.K_UP = self.buttons[0].key
        self.settings.K_DOWN = self.buttons[1].key
        self.settings.K_LEFT = self.buttons[2].key
        self.settings.K_RIGHT = self.buttons[3].key
        self.settings.K_MAP = self.buttons[4].key

    def chooseType(self):
        """
        When the game starts, allows user to choose between boy and girl
        :return: True when the choice is made
        """
        # buttons
        boyButton = Button(None, (self.settings.WIDTH // 1.6, self.settings.HEIGHT // 2), self.settings.TEXTS[self.settings.LANGUAGE]['BOY'],
                                  self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR)
        girlButton = Button(None, (self.settings.WIDTH // 2.4, self.settings.HEIGHT // 2), self.settings.TEXTS[self.settings.LANGUAGE]['GIRL'] + '        /',
                                   self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR)
        cancelButton = Button(None, (self.settings.WIDTH // 2, self.settings.HEIGHT // 1.3), self.settings.TEXTS[self.settings.LANGUAGE]['CANCEL'],
                                     self.settings.FONT, self.settings.TEXTCOLOR, self.settings.HOVERINGCOLOR)

        self.screen.blit(self.background, self.background.get_rect())

        boyButton.update(self.screen)
        girlButton.update(self.screen)
        cancelButton.update(self.screen)

        type = None
        while type is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if boyButton.checkForInput():
                        type = 'boy'
                    if girlButton.checkForInput():
                        type = 'girl'
                    if cancelButton.checkForInput():
                        self.main_menu()

            boyButton.update(self.screen)
            girlButton.update(self.screen)
            cancelButton.update(self.screen)

            if self.settings.SHADERON:
                self.shader.render(self.screen)
            else:
                pygame.display.update()

        self.settings.TYPE = type

        return True

    def drawScreen(self, getInput=True):
        """
        Draws background, buttons and additional debug info for menus
        """
        self.screen.blit(self.background, self.background.get_rect())

        for button in self.buttons:
            if isinstance(button, Slider):
                button.update(self.screen, getInput)
            else:
                button.update(self.screen)


if __name__ == '__main__':
    mazeGen = MazeGame()
    mazeGen.main_menu()
