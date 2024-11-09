# Class: CS540 Spring 2020
# Author: Yongzhi Lai

import math
from decimal import Decimal

# this program predicts the weather with data provided

# calculate the euclidien distance between two points in three dimension space
# and return the distance 
def euclidean_distance(data_point1, data_point2):
    
    return math.sqrt(math.pow(data_point1[list(data_point1)[1]]-data_point2[list(data_point2)[1]],2)+
    math.pow(data_point1[list(data_point1)[2]]-data_point2[list(data_point2)[2]],2)+
    math.pow(data_point1[list(data_point1)[3]]-data_point2[list(data_point2)[3]],2))

# return a list of data point dictionaries read from the specified file.
def read_dataset(filename):
    f = open (filename,'r')
    dictionaryList=[]

    # read lines from file :
    for x in f:
        newDict={'DATE': '1948-01-01', 'TMAX': 51.0, 'PRCP': 0.47,
                  'TMIN': 42.0, 'RAIN': 'TRUE'}
        valueList=x.split(' ')
        newDict['DATE']=valueList[0]
        newDict['TMAX']=(float)(valueList[1])
        newDict['PRCP']=(float)(valueList[2])
        newDict['TMIN']=(float)(valueList[3])
        newDict['RAIN']=valueList[4].strip()
        dictionaryList.append(newDict)
    return dictionaryList

# return a prediction of whether it is raining or not based on a majority vote
# of the list of neighbors.

def majority_vote(nearest_neighbors):
    yes=0
    no=0
    for x in nearest_neighbors:
        if x[list(x)[4]]=='TRUE':
            yes=yes+1

        else:
            no=no+1

    if yes>=no:
        return 'TRUE'
    else:
        return 'FALSE'

# using the above functions, return the majority vote prediction for whether
# it's raining or not on the provided test point.
def k_nearest_neighbors(filename, test_point, k):
    allPoints=read_dataset(filename)
    tupList=[]
    neighborList=[]
    index=0
    i=0
    for x in allPoints:
        curTup=(index,euclidean_distance(test_point,x))
        tupList.append(curTup)
        index=index+1
    

    for i in range(len(tupList)): 
      

        min_idx = i 
        for j in range(i+1, len(tupList)): 
            if tupList[min_idx][1] > tupList[j][1]: 
                min_idx = j 
                     
        tupList[i], tupList[min_idx] = tupList[min_idx], tupList[i]

    
    tupList=tupList[:k]
    for x in tupList:
        neighborList.append(allPoints[x[0]])
    
    return majority_vote(neighborList)
