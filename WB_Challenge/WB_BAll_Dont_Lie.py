# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 11:48:07 2020

@author: ANDUIN
"""

import requests

import json

import csv

import time

import pandas as pd


request_string = 'https://www.balldontlie.io/api/v1/stats?seasons[]=2018&per_page=100&page='
page_string = '1'

file_name = "Stats.csv"


with open(file_name, "w") as file:
    csv_file = csv.writer(file, lineterminator='\n')
    csv_file.writerow(["Stat_ID", "Player_ID", "First_Name", "Last_Name", "Points"])
    
    print('Getting data from Balldontlie.io')
    
    response = requests.get(request_string + page_string)
    
    data = response.json()
    
    num_of_pages = data['meta']['total_pages']
    
    i = 1
    while(i <= num_of_pages):
        try:
            last_page = page_string
            response = requests.get(request_string + page_string)
            data = response.json()
            i += 1
            page_string = str(i)
    
            for item in data['data']:
                try:
                    stat_id = item['id']
                    player_id = item['player']['id']
                    first_name = item['player']['first_name']
                    last_name = item['player']['last_name']
                    points = item['pts']
                    csv_file.writerow([stat_id, player_id, first_name, last_name, points])
                except TypeError:
                    print('Faulty stat on page:', str(i-1), 'Stat_ID:', stat_id, 'Skipping...')
        except ValueError:
            time.sleep(5)
            page_string = last_page
            i = int(last_page)



df = pd.read_csv(r'Stats.csv')

averaged_data = df.groupby(['First_Name', 'Last_Name'])['Points'].mean().to_frame()

averaged_data.sort_values(by='Points', ascending = False)

sorted_averaged_data = averaged_data.sort_values(by='Points', ascending = False)

top_ten_average = sorted_averaged_data.head(10)

top_ten_average.to_csv(r'Top_Ten_Average_Points.csv')

print('Done')