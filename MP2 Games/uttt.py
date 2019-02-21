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

        self.curBestMove=(0,0)

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')

    def createTree(uttt, node, currBoardIdx, isMax):
        num_child = 0
        # if uttt.checkWinner() is 1:
        #     node.data = uttt.evaluatePredifined(True)
        #     print("Done: " +str(node.data))
        #     return
        # if uttt.checkWinner() is -1:
        #     node.data = uttt.evaluatePredifined(False)
        #     print("Done: " +str(node.data))
        #     return
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
                    if isMax:
                        uttt.board[child.coord[0]][child.coord[1]]="X"
                    else:
                        uttt.board[child.coord[0]][child.coord[1]]="O"
                    num_child+=1
                y+=1
                curr_board=(x, y)
            x+=1
            y=uttt.globalIdx[currBoardIdx][1]
            curr_board=(x, y)
        #parent+=1
        #print("Parent: "+str(node.coord))
        # for child in node.children:
        #     print(child.coord)
        #print("children size: "+str(len(node.children)))
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
        if uttt.checkWinner() == 1:
            score += 10000
        #second rule
        elif uttt.countTwoInARow(isMax) != 0 or uttt.countPreventThreeInARow(isMax) != 0:
            score += 500 * uttt.countTwoInARow(isMax)
            score += 100 * uttt.countPreventThreeInARow(isMax)
        #third rule
        else:
            score += 30 * uttt.countCornerTaken(isMax)

        #predefined defensive agent
        #first rule
        if uttt.checkWinner() == -1:
            score += -10000
        #second rule
        elif uttt.countTwoInARow(not isMax) != 0 or uttt.countPreventThreeInARow(not isMax) != 0:
            score += -100 * uttt.countTwoInARow(not isMax)
            score += -500 * uttt.countPreventThreeInARow(not isMax)
        #third rule
        else:
            score += -30 * uttt.countCornerTaken(not isMax)
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
            if uttt.board[0+deltY][deltX] == uttt.board[1+deltY][deltX] == uttt.board[2+deltY][deltX]:
                if uttt.board[0+deltY][deltX]=="X":
                    return 1
                elif uttt.board[0+deltY][deltX]=="O":
                    return -1
            # -.X.-
            # -.X.-
            # -.X.-
            if uttt.board[0+deltY][1+deltX] == uttt.board[1+deltY][1+deltX] == uttt.board[2+deltY][1+deltX]:
                if uttt.board[0+deltY][1+deltX]=="X":
                    return 1
                elif uttt.board[0+deltY][1+deltX]=="O":
                    return -1
            # -.-.X
            # -.-.X
            # -.-.X
            if uttt.board[0+deltY][2+deltX] == uttt.board[1+deltY][2+deltX] == uttt.board[2+deltY][2+deltX]:
                if uttt.board[0+deltY][2+deltX]=="X":
                    return 1
                elif uttt.board[0+deltY][2+deltX]=="O":
                    return -1
            # X.X.X
            # -.-.-
            # -.-.-
            if uttt.board[deltY][0+deltX] == uttt.board[deltY][1+deltX] == uttt.board[deltY][2+deltX]:
                if uttt.board[deltY][0+deltX]=="X":
                    return 1
                elif uttt.board[deltY][0+deltX]=="O":
                    return -1
            # -.-.-
            # X.X.X
            # -.-.-
            if uttt.board[1+deltY][0+deltX] == uttt.board[1+deltY][1+deltX] == uttt.board[1+deltY][2+deltX]:
                if uttt.board[1+deltY][1+deltX]=="X":
                    return 1
                elif uttt.board[1+deltY][1+deltX]=="O":
                    return -1
            # -.-.-
            # -.-.-
            # X.X.X
            if uttt.board[2+deltY][0+deltX] == uttt.board[2+deltY][1+deltX] == uttt.board [2+deltY][2+deltX]:
                if uttt.board[2+deltY][0+deltX]=="X":
                    return 1
                elif uttt.board[2+deltY][0+deltX]=="O":
                    return -1
            # X.-.-
            # -.X.-
            # -.-.X
            if uttt.board[deltY][deltX] == uttt.board[1+deltY][1+deltX] == uttt.board[2+deltY][2+deltX]:
                if uttt.board[deltX][deltY]=="X":
                    return 1
                elif uttt.board[deltY][deltX]=="O":
                    return -1
            # -.-.X
            # -.X.-
            # X.-.-
            if uttt.board[2+deltY][deltX] == uttt.board[1+deltY][1+deltX] == uttt.board[deltY][2+deltX]:
                if uttt.board[1+deltX][1+deltY]=="X":
                    return 1
                elif uttt.board[1+deltY][1+deltX]=="O":
                    return -1

        return 0

    # def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
    #     """
    #     This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
    #     input args:
    #     depth(int): current depth level
    #     currBoardIdx(int): current local board index
    #     alpha(float): alpha value
    #     beta(float): beta value
    #     isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
    #                  True for maxPlayer, False for minPlayer
    #     output:
    #     bestValue(float):the bestValue that current player may have
    #     """
    #     #YOUR CODE HERE
    #     if depth==maxDepth or checkWinner():
    #         return evaluatePredifined(self, isMax)
    #     if isMax:
    #         maxVal=-float("inf")
    #         #for child of position
    #             eval=minimax(self, depth+1, childIdx, alpha, beta, false)
    #             maxVal=max(maxVal,eval)
    #             alpha=max(alpha, eval)
    #             if beta<=alpha:
    #                 break
    #         bestValue=maxVal
    #     else:
    #         minVal=float("inf")
    #         #for child of position
    #             eval=minimax(self, depth+1, childIdx, alpha, beta, true)
    #             minVal=min(minVal,eval)
    #             beta=min(beta, eval)
    #             if beta<=alpha:
    #                 break
    #         bestValue=minVal
    #     return bestValue

    def minimax(self, depth, currBoardIdx, isMax, node):
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
        if depth>=3:
            return uttt.evaluatePredifined(isMax)
        uttt.createTree(node, currBoardIdx, isMax)
        #print("child size: "+str( len(node.children)))
        if len(node.children) == 0:
            return uttt.evaluatePredifined(isMax)
        if isMax:
            bestValue=-float("inf")
            maxVal=-float("inf")
            for child in node.children:
                eval=uttt.minimax(depth+1, child.locIdx, not isMax, child)
                uttt.board[child.coord[0]][child.coord[1]]="_"
                if eval>maxVal:
                    uttt.curBestMove=child
                    #print(uttt.curBestMove)
                    maxVal=eval
                    print("max: "+str(maxVal))
            bestValue=maxVal
        else:
            bestValue=float("inf")
            minVal=float("inf")
            for child in node.children:
                eval=uttt.minimax(depth+1, child.locIdx, not isMax, child)
                uttt.board[child.coord[0]][child.coord[1]]="_"
                if eval<minVal:
                    uttt.curBestMove=child
                    #print(uttt.curBestMove)
                    minVal=eval
                    print("min: "+str(minVal))
            bestValue=minVal
        print("best: "+str(bestValue))
        print()
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
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        root = Tree()
        root.coord=(1,1)
        root.locIdx=4
        bestValue = uttt.minimax(0, root.locIdx, isMax, root)
        print(uttt.curBestMove.coord)
        if isMax:
            uttt.board[uttt.curBestMove.coord[0]][uttt.curBestMove.coord[1]]='X'
        else:
            uttt.board[uttt.curBestMove.coord[0]][uttt.curBestMove.coord[1]]='O'
        while uttt.checkWinner()==0:
            bestValue = uttt.minimax(0, uttt.curBestMove.locIdx, isMax, uttt.curBestMove)
            if isMax:
                uttt.board[uttt.curBestMove.coord[0]][uttt.curBestMove.coord[1]]='X'
            else:
                uttt.board[uttt.curBestMove.coord[0]][uttt.curBestMove.coord[1]]='O'
            print(uttt.board)
            #print(uttt.curBestMove.coord)
            #print(bestValue)
            print()
        winner=0
        return uttt.curBestMove.coord, bestValue
        #return gameBoards, bestMove, expandedNodes, bestValue, winner

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
    z=0
    isMax=True
    uttt=ultimateTicTacToe()
    root = Tree()
    root.coord=(1,1)
    root.locIdx=4
    print(uttt.playGamePredifinedAgent(0, root.locIdx, isMax))

    # uttt=ultimateTicTacToe()
    # gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,False,False)
    # if winner == 1:
    #     print("The winner is maxPlayer!!!")
    # elif winner == -1:
    #     print("The winner is minPlayer!!!")
    # else:
    #     print("Tie. No winner:(")
