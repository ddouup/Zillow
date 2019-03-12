import pandas as pd
import sys
import glob
import os


def main():
    dataframe = pd.DataFrame()
    count = 0

    info = pd.DataFrame(columns=['State', 'Number', 'Percentage'])

    for datafile in sorted(glob.glob("./processed_data/*.csv")):
        print("Processing ", datafile)

        df = pd.read_csv(datafile)
        dataframe = dataframe.append(df, ignore_index=True)

        state = os.path.basename(datafile).split('.')[0]
        info = info.append({'State': state, 'Number': df.shape[0], 'Percentage': None}, ignore_index=True)
        count += df.shape[0]

    dataframe.reset_index()
    print(dataframe)
    
    for i, row in info.iterrows():
        percentage = info.at[i,'Number']/float(count)
        info.loc[[i], ['Percentage']] = percentage
    
    print(info)
    path = './house_data.csv'
    print("Save to: ", path)
    #dataframe.to_csv(path, index=False)
    #info.to_csv('./info.csv', index=False)

    print("Total Number of Houses: ", count)



if __name__ == '__main__':
    main()