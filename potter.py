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
from utilities import table_plotter, mkdir, editedNames, labels, table_extraction, plots

files = sorted(glob('S800/*.GWO'))

#replaces file extensions and folder to extract case names
names = [names.replace(".GWO", "") for names in files]
names = [names.replace("S800/", "") for names in names]
A = [n for n in names if n.split()[2]=='A']
B = [n for n in names if n.split()[2]=='B']
# %% read data from the text files
output = 'Results/'
output_csv = output + 'Reformatted-S1200/'
mkdir(output_csv)

output_tables = output + 'Tables-S800/'
mkdir(output_tables)

#put all the data from the 12 files in one dict
d = {} #d will house all the data

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
    rows = np.zeros((len(data), len(columns)), dtype=object)
    rows[0, :] = units 


#go line by line and extract the values in each row after using split()

    for j in range(2, len(data)):
        if len(data[j].split()) == 8:#some rows have two columns combined into 1. this detects those rows and performs necessary operations to exxtract and place the values in to each column
            s = data[j].split()[5] #extreact the 5th element with the joint string
            index = s.find('-') #identify index of minus
            x = s[:index] #extract value of left of -
            y = s[index:] #extract value right of minus with a - sign
            row_val = (data[j].split()) #before filling in the row, create a new variable to adjust and shift valuees
            row_val[5] = x
            row_val.insert(6, y)
            rows[j, :] = row_val
            
        else: 
            rows[j, :] = data[j].split()


#write files to txt
    df = pd.DataFrame(data = rows, columns = columns)
    df.to_csv(output_csv + names[i] + '.txt', sep='\t', mode='a', index=False)
    df.to_csv(output_csv + names[i] + '.csv', index=False)
    
    #reformat df for use in the plotting functions below
    df2 = df.set_index('Depth')
    df2 = df2.iloc[1:]
    df2['Bl Ct'] = df2['Bl Ct'].astype(float) / 4 #convert datatype frm string to float. divide by 4 to get /25cm value

    d[names[i]] = df2
    
#generate tables for 
    path = output_tables + names[i] + '/'
    table_plotter(df, path)
    

# Code for plotting

gra = editedNames(A, 'A')
lab = labels(gra)  #reformat labels to the desired format
#create relational dictionary

#plot only for non-api files
non_api = [l for l in lab if 'API' not in l]
api = [l for l in lab if 'API' in l]
        
mapping_na = dict(zip(names, non_api)) 
mapping_api = dict(zip(names, api))

#plotting folder
plot_folder = 'Results/plots/'
mkdir(plot_folder)
plots(d, mapping_na, plot_folder, 'S-800')
plots(d, mapping_api, 'S-800')
    
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

gra = editedNames(A, 'A')
lab = labels(gra)  #reformat labels to the desired format
#create relational dictionary

#plot only for non-api files
non_api = [l for l in lab if 'API' not in l]
api = [l for l in lab if 'API' in l]
        
mapping_na = dict(zip(names, non_api)) 
mapping_api = dict(zip(names, api))


fig, ax = plt.subplots(figsize = (5, 20))
ax.set_xlabel(r'Blow Count (Blows/25cm)')
ax.set_ylabel(r'Depth (mBGL)')
#x = np.arange(0, 100, 20) # define the x to make ti the same for all cpts
y = np.arange(0, 100, 10)
ax.set_yticks(y)
##ax.set_xticks(x)
ax.invert_yaxis()
ax.xaxis.set_label_position('top')
ax.xaxis.tick_top()
ax.grid()



for k in mapping_na:
    ax.plot(d[k]['Bl Ct'],d[k].index, linewidth = 1, alpha = 0.5, label = mapping_na[k])  


ax.legend(ncol = 2)
plt.show()