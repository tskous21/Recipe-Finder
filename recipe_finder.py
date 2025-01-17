import streamlit as st
import pandas as pd
import numpy as np
import random
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as soup
from random import randint
from time import sleep
from urllib.request import Request, urlopen

pd.set_option('display.max_colwidth', None)

def find_ingredient(searchvals, ing_list):
    return all([any(val in string for string in ing_list) for val in searchvals])

def clean_ing(ings):
    clean = [ing.strip(" ,*") for ing in ings]
    return clean

def calc_time(time):
    try:
        hours = 0
        minutes = 0
        if time.find("hour") > -1:
            hours = int(time[:time.find("hour")-1].strip(" +:"))*60
        if time.find("min") > -1:
            minutes = int(time[time.find("min")-3: time.find("min")-1].strip(" +:"))
        return hours + minutes
    except:
        return 0

def convert(row):
    #print(row)
    return '<a href="{0}" target="_blank">{0}</a>'.format(row)
    
st.title('Recipe Finder')

searchlist = st.text_area('Enter the ingredients you want to search, line by line')

searchlist = searchlist.lower().split('\n')

#st.write(type(searchlist))

master = pd.read_csv(r'C:\Users\tanne\Documents\GitHub\Recipe-Finder\recipes_master.csv')

master = master.reset_index(drop=True)

master.Ingredients = master.Ingredients.str.replace("'","").str.strip('][').str.split(', ')

#master.Time = master.Time.apply(calc_time)

master.Link = master.Link.apply(convert)

#searchlist = ['sun-dried', 'cream']

df = master.loc[master.Ingredients.apply(lambda x: find_ingredient(searchlist, x)), ['Blog', 'Recipe', 'Link', 'Time']].sort_values('Time').reset_index(drop = True)

st.write(df.to_html(escape=False), unsafe_allow_html=True)