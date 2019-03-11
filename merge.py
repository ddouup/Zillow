import pandas as pd
import sys
import glob
import os


def main():
    dataframe = pd.DataFrame()
    count = 0

    for datafile in sorted(glob.glob("./processed_data/*.csv")):
        print("Processing ", datafile)

        df = pd.read_csv(datafile)
        dataframe = dataframe.append(df, ignore_index=True)

        count += df.shape[0]

    dataframe.reset_index()
    print(dataframe)

    path = './house_data.csv'
    print("Save to: ", path)
    dataframe.to_csv(path, index=False)

    print("Total Number of Houses: ", count)



if __name__ == '__main__':
    main()