import re

from bs4 import BeautifulSoup
from urllib.request import urlopen
from pandas import DataFrame, concat
import requests
from tqdm import tqdm


def get_urls_from_rev_site():
    url_list = []
    for i in range(3):
        url = f"https://www.rev.com/blog/transcript-tag/donald-trump-interview-transcripts/page/{i}"
        page = urlopen(url)
        soup = BeautifulSoup(page, "lxml")
        contents = soup.find_all('div', {"class": "fl-post-column"})
        for content in contents:
            url_list.append(content.find('a').get('href'))
    return url_list


def scrape_one_page(url):
    # It is applicable only for the pages
    # from https://www.rev.com/blog/transcript-tag/donald-trump-interview-transcripts/
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup.find("div", {"class": "fl-callout-text"}).get_text()


def parse_one_page_text(scraping_output) -> DataFrame:
    speakers_list = []
    minutes_list = []
    texts_list = []

    def is_name_and_time(str_name_and_time):
        return (len(str_name_and_time.split()) < 7) and \
               bool(re.search(r"(\([0-9]+:[0-9]+:[0-9]+\))|(\([0-9]+:[0-9]+\))", str_name_and_time))

    scraping_output_list = scraping_output.split('\n')[:-1]
    for index, item in enumerate(scraping_output_list):
        if ((index + 1 != len(scraping_output_list))
                and is_name_and_time(item) and
                (not is_name_and_time(scraping_output_list[index + 1]))):
            # speaker and minutes
            speaker, minutes = item.split(': ')
            speakers_list.append(speaker)
            minutes_list.append(minutes[1:-1])
        elif not is_name_and_time(item) and not ('Part ' in item):
            # texts
            texts_list.append(item)
        else:
            pass

    return DataFrame({
        'speaker': speakers_list,
        'minute': minutes_list,
        'text': texts_list
    })


def scrape_and_get_df():
    df_list = []
    url_list = get_urls_from_rev_site()
    for i, url in enumerate(tqdm(url_list)):
        print(url)
        df = parse_one_page_text(scrape_one_page(url))
        df['page_number'] = [i] * len(df)
        df_list.append(df)
    return concat(df_list)


df_overall = scrape_and_get_df()
df_overall.to_csv("data/trump_transcripts.csv")
