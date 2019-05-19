#!/usr/bin/env python
# -*- coding: utf-8 -*-
import folium
import pandas as pd
import os

from PIL import Image
import glob
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

### data is taken from https://community.data.gov.in/number-of-convicts-of-rape-in-2013/

#SF_COORDINATES = (37.76, -122.45)
pd.set_option('display.max_columns',1000)
path_of_input_file = "C:/Users/khushal/Documents/Python Scripts/Rape_cases_in_India_2015.xlsx"
input_data_df = pd.read_excel(path_of_input_file,sheet_name='Rape_cases_in_India_2015')
indian_states_df = pd.read_excel(path_of_input_file,sheet_name='States')
print(input_data_df)
print("--" * 60)
india_crime_data_by_state = pd.merge(left=input_data_df,right=indian_states_df,left_on='State/UT',right_on='State/UT')
state_df = india_crime_data_by_state['State/UT']
#incest_rape_case_reported_df = input_data_df['Incest Rape - Number of Cases Reported']
Number_of_Victims_under_Incest_Rape_Cases = india_crime_data_by_state['Number of Victims under Incest Rape Cases - Total Victims']
Number_of_Victims_under_Other_than_Incest_Rape_Cases = india_crime_data_by_state['Number of Victims under Other than Incest Rape Cases - Total Victims']
Number_of_Victims_Total_Rape_Cases_Total_Victims = india_crime_data_by_state['Number of Victims (Total Rape Cases) - Total Victims']

print("india_crime_data_by_state = \n",india_crime_data_by_state,"\n --" * 60)
print(Number_of_Victims_Total_Rape_Cases_Total_Victims)

indiaState = os.path.join('C:/Users/khushal/Documents/Python Scripts/','IndianStates.json')
maharashtra_Districts = os.path.join('C:/Users/khushal/Documents/Python Scripts/','Maharashtra_Districts.json')
print(maharashtra_Districts)

lat_mean = india_crime_data_by_state['Latitude'].mean()
lon_mean = india_crime_data_by_state['Longitude'].mean()
# Setup a folium map at a high-level zoom
map1 = folium.Map(location=[lat_mean,lon_mean], zoom_start=5,tiles='Mapbox bright')

def color(elev):
    if elev in range(0, 1000):
        col = 'green'
    elif elev in range(1001, 1999):
        col = 'blue'
    elif elev in range(2000, 2999):
        col = 'orange'
    else:
        col = 'red'
    return col
lat_df = india_crime_data_by_state['Latitude']
lon_df = india_crime_data_by_state['Longitude']

for lat,lan, state,elev in zip(lat_df,lon_df,state_df,Number_of_Victims_Total_Rape_Cases_Total_Victims):

    folium.Marker(location=[lat,lan], popup=state,icon=folium.Icon(color=color(elev),icon_color='black',icon='info-sign',angle=0),tooltip=elev).add_to(map1)

map1.choropleth(geo_data=indiaState, data=india_crime_data_by_state,
               fill_color='YlOrRd', fill_opacity=0.8,line_opacity=0.5,columns=['State/UT','Number of Victims under Other than Incest Rape Cases - Total Victims'],
               legend_name='State vs Rape cases',key_on='feature.id',name='choropleth')

folium.LayerControl().add_to(map1)
map1.save('C:/Users/khushal/Documents/Python Scripts/PyFolium_india.html')