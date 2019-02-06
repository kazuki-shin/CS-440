# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)
import pygame
import heapq
import queue as Q

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)


def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    start = maze.getStart()
    visited = set()
    queue = []

    queue.append(start)
    num_states_explored = 0
    parent = {}

    while queue:
        state = queue.pop(0)

        if maze.isObjective(state[0],state[1]):
            break
        for neighbor in maze.getNeighbors(state[0],state[1]):
            if neighbor not in visited:
                parent[neighbor] = state
                visited.add(neighbor)
                queue.append(neighbor)
                num_states_explored += 1

    path = []

    while state is not start:
        path.insert(0,state)
        state = parent[state]

    path.insert(0,start)
    return path, num_states_explored

def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    start = maze.getStart()
    visited = set()
    stack = []

    stack.append(start)
    num_states_explored = 0
    parent = {}

    while stack:
        state = stack.pop()

        if maze.isObjective(state[0],state[1]):
            break
        for neighbor in maze.getNeighbors(state[0],state[1]):
            if neighbor not in visited:
                parent[neighbor] = state
                visited.add(neighbor)
                stack.append(neighbor)
                num_states_explored += 1

    path = []

    while state is not start:
        path.insert(0,state)
        state = parent[state]

    path.insert(0,start)
    return path, num_states_explored


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored

    start= maze.getStart()
    goal = maze.getObjectives()[0]
    visited = set()
    q = Q.PriorityQueue()

    q.put((0,start))
    num_states_explored = 0
    parent = {}

    while q:
        state = q.get()[1]

        if maze.isObjective(state[0],state[1]):
            break

        for neighbor in maze.getNeighbors(state[0],state[1]):
            if neighbor not in visited:

                dist = abs((goal[0]-neighbor[0]))+abs((goal[1]-neighbor[1]))

                parent[neighbor] = state
                visited.add(neighbor)
                q.put((dist,neighbor))
                num_states_explored += 1

    path = []

    while state is not start:
        path.insert(0,state)
        state = parent[state]

    path.insert(0,start)
    return path, num_states_explored


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    i=0
    start= maze.getStart()
    minDist=100000000000000000000000
    print(maze.getObjectives())
    print(start)
    for obj in maze.getObjectives():
        if abs((obj[0]-start[0]))+abs((obj[1]-start[1]))<minDist: #((obj[0]-start[0])**2 + (obj[1]-start[1])**2)**2<minDist:
            minDist=abs((obj[0]-start[0]))+abs((obj[1]-start[1]))#((obj[0]-start[0])**2 + (obj[1]-start[1])**2)**2
            goal=obj
    print(goal)
    visited = {}
    heap= []
    heapq.heappush(heap, (0,start))
    num_states_explored = 0
    parent = {}
    parent[start]=None
    visited[start]=0
    path = []
    objectives=maze.getObjectives()
    #make list of objectives
    while heap:
        cur = heapq.heappop(heap)
        g = cur[0] + 1
        state= cur[1]
        for obj in objectives:
            if abs((obj[0]-state[0]))+abs((obj[1]-state[1]))<minDist:#((obj[0]-state[0])**2 + (obj[1]-state[1])**2)**2<minDist:
                minDist=abs((obj[0]-state[0]))+abs((obj[1]-state[1]))#((obj[0]-state[0])**2 + (obj[1]-state[1])**2)**2
                goal=obj
        #print(parent)
        #print(visited)
        if state==goal:
            if state in objectives:
                print(objectives)
                objectives.remove(state)
                #print(objectives)
            #get rid of objective form list
            #clear visited and parents
            #make parent of state equal to None after while
            #clear queue and put state on the queue
            temp=state
            tpath = []
            #print(parent)
            #print(state)
            while temp is not None:
                if temp is None:
                    break
                tpath.insert(0,temp)
                temp = parent[temp]
            path += tpath
            if not objectives:
                break
            print(objectives)
            minDist=100000000000000000000000
            for obj in objectives:
                if abs((obj[0]-state[0]))+abs((obj[1]-state[1]))<minDist:#((obj[0]-state[0])**2 + (obj[1]-state[1])**2)**2<minDist:
                    minDist=abs((obj[0]-state[0]))+abs((obj[1]-state[1]))#((obj[0]-state[0])**2 + (obj[1]-state[1])**2)**2
                    goal=obj
            print(goal)
            visited={}
            parent={}
            parent[state]=None
            visited[state]=0
            heap=[]
            heapq.heappush(heap, (0, state))
        for neighbor in maze.getNeighbors(state[0],state[1]):
            h= ((goal[0]-neighbor[0])**2 + (goal[1]-neighbor[1])**2)**2 #

            if neighbor not in visited and neighbor!=parent[state]:
                cost = g + h
                visited[neighbor]=g
                parent[neighbor]=state
                #print(parent)
                num_states_explored += 1
                heapq.heappush(heap, (cost, neighbor))

            else:
                if g<visited[neighbor] and neighbor!=parent[state]:
                    #print("here")
                    cost = g + h
                    visited[neighbor]=g
                    parent[neighbor]=state
                    num_states_explored += 1
                    heapq.heappush(heap, (cost, neighbor))


    return path, num_states_explored
