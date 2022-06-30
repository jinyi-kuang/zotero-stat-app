import os
import json
import importlib_metadata
import streamlit as st
import pandas as pd 
import numpy as np
from pyzotero import zotero

#library_id = "5338560"
#api_key = "7KP3EZAufApf1GfDB1u2vMsU"

def login_ztr(library_id, library_type, api_key):
    ztr = zotero.Zotero(library_id, library_type, api_key)
    return ztr

def get_top_items(ztr, n):
    items = ztr.top(limit=n)
    for item in items:
        print('Item: %s | Key: %s' % (item['data']['itemType'], item['data']['key']))

def get_num_total_items(ztr):
    n = ztr.count_items()
    return n

def get_num_collectionitems(ztr, collectionID):
    n = ztr.num_collectionitems(collectionID)
    return n

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
    st.success("Thanks! I am working on getting your stats.")
    ztr = login_ztr(library_id, library_type, api_key)

    # display total number of items in the zotero library
    total_n = get_num_total_items(ztr)
    st.write("## The total number of items in your library is ", total_n)
    n_top = st.slider("choose the number of top items to display", min_value=0, max_value=50, step=1, value=5)
    top_items =  get_top_items(ztr, n_top)
    st.write('## The  top items in your library are', top_items)
    

if not submitted:
    st.stop()
