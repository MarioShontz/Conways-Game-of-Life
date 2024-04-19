# -*- coding: utf-8 -*-

#Mario Shontz/MES19F
#ISC 4304C
#Due 03/03/23
#Lab 4: Conway's Game of life
    
#!/usr/bin/env/ Python3

from game import Game
import sys

def main():
    if len(sys.argv) > 2:
        raise Exception("Only one option allowed")
    elif sys.argv[1] == 'glider':
        GameOfLife = Game(starting_obj = 'glider')
    elif sys.argv[1] == 'glider_gun':
        GameOfLife = Game(starting_obj = 'glider_gun')
    else:
        print("No starting object. Nothing will happen!")
    tick_rate = 1 #per second
    GameOfLife.run(tick_rate)
    


if __name__ == "__main__":
    main()