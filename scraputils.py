import requests
from bs4 import BeautifulSoup
import time
from bottle import (
    route, run, template, request, redirect
)

from db import News, session
from bayes import NaiveBayesClassifier

def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    tbl_list1 = []  # points
    id_all = []
    tbl_list2 = []
    tbl_list3 = []
    tbl_list4 = []  # comments
    tbl_list5 = []  # points\
    tbl_list = parser.findAll(attrs={"class": "athing"})  # all
    for all_inf in tbl_list:
        try:
            tbl_list5.append(all_inf.find('span', attrs={"class": 'sitestr'}).text)  # url
        except:
            tbl_list5.append('None')
        try:
            tbl_list3.append(all_inf.find(attrs={"class": "storylink"}).text)  # title
        except:
            tbl_list3.append('None')

    id = parser.findAll(attrs={"class": "athing"})
    for id_num in id:
        id_all.append(int(str(id_num).split('"')[3]))

    for i in range(30):
        try:
            if (parser.findAll(attrs={"href": f"item?id={id_all[i]}"}))[-1].text == 'discuss':  # comments
                tbl_list4.append(0)
            else:
                tbl_list4.append(parser.findAll(attrs={"href": f"item?id={id_all[i]}"})[-1].text.split()[0])
        except:
            tbl_list4.append(0)

    for id_aut in id_all:

        try:
            tbl_list1.append(parser.find(attrs={"id": f"score_{id_aut}"}).text.split()[0])  # points
        except:
            tbl_list1.append(0)
    tbl_list = parser.findAll('td',attrs={"class": "subtext"})
    for i in tbl_list:
        try:
            tbl_list2.append(i.find(attrs={"class": "hnuser"}).text) #author
        except:
            tbl_list2.append('None')
    print(len(tbl_list2))

    for i in range(30):
        diction = {}
        diction['author'] = tbl_list2[i]
        diction['points'] = int(tbl_list1[i])
        diction['comments'] = int(tbl_list4[i])
        diction['title'] = tbl_list3[i]
        diction['url'] = tbl_list5[i]
        news_list.append(diction)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    # PUT YOUR CODE HERE
    tbl_list = parser.findAll(attrs={"class": "morelink"})
    start_let1 = str(tbl_list).index('newest')
    start_let2 = str(tbl_list).index('&')
    number = str(tbl_list)[start_let1:start_let2 + 1]
    start_let3 = str(tbl_list).index('n', start_let2)
    start_let4 = str(tbl_list).index(' ', start_let3)
    number2 = str(tbl_list)[start_let3:start_let4 - 1]
    return number+number2


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
        time.sleep(3)
    return news


'''pages = get_news("https://news.ycombinator.com/newest", 35)
print(pages)
s = session()
news = []

for i in pages:
    news.append(News(title=i['title'], author=i['author'], url=i['url'], comments=i['comments'],  points=i['points']))
s.bulk_save_objects(news)
s.commit()

'''