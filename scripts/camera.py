import random
import pygame.sprite

import settings

from Pygame_Lights import *
from enemy import Enemy
from tile import Tile
from objects import Chest, Torch, CobWeb
from shaders import Shader


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, settings: settings.Settings, get_neighbors: classmethod, check_tile: classmethod):
        """
        Camera group used to show sprites on the screen sorted by their y position
        :param settings: copy of the settings
        :param get_neighbors: get_neighbors function of the maze class
        :param check_tile: check_tile function of the maze class
        """
        super().__init__()

        # copy settings to self to access them in the whole class
        self.settings = settings

        # get the display surface
        self.screen = pygame.surface.Surface((self.settings.WIDTH, self.settings.HEIGHT))

        # initialize OpenGL shader
        if self.settings.SHADERON:
            self.shader = Shader(self.settings.RESOLUTION, self.settings)

        # precalculate half the width and half the height of the screen
        self.half_width = self.screen.get_width() // 2
        self.half_height = self.screen.get_height() // 2

        # initialize offset which is used to offset the display to center the view on the player
        self.offset = pygame.math.Vector2()

        # perspectiveOffset is used to offset each tile by a percentage (1 being no offset) to create fake perspective
        self.perspectiveOffset = 1.3

        # initialize background surface
        self.background = pygame.Surface((self.settings.MAZEWIDTHS[self.settings.CURRENTLEVEL],
                                          self.settings.MAZEHEIGHTS[self.settings.CURRENTLEVEL]))
        self.backgroundRect = self.background.get_rect()

        # we move the background lower so that it is aligned with the walls in perspective
        self.backgroundRect.y += self.settings.TILESIZE / 27 * 14

        # initialize notifications list
        self.notifications = []
        self.notificationsAlpha = []

        # item display
        self.itemDisplayRect = Rect(self.settings.WIDTH - 200 - self.settings.TILESIZE, 200, self.settings.TILESIZE, self.settings.TILESIZE)

        # helper methods
        self.get_neighbors = get_neighbors
        self.check_tile = check_tile

    def init_background(self):
        """
        Bakes background onto a surface for optimization
        """
        self.ySortSprites = []

        for sprite in self.sprites():
            if isinstance(sprite, Tile):
                if not sprite.isWall:
                    self.blit(sprite, customScreen=self.background)
                else:
                    self.ySortSprites.append(sprite)
            else:
                self.ySortSprites.append(sprite)

    def init_light(self):
        """
        Sets the light object of the player
        """
        lightColor = self.settings.LIGHTCOLOR
        lightSize = self.settings.LIGHTRADIUS
        self.light = LIGHT(lightSize, pixel_shader(lightSize, lightColor, 1, False))

        # create shadow objects (walls, etc...)
        # the rect's y parameter must be adjusted to the TILESIZE
        self.shadow_objects = [pygame.Rect(tile.rect.topleft[0], tile.rect.topleft[1] / self.perspectiveOffset - self.settings.TILESIZE/12, self.settings.TILESIZE, self.settings.TILESIZE).inflate(0, -14) for tile in self.sprites() if str(type(tile)) == "<class 'tile.Tile'>" and tile.isWall]

        self.torches = []
        for sprite in self.sprites():
            if str(type(sprite)) == "<class 'objects.Torch'>":
                torch = LIGHT(lightSize, pixel_shader(lightSize, lightColor, 1, False))
                pos = (sprite.rect.centerx, sprite.rect.centery / self.perspectiveOffset)
                torch.baked_lighting(self.shadow_objects, pos[0], pos[1], pygame.Vector2(0, 0), False)

                self.torches.append([torch, pos])

        self.lights_display = pygame.Surface(self.screen.get_size())
        self.global_light = global_light(self.screen.get_size(), self.settings.LIGHTINTENSITY)

    def render_light(self):
        """
        Blits the light on the screen with shadows cast from the shadow_objects
        """
        # reset screen
        self.lights_display.fill('black')

        # global light darkens the background
        self.lights_display.blit(self.global_light, (0, 0))

        # show lights
        self.light.main(self.shadow_objects, self.offset, self.lights_display, self.half_width, self.half_height)

        for torch, pos in self.torches:
            torch.main([], (0, 0), self.lights_display, pos[0] - self.offset.x, pos[1] - self.offset.y)

        # show the light on the screen
        self.screen.blit(self.lights_display, (0, 0), special_flags=BLEND_RGBA_MULT)

    def notification(self, x: int, y: int, text: str, corner: str, duration):
        """
        Sets a 'notification' to appear on the screen for a certain duration
        :param x: x position of the text
        :param y: y position of the text
        :param text: text to be displayed
        :param corner: which corner to be used for the position
        :param duration: duration of the notification
        """
        if corner == 'topleft':
            rect = self.settings.FONT.render(text, True, 'antiquewhite3').get_rect(topleft=(x, y))
        elif corner == 'topright':
            rect = self.settings.FONT.render(text, True, 'antiquewhite3').get_rect(topright=(x, y))
        elif corner == 'bottomleft':
            rect = self.settings.FONT.render(text, True, 'antiquewhite3').get_rect(bottomleft=(x, y))
        elif corner == 'bottomright':
            rect = self.settings.FONT.render(text, True, 'antiquewhite3').get_rect(bottomright=(x, y))

        self.notifications.append((text, rect))
        self.notificationsAlpha.append(duration)

    def blit(self, sprite: pygame.sprite.Sprite, customScreen=None, customImage=None):
        """
        :param sprite: sprite to blit on the screen
        :param customScreen: custom screen onto which blit the image instead of the normal screen
        :param customImage: custom image to blit on the screen instead of the sprite's image
        Blits the sprite on the screen after applying the perspective offset
        """
        if customImage is not None:
            self.screen.blit(customImage, (sprite.rect.topleft[0] - self.offset.x,
                                           sprite.rect.topleft[1] / self.perspectiveOffset - self.offset.y))

        elif customScreen is not None:
            customScreen.blit(sprite.image, (sprite.rect.topleft[0] - self.offset.x,
                                             sprite.rect.topleft[1] / self.perspectiveOffset - self.offset.y))

        else:
            self.screen.blit(sprite.image, (sprite.rect.topleft[0] - self.offset.x,
                                            sprite.rect.topleft[1] / self.perspectiveOffset - self.offset.y))

    def custom_draw(self, player: pygame.sprite.Sprite, blackGradient, getInput=True):
        """
        :param player: player sprite (used to calculate the offset to center the screen)
        :return: draws with perspective all the sprites in the visible_sprites group
        :param blackGradient: black surface used for transition
        """
        # reset screen
        self.screen.fill('black')

        # calculate offset of player to center of screen
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery / self.perspectiveOffset - self.half_height

        backgroundRect = pygame.Rect(self.backgroundRect.x - self.offset.x, self.backgroundRect.y - self.offset.y,
                                     self.backgroundRect.width, self.backgroundRect.height)
        self.screen.blit(self.background, backgroundRect)

        # we create a copy of the player sprite that we are going to cut to prevent overlap with the walls
        # we do that so that the player sprite isn't affected by lighting since it would cause some bugs
        cutPlayerSprite = player.image.copy()
        objects = []

        # draw every sprite sorted by y coordinate
        for sprite in sorted(self.ySortSprites, key=lambda sprite: sprite.rect.centery):
            # separate the player from the tiles
            if str(type(sprite)) == "<class 'tile.Tile'>":
                if sprite.isWall:
                    self.blit(sprite)

            elif str(type(sprite)) != "<class 'player.Player'>":
                # draw objects and enemies
                objects.append(sprite)
                self.blit(sprite)

        # remove all objects from player image
        for object in objects:
            if object.rect.centery > player.rect.centery:
                # offsets here are because of the images not being the same size
                if isinstance(object, Chest):
                    offsetRect = pygame.Rect(object.rect.centerx - player.rect.centerx + 9, (object.rect.centery - player.rect.centery) / self.perspectiveOffset + 7.5, object.rect.width, object.rect.height)
                elif isinstance(object, Torch):
                    offsetRect = pygame.Rect(object.rect.centerx - player.rect.centerx - 15, (object.rect.centery - player.rect.centery) / self.perspectiveOffset - 32, object.rect.width, object.rect.height)
                elif isinstance(object, CobWeb):
                    offsetRect = pygame.Rect(object.rect.centerx - player.rect.centerx + 11, (object.rect.centery - player.rect.centery) / self.perspectiveOffset + 9, object.rect.width, object.rect.height)
                elif isinstance(object, Enemy):
                    offsetRect = pygame.Rect(object.rect.centerx - player.rect.centerx, (object.rect.centery - player.rect.centery) / self.perspectiveOffset + 2, object.rect.width, object.rect.height)

                cutPlayerSprite.blit(object.image, offsetRect)

        # remove surrounding wall sprites from player image
        for sprite in self.get_neighbors(self.check_tile(player.rect.centerx // self.settings.TILESIZE,
                                                         player.rect.centery // self.settings.TILESIZE)):
            if sprite.isWall and sprite.rect.centery > player.rect.centery:
                pygame.draw.rect(cutPlayerSprite, (0, 0, 0, 0), Rect(sprite.rect.centerx - player.rect.centerx - 9, (sprite.rect.centery - player.rect.centery) / self.perspectiveOffset - 8, sprite.rect.width, sprite.rect.height))


        # lighting
        if self.settings.SHADERON:
            self.render_light()

        # draw player after lighting so that it is not affected
        self.blit(player, customImage=cutPlayerSprite)

        # draw every notification fading out
        for notification, alpha in zip(self.notifications, self.notificationsAlpha):
            text = self.settings.FONT.render(notification[0], True, 'antiquewhite3')
            text.set_alpha(alpha)
            self.screen.blit(text, notification[1])

            if alpha <= 0:
                self.notifications.remove(notification)
                self.notificationsAlpha.remove(alpha)
            else:
                self.notificationsAlpha[self.notificationsAlpha.index(alpha)] -= 4

        # draw number of lives
        livesText = self.settings.FONT.render(self.settings.TEXTS[self.settings.LANGUAGE]['LIVES'] + ": " + str(player.lives), True, self.settings.TEXTCOLOR)
        livesTextRect = livesText.get_rect(topleft=(100, 100))
        self.screen.blit(livesText, livesTextRect)

        pygame.draw.rect(self.screen, 'antiquewhite3', self.itemDisplayRect, 10)
        if player.currentItemIndex != 0:
            self.screen.blit(player.inventory[player.currentItemIndex].image, player.inventory[player.currentItemIndex].rect)

        # fade in transition
        self.screen.blit(blackGradient, blackGradient.get_rect())

        # apply heart beat effect if activated
        scaledScreen = self.screen

        if self.settings.SHOWHEARTBEATEFFECT:
            if self.settings.dstToClosestEnemy <= 300:
                hearBeatEffectFactor = int((-self.settings.dstToClosestEnemy + 400)/100)

                scaledScreen = pygame.transform.scale(self.screen, (self.settings.WIDTH + hearBeatEffectFactor*10, self.settings.HEIGHT + hearBeatEffectFactor*10))
                scaledScreen.blit(scaledScreen, (random.randint(-hearBeatEffectFactor, hearBeatEffectFactor) - hearBeatEffectFactor*5,
                                                 random.randint(-hearBeatEffectFactor, hearBeatEffectFactor) - hearBeatEffectFactor*5))

        # and finally render screen
        if self.settings.SHADERON and getInput:
            self.shader.render(scaledScreen)
        else:
            pygame.display.get_surface().blit(self.screen, self.screen.get_rect())

        return scaledScreen
