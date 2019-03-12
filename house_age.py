import requests
import pandas as pd
import sys
import time
from bs4 import BeautifulSoup

def main():
    df = pd.read_csv('house_data.csv')
    df.insert(3, 'age', value=0)
    print(df)

    for i, row in df.iterrows():
        headers= {
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, sdch, br',
            'accept-language':'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
            'cache-control':'max-age=0',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        url = df.at[i, 'url']

        response = requests.get(url, headers=headers)
        print("States code:", response.status_code)

        soup = BeautifulSoup(response.text, "lxml")
        #print(soup.prettify())
        mydivs = soup.find(attrs={'class': 'home-facts-at-a-glance-section'})
        #mydivs = soup.find("div", {"class": "home-facts-at-a-glance-section"})
        text = mydivs.get_text()
        print(text)

        index = text.find('Built')
        age = 2019-int(text[index+6:index+10])
        print(age)
        df.loc[[i], ['age']] = age
        time.sleep(1)
        

if __name__ == '__main__':
    main()