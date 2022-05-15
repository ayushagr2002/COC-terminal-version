import math
from re import S
import numpy as np
from colorama import Fore, Back, Style
import time


def check_wall(ch):
    if(ch == Fore.GREEN + '█' or ch == Fore.YELLOW + '█' or ch == Fore.RED + '█'):
        return True
    return False

class Player:
    def __init__(self, x, y, health, damage, grid):
        self.x = x
        self.y = y
        self.grid = grid
        self.health = health
        self.curhealth = health
        self.damage = damage
    
    def attack(self, game_map):
        att = 0
        for cn in game_map.cannons:
            if((cn.toplefty == self.y + 1 or cn.toplefty + cn.height == self.y) and cn.topleftx <= self.x and cn.topleftx + cn.width - 1 >= self.x):
                cn.attacked = 1
                game_map.render()
                time.sleep(0.1)
                cn.curhealth -= self.damage
                att = 1
                break
            
            if((cn.topleftx == self.x + 1 or cn.topleftx + cn.width == self.x) and cn.toplefty <= self.y and cn.toplefty + cn.height - 1 >= self.y):
                cn.attacked = 1
                game_map.render()
                time.sleep(0.1)
                cn.curhealth -= self.damage
                att = 1
                break

        if(att == 0):
            for obj in game_map.objects:
                if((obj.toplefty == self.y + 1 or obj.toplefty + obj.height == self.y) and obj.topleftx <= self.x and obj.topleftx + obj.width -1 >= self.x):
                    obj.attacked = 1
                    game_map.render()
                    time.sleep(0.1)
                    obj.curhealth -= self.damage
                    att = 1
                    break
            
                if((obj.topleftx == self.x + 1 or obj.topleftx + obj.width == self.x) and obj.toplefty <= self.y and obj.toplefty + obj.height - 1 >= self.y):
                    obj.attacked = 1
                    game_map.render()
                    time.sleep(0.1)
                    obj.curhealth -= self.damage
                    att = 1
                    break

        if(att == 0):
            for w in game_map.walls:
                if((w.y - 1 == self.y or w.y + 1 == self.y) and w.x == self.x):
                    w.attacked = 1
                    game_map.render()
                    time.sleep(0.1)
                    w.curhealth -= self.damage
                    break
                
                if((w.x - 1 == self.x or w.x + 1 == self.x) and w.y == self.y):
                    w.attacked = 1
                    game_map.render()
                    time.sleep(0.1)
                    w.curhealth -= self.damage
                    break
        if(att == 0):
            for tw in game_map.towers:
                if((tw.toplefty == self.y + 1 or tw.toplefty + tw.height == self.y) and tw.topleftx <= self.x and tw.topleftx + tw.width - 1 >= self.x):
                    tw.attacked = 1
                    game_map.render()
                    time.sleep(0.1)
                    tw.curhealth -= self.damage
                    att = 1
                    break
            
                if((tw.topleftx == self.x + 1 or tw.topleftx + tw.width == self.x) and tw.toplefty <= self.y and tw.toplefty + tw.height - 1 >= self.y):
                    tw.attacked = 1
                    game_map.render()
                    time.sleep(0.1)
                    tw.curhealth -= self.damage
                    att = 1
                    break
class ArcherQueen(Player):
    def __init__(self):
        self.grid = np.array([['Q']])
        self.range = 8
        self.aoe = 5
        self.eaglerange = 16
        self.eagleaoe = 9
        self.attacked = 0
        self.attackedeagle = 0
        self.lastmoved = 'W'
        super().__init__(90, 48, 100.0, 15, self.grid)
    
    def move_up(self, game_map):
        if(game_map.rage == 1):
            if(self.y >= 5 and game_map.grid[self.y - 1][self.x] == ' '):
                if(game_map.grid[self.y - 2][self.x] == ' '):
                    self.y -= 2
                else:
                    self.y -= 1
        else:
            if(self.y >= 4 and game_map.grid[self.y - 1][self.x] == ' '):
                    self.y -= 1
    
    def move_left(self, game_map):
        if(game_map.rage == 1):
            if(self.x >= 3 and game_map.grid[self.y][self.x - 1] == ' '):
                if(game_map.grid[self.y][self.x - 2] == ' '):
                    self.x -= 2
                else:
                    self.x -= 1
        else:
            if(self.x >= 2 and game_map.grid[self.y][self.x - 1] == ' '):
                    self.x -= 1
    
    def move_right(self, game_map):
        if(game_map.rage == 1):
            if(self.x <= game_map.columns-3 and game_map.grid[self.y][self.x + 1] == ' '):
                if(game_map.grid[self.y][self.x + 2] == ' '):
                    self.x += 2
                else:
                    self.x += 1 
        else:
            if(self.x <= game_map.columns-2 and game_map.grid[self.y][self.x + 1] == ' '):
                    self.x += 1

    def move_down(self, game_map):
        if(game_map.rage == 1):
            if(self.y <= game_map.rows-3 and game_map.grid[self.y + 1][self.x] == ' '):
                if(game_map.grid[self.y + 2][self.x] == ' '):
                    self.y += 2
                else:
                    self.y += 1
        else:
            if(self.y <= game_map.rows-2 and game_map.grid[self.y + 1][self.x] == ' '):
                self.y += 1
    
    def attack(self, game_map):
        
        if(self.lastmoved == 'W'):
            up = self.y - self.range - int(self.aoe/2)
            bot = self.y - self.range + int(self.aoe/2)
            left = self.x - int(self.aoe/2)
            right = self.x + int(self.aoe/2)
        elif(self.lastmoved == 'S'):
            up = self.y + self.range - int(self.aoe/2)
            bot = self.y + self.range + int(self.aoe/2)
            left = self.x - int(self.aoe/2)
            right = self.x + int(self.aoe/2)
        elif(self.lastmoved == 'D'):
            up = self.y - int(self.aoe/2)
            bot = self.y + int(self.aoe/2)
            left = self.x + self.range - int(self.aoe/2)
            right = self.x + self.range + int(self.aoe/2)
        elif(self.lastmoved == 'A'):
            up = self.y - int(self.aoe/2)
            bot = self.y + int(self.aoe/2)
            left = self.x - self.range - int(self.aoe/2)
            right = self.x - self.range + int(self.aoe/2)
        
        self.attacked = 1
        game_map.render()
        time.sleep(0.1)

        for obj in game_map.objects:
            if(((obj.topleftx <= left and obj.topleftx + obj.width >= left) or (obj.topleftx >= left and obj.topleftx <= right)) and ((obj.toplefty <= up and obj.toplefty + obj.height >= up) or (obj.toplefty >= up and obj.toplefty <= bot))):
                obj.attacked = 1
                obj.curhealth -= self.damage
        
        for w in game_map.walls:
            if(w.x >= left and w.x <= right and w.y >= up and w.y <= bot):
                w.attacked = 1
                w.curhealth -= self.damage

        for cn in game_map.cannons:
            if(((cn.topleftx <= left and cn.topleftx + cn.width >= left) or (cn.topleftx >= left and cn.topleftx <= right)) and ((cn.toplefty <= up and cn.toplefty + cn.height >= up) or (cn.toplefty >= up and cn.toplefty <= bot))):
                cn.attacked = 1
                cn.curhealth -= self.damage

        for tw in game_map.towers:
            if(((tw.topleftx <= left and tw.topleftx + tw.width >= left) or (tw.topleftx >= left and tw.topleftx <= right)) and ((tw.toplefty <= up and tw.toplefty + tw.height >= up) or (tw.toplefty >= up and tw.toplefty <= bot))):
                tw.attacked = 1
                tw.curhealth -= self.damage

    def attack_eagle_arrow(self, game_map):
        if(self.lastmoved == 'W'):
            up = self.y - self.eaglerange - int(self.eagleaoe/2)
            bot = self.y - self.eaglerange + int(self.eagleaoe/2)
            left = self.x - int(self.eagleaoe/2)
            right = self.x + int(self.eagleaoe/2)
        elif(self.lastmoved == 'S'):
            up = self.y + self.eaglerange - int(self.eagleaoe/2)
            bot = self.y + self.eaglerange + int(self.eagleaoe/2)
            left = self.x - int(self.eagleaoe/2)
            right = self.x + int(self.eagleaoe/2)
        elif(self.lastmoved == 'D'):
            up = self.y - int(self.eagleaoe/2)
            bot = self.y + int(self.eagleaoe/2)
            left = self.x + self.eaglerange - int(self.eagleaoe/2)
            right = self.x + self.eaglerange + int(self.eagleaoe/2)
        elif(self.lastmoved == 'A'):
            up = self.y - int(self.eagleaoe/2)
            bot = self.y + int(self.eagleaoe/2)
            left = self.x - self.eaglerange - int(self.eagleaoe/2)
            right = self.x - self.eaglerange + int(self.eagleaoe/2)

        self.attackedeagle = 1
        game_map.render()
        time.sleep(0.1)

        for obj in game_map.objects:
            if(((obj.topleftx <= left and obj.topleftx + obj.width >= left) or (obj.topleftx >= left and obj.topleftx <= right)) and ((obj.toplefty <= up and obj.toplefty + obj.height >= up) or (obj.toplefty >= up and obj.toplefty <= bot))):
                obj.attacked = 1
                obj.curhealth -= self.damage
        
        for w in game_map.walls:
            if(w.x >= left and w.x <= right and w.y >= up and w.y <= bot):
                w.attacked = 1
                w.curhealth -= self.damage

        for cn in game_map.cannons:
            if(((cn.topleftx <= left and cn.topleftx + cn.width >= left) or (cn.topleftx >= left and cn.topleftx <= right)) and ((cn.toplefty <= up and cn.toplefty + cn.height >= up) or (cn.toplefty >= up and cn.toplefty <= bot))):
                cn.attacked = 1
                cn.curhealth -= self.damage

        for tw in game_map.towers:
            if(((tw.topleftx <= left and tw.topleftx + tw.width >= left) or (tw.topleftx >= left and tw.topleftx <= right)) and ((tw.toplefty <= up and tw.toplefty + tw.height >= up) or (tw.toplefty >= up and tw.toplefty <= bot))):
                tw.attacked = 1
                tw.curhealth -= self.damage
        
class King(Player):
    def __init__(self):
        self.grid = np.array([['K']])
        super().__init__(90, 48, 100.0, 30, self.grid)

    def move_up(self, game_map):
        if(game_map.rage == 1):
            if(self.y >= 5 and game_map.grid[self.y - 1][self.x] == ' '):
                if(game_map.grid[self.y - 2][self.x] == ' '):
                    self.y -= 2
                else:
                    self.y -= 1
        else:
            if(self.y >= 4 and game_map.grid[self.y - 1][self.x] == ' '):
                    self.y -= 1
    
    def move_left(self, game_map):
        if(game_map.rage == 1):
            if(self.x >= 3 and game_map.grid[self.y][self.x - 1] == ' '):
                if(game_map.grid[self.y][self.x - 2] == ' '):
                    self.x -= 2
                else:
                    self.x -= 1
        else:
            if(self.x >= 2 and game_map.grid[self.y][self.x - 1] == ' '):
                    self.x -= 1
    
    def move_right(self, game_map):
        if(game_map.rage == 1):
            if(self.x <= game_map.columns-3 and game_map.grid[self.y][self.x + 1] == ' '):
                if(game_map.grid[self.y][self.x + 2] == ' '):
                    self.x += 2
                else:
                    self.x += 1 
        else:
            if(self.x <= game_map.columns-2 and game_map.grid[self.y][self.x + 1] == ' '):
                    self.x += 1

    def move_down(self, game_map):
        if(game_map.rage == 1):
            if(self.y <= game_map.rows-3 and game_map.grid[self.y + 1][self.x] == ' '):
                if(game_map.grid[self.y + 2][self.x] == ' '):
                    self.y += 2
                else:
                    self.y += 1
        else:
            if(self.y <= game_map.rows-2 and game_map.grid[self.y + 1][self.x] == ' '):
                self.y += 1

class barbarian(Player):
    def __init__(self, x, y):
        self.obj = 0
        self.grid = np.array([['T']])
        super().__init__(x, y, 50, 10, self.grid)

    def move(self, game_map):
        min_dist = 10000
        min_obj = 0
        for obj in game_map.objects:
            dist = abs(self.x - obj.centerx) + abs(self.y - obj.centery)
            if(dist < min_dist):
                min_dist = dist
                min_obj = obj
        
        for cn in game_map.cannons:
            dist = abs(self.x - cn.centerx) + abs(self.y - cn.centery)
            if(dist < min_dist):
                min_dist = dist
                min_obj = cn
        
        for tw in game_map.towers:
            dist = abs(self.x - tw.centerx) + abs(self.y - tw.centery)
            if(dist < min_dist):
                min_dist = dist
                min_obj = tw
        
        if(min_obj == 0):
            return
        self.obj = min_obj

        if(min_obj.toplefty + min_obj.height < self.y):
            if(check_wall(game_map.grid[self.y - 1][self.x])):
                if(game_map.grid[self.y - 1][self.x] != ' '):
                    self.attack_wall(game_map)
            else:
                self.y -= 1
        elif(min_obj.toplefty - 1 > self.y): 
            if(check_wall(game_map.grid[self.y + 1][self.x])):
                if(game_map.grid[self.y + 1][self.x] != ' '):
                    self.attack_wall(game_map)
            else:
                self.y += 1
        else:
            if(min_obj.topleftx + min_obj.width < self.x):
                if(check_wall(game_map.grid[self.y][self.x - 1])):
                    if(game_map.grid[self.y][self.x - 1] != ' '):
                        self.attack_wall(game_map)
                else:
                    self.x -= 1
            elif(min_obj.topleftx - 1 > self.x):
                if(check_wall(game_map.grid[self.y][self.x + 1])):
                    if(game_map.grid[self.y][self.x + 1] != ' '):
                        self.attack_wall(game_map)
                else:
                    self.x += 1
            elif(min_obj.topleftx - 1 == self.x and min_obj.toplefty - 1 == self.y):
                self.x += 1
            elif(min_obj.topleftx - 1 == self.x and min_obj.toplefty + min_obj.height == self.y):
                self.x += 1
            elif(min_obj.topleftx + min_obj.width == self.x and min_obj.toplefty - 1 == self.y):
                self.x -= 1
            elif(min_obj.topleftx + min_obj.width == self.x and min_obj.toplefty + min_obj.height == self.y):
                self.x -= 1

    def attack_wall(self, game_map):
        for w in game_map.walls:
            if(w.x == self.x):
                if(w.y == self.y + 1 or w.y == self.y - 1):
                    w.attacked = 1
                    game_map.render()
                    time.sleep(0.1)
                    w.curhealth -= self.damage
                    break

        
        for w in game_map.walls:
            if(w.y == self.y):
                if(w.x == self.x + 1 or w.x == self.x - 1):
                    w.attacked = 1
                    game_map.render()
                    time.sleep(0.1)
                    w.curhealth -= self.damage
                    break     

    def attack(self, game_map):

        if((self.obj.toplefty == self.y + 1 or self.obj.toplefty + self.obj.height == self.y) and self.obj.topleftx <= self.x and self.obj.topleftx + self.obj.width -1 >= self.x):
            self.obj.attacked = 1
            game_map.render()
            time.sleep(0.1)
            self.obj.curhealth -= self.damage
        
        if((self.obj.topleftx == self.x + 1 or self.obj.topleftx + self.obj.width == self.x) and self.obj.toplefty <= self.y and self.obj.toplefty + self.obj.height - 1 >= self.y):
            self.obj.attacked = 1
            game_map.render()
            time.sleep(0.1)
            self.obj.curhealth -= self.damage
    
class Archer(Player):
    def __init__(self, x, y):
        self.obj = 0
        self.grid = np.array([['A']])
        self.range = 8
        super().__init__(x, y, 25, 5, self.grid)

    def move(self, game_map):
            if(self.obj.topleftx > self.x):
                if(check_wall(game_map.grid[self.y][self.x + 2]) or check_wall(game_map.grid[self.y][self.x + 1])):
                    self.attack_wall(game_map)
                else:
                    self.x += 2
            elif(self.obj.topleftx + self.obj.width < self.x ):
                if(check_wall(game_map.grid[self.y][self.x - 2]) or check_wall(game_map.grid[self.y][self.x - 1])):
                    self.attack_wall(game_map)
                else:
                    self.x -= 2
            elif(self.obj.topleftx <= self.x and self.obj.topleftx + self.obj.width >= self.x):
                if(self.obj.toplefty > self.y):
                    if(check_wall(game_map.grid[self.y + 2][self.x]) or check_wall(game_map.grid[self.y + 1][self.x])):
                        self.attack_wall(game_map)
                    else:
                        self.y += 2
                elif(self.obj.toplefty + self.obj.height < self.y):
                    if(check_wall(game_map.grid[self.y - 2][self.x]) or check_wall(game_map.grid[self.y - 1][self.x])):
                        self.attack_wall(game_map)
                    else:
                        self.y -= 2
            
    def attack_wall(self, game_map):
        for w in game_map.walls:
            if(w.x == self.x):
                if(w.y == self.y + 1 or w.y == self.y - 1 or w.y == self.y + 2 or w.y == self.y - 2):
                    w.attacked = 1
                    game_map.render()
                    time.sleep(0.1)
                    w.curhealth -= self.damage
                    break

        
        for w in game_map.walls:
            if(w.y == self.y):
                if(w.x == self.x + 1 or w.x == self.x - 1 or w.x == self.x + 2 or w.x == self.x - 2):
                    w.attacked = 1
                    game_map.render()
                    time.sleep(0.1)
                    w.curhealth -= self.damage
                    break   
      
    def attack(self, game_map):
        min_dist = 10000
        min_obj = 0
        for obj in game_map.objects:
            dist = abs(self.x - obj.centerx) + abs(self.y - obj.centery)
            if(dist < min_dist):
                min_dist = dist
                min_obj = obj
        
        for cn in game_map.cannons:
            dist = abs(self.x - cn.centerx) + abs(self.y - cn.centery)
            if(dist < min_dist):
                min_dist = dist
                min_obj = cn
        
        for tw in game_map.towers:
            dist = abs(self.x - tw.centerx) + abs(self.y - tw.centery)
            if(dist < min_dist):
                min_dist = dist
                min_obj = tw

        if(min_obj == 0):
            return
        
        self.obj = min_obj
        if(min_dist <= self.range):
            self.obj.attacked = 1
            game_map.render()
            time.sleep(0.2)
            self.obj.curhealth -= self.damage
        else:
            self.move(game_map)

class Balloon(Player):
    
    def __init__(self, x, y):
        self.obj = 0
        self.grid = np.array([['B']])
        super().__init__(x, y, 50, 20, self.grid)

    def move(self):

        if(self.obj.topleftx > self.x):
            self.x += 2
        elif(self.obj.topleftx + self.obj.width < self.x ):
            self.x -= 2
        elif(self.obj.topleftx <= self.x and self.obj.topleftx + self.obj.width >= self.x):
            if(self.obj.toplefty >= self.y):
                self.y += 2
            elif(self.obj.toplefty + self.obj.height <= self.y):
                self.y -= 2


    
    def attack(self, game_map):

        min_dist = 1000
        min_obj = 0

        for cn in game_map.cannons:
            dist = abs(self.x - cn.centerx) + abs(self.y - cn.centery)
            if(dist < min_dist):
                min_dist = dist
                min_obj = cn
        
        for tw in game_map.towers:
            dist = abs(self.x - tw.centerx) + abs(self.y - tw.centery)
            if(dist < min_dist):
                min_dist = dist
                min_obj = tw
      
        if(min_obj == 0):
            for obj in game_map.objects:
                dist = abs(self.x - obj.centerx) + abs(self.y - obj.centery)
                if(dist < min_dist):
                    min_dist = dist
                    min_obj = obj

        self.obj = min_obj

        if(((self.obj.topleftx <= self.x and self.obj.topleftx + self.obj.width >= self.x)) and ((self.obj.toplefty <= self.y and self.obj.toplefty + self.obj.height >= self.y))):
                self.obj.attacked = 1
                self.obj.curhealth -= self.damage
        else:
            self.move()
        
       
       
    