from time import sleep
from random import randint

class Tree:
    def __init__(self):
        self.children = []
        self.data = None
        self.coord = None
        self.locIdx= None

class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True
        self.curBestMove=Tree()
        self.curNode=Tree()
        self.expandNode=0

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')

    def createTree(uttt, node, currBoardIdx):
        curr_board=uttt.globalIdx[currBoardIdx]
        x=curr_board[0]
        y=curr_board[1]
        for i in range(3):
            for j in range(3):
                child = Tree()
                child.coord = curr_board
                child.locIdx = i*3+j
                if uttt.board[child.coord[0]][child.coord[1]]=="_":
                    node.children.append(child)
                y+=1
                curr_board=(x, y)
            x+=1
            y=uttt.globalIdx[currBoardIdx][1]
            curr_board=(x, y)
        return

    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        score=0
        # predefined offensive agent
        #first rule
        if isMax:
            if uttt.checkWinner() == 1:
                score += 10000
            #second rule
            elif uttt.countTwoInARow(isMax) != 0 or uttt.countPreventThreeInARow(isMax) != 0:
                score += 500 * uttt.countTwoInARow(isMax)
                score += 100 * uttt.countPreventThreeInARow(isMax)
            #third rule
            else:
                score += 30 * uttt.countCornerTaken(isMax)
            return score
        #predefined defensive agent
        #first rule
        else:
            if uttt.checkWinner() == -1:
                score += -10000
            #second rule
            elif uttt.countTwoInARow(isMax) != 0 or uttt.countPreventThreeInARow(isMax) != 0:
                score += -100 * uttt.countTwoInARow(isMax)
                score += -500 * uttt.countPreventThreeInARow(isMax)
            #third rule
            else:
                score += -30 * uttt.countCornerTaken(isMax)
            return score

    # num of unblocked two-in-a-row
    def countTwoInARow(self,isMax):
        cnt = 0
        possible_states = [[(0,0),(0,1),(0,2)],  [(0,0),(1,0),(2,0)],  [(0,0),(2,0),(1,0)], [(0,0),(0,2),(0,1)],
                           [(0,1),(0,2),(0,0)],  [(0,1),(1,1),(2,1)],  [(0,1),(2,1),(1,1)],
                           [(0,2),(1,2),(2,2)],  [(0,2),(2,2),(1,2)],
                           [(1,0),(1,1),(1,2)],  [(1,0),(2,0),(0,0)],  [(1,0),(1,2),(1,2)],
                           [(1,1),(1,2),(1,0)],  [(1,1),(2,1),(0,1)],
                           [(1,2),(2,2),(0,2)],
                           [(2,0),(2,1),(2,2)],  [(2,0),(2,2),(2,1)],
                           [(2,1),(2,2),(2,0)]
        ]
        for startingLocal in uttt.globalIdx:
            rowDis=startingLocal[0]
            colDis=startingLocal[1]
            for state in possible_states:
                pt1 = (state[0][0]+rowDis, state[0][1]+colDis)
                pt2 = (state[1][0]+rowDis, state[1][1]+colDis)
                block_point = (state[2][0]+rowDis, state[2][1]+colDis)
                if uttt.isTwoInARow((pt1,pt2,block_point),isMax):
                    cnt+=1
        return cnt

    def isTwoInARow(self, state, isMax):
        pt1 = state[0]
        pt2 = state[1]
        block_point = state[2]
        if isMax:
            isTwo =  uttt.board[pt1[0]][pt1[1]] == uttt.maxPlayer and uttt.board[pt2[0]][pt2[1]] == uttt.maxPlayer and uttt.board[block_point[0]][block_point[1]] == '_'
            return isTwo
        if not isMax:
            isTwo =   uttt.board[pt1[0]][pt1[1]] == uttt.minPlayer and uttt.board[pt2[0]][pt2[1]] == uttt.minPlayer and uttt.board[block_point[0]][block_point[1]] == '_'
            return isTwo

    # num of blocks prevent tinghe opponent player from forming two-in-a-row
    def countPreventThreeInARow(self,isMax):
        cnt = 0
        possible_states = [[(0,0),(0,1),(0,2)],  [(0,0),(1,0),(2,0)],  [(0,0),(2,0),(1,0)], [(0,0),(0,2),(0,1)],
                           [(0,1),(0,2),(0,0)],  [(0,1),(1,1),(2,1)],  [(0,1),(2,1),(1,1)],
                           [(0,2),(1,2),(2,2)],  [(0,2),(2,2),(1,2)],
                           [(1,0),(1,1),(1,2)],  [(1,0),(2,0),(0,0)],  [(1,0),(1,2),(1,2)],
                           [(1,1),(1,2),(1,0)],  [(1,1),(2,1),(0,1)],
                           [(1,2),(2,2),(0,2)],
                           [(2,0),(2,1),(2,2)],  [(2,0),(2,2),(2,1)],
                           [(2,1),(2,2),(2,0)]
        ]
        for startingLocal in uttt.globalIdx:
            rowDis=startingLocal[0]
            colDis=startingLocal[1]
            for state in possible_states:
                pt1 = (state[0][0]+rowDis, state[0][1]+colDis)
                pt2 = (state[1][0]+rowDis, state[1][1]+colDis)
                block_point = (state[2][0]+rowDis, state[2][1]+colDis)
                if uttt.isBlocked((pt1,pt2,block_point),isMax):
                    cnt+=1
        return cnt

    def isBlocked(self,state, isMax):
        pt1 = state[0]
        pt2 = state[1]
        block_point = state[2]
        if isMax:
            return uttt.board[pt1[0]][pt1[1]] == uttt.minPlayer and uttt.board[pt2[0]][pt2[1]] == uttt.minPlayer and uttt.board[block_point[0]][block_point[1]] == uttt.maxPlayer
        if not isMax:
            return uttt.board[pt1[0]][pt1[1]] == uttt.maxPlayer and uttt.board[pt2[0]][pt2[1]] == uttt.maxPlayer and uttt.board[block_point[0]][block_point[1]] == uttt.minPlayer

    # num of corners taken
    def countCornerTaken(self,isMax):
        cnt = 0
        possible_states = [(0,0), (0,2), (2,0), (2,2)]
        for startingLocal in uttt.globalIdx:
            rowDis=startingLocal[0]
            colDis=startingLocal[1]
            for state in possible_states:
                if isMax and uttt.board[state[0]+rowDis][state[1]+colDis] == uttt.maxPlayer:
                    cnt+=1
                if not isMax and uttt.board[state[0]+rowDis][state[1]+colDis] == uttt.minPlayer:
                    cnt+=1
        return cnt

    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score=0
        return score

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        movesLeft=True
        for i in board:
            for j in i:
                if j is "_":
                    return movesLeft
        movesLeft = False
        return movesLeft

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        for tuple in uttt.globalIdx:
            deltY = tuple[0]
            deltX = tuple[1]
            # X.-.-
            # X.-.-
            # X.-.-
            if uttt.board[0+deltY][deltX] == uttt.board[1+deltY][deltX] == uttt.board[2+deltY][deltX] and (uttt.board[2+deltY][deltX]=="X" or uttt.board[2+deltY][deltX]=='O'):
                if uttt.board[0+deltY][deltX]=="X":
                    return 1
                elif uttt.board[0+deltY][deltX]=="O":
                    return -1
            # -.X.-
            # -.X.-
            # -.X.-
            if uttt.board[0+deltY][1+deltX] == uttt.board[1+deltY][1+deltX] == uttt.board[2+deltY][1+deltX] and (uttt.board[0+deltY][1+deltX]=="X" or uttt.board[0+deltY][1+deltX]=='O'):
                if uttt.board[0+deltY][1+deltX]=="X":
                    return 1
                elif uttt.board[0+deltY][1+deltX]=="O":
                    return -1
            # -.-.X
            # -.-.X
            # -.-.X
            if uttt.board[0+deltY][2+deltX] == uttt.board[1+deltY][2+deltX] == uttt.board[2+deltY][2+deltX] and (uttt.board[0+deltY][2+deltX]=="X" or uttt.board[0+deltY][2+deltX]=='O'):
                if uttt.board[0+deltY][2+deltX]=="X":
                    return 1
                elif uttt.board[0+deltY][2+deltX]=="O":
                    return -1
            # X.X.X
            # -.-.-
            # -.-.-
            if uttt.board[deltY][0+deltX] == uttt.board[deltY][1+deltX] == uttt.board[deltY][2+deltX] and (uttt.board[0+deltY][0+deltX]=="X" or uttt.board[0+deltY][0+deltX]=='O'):
                if uttt.board[deltY][0+deltX]=="X":
                    return 1
                elif uttt.board[deltY][0+deltX]=="O":
                    return -1
            # -.-.-
            # X.X.X
            # -.-.-
            if uttt.board[1+deltY][0+deltX] == uttt.board[1+deltY][1+deltX] == uttt.board[1+deltY][2+deltX] and (uttt.board[1+deltY][2+deltX]=="X" or uttt.board[1+deltY][2+deltX]=='O'):
                if uttt.board[1+deltY][1+deltX]=="X":
                    return 1
                elif uttt.board[1+deltY][1+deltX]=="O":
                    return -1
            # -.-.-
            # -.-.-
            # X.X.X
            if uttt.board[2+deltY][0+deltX] == uttt.board[2+deltY][1+deltX] == uttt.board [2+deltY][2+deltX] and (uttt.board[2+deltY][2+deltX]=="X" or uttt.board[2+deltY][2+deltX]=='O'):
                if uttt.board[2+deltY][0+deltX]=="X":
                    return 1
                elif uttt.board[2+deltY][0+deltX]=="O":
                    return -1
            # X.-.-
            # -.X.-
            # -.-.X
            if uttt.board[deltY][deltX] == uttt.board[1+deltY][1+deltX] == uttt.board[2+deltY][2+deltX] and (uttt.board[0+deltY][0+deltX]=="X" or uttt.board[0+deltY][0+deltX]=='O'):
                if uttt.board[deltX][deltY]=="X":
                    return 1
                elif uttt.board[deltY][deltX]=="O":
                    return -1
            # -.-.X
            # -.X.-
            # X.-.-
            if uttt.board[2+deltY][deltX] == uttt.board[1+deltY][1+deltX] == uttt.board[deltY][2+deltX] and (uttt.board[2+deltY][0+deltX]=="X" or uttt.board[2+deltY][0+deltX]=='O'):
                if uttt.board[1+deltX][1+deltY]=="X":
                    return 1
                elif uttt.board[1+deltY][1+deltX]=="O":
                    return -1

        return 0

    def alphabeta(self, depth, currBoardIdx, alpha, beta, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #creating tree
        #print("depth: "+str( depth))
        if depth==-1:
            parent=uttt.curNode
        if depth>=3 or uttt.checkWinner():
            return uttt.evaluatePredifined(isMax)
        #print("child size: "+str( len(node.children)))
        if (isMax and depth is not -1) or (not isMax and depth==-1):
            # print(str(uttt.curNode.coord)+str(isMax)+str(depth))
            if uttt.curNode.coord is not None and uttt.board[uttt.curNode.coord[0]][uttt.curNode.coord[1]]=="_":
                uttt.board[uttt.curNode.coord[0]][uttt.curNode.coord[1]]="X"
            uttt.createTree(uttt.curNode, currBoardIdx)
            # for triplet in uttt.board:
            #     print(triplet)
            # print(" ")
            bestValue=-float("inf")
            maxVal=-float("inf")
            for child in uttt.curNode.children:
                uttt.curNode=child
                if depth==-1:
                    child.data=uttt.alphabeta(depth+1, child.locIdx, alpha, beta, True)
                else:
                    child.data=uttt.alphabeta(depth+1, child.locIdx, alpha, beta, False)
                # uttt.board[child.coord[0]][child.coord[1]]="_"
                if child.data>maxVal:
                    maxVal=child.data
                if child.data>alpha:
                    alpha=child.data
                if beta<=alpha:
                    uttt.board[child.coord[0]][child.coord[1]]="_"
                    break
                uttt.board[child.coord[0]][child.coord[1]]="_"
            bestValue=maxVal
        else:
            # print(str(uttt.curNode.coord) + str(isMax) +str(depth))
            if uttt.curNode.coord is not None and uttt.board[uttt.curNode.coord[0]][uttt.curNode.coord[1]]=="_":
                uttt.board[uttt.curNode.coord[0]][uttt.curNode.coord[1]]="O"
            uttt.createTree(uttt.curNode, currBoardIdx)
            # for triplet in uttt.board:
            #     print(triplet)
            # print(" ")
            bestValue=float("inf")
            minVal=float("inf")
            for child in uttt.curNode.children:
                uttt.curNode=child
                if depth==-1:
                    child.data=uttt.alphabeta(depth+1, child.locIdx, alpha, beta,False)
                else:
                    child.data=uttt.alphabeta(depth+1, child.locIdx, alpha, beta,True)
                if child.data<minVal:
                    minVal=child.data
                if child.data<beta:
                    beta=child.data
                if beta<=alpha:
                    uttt.board[child.coord[0]][child.coord[1]]="_"
                    break
                uttt.board[child.coord[0]][child.coord[1]]="_"
            bestValue=minVal
        if depth==-1:
            for child in parent.children:
                if child.data==bestValue:
                    uttt.curBestMove=child
                    if not isMax:
                        uttt.board[uttt.curBestMove.coord[0]][uttt.curBestMove.coord[1]]="X"
                    else:
                        uttt.board[uttt.curBestMove.coord[0]][uttt.curBestMove.coord[1]]="O"
                    break
        uttt.expandNode+=1
        return bestValue

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #creating tree
        #print("depth: "+str( depth))
        if depth==-1:
            parent=uttt.curNode
        if depth>=3 or uttt.checkWinner():
            return uttt.evaluatePredifined(isMax)
        if (isMax and depth is not -1) or (not isMax and depth==-1):
            if uttt.curNode.coord is not None and uttt.board[uttt.curNode.coord[0]][uttt.curNode.coord[1]]=="_":
                uttt.board[uttt.curNode.coord[0]][uttt.curNode.coord[1]]="X"
            uttt.createTree(uttt.curNode, currBoardIdx)
            # for triplet in uttt.board:
            #     print(triplet)
            # print(" ")
            bestValue=-float("inf")
            maxVal=-float("inf")
            for child in uttt.curNode.children:
                uttt.curNode=child
                if depth==-1:
                    child.data=uttt.minimax(depth+1, child.locIdx, True)
                else:
                    child.data=uttt.minimax(depth+1, child.locIdx, False)
                # uttt.board[child.coord[0]][child.coord[1]]="_"
                if child.data>maxVal:
                    maxVal=child.data
                uttt.board[child.coord[0]][child.coord[1]]="_"
            bestValue=maxVal
        else:
            if uttt.curNode.coord is not None and uttt.board[uttt.curNode.coord[0]][uttt.curNode.coord[1]]=="_":
                uttt.board[uttt.curNode.coord[0]][uttt.curNode.coord[1]]="O"
            uttt.createTree(uttt.curNode, currBoardIdx)
            # for triplet in uttt.board:
            #     print(triplet)
            # print(" ")
            bestValue=float("inf")
            minVal=float("inf")
            for child in uttt.curNode.children:
                uttt.curNode=child
                if depth==-1:
                    child.data=uttt.minimax(depth+1, child.locIdx, False)
                else:
                    child.data=uttt.minimax(depth+1, child.locIdx, True)
                if child.data<minVal:
                    minVal=child.data
                    # print("min: "+str(minVal))
                uttt.board[child.coord[0]][child.coord[1]]="_"
            bestValue=minVal
        if depth==-1:
            # print(str(not isMax))
            # print("bestVal: "+str(bestValue))
            # for child in parent.children:
            #     print(child.data)
            for child in parent.children:
                if child.data==bestValue:
                    uttt.curBestMove=child
                    if not isMax:
                        uttt.board[uttt.curBestMove.coord[0]][uttt.curBestMove.coord[1]]="X"
                    else:
                        uttt.board[uttt.curBestMove.coord[0]][uttt.curBestMove.coord[1]]="O"
                    break
        uttt.expandNode+=1
        return bestValue


    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimax(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        isMax=maxFirst
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        expandedNodes=[]
        root = Tree()
        root.locIdx=4
        uttt.curNode=root
        if isMax:
            if not isMinimaxOffensive:
                bestVal = uttt.alphabeta(-1, root.locIdx, -float("inf"), -float("inf"), not isMax)
            else:
                bestVal = uttt.minimax(-1, root.locIdx, not isMax)
        else:
            if not isMinimaxDefensive:
                bestVal = uttt.alphabeta(-1, root.locIdx, -float("inf"), -float("inf"), not isMax)
            else:
                bestVal = uttt.minimax(-1, root.locIdx, not isMax)
        bestValue.append(bestVal)
        expandedNodes.append(uttt.expandNode)
        for triplet in uttt.board:
            print(triplet)
        gameBoards.append(uttt.board)
        print()
        while uttt.checkWinner()==0:
            bestMove.append(uttt.curBestMove.coord)
            root=Tree()
            root.locIdx=uttt.curBestMove.locIdx
            uttt.curNode=root
            uttt.curBestMove=Tree()
            isMax=not isMax
            print("here")
            uttt.expandNode=0
            if isMax:
                if not isMinimaxOffensive:
                    bestVal = uttt.alphabeta(-1, root.locIdx, -float("inf"), -float("inf"), not isMax)
                else:
                    bestVal = uttt.minimax(-1, root.locIdx, not isMax)
            else:
                if not isMinimaxDefensive:
                    bestVal = uttt.alphabeta(-1, root.locIdx, -float("inf"), -float("inf"), not isMax)
                else:
                    bestVal = uttt.minimax(-1, root.locIdx, not isMax)
            for triplet in uttt.board:
                print(triplet)
            bestValue.append(bestVal)
            expandedNodes.append(uttt.expandNode)
            gameBoards.append(uttt.board)
            print()
            print(uttt.curBestMove.coord)
        if(uttt.checkWinner()):
             print("checkWinner is " +str(uttt.checkWinner()))
        winner=uttt.checkWinner()
        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent(self):
        """
        This function implements the processes of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner

if __name__=="__main__":
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(False,True,True)
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
