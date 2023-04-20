import random
import pygame

import objects
import settings

from random import randint
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: (int, int), type: str, settings: settings.Settings, groups: [pygame.sprite.Group], obstacle_sprites: [pygame.sprite.Sprite]):
        super().__init__(groups)
        """
        :param pos: starting position of the player 
        :param type: type of the player, either 'boy' or 'girl'
        :param settings: settings of the maze
        :param groups: groups in which the player are
        :param obstacle_sprites: obstacles that the player should collide with
        """
        # get the display surface
        self.screen = pygame.display.get_surface()

        # get settings
        self.settings = settings

        # set type
        self.type = type

        # graphics setup
        self.import_player_assets(type)
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        # number of lives the player has
        self.lives = 1

        # set color on the minimap
        self.color = self.settings.PLAYERCOLOR

        # initialize rect (bounding box of the image) and hitbox (bounding box of the collision detection)
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(0, -self.settings.TILESIZE//10)  # the 10 must be adjusted to the TILESIZE

        # initialize direction vector and speed which is proportional to the tilesize
        self.direction = pygame.math.Vector2()
        self.speed = 1

        # if set to False, the player will no longer move
        self.getInput = True

        # initialize inventory
        self.maps = []
        self.inventory = [None]
        self.currentItemIndex = 0

        # get obstacles for collision
        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self, type: str):
        """
        :param type: type of the player either 'boy' or 'girl'
        Loads the corresponding animation frames onto the player
        """
        if type == 'boy':
            character_path = 'graphics/player/boy/'
            # create a dictionary with every state of the player and its corresponding animations
            self.animations = {'up': [], 'left': [], 'down': [], 'right': [],
                               'up_idle': [], 'left_idle': [], 'down_idle': [], 'right_idle': []}

            # then import every frame
            for animation in self.animations:
                full_path = character_path + animation
                self.animations[animation] = import_folder(full_path, 1.6)

        if type == 'girl':
            character_path = 'graphics/player/girl/'
            # create a dictionary with every state of the player and its corresponding animations

            self.animations = {'up': [], 'left': [], 'down': [], 'right': [],
                               'up_idle': [], 'left_idle': [], 'down_idle': [], 'right_idle': []}
            # then import every frame
            for animation in self.animations:
                full_path = character_path + animation
                self.animations[animation] = import_folder(full_path, 1.6)

        # set the first image of the player
        self.image = pygame.image.load('graphics/player/boy/down_idle/boy_sprite_front_idle1.png')

    def input(self):
        """
        Updates direction and status based on input
        """
        keys = pygame.key.get_pressed()
        if keys[self.settings.K_UP]:  # up
            self.direction.y = -1
            self.status = 'up'
        elif keys[self.settings.K_DOWN]:  # down
            self.status = 'down'
            self.direction.y = 1
        else:
            self.direction.y = 0  # idle

        if keys[self.settings.K_LEFT]:  # left
            self.status = 'left'
            self.direction.x = -1
        elif keys[self.settings.K_RIGHT]:  # right
            self.status = 'right'
            self.direction.x = 1
        else:
            self.direction.x = 0  # idle

    def set_status(self):
        """
        Set the current status of the player for animation
        """
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if '_idle' not in self.status:
                self.status = self.status + '_idle'

    def move(self, speed: float, dt: float):
        """
        Moves the player after applying collisions
        :param speed: speed of the player when moving
        :param dt: delta time in ms, used to make to player move at the same speed regardless of the FPS
        """
        # normalize the direction so that the speed is always the same
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # we check collision on one axis at a time to avoid bugs
        self.hitbox.x += self.direction.x * speed * dt * 250
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed * dt * 250
        self.collision('vertical')

        # update final position
        self.rect.center = self.hitbox.center

    def collision(self, direction: str):
        """
        :param direction: either 'horizontal' or 'vertical'. Checks collision with the walls on either directions
        If collision occurs, stop the player
        """
        # keep track of if player is in cobweb
        inCobweb = False

        if direction == 'horizontal':
            # check horizontal collision for every neighboring obstacles
            for sprite in self.obstacle_sprites.get_neighbors(self.rect.center):
                if sprite.hitbox.colliderect(self.hitbox):
                    # if player is inside cobweb reduce speed
                    if isinstance(sprite, objects.CobWeb):
                        self.speed = 0.5
                        inCobweb = True
                    else:
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            # check vertical collision for every neighboring obstacles
            for sprite in self.obstacle_sprites.get_neighbors(self.rect.center):
                if sprite.hitbox.colliderect(self.hitbox):
                    # if player is inside cobweb reduce speed
                    if isinstance(sprite, objects.CobWeb):
                        self.speed = 0.5
                        inCobweb = True
                    else:
                        if self.direction.y > 0:  # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # moving up
                            self.hitbox.top = sprite.hitbox.bottom

                # check if a chest is close and open it
                if isinstance(sprite, objects.Chest):
                    sprite.open(self)

        # if player is not inside cobweb set back original speed
        if not inCobweb:
            self.speed = 1

    def use(self, target: pygame.sprite.Sprite):
        """
        Uses the current item that is being hold by the player
        :param target: target to use the current item if it can
        """
        # use the item
        self.inventory[self.currentItemIndex].use(self)
        # then destroy it
        item = self.inventory.pop(self.currentItemIndex)
        # update the current index
        self.currentItemIndex = self.currentItemIndex % len(self.inventory)

        # if the item is a freeze item, freeze the target
        if isinstance(item, objects.Freeze) and target is not None:
            target.freeze(500)

    def animate(self, dt):
        """
        Animates the player based on the current status
        :param dt: delta time in ms
        """
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed * dt * 50
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def play_sounds(self):
        if '_idle' not in self.status:
            if not self.settings.SOUNDEFFECTCHANNEL.get_busy():
                self.settings.SOUNDEFFECTCHANNEL.play(self.settings.FOOTSTEPSOUNDEFFECTS[randint(0, len(self.settings.FOOTSTEPSOUNDEFFECTS) - 1)], loops=1)

    def update(self, dt):
        """
        Main update method
        :param dt: delta time in ms
        """
        self.input()  # get inputs
        self.set_status()  # set status
        self.animate(dt)  # animate based on status

        # if getInput is false, don't move the player
        if self.getInput:
            self.play_sounds()
            self.move(self.speed, dt)  # move based on inputs
