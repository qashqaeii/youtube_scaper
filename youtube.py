import scrapetube
import pandas as pd
import streamlit as st
import re
import io
from xlsxwriter import Workbook

def extract_data(channel_username, limit, sort_by):
    s = 2
    x = -1
    list_all_videos = []

    sort_by_map = {
        "newest": "newest",
        "oldest": "oldest",
        "popular": "popular"
    }

    # If sort_by is empty, use "newest" as the default sorting option
    sort_option = sort_by_map.get(sort_by, "newest")

    videos = scrapetube.get_channel(channel_username=channel_username, limit=int(limit), sleep=s, sort_by=sort_option,
                                    content_type='videos')

    for video in videos:
        title = video['title']['runs'][x + 1]['text']
        viewCountText = video['viewCountText']['simpleText']
        viewCount = re.sub(r'\D', '', viewCountText)
        videoId = video['videoId'] #for fun 🐍
        alink = video['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
        base_link = "https://www.youtube.com"
        link = f"{base_link}{alink}"
        desc = video['descriptionSnippet']['runs'][x + 1]['text']
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
            "viewCount": viewCount,
            "time": formatted_time,
            "description": desc,
            "link": link,
        }
        
        list_all_videos.append(all_info)

    return list_all_videos


# Streamlit setup
def main():
    st.set_page_config(
        page_title="qashqaeii App",
        page_icon="y.png",
    )
    
    col1, col2 = st.columns([2, 1])
    col1.markdown("# YouTube Scraper")
    col1.markdown("Data extraction from YouTube channel. With the help of this program, you can download a complete list of video titles, the number of views and time of the video, description, and the link to the videos in Excel file format.")
    
    col2.image("y.png", width=200)
    st.markdown("---")

    channel_username = st.text_input("Enter the channel username:🔎")
    number_input = st.number_input("Enter a number For Posts ? (min = 1 & max = 500)", min_value=1, max_value=500,
                                   value=10)
    selected_radio = st.radio("Select your sort", ["newest", "oldest", "popular"])
    st.markdown("---")
    st.write("developed by : HOSSEIN QASHQAEII 🧛 ")
    if st.button("Scrape Data"):
        if channel_username and selected_radio:
            extracted_videos = extract_data(channel_username, number_input, selected_radio)
            st.write(f"Scraped Videos  ({len(extracted_videos)}) 🧲️")
            st.write(pd.DataFrame(extracted_videos))
            st.markdown("---")
            df = pd.DataFrame(extracted_videos)
            excel_file = io.BytesIO()
            with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
            excel_file.seek(0)
            st.download_button("Download Excel 💾", data=excel_file, file_name=f'{channel_username}.xlsx')
            
        else:
            st.write("Please provide the channel username and select a sorting option.")
            st.markdown("---")


if __name__ == "__main__":
    main()
