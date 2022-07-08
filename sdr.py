#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 09:27:11 2022

@author: goharshoukat

Script to produce SRD 
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from utilities import mkdir
df = pd.read_excel('sdr_input.xlsx')

folder = 'Results'
output = folder + '/plots' 
mkdir(output)    



fig, ax = plt.subplots(figsize = (5, 20))
ax.set_xlabel(r'SRD (MN)')
ax.set_ylabel(r'Depth (mBGL)')
#x = np.arange(0, 100, 20) # define the x to make ti the same for all cpts
#y = np.arange(0, 100, 10)
#ax.set_yticks(y)
##ax.set_xticks(x)
ax.invert_yaxis()
ax.xaxis.set_label_position('top')
ax.xaxis.tick_top()
ax.grid()

# =============================================================================
# for k in df.columns[1:]:
#     ax.plot(df[k], df['Depth'], linewidth = 1, alpha = 0.5, label = k)
# 
# =============================================================================
ax.plot(df['Best Estimate A&H'], df['Depth'], linewidth = 1, alpha = 0.5, label = 'Best Estimate A&H')
ax.plot(df['Max Estimate API'], df['Depth'], linewidth = 1, alpha = 0.5, label = 'Max Estimate API')
ax.plot(df['API SRD'], df['Depth'], linewidth = 1, alpha = 0.5, label = 'API SRD')
ax.plot(df['IHC S1200 + Ballast + Pile'], df['Depth'], linewidth = 1, alpha = 0.5, label = 'IHC S1200 + Ballast + Pile', ls = '--')
ax.plot(df['IHC S800 + Ballast + Pile'], df['Depth'], linewidth = 1, alpha = 0.5, label = 'IHC S800 + Ballast + Pile', ls = '--')
ax.plot(df['Pile Only Weight'], df['Depth'], linewidth = 1, alpha = 0.5, label = 'Pile Only Weight', ls = '--')
ax.legend(ncol = 2, loc='lower center', bbox_to_anchor=(0.5,- 0.15))
plt.show()
plt.savefig(output + '/'  + 'SRD.pdf')
