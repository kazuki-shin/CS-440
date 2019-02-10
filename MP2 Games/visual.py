#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import numpy as np
import instances
from solve import solve
import random
import time
    
def get_pent_idx(pent):
    """
    Returns the index of a pentomino.
    """
    pidx = 0
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if pent[i][j] != 0:
                pidx = pent[i][j]
                break
        if pidx != 0:
            break
    if pidx == 0:
        return -1
    return pidx - 1
        
def is_pentomino(pent, pents):
    """
    Checks if a pentomino pent is part of pents
    """
    pidx = get_pent_idx(pent)
    if pidx == -1:
        return False
    true_pent = pents[pidx]
    
    for flipnum in range(3):
        p = np.copy(pent)
        if flipnum > 0:
            p = np.flip(pent, flipnum-1)
        for rot_num in range(4):
            if np.array_equal(true_pent, p):
                return True
            p = np.rot90(p)
    return False
                        
def add_pentomino(board, pent, coord, check_pent=False, valid_pents=None):
    """
    Adds a pentomino pent to the board. The pentomino will be placed such that
    coord[0] is the lowest row index of the pent and coord[1] is the lowest 
    column index. 
    
    check_pent will also check if the pentomino is part of the valid pentominos.
    """
    if check_pent and not is_pentomino(pent, valid_pents):
        return False
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                if board[coord[0]+row][coord[1]+col] != 0: # Overlap
                    return False
                else:
                    board[coord[0]+row][coord[1]+col] = pent[row][col]
    return True
    
def remove_pentomino(board, pent_idx):
    board[board==pent_idx+1] = 0
        
def check_correctness(sol_list, board, pents):
    """
    Sol is a list of pentominos (possibly rotated) and their upper left coordinate
    """
    # All tiles used
    if len(sol_list) != len(pents):
        return False
    # Construct board
    sol_board = np.zeros(board.shape)
    seen_pents = [0]*len(pents)
    for pent, coord in sol_list:
        pidx = get_pent_idx(pent)
        if seen_pents[pidx] != 0:
            return False
        else:
            seen_pents[pidx] = 1
        if not add_pentomino(sol_board, pent, coord, True, pents): 
            return False
            
    # Check same number of squares occupied
    if np.count_nonzero(board) != np.count_nonzero(sol_board):
        return False
    # Check overlap
    if np.count_nonzero(board) != np.count_nonzero(np.multiply(board, sol_board)):
        return False
    
    return True
        

class Application:
    def __init__(self, scale=20, fps=30):
        self.running = True
        self.displaySurface = None
        self.scale = scale
        self.fps = fps
        self.windowTitle = "CS440 MP2"
    
    # Initializes the pygame context and certain properties of the maze
    def initialize(self, board, pentominos):
        self.gridDim = board.shape
        self.pentominos = pentominos
        self.board = board
        self.windowHeight = self.gridDim[0] * self.scale
        self.windowWidth = self.gridDim[1] * self.scale

        self.blockSizeX = int(self.windowWidth / self.gridDim[1])
        self.blockSizeY = int(self.windowHeight / self.gridDim[0])

    # Simple wrapper for drawing a wall as a rectangle
    def drawWall(self, row, col):
        self.drawColorBlock(row, col, (0, 0, 0))

    # Simple wrapper for drawing a tile as a rectangle
    def drawTile(self, row, col):
        self.drawColorBlock(row, col, (255, 255, 255))

    def drawColorBlock(self, row, col, fill_col):
        pygame.draw.rect(self.displaySurface, fill_col, (col * self.blockSizeX, row * self.blockSizeY, self.blockSizeX, self.blockSizeY), 0)

    def draw_board(self):
        for row in range(self.gridDim[0]):
            for col in range(self.gridDim[1]):
                if self.board[row][col] == 0:
                    self.drawWall(row, col)
                else:
                    self.drawTile(row, col)


    def draw_solution_and_sleep(self, pents, slp):
        random.seed(3)
        self.draw_board()
        for idx, p in enumerate(pents):
            shape = p[0]
            shape_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            offset = p[1]
            for row in range(len(shape)):
                for col in range(len(shape[row])):
                    if shape[row][col] != 0:
                        self.drawColorBlock(row + offset[0], col + offset[1], shape_color)
            pygame.display.flip()
        time.sleep(slp)


    # Once the application is initiated, execute is in charge of drawing the game and dealing with the game loop
    def execute(self, board, pents):
        self.initialize(board, pents)
                    
        pygame.init()
        self.displaySurface = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        self.displaySurface.fill((255, 255, 255))
        self.draw_board()
        pygame.display.flip()
        pygame.display.set_caption(self.windowTitle)

        sol_list = solve(board, pents, self)
        self.draw_solution_and_sleep(sol_list, 0)
        pygame.display.flip()

        if check_correctness(sol_list, board, pents):
            print("PASSED!")
        else:
            print("FAILED...")

        clock = pygame.time.Clock()
        clock = pygame.time.Clock()

        while self.running:
            pygame.event.pump()            
            keys = pygame.key.get_pressed()            
            clock.tick(self.fps)

            if (keys[K_ESCAPE]):
                    raise SystemExit

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

        while self.running:
            pygame.event.pump()            
            keys = pygame.key.get_pressed()            
            clock.tick(self.fps)

            if (keys[K_ESCAPE]):
                    raise SystemExit

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit

if __name__ == "__main__":
    """
    Run python Pentomino.py to check your solution. You can replace 'board' and 
    'pents' with boards of your own. You can start off easy with simple dominos.
    
    We won't gaurantee which tests your code will be run on, however if it runs
    well on the pentomino set you should be fine. The TA solution is able to run
    in <15 sec for the pentominos on the 6x10 board. 
    """
    
    
    board = instances.board_6x10
    pents = instances.petnominos
    app = Application(40)
    app.execute(board, pents)
