# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 12:05:59 2018

@author: sbergmann

Copyright@Hach Lange GmbH 
"""

import pandas as pd
import glob
import os as os
import codecs
from shutil import copyfile

html_file = glob.glob('*.htm')[0]
bounds=pd.read_html(html_file, skiprows=1)[0]
bounds.columns=bounds.iloc[0]
bounds=bounds.reindex(bounds.index.drop(0)).reset_index(drop=True)

#bounds['Lower Limit'][bound['Test Name']==col]
