import string

import matplotlib.pyplot as plt

from dataloaders import partition_handler as ph
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('wordnet')

def get_insight_on(genre, df):
    df_genres = df.groupby(['genre'])[keys].sum().reset_index()
    all_keys = [df_genres[col].mean() > 10 for col in keys]
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
    df['title'] = df.apply(lambda x: x['title'].replace(x['artist'], ''), axis=1)

    return df

def titles_to_words(document):
    stop_words = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    stopwords_removed = " ".join([i for i in document.lower().split() if i not in stop_words])
    punct_removed = ''.join(ch for ch in stopwords_removed if ch not in exclude)
    normalized = [lemma.lemmatize(word,'v') for word in punct_removed.split()]
    return normalized

if __name__ == '__main__':
    df = ph.load_object_partition(state_name='clean',
                                  object_name='songs')
    df.drop(['page'], axis=1, inplace=True)
    keys = df.columns[145:]

    print(titles_to_words('i have love feeling loving what I am wanting'))