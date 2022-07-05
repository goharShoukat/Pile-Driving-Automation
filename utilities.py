#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 12:07:05 2022

@author: goharshoukat
"""

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
    j = list_search(data, 'Total')
    
    return data[i+3:j-1]