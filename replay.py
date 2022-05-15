from ast import For
from termios import TCIOFLUSH, tcflush
import numpy as np
import colorama
import sys
import os
import tty

sys.path.insert(0, './src')
from src.gamemap import game_map
from src.input import input_to
from src.object import cannon, hut, townhall, wall
from src.player import *
colorama.init()

from colorama import Fore, Back, Style
import time
import json

gameno = input("Enter game no: ")

replayfile = open("./replays/replay" + str(gameno) + ".json", 'r')
replayfulldata = json.loads(replayfile.read())
player = replayfulldata["player"]
replaydict = replayfulldata["replaydata"]
dictidx = 0
offset = 3
n = 50 + offset
m = 180


king = King()
queen = ArcherQueen()
globaltime2 = time.time()
timeelapsed = 0

map = game_map(n, m, offset)
map.setup_level(1, player)

tty.setcbreak(sys.stdin)
input = input_to()
input.hide_cursor()
itrarr = []
eagle_attack = 0
globaltime = time.time()
while(dictidx < len(replaydict)):
    itr = time.time() - globaltime - replaydict[dictidx]["timestamp"]
    
    if(itr >= 0.0 and itr <= 1.0):
        if(replaydict[dictidx]["keypress"] == 'e'):
            eagle_attack = 1
        else:
            map.handle_input(replaydict[dictidx]["keypress"])
        dictidx += 1
    elif(itr >= 0.0  and itr <= 2.0):
        if(replaydict[dictidx]["keypress"] == 'e'):
            eagle_attack = 1
        else:
            map.handle_input(replaydict[dictidx]["keypress"])
        dictidx += 1
        

    if(map.check_win()):
        if(map.level < 3):
            map.level += 1
            map.clear_map()
            map.setup_level(map.level, player)
        else:
            map.display_win()
            break

    if(map.check_lose()):
        map.display_lose()
        break

    for j in range(offset):
            for i in range(map.columns):
                map.grid[j][i] = ' '
    healthbar = ""
    steps = int(map.player.curhealth/10)
    for i in range(steps):
        healthbar += '█'
    for i in range(steps, 10):
        healthbar += ' '
    if(player == 'K'):
        if(map.player.curhealth > 0.0):
            info = "KING'S HEALTH = " + str(map.player.curhealth) +"    " + healthbar + "              TIME: " + str(timeelapsed) + "         LEVEL: " + str(map.level)
        else:
            info = "KING'S HEALTH = " + str(0) +"    " + healthbar + "              TIME: " + str(timeelapsed) + "         LEVEL: " + str(map.level)
    else:
        if(map.player.curhealth > 0.0):
            info = "QUEEN'S HEALTH = " + str(map.player.curhealth) +"    " + healthbar + "              TIME: " + str(timeelapsed) + "         LEVEL: " + str(map.level)
        else:
            info = "QUEEN'S HEALTH = " + str(0) +"    " + healthbar + "              TIME: " + str(timeelapsed) + "         LEVEL: " + str(map.level)
    for j in range(len(info), map.columns):
        info +=  ' '

    

    info += "TROOPS: "
    idx = 1

    for tr in map.troops:
        info += "B" + str(idx) + " H:" + str(tr.curhealth) + " | "
        idx += 1

    idx = 1
    for ar in map.archers:
        info += "A" + str(idx) + " H:" + str(ar.curhealth) + " | "
        idx += 1

    idx = 1
    for bl in map.balloons:
        info += "B" + str(idx) + " H:" + str(bl.curhealth) + " | "
        idx += 1

    for i in range(len(info), 2*map.columns):
        info += ' '
    

    info += "DEFENSIVE BUILDINGS: "

    idx = 1
    for cn in map.cannons:
        info += "C" + str(idx) + " H:" + str(cn.curhealth) + " | "
        idx += 1
    
    idx = 1
    for tw in map.towers:
        info += "W" + str(idx) + " H:" + str(tw.curhealth) + " | "
        idx += 1

    for i in range(len(info), 3*map.columns):
        info += ' '
    
    for i in range(map.columns):
        map.grid[0][i] = Fore.BLUE + info[i]
        map.grid[1][i] = Fore.BLUE + info[map.columns + i]
        map.grid[2][i] = Fore.BLUE + info[2*map.columns + i]

    
    map.render()

    if((time.time() - globaltime2 - timeelapsed) >= 1.00):
        if(eagle_attack):
            if(map.playerType == 'Q'):
                map.player.attack_eagle_arrow(map)
                eagle_attack = 0
        for tr in map.troops:
            tr.move(map)
            tr.attack(map)
        for cn in map.cannons:
            cn.attack(map)
        for ar in map.archers:
            ar.attack(map)
        for bl in map.balloons:
            bl.attack(map)
        for tw in map.towers:
            tw.attack(map)
        timeelapsed += 1

    
if(map.check_win()):
        if(map.level < 3):
            map.level += 1
            map.clear_map()
            map.setup_level(map.level, player)
        else:
            map.display_win()
            

if(map.check_lose()):
    map.display_lose()