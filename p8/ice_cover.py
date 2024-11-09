# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 06:45:15 2020

@author: 10655
"""
import math
import copy
import random

def get_dataset():
    data_set=[]
    year=1855
    filepath='ice_cover_final.txt'
    with open(filepath, 'r') as f:
        for x in f.readlines():
            x=x.strip('\n')
            x=x.strip()
            if x.isdigit():
                data_set.append([year, int(x)])
                year=year+1
        return data_set   

def print_stats(dataset):
    count=len(dataset)
    total=0
    total_deviation=0
    standard_devia=0
    print(count)
    for x in dataset:
        total=total+x[1]
    mean=total/count
    print(round(mean,2))
    for x in dataset:
        total_deviation=total_deviation+math.pow(x[1]-mean,2)
        
    total_deviation=total_deviation/(count-1)
    standard_devia=math.sqrt(total_deviation)
    print(round(standard_devia,2))
    

def regression(beta_0, beta_1):
    data = get_dataset()
    difference_sum=0
    for x in data:
        difference_sum=difference_sum+math.pow(beta_1*x[0]+beta_0-x[1],2)
        
    mse=difference_sum/len(data)
    return mse

def regression_new(beta_0, beta_1,dataset):
    data = dataset
    difference_sum=0
    for x in data:
        difference_sum=difference_sum+math.pow(beta_1*x[0]+beta_0-x[1],2)
        
    mse=difference_sum/len(data)
    return mse

def gradient_descent(beta_0, beta_1):
    data = get_dataset()
    difference_sum=0
    for x in data:
        difference_sum=difference_sum+beta_1*x[0]+beta_0-x[1]
        
    gradient1=2*difference_sum/len(data)
    difference_sum=0
    for x in data:
        difference_sum=difference_sum+(beta_1*x[0]+beta_0-x[1])*x[0]
    gradient2=2*difference_sum/len(data)
    return gradient1, gradient2

def gradient_descent_new(beta_0, beta_1,dataset):
    data = dataset
    difference_sum=0
    for x in data:
        difference_sum=difference_sum+beta_1*x[0]+beta_0-x[1]
        
    gradient1=2*difference_sum/len(data)
    difference_sum=0
    for x in data:
        difference_sum=difference_sum+(beta_1*x[0]+beta_0-x[1])*x[0]
    gradient2=2*difference_sum/len(data)
    return gradient1, gradient2

def gradient_descent_sgd(beta_0, beta_1,dataset):
    data = dataset
    pick=random.randint(0,len(data)-1)        
    gradient1=2*(beta_1*data[pick][0]+beta_0-data[pick][1])
    gradient2=2*data[pick][0]*(beta_1*data[pick][0]+beta_0-data[pick][1])
    return gradient1, gradient2

def iterate_gradient(T, eta):
    cur=[0,0]
    tmpstore=None
    i=1
    output=''
    rgs=0.0
    while i <= T:
        tmpstore=gradient_descent(cur[0],cur[1])
        cur[0]=cur[0]-eta*tmpstore[0]
        cur[1]=cur[1]-eta*tmpstore[1]
        rgs=regression(cur[0],cur[1])
        output= str(i)+' '+str(round(cur[0],2))+' '+str(round(cur[1],2))+' '+str(round(rgs,2))
        print(output)
        i=i+1

def iterate_gradient_new(T, eta,dataset):
    cur=[0,0]
    tmpstore=None
    i=1
    output=''
    rgs=0.0
    while i <= T:
        tmpstore=gradient_descent_new(cur[0],cur[1],dataset)
        cur[0]=cur[0]-eta*tmpstore[0]
        cur[1]=cur[1]-eta*tmpstore[1]
        rgs=regression_new(cur[0],cur[1],dataset)
        output= str(i)+' '+str(round(cur[0],2))+' '+str(round(cur[1],2))+' '+str(round(rgs,2))
        print(output)
        i=i+1

def iterate_gradient_sgd(T, eta,dataset):
    cur=[0,0]
    tmpstore=None
    i=1
    output=''
    rgs=0.0
    while i <= T:
        tmpstore=gradient_descent_sgd(cur[0],cur[1],dataset)
        cur[0]=cur[0]-eta*tmpstore[0]
        cur[1]=cur[1]-eta*tmpstore[1]
        rgs=regression_new(cur[0],cur[1],dataset)
        output= str(i)+' '+str(round(cur[0],2))+' '+str(round(cur[1],2))+' '+str(round(rgs,2))
        print(output)
        i=i+1

def compute_betas():
    data = get_dataset()
    total_x=0
    total_y=0
    numerator=0
    denominator=0
    for x in data:
        total_x=total_x+x[0]
        total_y=total_y+x[1]
    mean_x=total_x/len(data)
    mean_y=total_y/len(data)
    for x in data:
        numerator=numerator+(x[0]-mean_x)*(x[1]-mean_y)
        denominator=denominator+(x[0]-mean_x)*(x[0]-mean_x)
    beta_1=numerator/denominator
    beta_0=mean_y-beta_1*mean_x
    return beta_0,beta_1,regression(beta_0,beta_1)

def predict(year):
    betas=compute_betas()
    result=year*betas[1]+betas[0]
    return round(result,2)

def iterate_normalized(T, eta):
    data = get_dataset()
    cpy= copy.deepcopy(data)
    total_x=0
    s_deviation=0
    for x in data:
        total_x=total_x+x[0]
    mean_x=total_x/len(data)
    for x in data:
        s_deviation=s_deviation+(x[0]-mean_x)*(x[0]-mean_x)
    s_deviation=math.sqrt(s_deviation/(len(data)-1))
    for i in range(len(data)):
        cpy[i][0]=(data[i][0]-mean_x)/s_deviation
    iterate_gradient_new(T,eta,cpy)
     

def sgd(T, eta):
    data = get_dataset()
    cpy= copy.deepcopy(data)
    total_x=0
    s_deviation=0
    for x in data:
        total_x=total_x+x[0]
    mean_x=total_x/len(data)
    for x in data:
        s_deviation=s_deviation+(x[0]-mean_x)*(x[0]-mean_x)
    s_deviation=math.sqrt(s_deviation/(len(data)-1))
    for i in range(len(data)):
        cpy[i][0]=(data[i][0]-mean_x)/s_deviation
    iterate_gradient_sgd(T,eta,cpy)