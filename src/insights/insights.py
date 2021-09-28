import string

import matplotlib.pyplot as plt
import plotly.express as px
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from dataloaders import partition_handler as ph


# nltk.download('stopwords')
# nltk.download('wordnet')

def get_insight_on(genre, df):
    df_genres = df.groupby(['genre'])[keys].sum().reset_index()
    all_keys = [df_genres[col].mean() > 0 for col in keys]
    all_keys.insert(0, True)  # added a true element at the head of the list

    df_genre = df_genres.loc[df_genres.genre == genre, all_keys]
    return df_genre


def plot_genre_insight(genre, df):
    df_genre = get_insight_on(genre, df)
    df_genre.plot(kind='bar', xticks=[])
    plt.title(f'''{genre} songs' most used keys''')
    plt.xlabel('keys')
    plt.ylabel('number of songs')
    plt.show()


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


def get_bpm_distribution_figure(df):

    fig = px.box(df, x="genre", y="beats_per_minute")
    fig.update_xaxes(title='Genre', tickangle=45)
    fig.update_yaxes(title='Beats per minute', type='linear', tickangle=0)

    return fig


def get_release_year_distribution_figure(df):

    fig = px.box(df, x="genre", y="year_of_song")
    fig.update_xaxes(title='Genre', tickangle=45)
    fig.update_yaxes(title='Release Year', type='linear', tickangle=0)

    return fig


def get_keys_figure(df):

    keys = df.columns[145:]
    df = df.assign(number_of_songs=1)
    agg_dict = dict.fromkeys(keys, 'mean')
    agg_dict.update(dict(number_of_songs='sum'))

    stats = df.groupby('genre').agg(agg_dict)
    stats.reset_index(inplace=True)
    stats.sort_values(by='number_of_songs', ascending=False, inplace=True)

    return stats


if __name__ == '__main__':
    df = ph.load_object_partition(state_name='clean',
                                  object_name='songs')

    df.drop(['page'], axis=1, inplace=True)
    keys = df.columns[145:]
    print(df.shape)
    # fig = get_bpm_distribution_figure(df)
    # fig.show(renderer='browser')
    # fig = get_release_year_distribution_figure(df)
    # fig.show(renderer='browser')
    stats = get_keys_figure(df)
    print(stats)


