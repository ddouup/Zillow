import requests
import pandas as pd
import sys
import time
from bs4 import BeautifulSoup

def main():
    df = pd.read_csv('house_data.csv')
    df.insert(3, 'age', value='N/A')
    print(df)

    for i, row in df.iterrows():
        headers= {
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control':'max-age=0',
            'cookie':'abtest=3|DNFSDZ6PkaodaWRO6A; zguid=23|%2475513e67-9152-49f0-bbdb-add371ad1684; _ga=GA1.2.1927619733.1545098043; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%2275513e67-9152-49f0-bbdb-add371ad1684%22; __gads=ID=0a799997d43b84c6:T=1545098050:S=ALNI_MaxBnU3SosPBAnEcHbC-papsQa_zQ; _gcl_au=1.1.1128270467.1545098098; G_ENABLED_IDPS=google; KruxPixel=true; KruxAddition=true; _mkto_trk=id:324-WZA-498&token:_mch-zillow.com-1552220228011-85437; ki_r=; zgsession=1|7c568c73-21c2-48cc-a656-58b7b34932b8; _gid=GA1.2.258313923.1552367691; DoubleClickSession=true; ki_s=172156%3A0.0.0.0.2%3B195609%3A0.0.0.0.0%3B195614%3A0.0.0.0.0%3B195617%3A0.0.0.0.0; JSESSIONID=52A3FC2012FBD40C320B919175009893; _gat=1; search=6|1554964924121%7Crect%3D60.558924%252C-150.718947%252C60.522453%252C-150.897131%26zm%3D12%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26sort%3Ddays%26z%3D1%26fs%3D1%26fr%3D1%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%09%01%0926%09%09%092%090%09US_%09; _px3=56b7d57716c7e9e719548665ee5fb691f5a7ccba201c141186905237be284b16:y1KcdQbw7nFyLvKfzW0goSPt7pPPTacb+IHRYglh9oWak5HlLEPDMrqJA/IxZITZ1vuOOOHUjBnu2GC+439tIQ==:1000:1gV8UiwvhUlROYkbq6pOURUVQ0TTGr+6XLL4xBushXVxFAq6dikT88D9mf43Z4actyh/oTs5hbMoTOOWWKTRrhdLCxEaK7CpMdibnP4UgXqgAieVqISDYg7sHPjzN30Cec37z/C2Fk13YXUGTYStUxccVv8lJStahuWChnVq9Cs=; ki_t=1552222463732%3B1552367695376%3B1552372926531%3B2%3B12; AWSALB=TpLZsDncnqtb3imNPpq3g3tYsXp+9cvrXD7iifCsC22UweN0cYnj2w+dlDbILSNLGKNDTgmNGkNZw2gmXihRu6HtDoHmOtyjLdp6ZvPcLcm6wXYJFc11bJM44dn7',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        url = df.at[i, 'url']

        print()
        print(i)
        print(url)
        response = requests.get(url, headers=headers)
        print("States code:", response.status_code)

        soup = BeautifulSoup(response.text, "lxml")
        #print(soup.prettify())
        mydivs = soup.find(attrs={'class': 'home-facts-at-a-glance-section'})
        #mydivs = soup.find("div", {"class": "home-facts-at-a-glance-section"})
        if mydivs == None:
            break

        text = mydivs.get_text()
        print(text)

        index = text.find('Built')
        try:
            year = int(text[index+6:index+10])
            age = 2019-year
        except Exception as e:
            age = 'N/A'
        
        print('House age:', age)
        df.loc[[i], ['age']] = age
        #sys.exit()
        #time.sleep(1)
    
    df.to_csv('final_data.csv', index=False)

if __name__ == '__main__':
    main()