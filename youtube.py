import time
import scrapetube
import pandas as pd
import streamlit as st
import re
import io
from xlsxwriter import Workbook
from streamlit_extras.buy_me_a_coffee import button
from langchain.document_loaders import YoutubeLoader
from streamlit_lottie import st_lottie
import json
from deep_translator import GoogleTranslator
import requests

#-----------------------------------------------------------------------------------
def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
#__________________________________________________________________________________________
def translate_text(text):
    chunk_size = 4000
    text_size = len(text)
    
    translated_chunks = []
    for i in range(0, text_size, chunk_size):
        chunks = text[i:i + chunk_size]
        translated = GoogleTranslator(source='auto', target='fa').translate(chunks)
        translated_chunks.append(translated)
    translated_text = ' '.join(translated_chunks)
    return translated_text
#___________________________________________________________________________________________
def download_link(url):       
    headers = {
    'authority': 'srvcdn9.2convert.me',
    'accept': '*/*',
    'accept-language': 'en,fa;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'null',
    'referer': 'https://en1.y2mate.is/',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'x-csrf-token': '4yYLiSLCQJfE8eztZErbMCHE1b7eRHY3zotWJNLr',
    }
    llll=(f"https://srvcdn9.2convert.me/api/json?url={url}")
    response = requests.get(llll,headers=headers,)
    data = response.json()
    list_info = []
    if data['formats']['video'][4]['quality'] == "720p":
        link720 = data['formats']['video'][4]['url']  
    link_audio = data['formats']['audio'][0]['url']
    title =  data['formats']['basename']
    thumbnail =data['formats']['thumbnail']  
    rows = {
        "title" : title,
        "linkvideo" : link720,
        "linkaudio": link_audio,
        "thumbnail" : thumbnail
    }
    list_info.append(rows)
    return (list_info)
#___________________________________________________________________________________________
def Youtube_Extract(url):
    loader = YoutubeLoader.from_youtube_url(url)
    data = loader.load()
    try:
        dataa = data[0].page_content
    except:
        dataa = "ویدیو به زبان انگلیسی نیست"
    return (dataa)
#___________________________________________________________________________________________
#___________________________________________________________________________________________
def main():
    st.set_page_config(
        page_title="qashqaeii App",
        page_icon="y.png",
    )
    st.markdown("""
    <style type="text/css">
    body{
    direction:rtl;
    }
    </style>
""",unsafe_allow_html=True)
    col11, col22 = st.columns([2, 5])
    with col11:
        lottie_resume = load_lottiefile("youtube.json")
        st_lottie(
            animation_source=lottie_resume,
            speed=1,
            reverse=False,
            loop=True,
            quality="high",
            height=None,
            width=100,
            key=None,
        )
    with col22:
        st.markdown("# یوتوبر شو")
        st.markdown("""
        ###### به کمک این برنامه میتوانید متن کامل مربوط به
        ###### هر ویدیو یوتوب را هم به زبان فارسی و هم به زبان انگلیسی 
        ###### دریافت کنید .
        ###### توجه داشته باشد که ویدیو باید به زبان انگلیسی باشد
        """)
    with st.form("form2"):
        col3, col4 = st.columns([8, 5])
        url_query = col3.text_input(" لینک ویدیو مورد نظر را وارد کنید 🔎 ")
        if st.form_submit_button("جستجو"): 
            if url_query:
                st.video(url_query)
                text_url = Youtube_Extract(url_query)
                trans_text_url = translate_text(text_url)
                downl = download_link(url_query)
                title = downl[0]["title"]
                translate_title = translate_text(title)
                with st.expander(" متن کامل انگلیسی"):  
                    st.write(f"title : {title}")
                    st.text_area("English",value=text_url)
                with st.expander("ترجمه کامل فارسی"):  
                    st.write(f"عنوان : {translate_title}")                 
                    st.text_area("فارسی",value= trans_text_url)

                if downl:
                    link720 = downl[0]["linkvideo"]
                    linkaudio = downl[0]["linkaudio"]
                    tumb = downl[0]["thumbnail"]
                with st.expander(" لینک دانلود ویدیو"):
                    st.markdown(f"({link720})")
                with st.expander("لینک دانلود عکس کاور"):
                    st.markdown(f"({tumb})")    
                    
            else:
                st.warning("Please enter Url ",icon="🚨")                  
        else:
            st.write("لطفا لینک ویدیو مورد نظر را وارد کنید")
    st.markdown("-----")
    st.write("Developed by : qashqaeii.ps4@gmail.com 🧛 (حسین قشقایی)")
if __name__ == "__main__":
    main()