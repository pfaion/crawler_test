import requests
import time
import matplotlib.pyplot as plt
import numpy as np

headers = {
    'User-Agent': 'osx:testApp:v0.1 (by /u/xsinthx)'
}

response = requests.get('https://www.reddit.com/top.json', params = {'t': 'all', 'limit': 100}, headers = headers)
data = response.json()['data']

pages = 10
collector = {}

for i in range(pages):
    print("Crawling page {}".format(i))
    for child in data['children']:
        post = child['data']
        sub = post['subreddit']
        if sub in collector.keys():
            collector[sub] += 1
        else:
            collector[sub] = 1

    time.sleep(2)
    last_child = data['children'][-1]
    last_name = last_child['data']['name']
    response = requests.get('https://www.reddit.com/top.json', params = {'t': 'all', 'limit': 100, 'after': last_name}, headers = headers)
    data = response.json()['data']



counts = sorted(collector.items(), key = lambda item: item[1], reverse=True)

names, nums = zip(*counts)

plt.bar(range(len(nums)), nums)
plt.xticks(np.arange(len(nums)) + 0.5, names, rotation=90)
