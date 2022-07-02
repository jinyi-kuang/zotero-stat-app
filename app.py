import collections
import os
import json
import streamlit as st
import pandas as pd 
import numpy as np
from pyzotero import zotero

def login_ztr(library_id, library_type, api_key):
    ztr = zotero.Zotero(library_id, library_type, api_key)
    return ztr

def get_top_items(ztr, n):
    items = ztr.top(limit=n)
    df_raw = pd.json_normalize(items)
    df = df_raw[['data.itemType','meta.creatorSummary','data.title','data.date','data.publicationTitle', 'data.DOI','data.libraryCatalog']]
    df.columns = ['type','authors','title','date', 'journal', 'doi', 'catalog']
    return df

def get_num_total_items(ztr):
    n = ztr.count_items()
    return n

def get_num_items_by_collection(ztr):
    #Returns a library’s collections. This includes subcollections
    collections = ztr.collections()
    df_raw = pd.json_normalize(collections)
    df = df_raw[['data.key', 'data.name']]
    num = []
    for key in df['data.key']:
    # Returns the count of items in the specified collection
      num.append(ztr.num_collectionitems(key))
    df["count"] = num
    df.drop('data.key', axis='columns', inplace=True)
    df.rename(columns={'data.name':'collection'}, inplace=True)
    return df   

# page setting
st.set_page_config(
    layout="wide",
    page_title = "Track your reading statistics in zotero",
    page_icon = "📖"
 )

st.title("📖Track your reading statistics in zotero")
st.header("")

# get user info
form = st.form(key="annotation")

with form:
    ### inout userID
    st.write("""
    ## Step 1: Get your user ID
    - Your need to login to your zotero [here](https://www.zotero.org/user/login) to get your zotero userID and API key.
    - Your personal library ID is available [here](https://www.zotero.org/settings/keys), 
    - You can see a small line read like "Your userID for use in API calls is XXXXXXX."
    """)

    library_id = st.text_input("Copy and paste your userID below:")

    # input api key
    st.write("""
    ## Step 2: Get your API key
    - You need to get your zotero API key [here](https://www.zotero.org/settings/keys/new).
    - Give your personal key an name so you can manage it later.
    - Check Personal Library-> Allow library access and Allow notes access. 
    - Click **Save Key**.
    """
    )

    api_key = st.text_input("Copy and paste the api key below:")

    # select library type
    st.write("""
    ## Step 3: Select the type of your library 
    - Are you accessing your own Zotero library? Choose 'user'
    - Are you accessing a shared group library?  Choose 'group'.
    """)

    library_type = st.radio('Select one:', ['user', 'group'])
    submitted = st.form_submit_button(label="Submit")

if submitted:
    st.success("Thanks!")
    ztr = login_ztr(library_id, library_type, api_key)

    total_n = get_num_total_items(ztr)
    st.write("## The total number of items in your library is ", total_n)

    items_by_collections = get_num_items_by_collection(ztr)
    st.write('## The numbers of items in each collections are')
    st.dataframe(data=items_by_collections, width=None, height=None)

    top_items =  get_top_items(ztr, 10)
    st.write('## The most recently added/modified 10 items in your library are')
    st.dataframe(data=top_items, width=None, height=None)
    
    
    

if not submitted:
    st.stop()
