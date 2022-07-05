#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:25:51 2022

@author: goharshoukat

Plot graphs for different cases
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

files = sorted(glob('S800/*.GWO'))

#replaces file extensions and folder to extract case names
names = [names.replace(".GWO", "") for names in files]
names = [names.replace("S800/", "") for names in names]


# %% read data from the text files

    


    
    
    
with open(files[0], 'r') as f:
    lines = f.readlines()


#search for the summary table. 
#although format remains consistent throughout files
#it is better to be err on the side of caution. 
#each file will be searched for the data table. 
from utilities import table_extraction
data = table_extraction(lines)


#column names need to be readjusted after split operation. some columns
#have a psace in their names
columns = data[0].split()
columns[3] = 'End Bg'
columns.pop(4)
columns[4] = 'Bl Ct'
columns.pop(5)
columns[5] = 'Com Str'
columns.pop(6)
columns[6] = 'Ten Str'
columns.pop(7)

units = data[1].split()
#initialize array depending on size of input data
#13 columns remain fixed. number of rows will change. 
rows = np.zeros((len(data)-1, len(columns)), dtype=object)
rows[0, :] = units 

for i in range(2, len(data)):
    if len(data[i].split()) == 8:
        s = data[i].split()[5] #extreact the 5th element with the joint string
        index = s.find('-') #identify index of minus
        x = s[:index] #extract value of left of -
        y = s[index:] #extract value right of minus with a - sign
        row_val = (data[i].split()) #before filling in the row, create a new variable to adjust and shift valuees
        row_val[5] = x
        row_val.insert(6, y)
        rows[i-1, :] = row_val
        
    else: 
        rows[i-1, :] = data[i].split()
        
df = pd.DataFrame(data = rows, columns = columns)
df.to_csv('GWO.txt', sep='\t', mode='a', index=False)

test = pd.read_csv('GWO.txt', delimiter='\t')


# %% table plotter 
#divide the rowns into sequences of 40
pd.set_option("display.max_column", None)
pd.set_option("display.max_colwidth", None)
pd.set_option('display.width', -1)
pd.set_option('display.max_rows', None)
import dataframe_image as dfi
dfi.export(df.iloc[:40], "table.png")
dfi.export(df.iloc[40])

# %% graphs