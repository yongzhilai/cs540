import copy 
import random



def succ(state, boulderX, boulderY):
    succ=[]
    for i in range(len(state)):  

        for j in range(len(state)):
            tmpstore=copy.deepcopy(state)
            tmpstore[i]=j
            succ.append(tmpstore)

        succ.remove(state)
        j=0

    invalid_succ=copy.deepcopy(state)
    invalid_succ[boulderX]=boulderY

    if succ.count(invalid_succ):
        succ.remove(invalid_succ)
        

    return succ    


def convert_one(state):
    result=[]
    for i in range(len(state)):
        result.append(state[i]-i)

    return result
        
def convert_two (state):
    result=[]
    for i in range(len(state)):
        result.append(state[i]+i)

    return result
        
    
def attacked (indices,i,boulderX):
    if i==indices[0]:
        if boulderX<indices[1] and boulderX>i:
            return False
        else:
            return True

    elif i==indices[-1]:
        if boulderX<i and boulderX>indices[-2]:
            return False

        else:
            return True

    else:
        return True


def f(state, boulderX, boulderY):
    attacked_queens=0
    diagonal_one=convert_one(state)
    
    diagonal_two=convert_two(state)
    

    for i in range(len(state)):
        
        counted=False
        if state.count(state[i])>=2 and counted==False:
            if boulderY==state[i]:#boulder potentially blocking
                #are all the indices of same element
                indices=[j for j, x in enumerate(state) if x==state[i]]
                if attacked(indices,i,boulderX):
                    attacked_queens=attacked_queens+1
                    counted=True
            else:
                attacked_queens=attacked_queens+1
                counted=True

        if diagonal_one.count(diagonal_one[i])>=2 and counted==False:
            if boulderY-boulderX==diagonal_one[i]:#boulder potentially blocking
                indices=[j for j, x in enumerate(diagonal_one) if x==diagonal_one[i]]
                if attacked(indices,i,boulderX):
                    attacked_queens=attacked_queens+1
                    counted=True
                
            else:   
                attacked_queens=attacked_queens+1
                counted=True

        if diagonal_two.count(diagonal_two[i])>=2 and counted==False:
            
            if boulderY+boulderX==diagonal_two[i]:#boulder potentially blocking
                indices=[j for j, x in enumerate(diagonal_two) if x==diagonal_two[i]]
                if attacked(indices,i,boulderX):
                    attacked_queens=attacked_queens+1
                    counted=True

            else:    
                attacked_queens=attacked_queens+1
                counted=True

    return attacked_queens

def choose_next(curr, boulderX, boulderY):
    successors=succ(curr, boulderX, boulderY)
    score_list=[]
    lowest_score=f(curr,boulderX,boulderY)
    low_score_list=[]
    for x in successors:
        score=f(x,boulderX,boulderY)
        score_list.append(score)
        if lowest_score>score:
            lowest_score=score
    score_list.append(f(curr,boulderX,boulderY))
    successors.append(curr)
    if score_list.count(lowest_score)==1:
        result=successors[score_list.index(lowest_score)]
        
    else:
        indices=[j for j, x in enumerate(score_list) if x==lowest_score]
        for x in indices:
            low_score_list.append(successors[x])

        low_score_list.sort()
        result=low_score_list[0]
    if result==curr:
        return None

    return result 
        
#stop whenever stuck or find the goal
def nqueens(initial_state, boulderX, boulderY):
    parent=None
    while initial_state!=None:
        if f(initial_state,boulderX,boulderY)==0:
            return initial_state

        parent=initial_state
        print(initial_state,'- f=',f(initial_state,boulderX,boulderY))

    

        initial_state=choose_next(initial_state,boulderX,boulderY)
        
    return parent

def random_state(n,boulderX, boulderY):
    state=[]
    for i in range(n):
        a=random.randint(0,n-1)
        if i==boulderX:
            while a==boulderY:
                a=random.randint(0,n-1)
                    
        state.append(a)

    return state

    

# when stuck, start from another random state 
def nqueens_restart(n, k, boulderX, boulderY):
    initial_state=random_state(n,boulderX,boulderY)
    best_attempts=[]
    final_states=[]
    for i in range(k):
        result=nqueens(initial_state,boulderX,boulderY)
        if f(result,boulderX,boulderY)==0:
            print(result,'- f=',f(result,boulderX,boulderY))
            print(result)
            return
        
        initial_state=random_state(n,boulderX,boulderY)
        final_states.append(result)

    score_list=[]
    lowest_score=n
    for x in final_states:
        score=f(x,boulderX,boulderY)
        score_list.append(score)
        if lowest_score>score:
            lowest_score=score
    indices=[j for j, x in enumerate(score_list) if x==lowest_score]
    for x in indices:
            best_attempts.append(final_states[x])
            
    best_attempts.sort()
    print(best_attempts)

