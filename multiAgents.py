# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(self.index, action)
        newPos = successorGameState.getPacmanPosition(self.index)
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        if len(newFood.asList()):
            fooddist = util.manhattanDistance(newPos, newFood.asList()[0])
        else:
            fooddist = 0

        return successorGameState.getScore()[self.index] - fooddist

def scoreEvaluationFunction(currentGameState, index):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    # given just the gameState, return its value
    # assumed that this happens directly after an action

    newPos = currentGameState.getPacmanPosition(index)
    newFood = currentGameState.getFood().asList()
    newPower = currentGameState.getCapsules()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]    
    newGhostPos = currentGameState.getGhostPositions()

    # print("\nnewPos: ", newPos)
    # print("newFood: ", newFood)
    # print("newPower: ", newPower)
    # print("newGhostStates: ", newGhostStates)
    # print("newScaredTimes: ", newScaredTimes)
    # print("newGhostPos: ", newGhostPos)


    if currentGameState.isLose():
        return -float("inf")
    
    if currentGameState.isWin():
        return float("inf")

    # ghost function
    def ghostScore(gameState):
        if len(gameState.getGhostStates()) == 0:
                return 0
        score = 0
        for pacman in gameState.getPacmanPositions():
            for ghost in gameState.getGhostStates():
                score -= ((max(5 - manhattanDistance(gameState.getPacmanPositions(), ghost), 0)) ** 10)
        
        closestGhostDistance = 99999
        ghostIndex = 0
        for i in range(len(newGhostPos)):
            currDistance=manhattanDistance(newGhostPos[i], newPos)
            if closestGhostDistance > currDistance:
                closestGhostDistance = currDistance
                ghostIndex = i 
        if gameState.getGhostStates()[ghostIndex].scaredTimer > 0:
            score = score * -1
        return score
    
    # power function
    def powerScore(gameState):
        score = 0
        for pacman in gameState.getPacmanPositions():
            pacScore = []
            for powerCoord in gameState.currentGameState.getCapsules():
                pacScore.append(manhattanDistance(powerCoord, pacman))
            score -= min(pacScore)

        score = score * -2
        score -= len(gameState.currentGameState.getCapsules()) * 150
        return score

    
    # food function
    def foodScore(gameState):
        score = 0
        for pacman in gameState.getPacmanPositions():
            pacScore = []
            for foodCoord in gameState.currentGameState.getFood().asList()
                pacScore.append(manhattanDistance(foodCoord, pacman))
            score -= min(pacScore)
            
        score = score * -2
        score -= len(gameState.currentGameState.getCapsules()) * 50
        return score


    # want to decrease score if ghost is really close
    # totalScore = 0.0   
    # closestGhostDistance = 99999.0
    # closestFoodDistance = 99999.0
    # numFood = 0.0
    # closestPowerDistance = 99999.0
    # numPower = 0.0
    
    # ghostIndex = 0
    # for i in range(len(newGhostPos)):
    #     currDistance=manhattanDistance(newGhostPos[i], newPos)
    #     if closestGhostDistance > currDistance:
    #         closestGhostDistance = currDistance
    #         ghostIndex = i 
    
    # if len(newGhostPos) == 0:
    #     closestGhostDistance = 0

    # # want to increase score if close to food
    # for foodCoord in newFood:
    #     currDistance=manhattanDistance(foodCoord, newPos)
    #     if closestFoodDistance > currDistance:
    #         closestFoodDistance = currDistance 

    # # want to decrease score if more food left
    # numFood = currentGameState.getNumFood() nbvvn nvbgty

    # # want to increase score if close to power pellet
    # for powerCoord in newPower:
    #     currDistance=manhattanDistance(powerCoord, newPos)
    #     if closestPowerDistance > currDistance:
    #         closestPowerDistance = currDistance 

    # if len(newPower) == 0:
    #     closestPowerDistance = 0

    # # want to decrease score if more power pellets left
    # numPower = len(newPower)

    # if len(newGhostPos) != 0:
    #     if newGhostStates[ghostIndex].scaredTimer > 0:
    #         # go towards ghosts if scared
    #         print("GHOSTS ARE SCARED!")
    #         return -closestGhostDistance
    #     elif closestGhostDistance==3:
    #         return -1e3
    #     elif closestGhostDistance==2:
    #         return -1e5
    #     elif closestGhostDistance<=1:
    #         return -float("inf")

    # # print("\n\ninitial totalScore", totalScore)
    # # totalScore += closestGhostDistance * 1.5
    # # print("totalScore after closestGhostDistance", totalScore)
    # totalScore -= closestFoodDistance * 2
    # print("totalScore after closestFoodDistance", totalScore)
    # totalScore -= numFood * 3
    # print("totalScore after numFood", totalScore)
    # totalScore -= closestPowerDistance 
    # print("totalScore after closestPowerDistance", totalScore)
    # # totalScore -= numPower 
    # # print("totalScore after numPower", totalScore)

    # # print("\nclosestGhostDistance", closestGhostDistance)
    # # print("closestFoodDistance", closestFoodDistance)
    # # print("numFood", numFood)
    # # print("closestPowerDistance", closestPowerDistance)
    # # print("numPower", numPower)
    # print("totalScore", totalScore)
    # print()
    return totalScore

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, index = 0, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = index # Pacman is always agent index 0
        self.evaluationFunction = lambda state:util.lookup(evalFn, globals())(state, self.index)
        self.depth = int(depth)



class MultiPacmanAgent(MultiAgentSearchAgent):
    """
    You implementation here
    """
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()        
        legalMoves.remove("Stop")

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState.generatePacmanSuccessor(self.index, action)) for action in legalMoves]
        bestScore = max(scores)
        
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        if scores[chosenIndex] == float("inf"):
            print("scores", scores)
            # print("bestScore", bestScore)
            print("bestIndices", bestIndices)
            print("chosenIndex", chosenIndex)
            print("chosenAction", legalMoves[chosenIndex])
            print()
            return legalMoves[chosenIndex]

        chance = random.random()
        if chance > 0.8:
            print("RNG TIME")
            chosenIndex = random.randint(0,len(legalMoves)-1)
            initial = chosenIndex
            while scores[chosenIndex] == -float("inf"):
                print("CRISIS!! chosen index was: ", chosenIndex)
                chosenIndex+=1
                chosenIndex = chosenIndex % len(legalMoves)
                print("chosen index is now: ", chosenIndex)
                if chosenIndex == initial:
                    print("RIP no choices left")
                    break

        print("scores", scores)
        # print("bestScore", bestScore)
        print("bestIndices", bestIndices)
        print("chosenIndex", chosenIndex)
        print("chosenAction", legalMoves[chosenIndex])
        print()
        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]
    
class RandomAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions(self.index)
        return random.choice(legalMoves)




