# -*- coding: utf-8 -*-
import numpy as np
import queue as Q
from collections import defaultdict

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

def add_pentomino(board, pent, coord, constraints, choices, orientation, check_pent=False, valid_pents=None):
    pidx = get_pent_idx(pent)
    if (pent.shape[0] + coord[0]) > board.shape[0] or (pent.shape[1] + coord[1]) > board.shape[1]:
        return False
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                if board[coord[0]+row][coord[1]+col] == 0: # Overlap
                    return False
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                constraints[(row + coord[0], col + coord[1])].add((pidx, orientation, coord))
                choices[(pidx, orientation, coord)].add((row + coord[0], col + coord[1]))
    constraints[pidx].add((pidx, orientation, coord))
    choices[(pidx, orientation, coord)].add(pidx)
    return True

def solve(board, pents):
    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy arrays. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is
    the coordinate of the upper left corner of pi in the board (lowest row and column index
    that the tile covers).

    -Use np.flip and np.rot90 to manipulate pentominos.

    -You can assume there will always be a solution.
    """
    if len(pents) == 0:
        return []
    solution = []
    constraints = defaultdict(set)
    choices = defaultdict(set)
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            coord = (x, y)
            for i in pents:
                add_pentomino(board, i, coord, constraints, choices, 0)
                add_pentomino(board, np.rot90(i), coord, constraints, choices, 1)
                add_pentomino(board, np.rot90(np.rot90(i)), coord, constraints, choices, 2)
                add_pentomino(board, np.rot90(np.rot90(np.rot90(i))), coord, constraints, choices, 3)
                add_pentomino(board, np.fliplr(i), coord, constraints, choices, 4)
                add_pentomino(board, np.rot90(np.fliplr(i)), coord, constraints, choices, 5)
                add_pentomino(board, np.rot90(np.rot90(np.fliplr(i))), coord, constraints, choices, 6)
                add_pentomino(board, np.rot90(np.rot90(np.rot90(np.fliplr(i)))), coord, constraints, choices, 7)
    done = solve_helper(board, pents, solution, constraints, choices)
    return solution


def solve_helper(board, pents, solution, constraints, choices):
    if not constraints.keys() or len(solution) == len(pents):
        return True
    done = False
    min_val = float("inf")
    coord = ()

    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            if (x, y) in constraints.keys() and len(constraints[(x, y)]) <= min_val:
                min_val = len(constraints[(x, y)])
                if min_val == 0:
                    return False
                coord = (x, y)

    for choice in constraints[coord]:
        pidx = choice[0]
        pent = pents[pidx]
        if choice[1] == 1:
            pent = np.rot90(pent)
        if choice[1] == 2:
            pent = np.rot90(np.rot90(pent))
        if choice[1] == 3:
            pent = np.rot90(np.rot90(np.rot90(pent)))
        if choice[1] == 4:
            pent = np.fliplr(pent)
        if choice[1] == 5:
            pent = np.rot90(np.fliplr(pent))
        if choice[1] == 6:
            pent = np.rot90(np.rot90(np.fliplr(pent)))
        if choice[1] == 7:
            pent = np.rot90(np.rot90(np.rot90(np.fliplr(pent))))
        solution.append((pent, choice[2]))
        constraint_vals = {}
        for i in choices[choice]:
            constraint_vals[i] = constraints[i].copy()
            del constraints[i]
        choices_val = {}
        for k in constraint_vals.keys():
            for choice in constraint_vals[k]:
                if choice in choices.keys():
                    choices_val[choice] = choices[choice].copy()
                    del choices[choice]
        for k in choices_val.keys():
            for i in choices_val[k]:
                if i not in constraint_vals.keys():
                    constraint_vals[i] = constraints[i].copy()
                if i in constraints.keys() and k in constraints[i]:
                    constraints[i].remove(k)
        done = solve_helper(board, pents, solution, constraints, choices)
        if done or not constraints.keys() or len(solution) == len(pents):
            return True
        for i in constraint_vals.keys():
            constraints[i] = constraint_vals[i].copy()
        for k in choices_val.keys():
            choices[k] = choices_val[k].copy()
        solution.pop(-1)
    return False
