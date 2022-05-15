import numpy as np
from colorama import Fore, Back, Style

class game_object:
    def __init__(self, grid, health):
        self.grid = grid
        rows, columns = np.shape(grid)
        self.height = rows
        self.width = columns
        self.health = health
        self.attacked = 0


class hut(game_object):

    def __init__(self):
        self.grid = np.array(
        [
            [' ', '_', '_', '_', ' '],
            ['/', ' ', ' ', '/', '\\'],
            ['|', '_', '_', '|', '|']
        ]
        )
        health = 100
        super().__init__(self.grid, health)

class wall(game_object):
    def __init__(self):
        self.grid = np.array([['█']])
        health = 10
        super().__init__(self.grid, health)


class townhall(game_object):
    def __init__(self):
        self.grid = np.array(
            [
                [' ', ' ', '/', '/', '/', '/', '/', '/', '/', '/', '/', '/', '\\', ' '],
                [' ', '/', '/', '/', '/', '/', '/', '/', '/', '/', '/', ' ', ' ', '\\'],
                [' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', '|'],
                [' ', '|', '[', ']', ' ', '|', '|', ' ', '[', ']', '|', ' ', ' ', '|'],
                [' ', '|', ' ', ' ', ' ', '|', '|', ' ', ' ', ' ', '|', ' ', ' ', '|'],
                [' ', '|', ' ', ' ', ' ', '|', '|', ' ', ' ', ' ', '|', ' ', ' ', '|']
            ]
        )
        health = 500
        super().__init__(self.grid, health)

class cannon(game_object):
    def __init__(self):
        self.grid = np.array(
            [
                ['┌', '─', '─', '─', '┐'],
                ['└', '─', '─', '─', '┘'],
                [' ', 'O', ' ', 'O', ' ']   
            ]
        )
        health = 150
        self.damage = 20
        self.range = 5
        super().__init__(self.grid, health)

class WizardTower(game_object):
    def __init__(self):
        self.grid = np.array(
            [
                ['/', '_', '\\', ' ', '/', '_', '\\'],
                ['|', ' ', '|', ' ', '|', ' ', '|'],
                ['|', ' ', '|', '_', '|', ' ', '|'],
                ['|', ' ', '|', ' ', '|', ' ', '|']
            ]
        )
        health = 150
        self.damage = 20
        self.range = 5
        super().__init__(self.grid, health)