#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 12:07:05 2022

@author: goharshoukat
"""
import os
import dataframe_image as dfi
import pandas as pd
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


def editedNames(names):
    #Input
    #names : list of list : takes the list of names
    #edits them to make the labels like the zawtika file
    
    gra = []
    grb = []
    j = 0
    for i, n in enumerate(names):
        n = n.replace('14 GR', '')
        if n.split()[0] == 'A':
            
            gra.append(n)
            
            gra[i] = gra[i].split()
            
    
            #change 'S-xxx' to 'xxxS'
            gra[i][-2] = gra[i][-2].replace('S-', "")
            gra[i][-2] = gra[i][-2].replace(gra[i][-2], gra[i][-2] + 'S')
            
            #change E=xx to xx%
            gra[i][-1] = gra[i][-1].replace('E=', "")
            gra[i][-1] = gra[i][-1].replace(gra[i][-1], gra[i][-1] + '%')
    
            
            
        #create a seperate group for group b results
        elif n.split()[0] == 'B':
            grb.append(n)
            grb[j] = grb[j].split()
            
    
            #change 'S-xxx' to 'xxxS'
            grb[j][-2] = grb[j][-2].replace('S-', "")
            grb[j][-2] = grb[j][-2].replace(grb[j][-2], grb[j][-2] + 'S')
            
            #change E=xx to xx%
            grb[j][-1] = grb[j][-1].replace('E=', "")
            grb[j][-1] = grb[j][-1].replace(grb[j][-1], grb[j][-1] + '%')
            
            j = j + 1
        
    return gra, grb

def labels(lst):
    #Input
    #takes output from the editedNames function above and converts them
    #into labels
    lab = []
    for l in lst:
        lab.append('{} {} {}'.format(l[-2], l[-3], l[-1]))
        
    return lab
    