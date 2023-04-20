import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, settings, pos, isWall, groups):
        super().__init__(groups)
        """
        :param settings: settings that are used with the maze
        :param pos: position of the tile
        :param isWall: is the tile a wall or not
        :param groups: groups in which the tile are
        """
        self.settings = settings

        self.image = pygame.image.load('graphics/maze/Bush.png').convert_alpha()
        scale = self.settings.TILESIZE/27
        self.image = pygame.transform.scale(self.image, (27 * scale, 37 * scale))
        self.path = pygame.image.load('graphics/maze/Grass.png').convert_alpha()
        self.path = pygame.transform.scale(self.path, (27 * scale, 37 * scale))
        self.goal = pygame.image.load('graphics/maze/Stairs.png').convert_alpha()
        self.goal = pygame.transform.scale(self.goal, (27 * scale, 37 * scale))

        self.rect = pygame.rect.Rect(pos[0], pos[1], min(self.image.get_width(), self.image.get_height()), min(self.image.get_width(), self.image.get_height()))

        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.hitbox = self.rect.inflate(-10, -10)

        self.pos = pygame.Vector2(pos)

        self.color = self.settings.WALLCOLOR

        self.isWall = isWall

        # pathfinding variables
        self.gCost = 0
        self.hCost = 0

        self.parent = None

    def __lt__(self, other):
        """
        :param other: tile to compare fCost with
        :return: True if hCost of this tile is smaller than the other else False
        """
        compare = False if self.fCost() == other.fCost() else self.fCost() < other.fCost()
        if compare == False:
            compare = self.hCost < other.hCost
        return compare

    def fCost(self):
        """
        :return: fCost of the tile, fCost = gCost + hCost
        """
        return self.gCost + self.hCost

    def reset(self):
        """
        Reset the tile's properties
        """
        self.gCost = 0
        self.hCost = 0

    def update_color(self):
        """
        Update color of the tile if it's a wall or not
        """
        if self.isWall:
            self.color = self.settings.WALLCOLOR
        else:
            self.color = self.settings.PATHCOLOR
            self.image = self.path
