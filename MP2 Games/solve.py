# -*- coding: utf-8 -*-
import numpy as np

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
    while not done:
        a = pents[0]
        pents[0] = pents[-1]
        pents[-1] = a
        done = solve_helper(board, pents, solution, len(pents), pents)
    if app is not None:
        app.draw_solution_and_sleep(solution, 1)
    restore_board(solution, board)
    return solution


def solve_helper(board, pents, solution, num_pents, all_pents):
    added = False
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
    i = pents[0]
    if add_pentomino(board, i, coord):
        sol = (i, coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
        added = True
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
    if add_pentomino(board, np.rot90(i), coord):
        sol = (np.rot90(i), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
        added = True
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
    if add_pentomino(board, np.rot90(np.rot90(i)), coord):
        sol = (np.rot90(np.rot90(i)), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
        added = True
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
    if add_pentomino(board, np.rot90(np.rot90(np.rot90(i))), coord):
        sol = (np.rot90(np.rot90(np.rot90(i))), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
        added = True
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
    if add_pentomino(board, np.flip(i, 0), coord):
        sol = (np.flip(i, 0), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
        added = True
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
    if add_pentomino(board, np.rot90(np.flip(i, 0)), coord):
        sol = (np.rot90(np.flip(i, 0)), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
        added = True
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
    if add_pentomino(board, np.rot90(np.rot90(np.flip(i, 0))), coord):
        sol = (np.rot90(np.rot90(np.flip(i, 0))), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
        added = True
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
    if add_pentomino(board, np.rot90(np.rot90(np.rot90(np.flip(i, 0)))), coord):
        sol = (np.rot90(np.rot90(np.rot90(np.flip(i, 0)))), coord)
        solution.append(sol)
        done = solve_helper(board, pents[1:], solution, num_pents, all_pents)
        added = True
        if done or num_pents == len(solution):
            return True
        solution.pop(-1)
        remove_pentomino(board, sol[0], sol[1])
    if i.any() != all_pents[-1].any() and not added:
        a = pents[0]
        pents[0] = pents[-1]
        pents[-1] = a
        return solve_helper(board, pents, solution, num_pents, all_pents)
    return False
