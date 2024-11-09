# Class: CS540 Spring 2020
# Author: Yongzhi Lai

# this program is used to module the torus puzzle

from itertools import chain 
import copy
default = [[1,2,3],[4,5,6],[7,8,0]]
goal = [1,2,3,4,5,6,7,8,0]

def load(state):
    puzzle=[[1,2,3],[4,5,6],[7,8,0]]
    puzzle[0][0]=state[0]
    puzzle[0][1]=state[1]
    puzzle[0][2]=state[2]
    puzzle[1][0]=state[3]
    puzzle[1][1]=state[4]
    puzzle[1][2]=state[5]
    puzzle[2][0]=state[6]
    puzzle[2][1]=state[7]
    puzzle[2][2]=state[8]
    return puzzle

def print_succ(state):
    puzzle=load(state)
    succList=succ(findZero(puzzle),puzzle)
    listOfStates=transfer(succList)
    for x in listOfStates:
      print(x," h=",Heuristic(load(x)),"\n",sep="")
      
def succ_states(state):
    puzzle=load(state)
    succList=succ(findZero(puzzle),puzzle)
    listOfStates=transfer(succList)
    return listOfStates


def Heuristic(puzzle):
    i=0
    h=0
    for x in puzzle:
        for y in x:
            if y==goal[i]and y!=0:
                h=h+1
            i=i+1
    return 8-h

def findZero(puzzle):
    i=0
    j=0
    for x in puzzle:
        for y in x:
            if y==0:
                return [i,j]
            j=j+1
        i=i+1
        j=0

def succ(zero,puzzle):
    
    i=zero[0]
    j=zero[1]
    succList=[]

    succ1=copy.deepcopy(puzzle)
    succ1[i][j], succ1[i][j-1] = succ1[i][j-1], succ1[i][j]
    succ2=copy.deepcopy(puzzle)
    succ2[i][j], succ2[i][j-2] = succ2[i][j-2], succ2[i][j]
    succ3=copy.deepcopy(puzzle)
    succ3[i][j], succ3[i-1][j] = succ3[i-1][j], succ3[i][j]
    succ4=copy.deepcopy(puzzle)
    succ4[i][j], succ4[i-2][j] = succ4[i-2][j], succ4[i][j]
    succList.append(succ1)
    succList.append(succ2)
    succList.append(succ3)
    succList.append(succ4)
    return succList

def transfer(succList):
    listOfStates=[]
    for x in succList:
      state=list(chain.from_iterable(x))
      listOfStates.append(state)
    listOfStates=sorted(listOfStates)
    return listOfStates

def state_to_dict(state,g,parent):
    Dict= {'state':state,'h':Heuristic(load(state)),'g':g,'parent':parent,'f':
           g+Heuristic(load(state))}
    return Dict
    
# expand the given state, return list of dictionary of its successor
def expand(state,g,parent):
    listOfStates=succ_states(state)
    listOfDicts=[]
    for x in listOfStates:
        Dict=state_to_dict(x,g+1,parent)
        listOfDicts.append(Dict)        
    return listOfDicts

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

def search(state):
    OPEN=PriorityQueue()
    CLOSED=[]
    path = []
    OPEN.enqueue(state_to_dict(state,0,None))
    while not OPEN.is_empty():
        result=OPEN.pop()
        CLOSED.append(result)
        if result['state']==[1,2,3,4,5,6,7,8,0]:
            while result['parent']!=None:
                path.append(result)
                result=result['parent']
            path.append(result)
            break
        successors=expand(result['state'],result['g'],result)
        for x in successors:
            index=0
            in_CLOSED=False
            for i in range(len(CLOSED)):
                if CLOSED[i]['state']==x['state']:
                    index=i
                    in_CLOSED= True
            if in_CLOSED:
                if CLOSED[index]['f']>x['f']:
                    OPEN.enqueue(x)
                    del CLOSED[index]
            else:                                    
                OPEN.enqueue(x)
    return path

def solve(state):
    path=search(state)
    path.reverse()
    for x in path:
        print(x['state'], ' h=',x['h'], ' moves: ',x['g'],sep="")


''' author: hobbes
    source: cs540 canvas
    TODO: complete the enqueue method
'''
class PriorityQueue(object):
    def __init__(self):
        self.queue = []
        self.max_len = 0

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, state_dict):
        """ Items in the priority queue are dictionaries:
             -  'state': the current state of the puzzle
             -      'h': the heuristic value for this state
             - 'parent': a reference to the item containing the parent state
             -      'g': the number of moves to get from the initial state to
                         this state, the "cost" of this state
             -      'f': the total estimated cost of this state, g(n)+h(n)

            For example, an item in the queue might look like this:
             {'state':[1,2,3,4,5,6,7,8,0], 'parent':[1,2,3,4,5,6,7,0,8],
              'h':0, 'g':14, 'f':14}

            Please be careful to use these keys exactly so we can test your
            queue, and so that the pop() method will work correctly.

            TODO: complete this method to handle the case where a state is
                  already present in the priority queue
        """
        index=0
        in_open = False
        # TODO: set in_open to True if the state is in the queue already
        # TODO: handle that case correctly
        for i in range(len(self.queue)):
                if self.queue[i]['state']==state_dict['state']:
                    index=i
                    in_open= True
        
        if not in_open:
            self.queue.append(state_dict)
        else:
            if self.queue[index]['f']>state_dict['f']:
                del self.queue[index]
                self.queue.append(state_dict)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def requeue(self, from_closed):
        """ Re-queue a dictionary from the closed list (see lecture slide 21)
        """
        self.queue.append(from_closed)

        # track the maximum queue length
        if len(self.queue) > self.max_len:
            self.max_len = len(self.queue)

    def pop(self):
        """ Remove and return the dictionary with the smallest f(n)=g(n)+h(n)
        """
        minf = 0
        for i in range(1, len(self.queue)):
            if self.queue[i]['f'] < self.queue[minf]['f']:
                minf = i
        state = self.queue[minf]
        del self.queue[minf]
        return state


  














