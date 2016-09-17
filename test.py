import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import time


def get_soup(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def has_class(tag, class_string):
    return tag.has_attr('class') and class_string in tag['class']

def cb_has_class(class_string):
    return lambda tag: has_class(tag, class_string)

def get_next_link(soup):
    return soup.find_all(cb_has_class('next-button'))[0].a['href']

def get_next_soup(soup):
    link = get_next_link(soup)
    return get_soup(link)

def get_posts(soup):
    things = soup.find_all(cb_has_class('thing'))
    return things

def get_title(post):
    a_s = post.find_all(lambda tag: tag.name == 'a' and has_class(tag, 'title'))
    title = [a.text for a in a_s if has_class(a, 'title')][0]
    return title

def get_subreddit(post):
    return post.find_all(cb_has_class('subreddit'))[0].text[3:]


num_pages = 20

soup = get_soup('https://www.reddit.com/top/?sort=top&t=all')
d = {}

for i in range(num_pages):
    print("Crawling page {}".format(i))
    for post in get_posts(soup):
        sub = get_subreddit(post)
        if sub not in d.keys():
            d[sub] = 1
        else:
            d[sub] += 1

    time.sleep(10)
    soup = get_next_soup(soup)

plt.bar(np.arange(len(d.keys())), d.values())
plt.xticks(np.arange(len(d.keys()))+0.5, list(d.keys()), rotation=90)