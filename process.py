import pandas as pd
import sys
import glob
import os
import locale

def main():
    count = 0
    for datafile in glob.glob("./data/*.csv"):
        print("Processing ", datafile)
        df = pd.read_csv(datafile)
        df = df.drop(['title', 'postal_code', 'real estate provider'], axis=1)
        print(df)
        print()

        df.insert(2, 'sqft', value='.')
        df.insert(2, 'ba', value='.')
        df.insert(2, 'bds', value='.')
        df.insert(2, 'price(USD)', value='.')

        for i, row in df.iterrows():
            info = df.loc[[i], ['facts and features']]
            info = info.to_string().split(' , ')

            #print(info[0].split(' ')[-2])
            #print(info[1].split(' ')[-2])
            #print(locale.atoi(info[2].split(' ')[-2]))

            df.loc[[i], ['bds']] = info[0].split(' ')[-2]
            df.loc[[i], ['ba']] = info[1].split(' ')[-2]
            df.loc[[i], ['sqft']] = locale.atoi(info[2].split(' ')[-2])

            price = df.loc[[i], ['price']]
            #print(locale.atoi(price.to_string().split()[2][1::]))
            df.loc[[i], ['price(USD)']] = locale.atoi(price.to_string().split()[2][1::])

        df = df.drop(['facts and features', 'price'], axis=1)

        count += df.shape[0]

        print(df)

        path = './processed_data/'+os.path.basename(datafile)
        print(path)
        df.to_csv(path, index=False)

    print("Total Number of Houses: ", count)

if __name__ == '__main__':
    locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 
    main()