# -*- coding: utf-8 -*-
# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    stack = util.Stack()
    return generalSearch(problem, stack)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    return generalSearch(problem, queue)
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    queue = util.PriorityQueueWithFunction(costFunction)
    return generalSearch(problem, queue, True)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    queue = util.PriorityQueue()
    return generalSearch(problem, queue, True, heuristic)

def costFunction(item) :
    return item[2]

def generalSearch(problem, openTable, needCost=False, heuristic=None) :
    if not needCost :                # 深度优先 和 广度优先
        path = []
        visited = []
        openTable.push((problem.getStartState(), path))
        while not openTable.isEmpty() :
            state, path = openTable.pop()
            if state in visited :
                continue
            visited.append(state)
            if problem.isGoalState(state) :
                return path
            for successor, direction, cost in problem.getSuccessors(state) :
                if not successor in visited :
                    openTable.push((successor, path + [direction]))
        return []
    else :
        visited = []
        path = []
        parent = {}
        startState = problem.getStartState()
        if not heuristic == None :                 # A*
            ## A*
            openTable.push((startState, path), 0)
            while not openTable.isEmpty():
                state = openTable.pop()
                if problem.isGoalState(state[0]):
                    return state[1]
                if state[0] not in visited:
                    visited.append(state[0])
                    successors = problem.getSuccessors(state[0])
                    for successor, action, cost in successors:
                        tempActions = state[1] + [action]
                        if successor not in visited:
                            openTable.push((successor,tempActions), problem.getCostOfActions(tempActions) + heuristic(successor,problem))
            return []
        else :                                     # 代价一致
            ## 代价一致
            openTable.push((startState, None, 0))
            parent[(startState, None)] = None
            while not openTable.isEmpty() :
                state = openTable.pop()
                if problem.isGoalState(state[0]) :                # 到达目的地
                    break
                else :
                    if state[0] in visited :                          # 如果已经扩展过了，就不需要再扩展了
                        continue 
                    visited.append(state[0])                          # 加入到 closed 表
                    for successor, direction, cost in problem.getSuccessors(state[0]) :       # 遍历该节点所有子节点
                        if successor not in visited :              # 只扩展没有在 closed 表中的
                            openTable.push((successor, direction, cost + state[2]))
                            parent[(successor, direction)] = state
            # 回溯，找到路径数组
            child = state              # 否则，说明是 代价一致搜索
            while (child != None):
                path.append(child[1])
                if child[0] != problem.getStartState():
                    child = parent[(child[0],child[1])]
                else:
                    child = None
            path.reverse()
            return path[1:]

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
