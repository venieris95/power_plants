from re import I
from numpy import string_
import streamlit as st
import pandas as pd     
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium


##THE TUTORIAL I AM WORKING WITH https://www.youtube.com/watch?v=uXj76K9Lnqc&ab_channel=ZakariaChowdhury

##TITLE
APP_TITLE = "Powerplants Interactive Map"
APP_SUBTITLE = "Source: TBD"


def filter_country(df, country, primary_fuel, metric_title_country):
        if (primary_fuel != 'All'):
            if country != 'World':
                df = df[(df['country_long'] == country) & (df['primary_fuel'] == primary_fuel)] 
                total = df.shape[0]
                st.metric(metric_title_country, total)
            else:
                df = df[df['primary_fuel'] == primary_fuel]
                total = df.shape[0]
                st.metric(metric_title_country,total)
        elif (primary_fuel =='All'):
                if country != 'World':
                    df = df[df['country_long'] == country]
                    total = df.shape[0]
                    st.metric(metric_title_country, total)
                else:
                    total = primary_fuel
                    total = df.shape[0]
                    st.metric(metric_title_country, total)

##TODO FILTER BY CAPACITY
def loc_data(df):
    loc_data = pd.DataFrame({
                'lat': df['latitude'], 
                'lon': df['longitude'],
                'name': df['name'],
                'fuel': df['primary_fuel']
                })
    st.write(loc_data)
    st.map(loc_data)

def display_map(df, primary_fuel,country):
        if (primary_fuel != 'All'):
            if country != 'World':
                df = df[(df['country_long'] == country) & (df['primary_fuel'] == primary_fuel)] 
        ##TAKE COORDINATES AND NAME
                loc_data(df)
            else:
                df = df[df['primary_fuel'] == primary_fuel]
                loc_data(df)
        elif(primary_fuel == 'All'):
            if country != 'World':
                df = df[df['country_long'] == country]
                loc_data(df)
            else:
                loc_data(df)
                
def main():
    st.set_page_config(layout="wide")
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)

    @st.cache(persist = True)
    def load_data(nrows):
        df = pd.read_csv('data\global_power_plant_database.csv') 
        return df
    df = load_data(400000)

    primary_fuel_list = ['All'] + list(df['primary_fuel'].unique())
    primary_fuel_list.sort()
    primary_fuel = st.sidebar.selectbox('Primary fuel Source',primary_fuel_list,index = 0)
    
    country_list = ['World'] + list(df['country_long'].unique().astype(str))
    country_list.sort()
    country = st.sidebar.selectbox('Country',country_list,index = 164)

    metric_title_primary_fuel = f'Total Number of {primary_fuel} Power Plants'
    metric_title_country = f'Total Number of {primary_fuel} Power Plants in {country}'
        
 
    filter_country(df, country, primary_fuel, metric_title_country)
    
    display_map(df, primary_fuel,country)
    
if __name__ == "__main__":
    main()