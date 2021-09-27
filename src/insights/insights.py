import matplotlib.pyplot as plt

from dataloaders import partition_handler as ph


def get_insight_on(genre, df):
    df_genres = df.groupby(['genre'])[keys].sum().reset_index()
    all_keys = [df_genres[col].mean() > 10 for col in keys]
    all_keys.insert(0, True)  # added a true element at the head of the list

    df_genre = df_genres.loc[df_genres.genre == genre, all_keys]
    return df_genre




if __name__ == '__main__':
    df = ph.load_object_partition(state_name='clean',
                                  object_name='songs')
    df.drop(['page'], axis=1, inplace=True)
    keys = df.columns[145:]

    '''genre = 'pop'
        df_genre = get_insight_on('pop', df)
        df_genre.plot(kind='bar', xticks=[])
        plt.title(f{genre} songs' most used keys')
        plt.xlabel('keys')
        plt.ylabel('number of songs')
        plt.show()'''


    df['title'] = df['title'].str.replace('(remix stems)', '', regex=True)
    df['title'] = df['title'].str.replace('(rbn)', '', regex=True)
    df['title'] = df['title'].str.replace('(rb2)', '', regex=True)
    df['title'] = df['title'].str.replace('–', '', regex=True)
    df['title'] = df['title'].str.replace('(', '', regex=True)
    df['title'] = df['title'].str.replace(')', '', regex=True)
    df['title'] = df['title'].str.replace(df['artist'], '', regex=True)
    print(df['title'])