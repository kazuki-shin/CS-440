# -*- coding: utf-8 -*-
import numpy as np

def add_pentomino(board, pent, coord, check_pent=False, valid_pents=None):
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
    pents_used = []
    solve_helper(board, pents, pents_used, solution)
    if app is not None:
        app.draw_solution_and_sleep(solution, 1)
    return solution


def solve_helper(board, pents, pents_used, solution):
    if len(pents) == 0:
        return
    coord = []
    brk = False
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == 1:
                coord.append(x)
                coord.append(y)
                brk = True
                break
        if brk:
            break

    for i in pents:
        print(solution)
        if add_pentomino(board, i, coord):
            pent_used.append(i)
            sol = (i, (coord[0], coord[1]))
            solution.append(sol)
            pents.remove(i)
            solve_helper(board, pents, pents_used, solution)
        if add_pentomino(board, np.rot90(i), coord):
            pent_used.append(np.rot90(i))
            sol = (np.rot90(i), (coord[0], coord[1]))
            solution.append(sol)
            if i in pents:
                pents.remove(i)
            solve_helper(board, pents, pents_used, solution)
        if add_pentomino(board, np.rot90(np.rot90(i)), coord):
            pent_used.append(np.rot90(np.rot90(i)))
            sol = (np.rot90(np.rot90(i)), (coord[0], coord[1]))
            solution.append(sol)
            if i in pents:
                pents.remove(i)
            solve_helper(board, pents, pents_used, solution)
        if add_pentomino(board, np.rot90(np.rot90(np.rot90(i))), coord):
            pent_used.append(np.rot90(np.rot90(np.rot90(i))))
            sol = (np.rot90(np.rot90(np.rot90(i))), (coord[0], coord[1]))
            solution.append(sol)
            if i in pents:
                pents.remove(i)
            solve_helper(board, pents, pents_used, solution)
        if add_pentomino(board, np.flip(i, 0), coord):
            pent_used.append(np.flip(i, 0))
            sol = (np.flip(i, 0), (coord[0], coord[1]))
            solution.append(sol)
            if i in pents:
                pents.remove(i)
            solve_helper(board, pents, pents_used, solution)
        if add_pentomino(board, np.rot90(np.flip(i, 0)), coord):
            pent_used.append(np.rot90(np.flip(i, 0)))
            sol = (np.rot90(np.flip(i, 0)), (coord[0], coord[1]))
            solution.append(sol)
            if i in pents:
                pents.remove(i)
            solve_helper(board, pents, pents_used, solution)
        if add_pentomino(board, np.rot90(np.rot90(np.flip(i, 0))), coord):
            pent_used.append(np.rot90(np.rot90(np.flip(i, 0))))
            sol = (np.rot90(np.rot90(np.flip(i, 0))), (coord[0], coord[1]))
            solution.append(sol)
            if i in pents:
                pents.remove(i)
            solve_helper(board, pents, pents_used, solution)
        if add_pentomino(board, np.rot90(np.rot90(np.rot90(np.flip(i, 0)))), coord):
            pent_used.append(np.rot90(np.rot90(np.rot90(np.flip(i, 0)))))
            sol = (np.rot90(np.rot90(np.rot90(np.flip(i, 0)))), (coord[0], coord[1]))
            solution.append(sol)
            if i in pents:
                pents.remove(i)
            solve_helper(board, pents, pents_used, solution)
    if len(pents) == 0:
        return
    else:
        if solution:
            solution.pop()
        if pents_used:
            pents.append(pents_used.pop())
            remove_pentomino(pents[-1])
        if not pents_used:
            a = pents[0]
            del pents[0]
            pents.append(a)
        solve_helper(board, pents, pents_used, solution)
