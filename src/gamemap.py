from ast import ExtSlice
import time
import numpy as np
from colorama import Fore, Back, Style
from sqlalchemy import false, true
from src.object import *
from src.player import *


class map_object(game_object):
    def __init__(self, game_object, topleftx, toplefty):
        self.topleftx = topleftx
        self.toplefty = toplefty
        self.curhealth = game_object.health
        self.centerx = self.topleftx + int((game_object.width - 1)/2)
        self.centery = self.toplefty + int((game_object.height - 1)/2)
        super().__init__(game_object.grid, game_object.health)

class map_tower(game_object):
    def __init__(self, tower, topleftx, toplefty):
        self.topleftx = topleftx
        self.toplefty = toplefty
        self.curhealth = tower.health
        self.centerx = self.topleftx + int((tower.width - 1)/2)
        self.centery = self.toplefty + int((tower.height - 1)/2)
        self.damage = tower.damage
        self.range = tower.range
        self.attacks = 0
        super().__init__(tower.grid, tower.health)

    def attack_aoe(self, game_map, x, y):

        if(game_map.player.curhealth >= 0.0):
            if(game_map.player.x >= x-1 and game_map.player.x <= x + 1):
                if(game_map.player.y >= y -1 and game_map.player.y <= y + 1):
                    game_map.player.curhealth -= self.damage

        for bln in game_map.balloons:
            if(bln.x >= x - 1 and bln.x <= x + 1):
                if(bln.y >= y - 1 and bln.y <= y + 1):
                    bln.curhealth -= self.damage
                    
        for ar in game_map.archers:
            if(ar.x >= x - 1 and ar.x <= x + 1):
                if(ar.y >= y - 1 and ar.y <= y + 1):
                    ar.curhealth -= self.damage
        
        for tr in game_map.troops:
            if(tr.x >= x - 1 and tr.x <= x + 1):
                if(tr.y >= y - 1 and tr.y <= y + 1):
                    tr.curhealth -= self.damage
        
    def attack(self, game_map):
        att = 0
        if(game_map.player.curhealth >= 0.0):
            dist = abs(self.centerx - game_map.player.x) + abs(self.centery - game_map.player.y)
            if(dist <= self.range):
                self.attack_aoe(game_map, game_map.player.x, game_map.player.y)
                att = 1
        
        if(att == 0):
            for bl in game_map.balloons:
                dist = abs(self.centerx - bl.x) + abs(self.centery - bl.y)
                if(dist <= self.range):
                    self.attack_aoe(game_map, bl.x, bl.y)
                    att = 1
        
        if(att == 0):
            for ar in game_map.archers:
                dist = abs(self.centerx - ar.x) + abs(self.centery - ar.y)
                if(dist < self.range):
                    self.attack_aoe(game_map, ar.x, ar.y)
                    att = 1
        
        if(att == 0):
            for tr in game_map.troops:
                dist = abs(self.centerx - tr.x) + abs(self.centery - tr.y)
                if(dist < self.range):
                    self.attack_aoe(game_map, tr.x, tr.y)
                    att = 1
        
        
        
class map_cannon(game_object):
    def __init__(self, cannon, topleftx, toplefty):
        self.topleftx = topleftx
        self.toplefty = toplefty
        self.curhealth = cannon.health
        self.centerx = self.topleftx + int((cannon.width - 1)/2)
        self.centery = self.toplefty + int((cannon.height - 1)/2)
        self.damage = cannon.damage
        self.range = cannon.range
        self.attacks = 0
        super().__init__(cannon.grid, cannon.health)
    
    def attack(self, game_map):
        att = 0

        if(game_map.player.curhealth >= 0.0):
            dist = abs(self.centerx - game_map.player.x) + abs(self.centery - game_map.player.y)
            if(dist <= self.range):
                game_map.player.curhealth -= self.damage
                att = 1
        
        if(att == 0):
            for tr in game_map.troops:
                dist = abs(self.centerx - tr.x) + abs(self.centery - tr.y)
                if(dist <= self.range):
                    tr.curhealth -= self.damage
                    att = 1
                    break
        
        if(att == 0):
            for ar in game_map.archers:
                dist = abs(self.centerx - ar.x) + abs(self.centery - ar.y)
                if(dist <= self.range):
                    ar.curhealth -= self.damage
                    att = 1
                    break

class map_wall(game_object):
    def __init__(self, wall, x, y):
        self.x = x
        self.y = y
        self.curhealth = wall.health
        super().__init__(wall.grid, wall.health)


class game_map:

    def __init__(self, rows, columns, offset):
        self.rows = rows
        self.columns = columns
        self.grid = np.empty([rows, columns], dtype=object)
        self.objects = np.empty(0, dtype=map_object)
        self.walls = np.empty(0, dtype=map_wall)
        self.cannons = np.empty(0, dtype=map_cannon)
        self.towers = np.empty(0, dtype=WizardTower)
        self.offset = offset
        self.player = 0
        self.playerType = 'K'
        self.troops = np.empty(0, dtype=barbarian)
        self.archers = np.empty(0, dtype=Archer)
        self.balloons = np.empty(0, dtype=Balloon)
        self.rage = 0
        self.heal = 0
        self.level = 1
        self.ntroops = 0
        self.narchers = 0
        self.nballoons = 0
        self.maxtroops = 6
        self.maxarchers = 6
        self.maxballoons = 3
        
    def setup_level(self, level, player):
        self.level = level
        if(player == 'K'):
            self.player = King()
            self.playerType = 'K'
        else:
            self.player = ArcherQueen()
            self.playerType = 'Q'

        
        self.add_object(hut(), 109, 15)
        self.add_object(hut(), 123, 15)
        
        self.add_object(hut(), 54, 35)
        self.add_object(hut(), 68, 35)
        
        

        th = townhall()
        thheight = 6
        thwidth = 14
        thposx = int((self.columns/2) - thwidth/2)
        thposy = int(((self.rows-2)/2) - thheight/2) 
        self.add_object(th, thposx, thposy)

        for i in range(thwidth+4):
            tempwall = wall()
            self.add_wall(tempwall, thposx-2+i, thposy-2)
            self.add_wall(tempwall, thposx-2+i, thposy+thheight+2)
            self.add_wall(tempwall, thposx+thwidth+2, thposy+thheight+2)

        for i in range(thheight+4):
            tempwall = wall()
            self.add_wall(tempwall, thposx-2, thposy-2+i)
            self.add_wall(tempwall, thposx+thwidth+2, thposy-2+i)
        
        if(level >= 1):
            self.add_cannon(cannon(), 60, 25)
            self.add_cannon(cannon(), 115, 25)

            self.add_wizardtower(WizardTower(), 60, 35)
            self.add_wizardtower(WizardTower(), 115, 15)
            

            if(level >= 2):

                self.add_cannon(cannon(), 85, 15)
                self.add_wizardtower(WizardTower(), 60, 15)
                self.add_object(hut(), 68, 15)
                self.add_object(hut(), 54, 15)

                if(level >= 3):

                    self.add_cannon(cannon(), 85, 35)
                    self.add_wizardtower(WizardTower(), 115, 35)
                    self.add_object(hut(), 109, 35)
                    self.add_object(hut(), 123, 35)
        
    def clear_map(self):

        self.objects = np.empty(0, dtype=map_object)
        self.walls = np.empty(0, dtype=map_wall)
        self.cannons = np.empty(0, dtype=map_cannon)
        self.towers = np.empty(0, dtype=WizardTower)
        self.troops = np.empty(0, dtype=barbarian)
        self.archers = np.empty(0, dtype=Archer)
        self.balloons = np.empty(0, dtype=Balloon)
        self.nballoons = 0
        self.ntroops = 0
        self.narchers = 0
        self.rage = 0
        self.heal = 0


    def add_object(self, game_object, topleftx, toplefty):
        temp = map_object(game_object, topleftx, toplefty)
        self.objects = np.append(self.objects, temp)

    def add_wall(self, given_wall, x, y):
        tempwall = map_wall(given_wall, x, y)
        self.walls = np.append(self.walls, tempwall)

    def add_cannon(self, given_cannon, topleftx, toplefty):
        tempcannon = map_cannon(given_cannon, topleftx, toplefty)
        self.cannons = np.append(self.cannons, tempcannon)

    def add_wizardtower(self, giventower, topleftx, toplefty):
        temptower = map_tower(giventower, topleftx, toplefty)
        self.towers = np.append(self.towers, temptower)

    def king_attack(self):
        for obj in self.objects:
            if(obj.toplefty + obj.height - 1 == self.player.y - 1 and obj.topleftx + obj.width - 1 >= self.player.x and obj.topleftx <= self.player.x):
                obj.attacked = 1
                self.render()
                time.sleep(0.2)
                obj.curhealth -= self.player.damage
                break

    def activate_rage(self):
        self.player.damage *= 2
        for tr in self.troops:
            tr.damage *= 2
        self.rage = 1
        

    def activate_heal(self):
        temphealth = self.player.curhealth * 1.5
        if(temphealth > self.player.health):
            self.player.curhealth = 100
        else:
            self.player.curhealth = temphealth
        for tr in self.troops:
            temph = tr.curhealth * 1.5
            if(temph > tr.health):
                tr.curhealth = tr.health
            else:
                tr.curhealth = temph
        for ar in self.archers:
            temph = ar.curhealth * 1.5
            if(temph > ar.health):
                ar.curhealth = ar.health
            else:
                ar.curhealth = temph
        for bl in self.balloons:
            temph = bl.curhealth * 1.5
            if(temph > bl.health):
                bl.curhealth = bl.health
            else:
                bl.curhealth = temph            

        
    def handle_input(self, ch):
        if(ch == 'W' or ch == 'w'):
            self.player.move_up(self)
            self.player.lastmoved = 'W'
        elif(ch == 'A' or ch == 'a'):
            self.player.move_left(self)
            self.player.lastmoved = 'A'
        elif(ch == 'D' or ch == 'd'):
            self.player.move_right(self)
            self.player.lastmoved = 'D'
        elif(ch == 'S' or ch == 's'):
            self.player.move_down(self)
            self.player.lastmoved = 'S'
        elif(ch == ' '):
            self.player.attack(self)
        elif(ch == 'R' or ch == 'r'):
            self.activate_rage()
        elif(ch == 'H' or ch == 'h'):
            self.activate_heal()
        elif(ch == 'P' or ch == 'p'):
            self.spawn_troop(20, 25)
        elif(ch == 'O' or ch == 'o'):
            self.spawn_troop(145, 25)
        elif(ch == 'I' or ch == 'i'):
            self.spawn_troop(20, 15)
        elif(ch == 'U' or ch == 'u'):
            self.spawn_archer(85, 10)
        elif(ch == 'Y' or ch == 'y'):
            self.spawn_archer(85, 40)
        elif(ch == 'T' or ch == 't'):
            self.spawn_archer(145, 35)
        elif(ch == 'L' or ch == 'l'):
            self.spawn_balloon(60, 23)
        elif(ch == 'K' or ch == 'k'):
            self.spawn_balloon(115, 23)
        elif(ch == 'J' or ch == 'j'):
            self.spawn_balloon(80, 35)

    def spawn_balloon(self, x, y):
        if(self.nballoons >= self.maxballoons):
            return
        else:
            self.nballoons += 1
            self.balloons = np.append(self.balloons, Balloon(x, y))

    def spawn_archer(self, x, y):
        if(self.narchers >= self.maxarchers):
            return
        else:
            self.narchers += 1
            self.archers = np.append(self.archers, Archer(x, y))

    def spawn_troop(self, x, y):
        if(self.ntroops >= self.maxtroops):
            return
        else:
            self.ntroops += 1
            self.troops = np.append(self.troops, barbarian(x, y))

    def update(self):
        for tr in self.troops:
            tr.move()
            tr.attack()

    def show_aoe(self):
        lastmoved = self.player.lastmoved
        aoe = self.player.aoe
        rangeplayer = self.player.range
        curx = self.player.x
        cury = self.player.y

        rangeplayere = self.player.eaglerange
        aoee = self.player.eagleaoe

        if(lastmoved == 'W'):
            if(self.player.attackedeagle):
                up = cury - rangeplayere - int(aoee/2)
                bot = cury - rangeplayere + int(aoee/2)
                left = curx - int(aoee/2)
                right = curx + int(aoee/2)
            else:
                up = cury - rangeplayer - int(aoe/2)
                bot = cury - rangeplayer + int(aoe/2)
                left = curx - int(aoe/2)
                right = curx + int(aoe/2)
        elif(lastmoved == 'S'):
            if(self.player.attackedeagle):
                up = cury + rangeplayere - int(aoee/2)
                bot = cury + rangeplayere + int(aoee/2)
                left = curx - int(aoee/2)
                right = curx + int(aoee/2)
            else:
                up = cury + rangeplayer - int(aoe/2)
                bot = cury + rangeplayer + int(aoe/2)
                left = curx - int(aoe/2)
                right = curx + int(aoe/2)
        elif(lastmoved == 'D'):
            if(self.player.attackedeagle):
                up = cury - int(aoee/2)
                bot = cury + int(aoee/2)
                left = curx + rangeplayere - int(aoee/2)
                right = curx + rangeplayere + int(aoee/2)
            else:
                up = cury - int(aoe/2)
                bot = cury + int(aoe/2)
                left = curx + rangeplayer - int(aoe/2)
                right = curx + rangeplayer + int(aoe/2)
        elif(lastmoved == 'A'):
            if(self.player.attackedeagle):
                up = cury - int(aoee/2)
                bot = cury + int(aoee/2)
                left = curx - rangeplayere - int(aoee/2)
                right = curx - rangeplayere + int(aoee/2)
            else:
                up = cury - int(aoe/2)
                bot = cury + int(aoe/2)
                left = curx - rangeplayer - int(aoe/2)
                right = curx - rangeplayer + int(aoe/2)

        if(up >= self.rows):
            return

        if(left >= self.columns):
            return

        if(bot >= self.rows):
            bot = self.rows - 1
        
        if(right >= self.columns):
            right = self.columns - 1

        for j in range(left, right+1):
            self.grid[up][j] = Fore.MAGENTA + '‾'
            self.grid[bot][j] = Fore.MAGENTA + '_'
        
        for i in range(up, bot+1):
            self.grid[i][left] = Fore.MAGENTA + '|'
            self.grid[i][right] = Fore.MAGENTA + '|'

    def render(self):

        for i in range(self.offset, self.rows):
            self.grid[i][0] = Fore.MAGENTA + '|'
            self.grid[i][self.columns-1] = Fore.MAGENTA + '|'

        for i in range(self.columns):
            self.grid[self.offset][i] = Fore.MAGENTA + '-'
            self.grid[self.rows-1][i] = Fore.MAGENTA + '-'

        for i in range(self.offset+1, self.rows-1):
            for j in range(1, self.columns-1):
                self.grid[i][j] = ' '

        for obj in self.objects:
            if(obj.health <= 0.0):
                idx = np.where(self.objects == obj)
                self.objects = np.delete(self.objects, idx)

        for obj in self.objects:
            if(obj.curhealth > 0.0):
                if(obj.attacked == 1):
                    obj.attacked = 0
                    for i in range(obj.height):
                        for j in range(obj.width):
                            self.grid[obj.toplefty + i][obj.topleftx + j] = Fore.MAGENTA + obj.grid[i][j]
                    continue
                for i in range(obj.height):
                    for j in range(obj.width):
                        if(obj.curhealth/obj.health >= 0.5):
                            self.grid[obj.toplefty + i][obj.topleftx + j] = Fore.GREEN + obj.grid[i][j]
                        elif(obj.curhealth/obj.health >= 0.2):
                            self.grid[obj.toplefty + i][obj.topleftx + j] = Fore.YELLOW + obj.grid[i][j]
                        else:
                            self.grid[obj.toplefty + i][obj.topleftx + j] = Fore.RED + obj.grid[i][j]
            else:
                idx = np.where(self.objects == obj)
                self.objects = np.delete(self.objects, idx)
        
        for cn in self.cannons:
            if(cn.curhealth > 0.0):
                if(cn.attacked == 1):
                    cn.attacked = 0
                    for i in range(cn.height):
                        for j in range(cn.width):
                            self.grid[cn.toplefty + i][cn.topleftx + j] = Fore.MAGENTA + cn.grid[i][j]
                    continue
                for i in range(cn.height):
                    for j in range(cn.width):
                        if(cn.curhealth/cn.health >= 0.5):
                            self.grid[cn.toplefty + i][cn.topleftx + j] = Fore.GREEN + cn.grid[i][j]
                        elif(cn.curhealth/cn.health >= 0.2):
                            self.grid[cn.toplefty + i][cn.topleftx + j] = Fore.YELLOW + cn.grid[i][j]
                        else:
                            self.grid[cn.toplefty + i][cn.topleftx + j] = Fore.RED + cn.grid[i][j]
            else:
                idx = np.where(self.cannons == cn)
                self.cannons = np.delete(self.cannons, idx)

        for tw in self.towers:
            if(tw.curhealth > 0.0):
                if(tw.attacked == 1):
                    tw.attacked = 0
                    for i in range(tw.height):
                        for j in range(tw.width):
                            self.grid[tw.toplefty + i][tw.topleftx + j] = Fore.MAGENTA + tw.grid[i][j]
                    continue
                for i in range(tw.height):
                    for j in range(tw.width):
                        if(tw.curhealth/tw.health >= 0.5):
                            self.grid[tw.toplefty + i][tw.topleftx + j] = Fore.GREEN + tw.grid[i][j]
                        elif(tw.curhealth/tw.health >= 0.2):
                            self.grid[tw.toplefty + i][tw.topleftx + j] = Fore.YELLOW + tw.grid[i][j]
                        else:
                            self.grid[tw.toplefty + i][tw.topleftx + j] = Fore.RED + tw.grid[i][j]
            else:
                idx = np.where(self.towers == tw)
                self.towers = np.delete(self.towers, idx)
        
        for w in self.walls:
            if(w.curhealth >= 0.0):
                if(w.attacked == 1):
                    w.attacked = 0
                    self.grid[w.y][w.x] = Fore.MAGENTA + w.grid[0][0]
                    continue
                if(w.curhealth/w.health >= 0.5):
                    self.grid[w.y][w.x] = Fore.GREEN + w.grid[0][0]
                elif(w.curhealth/w.health >= 0.2):
                    self.grid[w.y][w.x] = Fore.YELLOW + w.grid[0][0]
                else:
                    self.grid[w.y][w.x] = Fore.RED + w.grid[0][0]
            else:
                idx = np.where(self.walls == w)
                self.walls = np.delete(self.walls, idx)
        
        if(self.player.curhealth > 0.0):
            self.grid[self.player.y][self.player.x] = Fore.CYAN + self.player.grid[0][0]

        for tr in self.troops:
            if(tr.curhealth > 0.0):
                if(tr.curhealth/tr.health >= 0.5):
                    self.grid[tr.y][tr.x] = Fore.GREEN + tr.grid[0][0]
                elif(tr.curhealth/tr.health >= 0.2):
                    self.grid[tr.y][tr.x] = Fore.YELLOW + tr.grid[0][0]
                else:
                    self.grid[tr.y][tr.x] = Fore.RED + tr.grid[0][0]
            else:
                idx = np.where(self.troops == tr)
                self.troops = np.delete(self.troops, idx)

        for ar in self.archers:
            if(ar.curhealth > 0.0):
                if(ar.curhealth/ar.health >= 0.5):
                    self.grid[ar.y][ar.x] = Fore.GREEN + ar.grid[0][0]
                elif(ar.curhealth/ar.health >= 0.2):
                    self.grid[ar.y][ar.x] = Fore.YELLOW + ar.grid[0][0]
                else:
                    self.grid[ar.y][ar.x] = Fore.RED + ar.grid[0][0]
            else:
                idx = np.where(self.archers == ar)
                self.archers = np.delete(self.archers, idx)
        
        for bl in self.balloons:
            if(bl.curhealth > 0.0):
                if(bl.curhealth/bl.health >= 0.5):
                    self.grid[bl.y][bl.x] = Fore.GREEN + bl.grid[0][0]
                elif(bl.curhealth/bl.health >= 0.2):
                    self.grid[bl.y][bl.x] = Fore.YELLOW + bl.grid[0][0]
                else:
                    self.grid[bl.y][bl.x] = Fore.RED + bl.grid[0][0]
            else:
                idx = np.where(self.balloons == bl)
                self.balloons = np.delete(self.balloons, idx)

        if(self.playerType == 'Q'):
            if(self.player.attacked == 1):
                self.player.attacked = 0
                self.show_aoe()

        if(self.playerType == 'Q'):    
            if(self.player.attackedeagle == 1):
                self.show_aoe()
                self.player.attackedeagle = 0
        
        outputstr = ""
        for i in range(self.rows):
            for j in range(self.columns):
                outputstr += Back.BLACK + self.grid[i][j]
            outputstr += "\n"

        print('\033[H' + outputstr)

    def check_win(self):
        objects_left = np.shape(self.objects)
        cannons_left = np.shape(self.cannons)
        towers_left = np.shape(self.towers)
        if(objects_left[0] == 0 and cannons_left[0] == 0 and towers_left[0] == 0):
            return True
        else:
            return False

    def display_win(self):
        win = """
             .----------------.  .----------------.  .-----------------.
            | .--------------. || .--------------. || .--------------. |
            | | _____  _____ | || |     _____    | || | ____  _____  | |
            | ||_   _||_   _|| || |    |_   _|   | || ||_   \|_   _| | |
            | |  | | /\ | |  | || |      | |     | || |  |   \ | |   | |
            | |  | |/  \| |  | || |      | |     | || |  | |\ \| |   | |
            | |  |   /\   |  | || |     _| |_    | || | _| |_\   |_  | |
            | |  |__/  \__|  | || |    |_____|   | || ||_____|\____| | |
            | |              | || |              | || |              | |
            | '--------------' || '--------------' || '--------------' |
            '----------------'  '----------------'  '----------------' 
        """
        print('\033c', end="")
        print(Fore.GREEN + Back.BLACK + win)

    def check_lose(self):
        if(self.player.curhealth <= 0.0):
            if(self.ntroops < self.maxtroops):
                return False
            if(self.narchers < self.maxarchers):
                return False
            if(self.nballoons < self.maxballoons):
                return False
            for tr in self.troops:
                if(tr.curhealth > 0.0):
                    return False
            for ar in self.archers:
                if(ar.curhealth > 0.0):
                    return False
            for bl in self.balloons:
                if(bl.curhealth > 0.0):
                    return False
            return True
        else:
            return False

    def display_lose(self):
        lose = """
            .----------------.  .----------------.  .----------------.  .----------------. 
            | .--------------. || .--------------. || .--------------. || .--------------. |
            | |   _____      | || |     ____     | || |    _______   | || |  _________   | |
            | |  |_   _|     | || |   .'    `.   | || |   /  ___  |  | || | |_   ___  |  | |
            | |    | |       | || |  /  .--.  \  | || |  |  (__ \_|  | || |   | |_  \_|  | |
            | |    | |   _   | || |  | |    | |  | || |   '.___`-.   | || |   |  _|  _   | |
            | |   _| |__/ |  | || |  \  `--'  /  | || |  |`\____) |  | || |  _| |___/ |  | |
            | |  |________|  | || |   `.____.'   | || |  |_______.'  | || | |_________|  | |
            | |              | || |              | || |              | || |              | |
            | '--------------' || '--------------' || '--------------' || '--------------' |
            '----------------'  '----------------'  '----------------'  '----------------' 
        """
        print('\033c', end="")
        print(Fore.RED + Back.BLACK + lose)

        """
             _____
            |     |_____|
            |     |     |
            |     |
            |     |
            |_____|
        """