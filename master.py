#!/usr/bin/env python3
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
from utilities import post_processor_gwo, combine_api_data, plots_api

#if both hammers are present S800 and S1200
#the datafile directory for S800 hammer should be S800
#likewise on S1200

#the folder needs to hold both A type and B type files
s800_folder = 'S800'
s1200_folder = 'S1200'

#results folder with 
output = 'Results/'

#file cleaning, data extraction and plotting of non-api files
cache800  = post_processor_gwo(s800_folder, 'S800', output)
cache1200 = post_processor_gwo(s1200_folder, 'S1200', output)


# =============================================================================
# create a combined api dataset for plots and further filtering in the backend
# =============================================================================
mapped = combine_api_data(cache800, cache1200)
plots_api(mapped['d'], mapped['mapping_api_A'], output, 'A', confidence_limit= 100,
          api_limit=250)
plots_api(mapped['d'], mapped['mapping_api_B'], output, 'B', confidence_limit = 100, api_limit=250)
