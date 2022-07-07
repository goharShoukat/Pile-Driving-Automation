#!/usr/bin/env python3'
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 10:05:06 2022

@author: goharshoukat

Master Script for the user to interact with
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob
from utilities import post_processor_gwo, combine_api_data, plots_api, plots, labels, editedNames

#if both hammers are present S800 and S1200
#the datafile directory for S800 hammer should be S800
#likewise on S1200

#the folder needs to hold both A type and B type files
s800_folder = 'S800' 
s1200_folder = 'S1200' 

#results folder with 
output = 'Results/'

#file cleaning, data extraction and plotting of non-api files
# do not edit
cache800  = post_processor_gwo(s800_folder, 'S800', output)
cache1200 = post_processor_gwo(s1200_folder, 'S1200', output)




non_api_800A = [k for k in cache800['names'][:6] if 'API' not in k]
gra = editedNames(non_api_800A, 'A')
lab = labels(gra)  #reformat labels to the desired format
plots(cache800['d'], non_api_800A, 'Results', 'S800', 'A', lab)


non_api_800B = [k for k in cache800['names'][6:] if 'API' not in k]
grb = editedNames(non_api_800B, 'B')
lab = labels(grb)  #reformat labels to the desired format
plots(cache800['d'], non_api_800B, 'Results', 'S800', 'B', lab)



non_api_1200A = [k for k in cache1200['names'][:6] if 'API' not in k]
gra = editedNames(non_api_1200A, 'A')
lab = labels(gra)  #reformat labels to the desired format
plots(cache1200['d'], non_api_1200A, 'Results', 'S1200', 'A', lab)


non_api_1200B = [k for k in cache1200['names'][6:] if 'API' not in k]
grb = editedNames(non_api_1200B, 'B')
lab = labels(grb)  #reformat labels to the desired format
plots(cache1200['d'], non_api_1200B, 'Results', 'S1200', 'B', lab)