import pandas as pd

pd.set_option("display.max_columns", 100)
pd.set_option("display.max_rows", 1000)


def clean_data(df):
    print(f'Started cleaning raw data')

    renamed_columns = {'year of song': 'year_of_song',
                       'bpm1': 'beats_per_minute'}

    df.rename(columns=renamed_columns, inplace=True)

    max_str_length = 10
    invalid_key = df.loc[:, 'key'].str.len() > max_str_length
    df.loc[invalid_key, 'key'] = pd.NA
    max_str_length = 30
    invalid_key = df.loc[:, 'artist'].str.len() > max_str_length
    df.loc[invalid_key, 'artist'] = pd.NA

    chars_to_remove = [',', '?', '!']

    for char in chars_to_remove:
        df.loc[:, 'key'] = df.loc[:, 'key'].str.replace(char, '', regex=True)
        df.loc[:, 'artist'] = df.loc[:, 'artist'].str.replace(char, '', regex=True)

    df.loc[:, 'year_of_song'] = pd.to_numeric(df.loc[:, 'year_of_song'], errors='coerce')
    df.loc[:, 'year_of_song'] = df.loc[:, 'year_of_song'].fillna(int(df.year_of_song.mean()))
    df.loc[:, 'country'] = df.loc[:, 'country'].fillna('undefined')
    df.loc[:, 'key'] = df.loc[:, 'key'].fillna('undefined')
    df.loc[:, 'genre'] = df.loc[:, 'genre'].fillna('undefined')
    df.loc[:, 'artist'] = df.loc[:, 'artist'].fillna('undefined')

    df.loc[:, 'beats_per_minute'] = df.loc[:, 'beats_per_minute'].str.replace(' ', '', regex=True)
    df.loc[:, 'beats_per_minute'] = df.loc[:, 'beats_per_minute'].str.replace(',', '.', regex=True)
    df.loc[:, 'beats_per_minute'] = pd.to_numeric(df.loc[:, 'beats_per_minute'], downcast="float", errors='coerce')
    df.loc[:, 'beats_per_minute'] = df.loc[:, 'beats_per_minute'].fillna(df.beats_per_minute.mean())

    # preprocessing attributes
    attribute_cols = [col for col in df.columns if 'attribute' in col]
    attributes = pd.unique(df.loc[:, attribute_cols].values.ravel())

    cols_to_lower = ['genre', 'artist', 'key', 'title'] + attribute_cols

    for col in cols_to_lower:
        df.loc[:, col] = df.loc[:, col].str.lower()
        df.loc[:, col] = df.loc[:, col].str.strip()

    for col in attribute_cols:
        df.loc[:, col] = df.loc[:, col].fillna('')

    df = df.assign(attributes='')
    df.loc[:, list(attributes)] = False

    for i in range(len(attribute_cols)):
        df.loc[:, 'attributes'] = df.loc[:, 'attributes'].str.cat(df.loc[:, 'attribute_' + str(i)], sep=',')

    for attribute in attributes:
        df.loc[:, attribute] = df.loc[:, 'attributes'].str.contains(str(attribute), case=False)
        df.loc[:, attribute] = df.loc[:, attribute].astype(int)

    # one-hot encoding key column
    one_hot = pd.get_dummies(df['key'])
    # Drop column B as it is now encoded
    df.drop(columns='key', inplace=True)
    # Join the encoded df
    df = df.join(one_hot)

    cols_to_drop = ['attributes', 'undefined'] + attribute_cols
    df.drop(columns=cols_to_drop, inplace=True)

    print(f'Ended cleaning raw data')

    return df
