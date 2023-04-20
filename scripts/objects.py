import pygame

import player
import settings
import spatial_hashmap

from math import floor
from support import import_folder
from random import randint


class Torch(pygame.sprite.Sprite):
    def __init__(self, pos: (int, int), settings: settings.Settings, groups: [pygame.sprite.Group]):
        super().__init__(groups)
        """
        Torch object which lights up a portion of the maze
        :param pos: position of the torch
        :param settings: copy of the settings
        :param groups: groups in which the torch are
        """
        # get the display surface
        self.screen = pygame.display.get_surface()

        self.settings = settings

        # graphics setup
        self.import_object_assets()
        self.frame_index = 0
        self.animation_speed = 0.15

        # initialize rect (bounding box of the image) and hitbox (bounding box of the collision detection)
        self.rect = self.image.get_bounding_rect()
        self.rect.center = pos
        self.hitbox = self.rect

        # set color on the minimap
        self.color = 'white'

    def import_object_assets(self):
        """
        Loads the corresponding animation frames onto the object
        """
        object_path = 'graphics/special/torch/'
        self.animations = {'right': []}

        for animation in self.animations:
            full_path = object_path + animation
            self.animations[animation] = import_folder(full_path, 5)

        self.image = self.animations['right'][0]

    def animate(self, dt: float):
        """
        Animates the torch based on the current status
        :param dt: delta time in ms
        """
        animation = self.animations['right']

        # loop over the frame index
        self.frame_index += self.animation_speed * dt * 50
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.rect.center)

    def update(self, dt: float):
        """
        Main update method
        :param dt: delta time in ms
        """
        self.animate(dt)  # animate based on status


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos: (int, int), settings: settings.Settings, groups: [pygame.sprite.Group], visible_sprites):
        super().__init__(groups)
        """
        Chest object containing one object
        :param pos: position of the chest
        :param settings: copy of the settings
        :param groups: groups in which the chest are
        :param visible_sprites: copy of the visible sprites
        """
        # get the display surface
        self.screen = pygame.display.get_surface()

        self.settings = settings

        # graphics setup
        self.import_object_assets()
        self.frame_index = 0
        self.animation_speed = 0.15

        # current state of the chest, either closed or opened
        self.state = 'closed'

        # initialize rect (bounding box of the image) and hitbox (bounding box of the collision detection)
        # self.rect = self.image.get_rect(center=pos)
        self.rect = self.image.get_bounding_rect()
        self.rect.center = pos
        self.hitbox = self.rect

        # set color on the minimap
        self.color = self.settings.CHESTCOLOR

        # chose random item to put in the chest 0=freeze, 1=map, 2=heal
        items = {0: Freeze(visible_sprites.itemDisplayRect.center, settings),
                 1: Map((self.rect.centerx / self.settings.MAZEWIDTHS[self.settings.CURRENTLEVEL],
                        self.rect.centery / self.settings.MAZEHEIGHTS[self.settings.CURRENTLEVEL]), settings),
                 2: Heal(visible_sprites.itemDisplayRect.center, settings)}
        self.item = items[randint(0, 2)]

        self.visible_sprites = visible_sprites

    def import_object_assets(self):
        """
        Loads the corresponding animation frames onto the object
        """
        character_path = 'graphics/special/chest/'
        self.animations = {'closed': [], 'opened': []}

        for animation in self.animations:
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path, 5)

        self.image = self.animations['closed'][0]

    def open(self, player):
        """
        Change image to open chest sprite
        """
        if self.state != 'opened':
            animation = self.animations['opened']

            self.image = animation[0]
            if isinstance(self.item, Map):
                player.maps.append(self.item)
            else:
                player.inventory.append(self.item)

            self.visible_sprites.notification(self.settings.WIDTH / 1.1, self.settings.HEIGHT / 1.1,
                                              self.settings.TEXTS[self.settings.LANGUAGE]["YOU HAVE FOUND"] + " " + self.item.text + "!", 'bottomright', 300)

        self.state = 'opened'

    def close(self):
        """
        Change image to closed chest sprite
        """
        self.state = 'closed'

        animation = self.animations['closed']
        self.image = animation[0]


class CobWeb(pygame.sprite.Sprite):
    def __init__(self, pos: (int, int), groups: [pygame.sprite.Group], obstacle_sprites: spatial_hashmap):
        super().__init__(groups)
        """
        Cobweb object, slows down entities walking into it
        :param pos: position of the chest
        :param groups: groups in which the cobweb are
        :param obstacle_sprites: copy of the obstacle sprites
        """
        self.image = pygame.image.load('graphics/special/cobweb.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 3)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        self.pos = pos

        obstacle_sprites.set(self.pos, self)


class Useable(pygame.sprite.Sprite):
    """
    Base class for useable objects
    """
    def use(self, *args, **kwargs):
        self.kill()


class Map(Useable):
    def __init__(self, pos: (int, int), settings):
        super().__init__()
        """
        Map object, reveals a portion of the map
        :param pos: position at which it was found
        """
        self.text = settings.TEXTS[settings.LANGUAGE]["A PIECE OF MAP"]
        self.pos = pos


class Freeze(Useable):
    def __init__(self, pos: (int, int), settings):
        """
        Freeze object, slows down the enemy it touches for 5s
        :param pos: position at which it was found
        """
        super().__init__()
        self.image = pygame.image.load('graphics/special/objects/freeze.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.rect = self.image.get_rect(center=pos)
        self.text = settings.TEXTS[settings.LANGUAGE]["A FREEZE ITEM"]


class Heal(Useable):
    def __init__(self, pos: (int, int), settings):
        """
        Heal object, adds one life to the player
        :param pos: position at which it was found
        """
        super().__init__()
        self.image = pygame.image.load('graphics/special/objects/heal.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.rect = self.image.get_rect(center=pos)
        self.text = settings.TEXTS[settings.LANGUAGE]["AN EXTRA LIFE"]

    def use(self, player: player.Player):
        player.lives += 1
        self.kill()
