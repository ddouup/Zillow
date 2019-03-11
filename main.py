import requests
import pandas as pd
import sys
import math
import unicodecsv as csv
import argparse
from lxml import html
from bs4 import BeautifulSoup

def parse(zipcode, num, filter=None):
    properties_count = 0
    page_count = 1

    if filter=="newest":
        url = "https://www.zillow.com/homes/for_sale/{0}/0_singlestory/days_sort".format(zipcode)
    elif filter == "cheapest":
        url = "https://www.zillow.com/homes/for_sale/{0}/0_singlestory/pricea_sort/".format(zipcode)
    else:
        #url = "https://www.zillow.com/homes/for_sale/{0}_rb/?fromHomePage=true&shouldFireSellPageImplicitClaimGA=false&fromHomePageTab=buy".format(zipcode)
        url = 'https://www.zillow.com/homes/for_sale/'+zipcode+'_rb/'

    properties_list = []

    while True:
        # try:
        headers= {
                    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'accept-encoding':'gzip, deflate, sdch, br',
                    'accept-language':'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
                    'cache-control':'max-age=0',
                    'upgrade-insecure-requests':'1',
                    'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        
        page_url = url+str(page_count)+'_p'
        print(page_url)
        response = requests.get(page_url,headers=headers)
        print("States code:", response.status_code)
        parser = html.fromstring(response.text)
        search_results = parser.xpath("//div[@id='search-results']//article")

        print('Number of houses:', len(search_results))

        for properties in search_results:
            raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
            raw_city = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressLocality']//text()")
            raw_state= properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressRegion']//text()")
            raw_postal_code= properties.xpath(".//span[@itemprop='address']//span[@itemprop='postalCode']//text()")
            raw_price = properties.xpath(".//span[@class='zsg-photo-card-price']//text()")
            raw_info = properties.xpath(".//span[@class='zsg-photo-card-info']//text()")
            raw_broker_name = properties.xpath(".//span[@class='zsg-photo-card-broker-name']//text()")
            urls = properties.xpath(".//a[contains(@class,'overlay-link')]/@href")
            raw_title = properties.xpath(".//h4//text()")
            
            address = ' '.join(' '.join(raw_address).split()) if raw_address else None
            city = ''.join(raw_city).strip() if raw_city else None
            state = ''.join(raw_state).strip() if raw_state else None
            postal_code = ''.join(raw_postal_code).strip() if raw_postal_code else None
            price = ''.join(raw_price).strip() if raw_price else None
            info = ' '.join(' '.join(raw_info).split()).replace(u"\xb7",',')
            broker = ''.join(raw_broker_name).strip() if raw_broker_name else None
            title = ''.join(raw_title) if raw_title else None
            property_url = "https://www.zillow.com"+urls[0] if urls else None 
            is_forsale = properties.xpath('.//span[@class="zsg-icon-for-sale"]')
            properties = {
                            'address':address,
                            'city':city,
                            'state':state,
                            'postal_code':postal_code,
                            'price':price,
                            'facts and features':info,
                            'real estate provider':broker,
                            'url':property_url,
                            'title':title
            }
            if is_forsale:
                properties_list.append(properties)
                properties_count += 1

            if properties_count == num:
                print(properties_count)
                print(num)
                break

        print(properties_count)
        page_count += 1
        if properties_count == num:
            print(properties_count)
            print(num)
            break

    return properties_list
        # except:
        #   print ("Failed to process the page",url)


def getState(code, num, sort=None):
    print ("Fetching data for %s"%(code))
    scraped_data = parse(code,num,sort)
    print ("Writing data to output file: /data/%s.csv"%(code))
    with open("./data/%s.csv"%(code),'wb')as csvfile:
        fieldnames = ['title','address','city','state','postal_code','price','facts and features','real estate provider','url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in  scraped_data:
            writer.writerow(row)


def main():
    df = pd.read_csv('data.csv')

    '''
    argparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument('code',help = '')
    sortorder_help = """
    available sort orders are :
    newest : Latest property details,
    cheapest : Properties with cheapest price
    """
    argparser.add_argument('sort',nargs='?',help = sortorder_help,default ='Homes For You')
    args = argparser.parse_args()
    code = args.code
    sort = args.sort
    '''
    sort = None
    total_num = 0
    for i, row in df.iterrows():
        code = row['Code']
        num = math.ceil(2000*row['% of US'])
        getState(code, num, sort)
        total_num += num

    print(total_num)



def preprocess():
    df = pd.read_csv('data.csv')
    print(df)

    dic = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'District of Columbia': 'DC',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
    }


    df.insert(2, 'Code', value='.')
    for i, row in df.iterrows():
        df.loc[[i], ['Code']] = dic[row['State']]

    print(df)

    df.to_csv('data.csv', index=False)

if __name__ == '__main__':
    #preprocess()
    main()