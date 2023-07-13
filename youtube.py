import scrapetube
import pandas as pd
import streamlit as st
import re
import io
from xlsxwriter import Workbook
from streamlit_extras.buy_me_a_coffee import button
from langchain.document_loaders import YoutubeLoader

def extract_data(channel_username, limit, sort_by, search_query=None):
    s = 2
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

    if search_query:
        videos = filter_videos(videos, search_query)

    for video in videos:
        title = video['title']['runs'][0]['text']
        viewCountText = video['viewCountText']['simpleText']
        viewCount = re.sub(r'\D', '', viewCountText)
        videoId = video['videoId']  # for fun 🐍
        alink = video['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']
        base_link = "https://www.youtube.com"
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
            "viewCount": viewCount,
            "time": formatted_time,
            "description": desc,
            "link": link,
            "thumbnail": thumbnail
        }

        list_all_videos.append(all_info)

    return list_all_videos


def filter_videos(videos, search_query):
    filtered_videos = []
    regex = re.compile(search_query, re.IGNORECASE)

    for video in videos:
        title = video['title']['runs'][0]['text']

        if regex.search(title):
            filtered_videos.append(video)

    return filtered_videos
def Youtube_Extract(url):
    loader = YoutubeLoader.from_youtube_url(url)
    data =loader.load()
    dataa = data[0].page_content
    return (dataa)


def main():
    st.set_page_config(
        page_title="qashqaeii App",
        page_icon="y.png",
    )

    col1, col2 = st.columns([2, 1])
    col1.markdown("# YouTube Scraper")
    col1.markdown(
        "Data extraction from YouTube channel. With the help of this program, you can download a complete list of video titles, the number of views and time of the video, description, and the link to the videos in Excel file format.")

    col2.image("y.png", width=200)
    st.markdown("---")
    col3, col4 = st.columns([2, 1])
    channel_username = col3.text_input("Enter the channel username 🔎 ")
    search_query = col4.text_input("Search Keyword in Titles 🔎 ")
    number_input = col3.number_input("number Of Posts You want to scrape? (min = 1 & max = 500)", min_value=1, max_value=500,value=20) 
    selected_radio = col3.radio("Select your sort", ["newest", "oldest", "popular"])

    
    
    st.write("Developed by : HOSSEIN QASHQAEII 🧛 ")
    st.markdown("---")
    if st.button("Scrape Data"):
        if channel_username and selected_radio:
            extracted_videos = extract_data(channel_username, number_input, selected_radio, search_query)
            len_list = len(extracted_videos)
            df = pd.DataFrame(extracted_videos)
            excel_file = io.BytesIO()
            with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
            excel_file.seek(0)
            st.write(f"Scraped Videos ({len_list}) 🧲️")
            st.write(pd.DataFrame(extracted_videos))
            st.download_button("Download Excel 💾", data=excel_file, file_name=f'{channel_username}.xlsx')
            st.markdown("---")
            cols = st.columns(1)
            for x, video in enumerate(extracted_videos):
                with cols[x % 1]:
                    l = video["link"]
                    st.title(video["title"])
                    st.video(video["link"])
                    st.write(video["description"])
                    with st.expander("The Text Of Video 👇 "):
                        t = Youtube_Extract(l)
                        text = st.text_area("متن ویدیو", value=t)
                        if text:
                            st.download_button("Download", data=text, file_name=f"text.txt")

                    st.markdown("---")



        else:
            st.write("Please provide the channel username and select a sorting option.")
            st.markdown("---")


if __name__ == "__main__":
    main()
