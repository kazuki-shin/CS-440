# -*- coding: utf-8 -*-
import numpy as np
import random

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
    return pidx

def add_pentomino(board, pent, coord, check_pent=False, valid_pents=None):
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
                board[coord[0]+row][coord[1]+col] = 0
    return True

def remove_pentomino(board, pent, coord):
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                board[coord[0]+row][coord[1]+col] = 1

def restore_board(solution, board):
    for i in solution:
        for row in range(i[0].shape[0]):
            for col in range(i[0].shape[1]):
                if i[0][row][col] != 0:
                    board[i[1][0]+row][i[1][1]+col] = 1

<<<<<<< HEAD
def factorial(fact):
    if fact == 1:
        return 1
    return fact * factorial(fact - 1)
=======
>>>>>>> 8a3df55d1982e8e2ed4aefc1bc8a3c06ed8e10b3
def solve(board, pents, app=None):
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
    if 1 not in board:
        return []
    solution = []
    done = solve_helper(board, pents, solution, len(pents), pents)
<<<<<<< HEAD
    i = 0
    print(len(pents))
    print(factorial(len(pents)))
    while not done and i < factorial(len(pents)):
        random.shuffle(pents)
        done = solve_helper(board, pents, solution, len(pents), pents)
        i += 1
=======
    while not done:
        a = pents[0]
        pents[0] = pents[-1]
        pents[-1] = a
        done = solve_helper(board, pents, solution, len(pents), pents)
>>>>>>> 8a3df55d1982e8e2ed4aefc1bc8a3c06ed8e10b3
    if app is not None:
        app.draw_solution_and_sleep(solution, 1)
    restore_board(solution, board)
    return solution


def solve_helper(board, pents, solution, num_pents, all_pents):
<<<<<<< HEAD
=======
    added = False
>>>>>>> 8a3df55d1982e8e2ed4aefc1bc8a3c06ed8e10b3
    if num_pents == len(solution):
        return True
    coord = ()
    brk = False
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            if board[x][y] != 0:
                coord = (x, y)
                brk = True
                break
        if brk:
            break
    if not coord:
        return False
<<<<<<< HEAD
    counter = 0
=======
>>>>>>> 8a3df55d1982e8e2ed4aefc1bc8a3c06ed8e10b3
    i = pents[0]
    if add_pentomino(board, i, coord):
        sol = (i, coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
<<<<<<< HEAD
=======
        added = True
>>>>>>> 8a3df55d1982e8e2ed4aefc1bc8a3c06ed8e10b3
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
    if add_pentomino(board, np.rot90(i), coord):
        sol = (np.rot90(i), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
<<<<<<< HEAD
=======
        added = True
>>>>>>> 8a3df55d1982e8e2ed4aefc1bc8a3c06ed8e10b3
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
    if add_pentomino(board, np.rot90(np.rot90(i)), coord):
        sol = (np.rot90(np.rot90(i)), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
<<<<<<< HEAD
=======
        added = True
>>>>>>> 8a3df55d1982e8e2ed4aefc1bc8a3c06ed8e10b3
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
    if add_pentomino(board, np.rot90(np.rot90(np.rot90(i))), coord):
        sol = (np.rot90(np.rot90(np.rot90(i))), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
<<<<<<< HEAD
=======
        added = True
>>>>>>> 8a3df55d1982e8e2ed4aefc1bc8a3c06ed8e10b3
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
<<<<<<< HEAD
    if add_pentomino(board, np.fliplr(i), coord):
        sol = (np.fliplr(i), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
=======
    if add_pentomino(board, np.flip(i, 0), coord):
        sol = (np.flip(i, 0), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
        added = True
>>>>>>> 8a3df55d1982e8e2ed4aefc1bc8a3c06ed8e10b3
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
<<<<<<< HEAD
    if add_pentomino(board, np.rot90(np.fliplr(i)), coord):
        sol = (np.rot90(np.fliplr(i)), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
=======
    if add_pentomino(board, np.rot90(np.flip(i, 0)), coord):
        sol = (np.rot90(np.flip(i, 0)), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
        added = True
>>>>>>> 8a3df55d1982e8e2ed4aefc1bc8a3c06ed8e10b3
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
<<<<<<< HEAD
    if add_pentomino(board, np.rot90(np.rot90(np.fliplr(i))), coord):
        sol = (np.rot90(np.rot90(np.fliplr(i))), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
=======
    if add_pentomino(board, np.rot90(np.rot90(np.flip(i, 0))), coord):
        sol = (np.rot90(np.rot90(np.flip(i, 0))), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
        added = True
>>>>>>> 8a3df55d1982e8e2ed4aefc1bc8a3c06ed8e10b3
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
<<<<<<< HEAD
    if add_pentomino(board, np.rot90(np.rot90(np.rot90(np.fliplr(i)))), coord):
        sol = (np.rot90(np.rot90(np.rot90(np.fliplr(i)))), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
=======
    if add_pentomino(board, np.rot90(np.rot90(np.rot90(np.flip(i, 0)))), coord):
        sol = (np.rot90(np.rot90(np.rot90(np.flip(i, 0)))), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
        added = True
>>>>>>> 8a3df55d1982e8e2ed4aefc1bc8a3c06ed8e10b3
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
<<<<<<< HEAD
=======
    if i.any() != all_pents[-1].any() and not added:
        a = pents[0]
        pents[0] = pents[-1]
        pents[-1] = a
        return solve_helper(board, pents, solution, num_pents, all_pents)
>>>>>>> 8a3df55d1982e8e2ed4aefc1bc8a3c06ed8e10b3
    return False
