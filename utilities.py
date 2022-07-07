#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 12:07:05 2022

@author: goharshoukat
"""
import os
import dataframe_image as dfi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
def list_search(data, search):
    #function to search and return the index for which a keyword is seen in the file. 
    
    for i, l in enumerate(data):
        if len(l.split()) != 0:
            dummy = l.split()
            if dummy[0] == search:
                return (i)

def table_extraction(data):
    #Input
    #data : list : list of lines read from the file
    #Output : pd.DataFrame : data table bounded between SUMMARY and Total. 
    
    i = list_search(data, 'SUMMARY')
    try:
        j = list_search(data, 'Total')
        
        return data[(i+3):(j-1)]
    except:
        j = list_search(data, 'Refusal')
        return data[(i+3):(j-1)]
    
def mkdir(path):
    #Input
    #path : str : path to make a directory
    
    if not os.path.isdir(path):
        os.makedirs(path)
    
    return True


def table_plotter(df, filename):
    #Input
    #df : dataframe : dataframe with the information
    #divides it into rows of 40 and puts it in a folder with the name of the file
    #as the directory name
    #divide the rowns into sequences of 40
    #filename : str : has to have a parent directory mentioned in the name
    
    
    #ensure a directory exisits for this particular file to dump the images in
    path = filename
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
        dfi.export(df, filename + '.png')


def editedNames(names, group):
    #Input
    #names : list of list : takes the list of names
    #edits them to make the labels like the zawtika file
    
    gra = []

    for i, n in enumerate(names):
        n = n.replace('14 GR', '')
        if n.split()[0] == group:
            
            gra.append(n)
            
            gra[i] = gra[i].split()
            
    
            #change 'S-xxx' to 'xxxS'
            gra[i][-2] = gra[i][-2].replace('S-', "")
            gra[i][-2] = gra[i][-2].replace(gra[i][-2], gra[i][-2] + 'S')
            
            #change E=xx to xx%
            gra[i][-1] = gra[i][-1].replace('E=', "")
            gra[i][-1] = gra[i][-1].replace(gra[i][-1], gra[i][-1] + '%')
    
            
            
        #create a seperate group for group b results
       
    return gra

def labels(lst):
    #Input
    #takes output from the editedNames function above and converts them
    #into labels
    lab = []
    for l in lst:
        lab.append('{} {} {}'.format(l[-2], l[-3], l[-1]))
        
    return lab


def plots(d, names, folder, title, group, lab):
    #Input
    #d : {} : dictionary of dataframes from all the datafiles
    #mapping : {} : dictionary mapping the filenames with the ones that are specific to the files that will be plotted
    #title : str : S800 or S1200 depending or S800-S1200 API
    #group : str : A or B
    output = folder + '/plots' 
    mkdir(output)    
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
    
    
    i = 0
    for k in names:
        ax.plot(d[k]['Bl Ct'],d[k].index.astype(float), linewidth = 1, alpha = 0.5, label = lab[i])
        i = i + 1
    
    
    ax.legend(ncol = 2, loc='lower center', bbox_to_anchor=(0.5,- 0.15))
    plt.show()
    plt.savefig(output + '/' + title + ' ' + group + '.pdf')

def combine_api_data(cache800, cache1200):
    #function takes in the datafiles from the two hammer type and 
    #returns the combined set for plotting further
    mapped = cache800
    for d in cache1200['d']:
        mapped['d'][d] = cache1200['d'][d] 

    return mapped

def plots_api(d, names, folder, group, lab, confidence_limit = 100, api_limit = 250):
    #function to plot the api files
    #d : {} : dictionary of dataframes from all the datafiles
    #mapping : {} : dictionary mapping the filenames with the ones that are specific to the files that will be plotted
    #title : str : S800 or S1200 depending or S800-S1200 API
    #group : str : A or B      
    #confidence limit : float : user defined
    #api_limit : float : user defined
    plot_folder = folder + '/plots'
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

    i = 0
    for k in names:
        ax.plot(d[k]['Bl Ct'],d[k].index.astype(float), linewidth = 1, alpha = 0.5, label = lab[i])
        i = i + 1
    

    ax.axvline(confidence_limit, label = 'Confidence Limit', ls = '--', color = 'red')    
    ax.axvline(api_limit, label = 'API Limit', ls = '--', color = 'Blue')    
    ax.legend(ncol = 2, loc='lower center', bbox_to_anchor=(0.5,- 0.15))
    plt.show()
    plt.savefig(plot_folder + '/' + 'API ' + group + '.pdf')
    
    
def post_processor_gwo(input_folder, hammer_type, output):
    #function that takes input directory
    #Input
    #input_folder : str : directory for input filetypes
    #hammer_type : str : S800 or S1200
    #group : str : A or B
    #outputs
    #d {} : dictionary with all the relevant filenames
    #mapped_api : relevant api file names for plots
    #mapped_na : non api mapped names for plots
    files = sorted(glob(input_folder + '/*.GWO'))
        
    #replaces file extensions and folder to extract case names
    names = [names.replace(".GWO", "") for names in files]
    names = [names.replace("{}/".format(hammer_type), "") for names in names]
    A = [n for n in names if n.split()[2]=='A']
    B = [n for n in names if n.split()[2]=='B']
    
    

    output_csv = output + 'Reformatted-{}/'.format(hammer_type) 
    mkdir(output_csv)

    output_tables = output + 'Tables-{}/'.format(hammer_type)
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
        #table_plotter(df2, path)
     
    
    return {'d' : d, 'names' : names}


def graphs(cache800, cache1200, output):
        
    
    non_api_800A = [k for k in cache800['names'][:6] if 'API' not in k]
    gra = editedNames(non_api_800A, 'A')
    lab = labels(gra)  #reformat labels to the desired format
    plots(cache800['d'], non_api_800A, output, 'S800', 'A', lab)
    
    
    non_api_800B = [k for k in cache800['names'][6:] if 'API' not in k]
    grb = editedNames(non_api_800B, 'B')
    lab = labels(grb)  #reformat labels to the desired format
    plots(cache800['d'], non_api_800B, output, 'S800', 'B', lab)
    
    
    
    non_api_1200A = [k for k in cache1200['names'][:6] if 'API' not in k]
    gra = editedNames(non_api_1200A, 'A')
    lab = labels(gra)  #reformat labels to the desired format
    plots(cache1200['d'], non_api_1200A, output, 'S1200', 'A', lab)
    
    
    non_api_1200B = [k for k in cache1200['names'][6:] if 'API' not in k]
    grb = editedNames(non_api_1200B, 'B')
    lab = labels(grb)  #reformat labels to the desired format
    plots(cache1200['d'], non_api_1200B, output, 'S1200', 'B', lab)
    
    
    #plot api values fro group A
    api800A = [k for k in cache800['names'][:6] if 'API' in k]
    api1200A = [k for k in cache1200['names'][:6] if 'API' in k]
    apiA = api800A + api1200A
    gra = editedNames(apiA, 'A')
    lab = labels(gra)  #reformat labels to the desired format
    combined_d_A = combine_api_data(cache800, cache1200)
    
    plots_api(combined_d_A['d'], apiA, output, 'A', lab)
    
    
    
    #plot api values fro group B
    api800B = [k for k in cache800['names'][6:] if 'API' in k]
    api1200B = [k for k in cache1200['names'][6:] if 'API' in k]
    apiB = api800B + api1200B
    grb = editedNames(apiB, 'B')
    lab = labels(grb)  #reformat labels to the desired format
    combined_d_B = combine_api_data(cache800, cache1200)
    
    plots_api(combined_d_B['d'], apiB, output, 'B', lab)