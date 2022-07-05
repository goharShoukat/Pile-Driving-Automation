#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 11:11:47 2022

@author: goharshoukat
"""
import numpy as np
import pandas as pd
with open('S800/14 GR A A&H BE S-800 E=75.GWF') as f:
    lines = f.readlines()[1:]

f.close()

#removes all the 111s from the data
for i in reversed(range(len(lines))):
    if (lines[i].split()[0]) == '111':
        lines.pop(i)


x = np.zeros((len(lines[0].split()), len(lines)))

for i in range(len(lines)):
    
    x[:, i] =  np.array(lines[i].split(), dtype = float)
    

excel = pd.read_excel('Stress histogram output from WEAP.xlsx', skiprows=2)
