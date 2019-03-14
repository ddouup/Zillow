import requests
import pandas as pd
import sys
import time
from bs4 import BeautifulSoup


def main():
    df = pd.read_csv('final_data.csv')
    
    df.insert(2, 'income(USD)', value='N/A')
    df.insert(2, 'density(sq mi)', value='N/A')
    df.insert(len(df.columns), 'city_wiki', value='N/A')
    df.insert(len(df.columns), 'text', value='N/A')

    print(df)

    for i, row in df.iterrows():
        print()
        city = row['city'].title().replace(' ', '_')
        state = row['state']

        url = 'https://en.wikipedia.org/wiki/'+city+',_'+state

        #url = 'https://en.wikipedia.org/wiki/Huntsville,_AL'
        print(url)
        df.loc[[i], ['city_wiki']] = url

        response = requests.get(url)
        print("States code:", response.status_code)
        if response.status_code == 404:
            continue

        soup = BeautifulSoup(response.text, "lxml")
        #print(soup.prettify())
        
        # Find Population Density
        print('Find Population Density...')
        table = soup.find("table", attrs={'class': 'infobox geography vcard'})
        if table != None:
            text = table.get_text()
            #print(text)
            begin = text.find('Density')
            text = text[begin:]
            end = text.find('/')
            text = text[:end]

            density = text[7:]
            print('Density: ', density)
            print()
            df.loc[[i], ['density(sq mi)']] = density

        # Find Median Income
        print('Find Median Income...')
        body = soup.find("div", attrs={'id': 'mw-content-text'})
        if body != None:
            text = body.get_text()
            # Find the paragraph contains 'income'
            paragraphs = text.split('\n')
            for para in paragraphs:
                if ' income ' in para:
                    paragraph = para
                    break
            '''        
            index = text.find('income')
            begin = text[:index].rfind('\n')
            text = text[begin+1:]
            text = text[:text.find('\n')]
            print(text)
            '''
            print(para)
            df.loc[[i], ['text']] = para

            target = para[para.find('median'):]
            target = target[target.find('$'):]
            target = target.replace('.', ',')
            target = target.replace(' ', ',')
            #print(target)
            income = target.replace(',', '', 1)[1:target.replace(',', '', 1).find(',')]
            print('Income: ', income)
            print()
            df.loc[[i], ['income(USD)']] = income
        
    df.to_csv('f_data.csv', index=False) 


if __name__ == '__main__':
    main()