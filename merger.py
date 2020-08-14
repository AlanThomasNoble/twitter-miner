'''This script joins multiple csv files in a directory into a single file.'''
import os
from glob import glob
import pandas as pd
os.chdir("./output/watson")
extension = 'csv'
files = [i for i in glob(f'*.{extension}')] # all filenames
# Combine All Files Into List
df = pd.concat([pd.read_csv(f) for f in files ])
os.chdir("../../")
df.to_csv('output/keywords_output_full_watson.csv', index=False, encoding='utf-8-sig')