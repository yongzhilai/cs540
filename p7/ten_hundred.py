# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 23:11:02 2020

@author: 10655
"""
import csv

def load_data(filepath):
    data_set=[]
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:           
            if 'Lat' in row:
                del row['Lat']
            if 'Long' in row:
                del row['Long']
            data_set.append(row)
        return data_set
            
    
    
def calculate_x_y(time_series):
    char_list=list(time_series.values())    
    del char_list[0]
    del char_list[0]
    print(char_list)
    values=[]
    for i in char_list:
        values.append(int(i))
    t = len(values)-1

    if values[t]<=0:
        x = None
        y = None
# find the day with 10 times less cases
    threshold10 = values[t]/10;
    below10 = [i for i in values if i <= threshold10]
    if len(below10)==0 :
        x = None
    else:
        i = max(below10)
        x = t - below10.index(i)
        
    
# find the day with 100 times less cases
    threshold100 = values[t]/100;
    below100 = [i for i in values if i <= threshold100]
    if len(below100)==0 :
        y = None
    else:
        j = max(below100)
        y = i - below100.index(j)# if x is not applicable, so is y.    
    return (x,y)
    
def hac(dataset):
    return None