#Mario Shontz/MES19F
#ISC 4304C
#Due 03/03/23
#Lab 4: Conway's Game of life
    
#!/usr/bin/env/ Python3



from config import Config
try:
    from IPython.display import clear_output
    IPY = 1
except:
    IPY = 0
import sys
import os
import random
import math
import time
   
CELL_CHAR = chr(0x25A0)
MAX_TIME = 200 #seconds

class Game(object):
    def __init__(self,size=int(50), starting_obj = 'glider'):
        self.size = size
        self.cell = chr(0x25A0) #black square
        self.grid = []
        self.alive_cells = []
        self.local_dead_cells = []
        
        for Y in range(self.size): # (size)x(size) matrix of dead cells
            self.grid.append([])
            for X in range(self.size):
                self.grid[Y].append(Cell(self,X,Y,alive=0)) #input cells into matrix
        
        if starting_obj == 'glider':
            coordX = self.size//2 - 3
            coordY = self.size//2 - 3 
            Glider = Config('glider')
            self.add_obj(Glider,coordX,coordY)
        if starting_obj == 'glider_gun':
            coordX = 5
            coordY = self.size//2
            GG = Config('glider_gun')
            self.add_obj(GG,coordX,coordY)

            
        self.first_update() #get neighbors once all cells added

    def add_obj(self,obj,coordX,coordY):
        for Y in range(len(obj.config)):
                for X in range(len(obj.config[Y])):
                    self.grid[coordY+Y][coordX+X].change_status(obj.config[Y][X]) #if 1, updates to alive

    def first_update(self): #lists of alive and nearby dead cells
        for Y in range(self.size):
                for X in range(self.size):
                    self.grid[Y][X].get_neighbors()
                    if self.grid[Y][X].alive:
                        self.alive_cells.append(self.grid[Y][X])
                        # print("in local cells loop:")
                        for local in self.grid[Y][X].local_cells:
                            if not local.alive and not local.checked:
                                self.local_dead_cells.append(local)
                                local.checked = 1
                                # print(f'local_cell {k.X},{k.Y}, status - {k.alive}, next_state = {k.next}')
        print(self)

    def update_local_dead_cells(self):
        for alive in self.alive_cells:
            alive.update_neighbors()
            for local in alive.local_cells:
                if not local.alive and not local.checked:
                    self.local_dead_cells.append(local)
                    local.update_neighbors()
                    local.checked = 1
                    
    def evolve(self):
        new_alive = []
        # print("In alive loop")
        for alive in self.alive_cells:
            # print(f'alive: indices - {alive.X},{alive.Y}, status - {alive.alive}, next_state = {alive.next}')
            if (next_status := alive.move()): #moves and checks next status
                new_alive.append(alive)
            alive.checked = 0
        
        # print("In dead cells loop")
        for dead in self.local_dead_cells:
            # print(f'dead: indices - {dead.X},{dead.Y}, status - {dead.alive}, next_state = {dead.next}')
            if (next_status := dead.move()):
                new_alive.append(dead)
            dead.checked = 0
        print(self)

        self.alive_cells = new_alive

        if len(self.alive_cells) == 0:
            return 0

        self.local_dead_cells.clear()
        self.update_local_dead_cells()
        return 1

    def run(self,tick_rate):
        start_time = time.time()
        frame = 1/tick_rate
        time_of_last_iteration = start_time
        while(True):
            if time.time() - start_time < MAX_TIME and time.time() - time_of_last_iteration < frame:
                time.sleep(time_of_last_iteration+frame-time.time())
                print(f'sleeping for {time_of_last_iteration+frame-time.time()}')
            else:
                if not (alive := self.evolve()):
                    print("All cells are dead")
                    return
                time_of_last_iteration = time.time()
    
    def __str__(self):
        if IPY: #for IPython like Colab
            clear_output()
        elif os.name == 'posix':  # for Linux/Unix/Mac OS
            os.system('clear')
        else:  # for Windows
            os.system('cls')
        output = '\n'.join([' '.join([str(self.grid[i][j]) for j in range(self.size)]) for i in range(self.size)])
        return output
        
class Cell(object):
    def __init__(self,parent,X:int,Y:int,alive=0):
        self.map = parent 
        self.X = X
        self.Y = Y
        self.alive = alive
        self.map_size = self.map.size
        self.checked = 0 #for update methods of map to avoid double-checking

    def get_neighbors(self):
        #define space one square around cell, using torus
        left = self.X-1 if self.X > 0 else self.map_size-1
        right = self.X+1 if self.X < self.map_size-1 else 0
        top = self.Y-1 if self.Y > 0 else self.map_size-1
        bottom = self.Y+1 if self.Y < self.map_size-1 else 0
    
        self.local_cells = [self.map.grid[top][left],self.map.grid[top][self.X],self.map.grid[top][right],
                            self.map.grid[self.Y][left],self.map.grid[self.Y][right], #note: does not include self ([self.Y,self.X]).
                            self.map.grid[bottom][left],self.map.grid[bottom][self.X],self.map.grid[bottom][right]]
        
        self.update_neighbors()
        
    def update_neighbors(self):
        self.neighbors = 0
        for local in self.local_cells:
            if local.alive:
                self.neighbors+=1
        self.get_next_state() 
        # print(f'Cell {self.X},{self.Y}, status = {self.alive}, neighbors = {self.neighbors}, next_state = {self.next}')

    def get_next_state(self): #define Game of Life rules
        if self.neighbors == 3:
            self.next = 1
        elif self.alive and (self.neighbors == 2):
            self.next = 1
        else:
            self.next = 0

    def move(self):
        self.alive = self.next
        return self.alive

    def change_status(self,status):
        self.alive = status

    def __str__(self):
        return CELL_CHAR if self.alive else ' '