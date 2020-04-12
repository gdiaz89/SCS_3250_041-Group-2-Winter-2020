# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 17:56:42 2020

@author: Lucas Merrick

Foundations of Data Science 3250 Term Project

Questions I will be answering:
    
    1. Regarding the neighborhoods, one interesting thing would be to get more 
    info about different features of neighborhoods, such as demographics, 
    wellbeing, etc., and find out if there is any relationship between these 
    features and crime rate in each neighborhood.
    
    2. What effect, if any, does weather have on BnE?

Data sets used:
    1. Bne data set
    2. Weather data set
    3. Neighbourhood data set
    4. Income data set (I need to find still)

"""

#import required add-ins
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import xlrd
from datetime import datetime
from datetime import timedelta

# Read in and clean weather data
### --------------------------------------------------------------------------
# This is used to pull data from the Government of Canada weather site
# From what I could find, the site only allowed you to pull data for one month
# at a time. Given this I used a loop to update the URL with a new month/year
# after each download.
weather_year = '2010'
weather_canada = pd.DataFrame()

while int(weather_year) <= 2019:
    weather_month = '1'
    while int(weather_month) <= 12:
        weather_canada_url =  ("https://climate.weather.gc.ca/climate_data/"
                               "bulk_data_e.html?format=csv&stationID=31688&"
                               "Year=" + weather_year + 
                               "&Month=" + weather_month +
                               "&Day=1&timeframe=1&submit=Download+Data"
                               )
        weather_canada_new = pd.read_csv(weather_canada_url)
        weather_canada = pd.concat([weather_canada,weather_canada_new])
        weather_month = str(int(weather_month)+1)
    weather_year = str(int(weather_year) + 1)
### --------------------------------------------------------------------------

# create a date column by slicing the date and time column, 
# then delete the date and time column
# weather_canada['date'] = weather_canada['Date/Time'].str[:10]
#weather_canada.drop(columns=['Date/Time'],inline=True)

# delete all empty columns
weather_canada = weather_canada.dropna(how='all', axis=1)

# Read in and clean BNE data

bne_url = ("https://opendata.arcgis.com/datasets/"
           "8ab59b498f6d4eae8ec631a287550376_0.csv?"
           "outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D"
           )

bne_data = pd.read_csv(bne_url)

# Need to create a column to merge the data on. This will be a date and time
# column. Currently the date and time column (occurancedate) is formatted 
# differently than the date and time column in the weather data. In addition
# to this the occurance time for the bne data is to the minute where the
# weather data is hourly. Given this we need to round the bne time to the
# nearest hour.

def round_time(time_str):
    '''(str) -> (str)
    
    Return the time rounded to the nearest hour with the time_str provided.
    
    >>> round_time('13:30')
    '14:00'
    
    >>> round_time('13:20')
    '13:00'
    
    >>> round_time('23:40')
    '00:00'
    '''
    if int(time_str[3:]) < 30:
        return str(time_str[:2]) + ':00'
    else:
        if int(time_str[:2]) == 23:
            return '00:00'
        else:
            return str(int(time_str[:2]) + 1) + ':00'
            

bne_data['Date/Time'] = (bne_data['occurrencedate'].str[:10] + ' ' +
                         bne_data['occurrencedate'].str[11:16]
                         .apply(round_time)
                         )


bne_data['Date/Time'] = pd.to_datetime(bne_data['Date/Time'],
                                       format='%Y-%m-%d %H:%M', 
                                       errors='coerce')

weather_canada['Date/Time'] = pd.to_datetime(weather_canada['Date/Time'],
                                       format='%Y-%m-%d %H:%M', 
                                       errors='coerce')

bne_weather_data = pd.merge(bne_data, weather_canada,how='left', 
                            on='Date/Time')


























