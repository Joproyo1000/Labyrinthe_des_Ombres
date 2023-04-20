import heapq
import pygame

from tile import Tile


def distance(a: Tile, b: Tile):
    """
    :param a: first tile
    :param b: second tile
    :return: fake euclidian distance between two tiles a and b
    """
    dstX = abs(a.rect.x - b.rect.x)
    dstY = abs(a.rect.y - b.rect.y)

    y = min(dstX, dstY)
    x = max(dstX, dstY)

    return 14 * y + 10 * (x - y)


# Define the PathFinder class
class PathFinder:
    def __init__(self, level):
        """
        A* pathfinding algorithm object
        :param level: current maze level that is used
        """
        # Get the grid of tiles in the maze that are not walls
        self.grid = [tile for tile in level.grid_tiles if not tile.isWall]

        # Get the function to get the neighbors of a tile
        self.get_neighbors = level.get_neighbors

        # Initialize the open and closed lists and heapify the open list
        self.open = []
        self.closed = []
        heapq.heapify(self.open)

    def findPath(self, start, end):
        """
        Finds the shortest path between start and end using the A* algorithm
        :param start: starting tile
        :param end: ending tile

        The A* algorithm works this way:
        1) Initialize the starting node and the end node.
        2) Initialize the open list with the starting node.
        3) Initialize the closed list as empty.
        4) While the open list is not empty:
            A. Get the node with the lowest f-cost from the open list.
            B. Add the current node to the closed list.
            C. For each neighbor of the current node:
                I. If the neighbor is the end node, we have found the path. Return it.
                II. If the neighbor is not passable or is in the closed list, skip it.
                III. If the neighbor is not in the open list, add it to the open list.
                IV. If the neighbor is already in the open list, update its f-cost if the current path is better.
        5) If the end node is not found, there is no path from the start node to the end node.

        h-cost (heuristic cost): An estimate of the distance from the current node to the goal node. This is usually
            calculated using a heuristic function, which may not be exact but should never overestimate the actual
            distance.
        g-cost (movement cost): The cost of moving from the starting node to the current node. This is typically
            calculated as the sum of the movement costs of all the nodes visited along the path from the starting node
            to the current node.
        f-cost (total cost): The sum of the g-cost and the h-cost for a particular node. This represents the estimated
            total cost of the cheapest path from the starting node to the goal node that goes through the current node.
            The algorithm selects the node with the lowest f-cost as the next node to explore.
        """

        self.open.clear()
        self.closed.clear()

        # Reset the cost values of each tile in the grid
        for tile in self.grid:
            tile.reset()

        # Push the start tile onto the open list
        heapq.heappush(self.open, (start.fCost(), start))

        # While the open list is not empty, continue searching for the shortest path
        while len(self.open) > 0:
            # Get the tile with the lowest fCost from the open list and add it to the closed list
            current = heapq.heappop(self.open)[1]
            self.closed.append(current)

            # If the current tile is the end tile, return the path from start to end
            if current == end:
                return self.getPath(start, end)

            # Check the neighboring tiles of the current tile
            for neighbor in self.get_neighbors(current):
                # Mark the neighbor tile as visited
                neighbor.isVisited = True

                # If the neighbor tile is a wall or is already in the closed list, skip it
                if neighbor.isWall or neighbor in self.closed:
                    continue

                # Calculate the cost to move from the current tile to the neighbor tile
                movementCost = current.gCost + distance(current, neighbor)

                # If the new cost is less than the previous cost or the neighbor tile is not in the open list,
                # update the neighbor tile's cost values and add it to the open list
                if movementCost < neighbor.gCost or neighbor not in [d[1] for d in self.open]:
                    neighbor.gCost = movementCost
                    neighbor.hCost = distance(neighbor, end)
                    neighbor.parent = current

                    # If the neighbor tile is not already in the open list, add it
                    if neighbor not in [d[0] for d in self.open]:
                        heapq.heappush(self.open, (neighbor.fCost(), neighbor))

    def getPath(self, start, end):
        """
        :param start: starting tile
        :param end: ending tile
        :return: the list of tiles in the path
        """
        path = []
        current = end

        # Traverse the tiles from the end tile to the start tile and append them to the path list
        while current != start:
            path.append(current)
            current = current.parent

        # Reverse the path list to get the path from the start tile to the end tile
        path.reverse()
        return path
