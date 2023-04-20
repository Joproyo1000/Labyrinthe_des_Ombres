import pygame.sprite
from math import floor


class HashMap(pygame.sprite.Group):
    def __init__(self, TILESIZE, cols):
        super().__init__()
        """
        Optimized version of getting collisions sprites with a complexity of O(1)
        :param TILESIZE: size of the tiles in the maze
        :param cols: number of columns
        """
        self.TILESIZE = TILESIZE
        self.cols = cols
        self.grid = {}

    def get_grid_pos(self, posX, posY):
        """
        :param posX: 2D x position in the grid
        :param posY: 2D y position in the grid
        :return: the position in the 1D grid based on the 2D position given
        """
        gridPosX = floor(posX / self.TILESIZE) * self.TILESIZE
        gridPosY = floor(posY / self.TILESIZE) * self.TILESIZE
        gridPos = gridPosX + gridPosY * self.cols
        return gridPos

    def get_neighbors(self, pos):
        """
        :param pos: position of the target tile
        :return: all neighbors of this tile
        """
        neighborsIndex = [self.get_grid_pos(pos[0], pos[1]),  # center
                          self.get_grid_pos(pos[0] - self.TILESIZE, pos[1] - self.TILESIZE),  # topleft
                          self.get_grid_pos(pos[0], pos[1] - self.TILESIZE),  # top
                          self.get_grid_pos(pos[0] + self.TILESIZE, pos[1] - self.TILESIZE),  # topright
                          self.get_grid_pos(pos[0] - self.TILESIZE, pos[1]),  # left
                          self.get_grid_pos(pos[0] + self.TILESIZE, pos[1]),  # right
                          self.get_grid_pos(pos[0] - self.TILESIZE, pos[1] + self.TILESIZE),  # bottomleft
                          self.get_grid_pos(pos[0], pos[1] + self.TILESIZE),  # bottom
                          self.get_grid_pos(pos[0] + self.TILESIZE, pos[1] + self.TILESIZE)]  # bottomright

        neighbors = []
        for key in neighborsIndex:
            neighbor = self.grid.get(key, False)
            if neighbor:
                neighbors.append(neighbor)

        return neighbors

    def set(self, key, value):
        """
        Sets the value 'value' at the key 'key' in the hashMap
        :param key:
        :param value:
        """
        alignedKey = floor(key[0] / self.TILESIZE) * self.TILESIZE + \
                     floor(key[1] / self.TILESIZE) * self.TILESIZE * self.cols
        self.grid[alignedKey] = value

    def generate_hashmap(self):
        """
        Generates hashmap from a list of sprites
        """
        for sprite in self.sprites():
            self.set(sprite.rect.center, sprite)
