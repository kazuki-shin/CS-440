from time import sleep
from math import inf
from random import randint

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

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')


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
            if checkWinner() is 1:
                score += winnerMaxUtility
                return score
            #second rule
            if countTwoInARow() not 0 or countPreventThreeInARow() not 0:
                score += twoInARowMaxUtility * countTwoInARow()
                score += preventThreeInARowMaxUtility * countPreventThreeInARow()
                return score
            #third rule
            score += cornerMaxUtility * countCornerTaken()
        #predefined defensive agent
        else:
            #first rule
            if checkWinner() is -1:
                score += winnerMinUtility
                return score
            #second rule
            if countTwoInARow() not 0 or countPreventThreeInARow() not 0:
                score += twoInARowMinUtility * countTwoInARow()
                score += preventThreeInARowMinUtility * countPreventThreeInARow()
                return score
            #third rule
            score += cornerMinUtility * countCornerTaken()
        return score

    # num of unblocked two-in-a-row
    def countTwoInARow(self):
        cnt = 0
        return cnt

    # num of blocks prevent tinghe opponent player from forming two-in-a-row
    def countPreventThreeInARow(self):
        cnt = 0
        return cnt

    # num of corners taken
    def countCornerTaken(self):
        cnt = 0
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
        for tuple in range(len(globalIdx)):
            deltY = tuple[0]
            deltX = tuple[1]
            # X.-.-
            # X.-.-
            # X.-.-
            if board[0+deltY][deltX] == board[1+deltY][deltX] == board [2+deltY][deltX]:
                if board[0+deltY][deltX]=="X":
                    return 1
                else:
                    return -1
            # -.X.-
            # -.X.-
            # -.X.-
            if board[0+deltY][1+deltX] == board[1+deltY][1+deltX] == board [2+deltY][1+deltX]:
                if board[0+deltY][1+deltX]=="X":
                    return 1
                return -1
            # -.-.X
            # -.-.X
            # -.-.X
            if board[0+deltY][2+deltX] == board[1+deltY][2+deltX] == board [2+deltY][2+deltX]:
                if board[0+deltY][2+deltX]=="X":
                    return 1
                return -1
            # X.X.X
            # -.-.-
            # -.-.-
            if board[deltY][0+deltX] == board[deltY][1+deltX] == board [deltY][2+deltX]:
                if board[deltY][0+deltX]=="X":
                    return 1
                return -1
            # -.-.-
            # X.X.X
            # -.-.-
            if board[1+deltY][0+deltX] == board[1+deltY][1+deltX] == board [1+deltY][2+deltX]:
                if board[1+deltY][1+deltX]=="X":
                    return 1
                return -1
            # -.-.-
            # -.-.-
            # X.X.X
            if board[2+deltY][0+deltX] == board[2+deltY][1+deltX] == board [2+deltY][2+deltX]:
                if board[2+deltY][0+deltX]=="X":
                    return 1
                return -1
            # X.-.-
            # -.X.-
            # -.-.X
            if board[deltY][deltX] == board[1+deltY][1+deltX] == board[2+deltY][2+deltX]
                if board[deltX][deltY]=="X":
                    return 1
                return -1
            # -.-.X
            # -.X.-
            # X.-.-
            if board[2+deltY][deltX] == board[1+deltY][1+deltX] == board[deltY][2+deltX]
                if board[1+deltX][1+deltY]=="X":
                    return 1
                return -1

        return 0

    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
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
        #YOUR CODE HERE
        bestValue=0.0
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
        #YOUR CODE HERE
        if isMax:
            if board[currBoardIdx]>alpha:
                alpha=board[currBoardIdx]
            return alpha
        else:
            if board[currBoardIdx]<beta:
                beta=board[currBoardIdx]
            return beta
        bestValue=0.0
        return bestValue

    def playGamePredifinedAgent(self,maxFirst,isMinimax):
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
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, bestValue, winner=uttt.playGamePredifinedAgent()
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
