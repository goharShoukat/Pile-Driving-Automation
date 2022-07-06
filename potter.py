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
from utilities import table_extraction, table_plotter, mkdir, editedNames, labels
files = sorted(glob('S800/*.GWO'))
A = [n for n in files if n.split()[2]=='A']
B = [n for n in files if n.split()[2]=='B']
#replaces file extensions and folder to extract case names
names = [names.replace(".GWO", "") for names in files]
names = [names.replace("S800/", "") for names in names]


# %% read data from the text files
output = 'Results/'
output_csv = output + 'Reformatted-S800/'
mkdir(output_csv)

output_tables = output + 'Tables-S800/'
mkdir(output_tables)


for i in range(len(files)):
    with open(files[i], 'r') as f:
        lines = f.readlines()

    #search for the summary table. 
    #although format remains consistent throughout files
    #it is better to be err on the side of caution. 
    #each file will be searched for the data table. 

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


#go line by line and extract the values in each row after using split()

    for j in range(2, len(data)):
        if len(data[j].split()) == 8:
            s = data[j].split()[5] #extreact the 5th element with the joint string
            index = s.find('-') #identify index of minus
            x = s[:index] #extract value of left of -
            y = s[index:] #extract value right of minus with a - sign
            row_val = (data[j].split()) #before filling in the row, create a new variable to adjust and shift valuees
            row_val[5] = x
            row_val.insert(6, y)
            rows[j-1, :] = row_val
            
        else: 
            rows[j-1, :] = data[j].split()


#write files to txt
    df = pd.DataFrame(data = rows, columns = columns)
    df.to_csv(output_csv + names[i] + '.txt', sep='\t', mode='a', index=False)

    
#generate tables for 
    path = output_tables + names[i] + '/'
    table_plotter(df, path)
    
    
# =============================================================================
#     
# =============================================================================
# #   tester below  
# =============================================================================
# =============================================================================
    
# %% tester
with open(files[1], 'r') as f:
    lines = f.readlines()


#search for the summary table. 
#although format remains consistent throughout files
#it is better to be err on the side of caution. 
#each file will be searched for the data table. 

data = table_extraction(lines)
search = 'Total'
for i, l in enumerate(lines):
    if len(l.split()) != 0:
        dummy = l.split()
        if dummy[0] == search:
            print(i)
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




#ensure a directory exisits for this particular file to dump the images in
path = output_tables + names[1] + '/'
mkdir(path)


pd.set_option("display.max_column", None)
pd.set_option("display.max_colwidth", None)
pd.set_option('display.width', -1)
pd.set_option('display.max_rows', None)
if len(df) / 40 > 1:
    times = int(len(df) / 40) + 1 #determines number of images the df has to be broken down into
                             #+1 take cares of the leftover values
    
    for i in range((times)):
        dfi.export(df.iloc[(40*i):(40 + 40 * i)], path  + '{}.png'.format(i))
else:
    dfi.export(df, output_tables + names[i] + '.png')
# %% graphs
#create relational lists. map filenames, to gra and grb
#first do it for A

gra, grb = editedNames(names)
gr = gra + grb
lab = labels(gr)  #reformat labels to the desired format
#create relational dictionary
dict(zip(files, lab)) 

df2 = df.set_index('Depth')
df2 = df2.iloc[1:]
df2['Bl Ct'] = df2['Bl Ct'].astype(float) / 4 #convert datatype frm string to float. divide by 4 to get /25cm value

fig, ax = plt.subplots(figsize = (5, 20))
ax.plot(df2['Bl Ct'], df2.index, linewidth = 1, alpha = 0.5, label = names[1])

ax.set_xlabel(r'Blow Count (Blows/25cm)')
ax.set_ylabel(r'Depth (m)')
x = np.arange(0, 100, 20) # define the x to make ti the same for all cpts
y = np.arange(0, 100, 5)
ax.set_xticks(x)
ax.set_yticks(y)
ax.invert_yaxis()
ax.xaxis.set_label_position('top')
ax.xaxis.tick_top()
ax.grid()
ax.legend(loc='upper center',
        ncol=6)
plt.show()
