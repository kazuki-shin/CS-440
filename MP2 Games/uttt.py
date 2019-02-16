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
                node.children.append(child)
                if isMax:
                    uttt.board[child.coord[0]][child.coord[1]]="X"
                else:
                    uttt.board[child.coord[0]][child.coord[1]]="O"
                num_child+=1
                z+=1
                y+=1
                curr_board=(x, y)
            x+=1
            y=uttt.globalIdx[currBoardIdx][1]
            curr_board=(x, y)
        #parent+=1
        print("Parent: "+str(node.coord))
        for child in node.children:
            print(child.coord)
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
        if isMax:
            #first rule
            if uttt.checkWinner() == 1:
                score += 10000
                return score
            #second rule
            if uttt.countTwoInARow() != 0 or uttt.countPreventThreeInARow() != 0:
                score += 500 * uttt.countTwoInARow()
                score += 100 * uttt.countPreventThreeInARow()
                return score
            #third rule
            score += 30 * uttt.countCornerTaken()
        #predefined defensive agent
        else:
            #first rule
            if uttt.checkWinner() == -1:
                score += -10000
                return score
            #second rule
            if uttt.countTwoInARow() != 0 or uttt.countPreventThreeInARow() != 0:
                score += -100 * uttt.countTwoInARow()
                score += -500 * uttt.countPreventThreeInARow()
                return score
            #third rule
            score += -30 * uttt.countCornerTaken()
        return score

    # num of unblocked two-in-a-row
    def countTwoInARow(isMax):
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
        for startingLocal in globalIdx:
            rowDis=startingLocal[0]
            colDis=staringLocal[1]
            for state in possible_states:
                if uttt.isTwoInARow((state[0]+rowDis, state[1]+colDis),isMax):
                    cnt+=1
        return cnt

    def isTwoInARow(state, isMax):
        pt1 = state[0]
        pt2 = state[1]
        block_point = state[2]
        if isMax:
            return board[pt1[0]][pt1[1]] == maxPlayer and board[pt2[0]][pt2[1]] == maxPlayer and board[block_point[0]][block_point[1]] == '_'
        if not isMax:
            return board[pt1[0]][pt1[1]] == minPlayer and board[pt2[0]][pt2[1]] == minPlayer and board[block_point[0]][block_point[1]] == '_'

    # num of blocks prevent tinghe opponent player from forming two-in-a-row
    def countPreventThreeInARow(self):
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
        for startingLocal in globalIdx:
            rowDis=startingLocal[0]
            colDis=staringLocal[1]
            for state in possible_states:
                if uttt.isBlocked((state[0]+rowDis, state[1]+colDis),isMax):
                    cnt+=1
        return cnt

    def isBlocked(state, isMax):
        pt1 = state[0]
        pt2 = state[1]
        block_point = state[2]
        if isMax:
            return board[pt1[0]][pt1[1]] == minPlayer and board[pt2[0]][pt2[1]] == minPlayer and board[block_point[0]][block_point[1]] == maxPlayer
        if not isMax:
            return board[pt1[0]][pt1[1]] == maxPlayer and board[pt2[0]][pt2[1]] == maxPlayer and board[block_point[0]][block_point[1]] == minPlayer

    # num of corners taken
    def countCornerTaken(self):
        cnt = 0
        possible_states = [(0,0), (0,2), (2,0), (2,2)]
        for startingLocal in globalIdx:
            rowDis=startingLocal[0]
            colDis=staringLocal[1]
            for state in possible_states:
                if isMax and board[state[0]+rowDis][state[1]+colDis] == maxPlayer:
                    cnt+=1
                if not isMax and board[state[0]+rowDis][state[1]+colDis] == minPlayer:
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
        if depth>=3:
            return
        tree = Tree()
        createTree(tree, currBoardIdx)
        if tree.children is empty:
            return tree.data
        if isMax:
            maxVal=-float("inf")
            for child in tree.children:
                eval=uttt.minimax(self, depth+1, child.locIdx, false)
                uttt.board[child.coord[0]][child.coord[1]]="_"
                maxVal=max(maxVal,eval)
            bestValue=maxVal
        else:
            minVal=float("inf")
            for child in tree.children:
                eval=minimax(self, depth+1, childIdx, true)
                minVal=min(minVal,eval)
            bestValue=minVal
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
        winner=0
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
    z=0
    isMax=True
    uttt=ultimateTicTacToe()
    root = Tree()
    root.coord=(1,1)
    root.locIdx=4
    uttt.createTree(root, root.locIdx, isMax, z)
    # uttt=ultimateTicTacToe()
    # gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,False,False)
    # if winner == 1:
    #     print("The winner is maxPlayer!!!")
    # elif winner == -1:
    #     print("The winner is minPlayer!!!")
    # else:
    #     print("Tie. No winner:(")
