import pygame
import math
from queue import PriorityQueue
from contextlib import suppress
from heapq import heappush, heappop

pygame.init()

WIDTH = 800

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Dijkstra Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
PINK = (255, 52, 179)

spotSize = 20
totalRows = WIDTH // 20
grid = []


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = WHITE
        self.neighborList = []
        with suppress(ZeroDivisionError):
            self.row = self.y // 20
            self.column = self.x // 20

    def drawNode(self):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, spotSize, spotSize))

    def makeStartNode(self):
        self.color = GREEN

    def makeEndNode(self):
        self.color = RED

    def isStartNode(self):
        return self.color == GREEN

    def isEndNode(self):
        return self.color == RED

    def makeUnvisited(self):
        self.color = PURPLE

    def makeVisited(self):
        self.color = BLACK

    def isVisited(self):
        return self.color == BLACK

    def makePath(self):
        self.color = TURQUOISE

    def makeWall(self):
        self.color = PINK

    def isWall(self):
        return self.color == PINK

    def neighbors(self):
        # up
        if self.row - 1 >= 0 and not grid[self.row - 1][self.column].isWall():
            self.neighborList.append(grid[self.row - 1][self.column])
        # down
        if self.row + 1 < totalRows and not grid[self.row + 1][self.column].isWall():
            self.neighborList.append(grid[self.row + 1][self.column])
        # right
        if self.column + 1 < totalRows and not grid[self.row][self.column + 1].isWall():
            self.neighborList.append(grid[self.row][self.column + 1])
        # left
        if self.column - 1 >= 0 and not grid[self.row][self.column - 1].isWall():
            self.neighborList.append(grid[self.row][self.column - 1])


def makeGrid():
    gridx = 0
    for y in range(0, WIDTH, 20):
        grid.append([])
        for x in range(0, WIDTH, 20):
            node = Node(x, y)
            grid[gridx].append(node)
        gridx += 1


def draw_grid():
    num = WIDTH // 2
    start = 0
    end = WIDTH
    for i in range(num):
        increment = 20 * i
        pygame.draw.line(WIN, GREY, (increment, start), (increment, end), width=1)
        pygame.draw.line(WIN, GREY, (start, increment), (end, increment), width=1)


def draw():
    WIN.fill(WHITE)

    for row in grid:
        for node in row:
            node.drawNode()

    draw_grid()
    pygame.display.update()


def main():
    makeGrid()
    run = True
    click = 0
    while run:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if click == 0:
                    x, y = pygame.mouse.get_pos()
                    startcol = x // 20
                    startrow = y // 20
                    startNode = grid[startrow][startcol]
                    startNode.makeStartNode()
                    grid[startrow][startcol] = startNode
                    click += 1

                elif click == 1:
                    x, y = pygame.mouse.get_pos()
                    startcol = x // 20
                    startrow = y // 20
                    endNode = grid[startrow][startcol]
                    endNode.makeEndNode()
                    grid[startrow][startcol] = endNode
                    click += 1

                else:
                    x, y = pygame.mouse.get_pos()
                    startcol = x // 20
                    startrow = y // 20
                    wall = grid[startrow][startcol]
                    wall.makeWall()
                    grid[startrow][startcol] = wall
                    click += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    algorithm(startNode, endNode)


def makePath(came_from, current, startNode, endNode):
    while current in came_from:
        current = came_from[current]
        if current is not startNode and current is not endNode:
            current.makePath()
        draw()


def algorithm(startNode, endNode):
    tentative_distances = {}
    came_from = {}

    for row in grid:
        for node in row:
            tentative_distances[node] = math.inf
    tentative_distances[startNode] = 0

    unvisited_nodes = []
    count = 0
    heappush(unvisited_nodes, (0, count, startNode))

    while not len(unvisited_nodes) == 0:
        current = heappop(unvisited_nodes)[2]
        current.neighbors()

        if current == endNode:
            endNode.makeEndNode()
            makePath(came_from, current, startNode, endNode)
            break

        for neighbor in current.neighborList:
            temp_distance = tentative_distances[current] + 1
            if temp_distance < tentative_distances[neighbor]:
                tentative_distances[neighbor] = temp_distance
                came_from[neighbor] = current
                if not neighbor.isVisited():
                    count += 1
                    heappush(unvisited_nodes, (tentative_distances[neighbor], count, neighbor))
                    neighbor.makeUnvisited()

        if current != startNode:
            current.makeVisited()
        draw()


main()
