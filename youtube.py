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

#-----------------------------------------------------------------------------------
def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
#------------------------------------------
def translate_text(text):
    chunk_size = 4000
    text_size = len(text)
    print(text)
    translated_chunks = []
    for i in range(0, text_size, chunk_size):
        chunks = text[i:i + chunk_size]
        translated = GoogleTranslator(source='auto', target='fa').translate(chunks)
        translated_chunks.append(translated)
    translated_text = ' '.join(translated_chunks)
    return translated_text
#------------------------------------------
def extract_data(channel_username, limit, sort_by):
    s = 2
    list_all_videos = []
    sort_by_map = {
        "newest": "newest",
        "oldest": "oldest",
        "popular": "popular"
    }
    sort_option = sort_by_map.get(sort_by, "newest")
    videos = scrapetube.get_channel(channel_username=channel_username, limit=int(limit), sleep=s, sort_by=sort_option,
                                    content_type='videos')
    for video in videos:
        title = video['title']['runs'][0]['text']
        viewCountText = video['viewCountText']['simpleText']
        viewCount = re.sub(r'\D', '', viewCountText)
        videoId = video['videoId']  # for fun 🐍
        alink = video['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
        base_link = "https://www.youtube.com"#develop By Hossein Qashqaeii
        link = f"{base_link}{alink}"
        thumbnail = video['thumbnail']['thumbnails'][0]['url']
        desc = video['descriptionSnippet']['runs'][0]['text']
        time = video['lengthText']['accessibility']['accessibilityData']['label']
        time_parts = time.split(",")
        try:
            minutes = time_parts[0].split()[0]
        except:
            minutes = "00"
        try:
            seconds = time_parts[1].split()[0]
        except:
            seconds = "00"

        formatted_time = f"{minutes}:{seconds}"

        all_info = {
            "title": title,
            "time": formatted_time,
            "link": link,
            "viewCount": viewCount,
            "description": desc,
            
        }

        list_all_videos.append(all_info)

    return list_all_videos

def Youtube_Extract(url):
    loader = YoutubeLoader.from_youtube_url(url)
    data = loader.load()
    dataa = data[0].page_content
    return (dataa)


def main():
    st.set_page_config(
        page_title="qashqaeii App",
        page_icon="y.png",
    )

    col1, col2 = st.columns([2, 1])
    col1.markdown("# YTMiner Pro")
    col1.markdown("""
    YTMiner Pro is a professional YouTube mining tool that extracts valuable video data effortlessly. 
    
    Dive into YouTube analytics by scraping titles, views, durations, descriptions, links, and even extract the full text from videos. 
    
    Gain deep insights and make data-driven decisions with ease using YTMiner Pro's comprehensive scraping and text extraction features
    
    """)

    with col2:
        lottie_resume = load_lottiefile("youtube.json")
        st_lottie(
            animation_source=lottie_resume,
            speed=1,
            reverse=False,
            loop=True,
            quality="high",
            height=None,
            width=250,
            key=None,
        )
    
    st.markdown("#### Options")
    with st.form("form1",clear_on_submit=False):
        col3, col4 = st.columns([8, 5])
        channel_username = col3.text_input("Enter the channel username 🔎 ")
        
        number_input = col3.number_input("number Of Posts You want to scrape? (min = 1 & max = 500)", min_value=1,
                                        max_value=500, value=20)
        selected_radio = col4.radio("Select your sort 📑", ["newest", "oldest", "popular"])

        if st.form_submit_button("Scrape Data"):    
            if channel_username and selected_radio:    
                try:
                    extracted_videos = extract_data(channel_username, number_input, selected_radio)                       
                    len_list = len(extracted_videos)
                    df = pd.DataFrame(extracted_videos)
                    excel_file = io.BytesIO()
                    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
                        df.to_excel(writer, sheet_name='Sheet1', index=False)
                    excel_file.seek(0)
                    st.write(f"Scraped Videos ({len_list}) 🧲️")
                    st.write(pd.DataFrame(extracted_videos))
                    st.markdown("---")
                    cols = st.columns(1)
                except:
                    st.warning("Username is Not True ",icon="🚨")

            else:
                st.warning("Please Enter Channel Username",icon="🚨")    
    with st.form("form2"):
        col3, col4 = st.columns([8, 5])
        url_query = col3.text_input("Search For Url  🔎 ")
        if st.form_submit_button("Serch For"): 
            if url_query:
                st.video(url_query)
                text_url = Youtube_Extract(url_query)
                trans_text_url = translate_text(text_url)
                st.text_area("فارسی",value= trans_text_url)
                st.text_area("English",value=text_url)

            else:
                st.warning("Please enter Url ",icon="🚨")    

                
#st.download_button("Download Excel 💾", data=excel_file, file_name=f'{channel_username}.xlsx')
#st.download_button("دانلود متن ترجمه شده", data=t_text, file_name=f"text.txt")
#if text:
#st.download_button("Download", data=text, file_name=f"text.txt")

        else:
            st.write("Please provide the channel username and select a sorting option Or Give Us English Video Url To Translat")
            
    st.markdown("-----")

    st.write("Developed by : qashqaeii.ps4@gmail.com 🧛 (حسین قشقایی)")

if __name__ == "__main__":
    main()