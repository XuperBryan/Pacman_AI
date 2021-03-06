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
from game import Actions
from game import Directions
from pacman import GhostRules
import random, util
from game import Agent
from math import sqrt

def euclidDistance(xy1, xy2):
    "Returns the euclidean distance between points xy1 and xy2"
    return sqrt((xy1[0]-xy2[0])**2+(xy1[1]-xy2[1])**2)

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
        legalMoves = gameState.getLegalActions(self.index)

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
    if currentGameState.isLose():
        return -float("inf")
    
    if currentGameState.isWin():
        return float("inf")

    # ghost function
    def ghostScore(gameState):
        if len(gameState.getGhostStates()) == 0:
                return 0
        score = 0
        newGhostPos = gameState.getGhostPositions()
        newGhostStates = gameState.getGhostStates()
        for pacman in gameState.getPacmanPositions():
            for i in range(len(newGhostPos)):
                if newGhostStates[i].scaredTimer > 0:
                    score += ((max(4 - euclidDistance(pacman, newGhostPos[i]), 0)) ** 2)
                else:
                    score -= ((max(4 - euclidDistance(pacman, newGhostPos[i]), 0)) ** 2)
                    if manhattanDistance(pacman, newGhostPos[i]) < 2:
                        return -float("inf")
        
        return score
    
    # food function
    def foodScore(gameState):
        score = 0
        for pacman in gameState.getPacmanPositions():
            pacScore = []
            for foodCoord in gameState.getFood().asList():
                pacScore.append(euclidDistance(foodCoord, pacman))
            score = min(pacScore)
            
        score = score * -2
        score -= len(gameState.getFood().asList()) * 15
        return score


    totalScore = currentGameState.getScore()[0]
    totalScore += ghostScore(currentGameState) 
    totalScore += foodScore(currentGameState)
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
        def getDistribution(self, state, ghostIndex):
            # Read variables from state
            ghostState = state.getGhostState(ghostIndex % state.getNumAgents())
            legalActions = state.getLegalActions(ghostIndex % state.getNumAgents())
            pos = state.getGhostPosition(ghostIndex % state.getNumAgents())
            isScared = ghostState.scaredTimer > 0

            speed = 1
            if isScared:
                speed = 0.5

            actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
            newPositions = [(pos[0]+a[0], pos[1]+a[1]) for a in actionVectors]
            pacmanPositions = state.getPacmanPositions()

            # Select best actions given the state
            distancesToPacman = [min([manhattanDistance(pos, pacpos) for pacpos in pacmanPositions]) for pos in newPositions]
            if len(distancesToPacman) == 0: 
                distancesToPacman = [0]
            if isScared:
                bestScore = max(distancesToPacman)
                bestProb = 0.5
            else:
                bestScore = min(distancesToPacman)
                bestProb = 0.5
            bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]

            # Construct distribution
            dist = util.Counter()
            for a in bestActions:
                dist[a] = bestProb / len(bestActions)
            for a in legalActions:
                dist[a] += (1-bestProb) / len(legalActions)
            dist.normalize()
            return dist

        def maxValue(gameState, agentIndex):
            value = -float("inf")
            legalMoves = gameState.getLegalActions(agentIndex % gameState.getNumAgents())  
            for action in legalMoves:
                value = max(value, expectiMax(gameState.generatePacmanSuccessor(agentIndex % gameState.getNumAgents(), action), agentIndex+1))
            return value
        
        def expectValue(gameState, agentIndex):
            value = 0
            legalMoves = gameState.getLegalActions(agentIndex % gameState.getNumAgents())

            dist = getDistribution(self, gameState, agentIndex)
            if len(dist) == 0:
                value = -float("inf")
            for action in dist:
                p = dist[action]
                value += p * expectiMax(gameState.generateSuccessor(agentIndex % gameState.getNumAgents(), action), agentIndex+1)
            return value

        def expectiMax(gameState, agentIndex):
            # with index 0 = pacman, and numAgents = 3, if agentIndex == 3, then stop
            # with index 0,1 = pacman, and numAgents = 4, if agentIndex == 4, then stop
            if gameState.isWin():
                return float("inf")
            
            if gameState.isLose():
                return -float("inf")

            if agentIndex >= self.depth * gameState.getNumAgents():
                return self.evaluationFunction(gameState)

            # this is pacman
            if agentIndex % gameState.getNumAgents() < (gameState.data.numPacman):
                return maxValue(gameState, agentIndex)
            # this is ghost
            else:
                return expectValue(gameState, agentIndex)
                


        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(self.index)       

        # Choose one of the best actions
        scores = [expectiMax(gameState.generatePacmanSuccessor(self.index, action), self.index + 1) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        

        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        if scores[chosenIndex] == float("inf"):
            return legalMoves[chosenIndex]

        chance = random.random()
        if chance > 1:
            chosenIndex = random.randint(0,len(legalMoves)-1)
            initial = chosenIndex
            while scores[chosenIndex] == -float("inf"):
                chosenIndex+=1
                chosenIndex = chosenIndex % len(legalMoves)
                if chosenIndex == initial:
                    break

        return legalMoves[chosenIndex]
    
class RandomAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions(self.index)
        return random.choice(legalMoves)




