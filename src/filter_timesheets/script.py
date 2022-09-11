#imports 
import pandas as pd 
import os

import logging
import sys


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

min_duration_per_project = 610
year = 2012
#get data  and year boolean (I will choose 2015)
logging.info('Creating filtered.csv file ...')
data = pd.read_csv('data/data.csv')
bool_year = pd.to_datetime(data['time_start']).dt.year == year

# threshold
threshold_hour = min_duration_per_project

bool_proj_thres = data.groupby(['project'])['duration'].sum()>=threshold_hour
selected_pj = list(bool_proj_thres[bool_proj_thres].index)

bool_proj = data.project.isin(selected_pj)


filtered = data[(bool_year&bool_proj)]
filtered.to_csv('data/filtered.csv')
logging.info('filtered.csv has been created and written to  the data folder')
