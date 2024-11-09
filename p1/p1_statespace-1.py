# Class: CS540 Spring 2020
# author: Yongzhi Lai
# generates different states of two water jugs

# return a copy of state which fills the jug corresponding to the index
# in which (0 or 1) to its maximum capacity. 
def fill(state, max, which):
    result = [state[0],state[1]]
    result[which]=max[which]# fill
    return result




# return a copy of state which empties the jug corresponding to the index
# in which (0 or 1).
def empty(state, max, which):
    result = [state[0],state[1]]
    result[which]=0 # empty
    return result



# return a copy of state which pours the contents of the jug at index source
# into the jug at index dest, until source is empty or dest is full.
def xfer(state, max, source, dest):
    result = [state[0],state[1]]
    result[dest]=result[dest]+result[source]# transfer water
    result[source]=0
    if result[dest]> max[dest]: # excess water return to empty jug
        result[source]=result[dest]-max[dest]
        result[dest]=max[dest]
    return result



# display the list of unique successor states of the current state in any order.
def succ(state, max):
    # list of all states but not unique
    list1=[fill(state, max, 0),fill(state, max, 1),empty(state, max, 0),
            empty(state, max, 1),xfer(state, max, 0,1),xfer(state, max, 1,0)]
    unique_list=[]
    for x in list1: 
        # check if exists in unique_list or not 
      if x not in unique_list: 
            unique_list.append(x)  
    for i in unique_list:
      print(i)
    
