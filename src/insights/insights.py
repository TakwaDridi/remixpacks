import string

import matplotlib.pyplot as plt
import plotly.express as px
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from dataloaders import partition_handler as ph


# nltk.download('stopwords')
# nltk.download('wordnet')

def get_song_distribution_figure(df):
    keys = df.columns[145:]
    df = df.assign(number_of_songs=1)
    agg_dict = dict.fromkeys(keys, 'mean')
    agg_dict.update(dict(number_of_songs='sum'))

    stats = df.groupby('genre').agg(agg_dict)
    stats.reset_index(inplace=True)
    stats.sort_values(by='number_of_songs', ascending=False, inplace=True)

    fig = px.histogram(stats, x='genre', y='number_of_songs', histnorm='percent', title='songs distribution per genre')
    fig.update_xaxes(title='Genre', tickangle=45)
    fig.update_yaxes(title='% Number of songs', type='linear', tickangle=0)
    fig.show()

def get_keys_figure(df, genre):
    keys = df.columns[145:]
    df = df.assign(number_of_songs=1)
    agg_dict = dict.fromkeys(keys, 'mean')
    agg_dict.update(dict(number_of_songs='sum'))

    stats = df.groupby('genre').agg(agg_dict)
    stats.reset_index(inplace=True)
    stats.sort_values(by='number_of_songs', ascending=False, inplace=True)
    genre_stats = stats.loc[stats['genre'] == genre, :]

    genre_stats = genre_stats.iloc[0].to_frame()
    genre_stats = genre_stats.iloc[1:-1, :]
    genre_stats.reset_index(level=0, inplace=True)
    genre_stats = genre_stats.rename(columns={genre_stats.columns[0]: 'key', genre_stats.columns[1]: 'percentage'})
    fig = px.histogram(genre_stats, x='key', y='percentage', title=f'{genre} songs most used keys')
    fig.update_xaxes(title='keys', tickangle=45)
    fig.update_yaxes(title='%', type='linear', tickangle=0)
    fig.show()


def get_bpm_distribution_figure(df):
    fig = px.box(df, x="genre", y="beats_per_minute", title='beats per minute per genre')
    fig.update_xaxes(title='Genre', tickangle=45)
    fig.update_yaxes(title='Beats per minute', type='linear', tickangle=0)
    fig.show()


def get_release_year_distribution_figure(df):
    fig = px.box(df, x="genre", y="year_of_song", title='year of song per genre')
    fig.update_xaxes(title='Genre', tickangle=45)
    fig.update_yaxes(title='Release Year', type='linear', tickangle=0)
    fig.show()


def clean_title(df):
    df['title'] = df['title'].str.replace('(remix stems)', '', regex=True)
    df['title'] = df['title'].str.replace('(rbn)', '', regex=True)
    df['title'] = df['title'].str.replace('(rb2)', '', regex=True)
    df['title'] = df['title'].str.replace('–', '', regex=True)
    df['title'] = df.apply(lambda x: x['title'].replace(x['artist'], ''), axis=1)

    return df


def titles_to_words(document):
    stop_words = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    stopwords_removed = " ".join([i for i in document.lower().split() if i not in stop_words])
    punct_removed = ''.join(ch for ch in stopwords_removed if ch not in exclude)
    normalized = ' '.join(lemma.lemmatize(word, 'v') for word in punct_removed.split())
    return normalized


def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def title_unique_words(df):
    words = []
    for word in df['title'].tolist():
        words.append(unique(titles_to_words(word).split()))

    df['title_words'] = words
    return df


if __name__ == '__main__':
    df = ph.load_object_partition(state_name='clean',
                                  object_name='songs')

    df.drop(['page'], axis=1, inplace=True)
    keys = df.columns[145:]

    get_song_distribution_figure(df)
    get_keys_figure(df, 'pop')
    get_keys_figure(df, 'rock')
    get_release_year_distribution_figure(df)
    get_bpm_distribution_figure(df)
