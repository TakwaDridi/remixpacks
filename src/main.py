from extract.extract import extract_raw_data
from preprocess.preprocess import clean_data

if __name__ == '__main__':
    total_pages = 10
    df = extract_raw_data(total_pages)
    df = clean_data(df)
    df.to_csv('clean_data.csv', header=True, index=False, sep=',')
    print(df.sample(5))
