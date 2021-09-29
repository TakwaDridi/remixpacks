import multiprocessing as mp

import pandas as pd
import parsel
import requests

from dataloaders import partition_handler as ph


def get_element(text,
                object_name,
                class_name):
    selector = parsel.Selector(text=text)
    elements = selector.xpath(f"""//{object_name}[@class="{class_name}"]""").get()
    return elements


def get_elements(text,
                 object_name,
                 class_name):
    selector = parsel.Selector(text=text)
    elements = selector.xpath(f"""//{object_name}[@class="{class_name}"]""").getall()
    return elements


def extract_song_containers(page):
    url = 'https://remixpacks.ru/'
    url = url + 'page/' + str(page) + '/'
    text = requests.get(url).text

    songs_containers = get_elements(text=text,
                                    object_name="div",
                                    class_name="idstems marginbottom20")
    return songs_containers


def extract_song_title(song_container):
    title = get_element(text=song_container,
                        object_name="div",
                        class_name="titlestems")

    selector = parsel.Selector(text=title)
    title = selector.xpath('//div[@class="titlestems"]/a/text()').get()
    return title


def extract_genre_information(song_container):
    genre_info = get_element(text=song_container,
                             object_name="div",
                             class_name="genres1 genrescomp")

    selector = parsel.Selector(text=genre_info)
    genres = selector.xpath('//div[@class="genres1 genrescomp"]/a/text()').get()
    return genres


def extract_song_tags(song_container):
    selector = parsel.Selector(text=song_container)
    song_info = selector.xpath("""//div[@class="row"]""").get()

    selector = parsel.Selector(text=song_info)
    song_info = selector.xpath("""//div[@class="col-md-12"]""").get()

    selector = parsel.Selector(text=song_info)
    song_info = selector.xpath('//div/div').get()

    selector = parsel.Selector(text=song_info)
    song_info = selector.xpath('//a/@href').getall()

    named_tag_pattern = '/search/#search/wpcf-'
    unnamed_tag_pattern = 'https://remixpacks.ru/load/tag/'

    named_tags = []
    unnamed_tags = []

    for info in song_info:
        if named_tag_pattern in info:
            info = info.replace(named_tag_pattern, '')
            named_tags.append(info)

        if unnamed_tag_pattern in info:
            info = info.replace(unnamed_tag_pattern, '')
            unnamed_tags.append(info)

    return named_tags, unnamed_tags


def remove_special_chars(string):
    special_chars = ['%20', '-', '/']
    for char in special_chars:
        string = string.replace(char, ' ')

    string = string.strip()

    return string


def process_named_tags(tags):
    info_dict = dict()
    for tag in tags:
        tag_name, tag_value = tag.split('=')
        tag_name = remove_special_chars(tag_name)
        tag_value = remove_special_chars(tag_value)
        info_dict[tag_name] = tag_value
    return info_dict


def process_unnamed_tags(tags):
    info_dict = dict()
    for i, tag in enumerate(tags):
        key = '_'.join(['attribute', str(i)])
        info_dict[key] = remove_special_chars(tag)
    return info_dict


def process_tags(named_tags, unnamed_tags):
    named_dict = process_named_tags(named_tags)
    unnamed_dict = process_unnamed_tags(unnamed_tags)
    named_dict.update(unnamed_dict)
    return named_dict


def extract_song_information(song_container):
    genre = extract_genre_information(song_container)
    title = extract_song_title(song_container)

    info_dict = dict()
    info_dict['title'] = title
    info_dict['genre'] = genre

    named_tags, unnamed_tags = extract_song_tags(song_container)
    tags_dict = process_tags(named_tags, unnamed_tags)
    info_dict.update(tags_dict)

    return info_dict


def extract_page(page_number):
    songs = []
    song_containers = extract_song_containers(page=page_number)
    print(f'Started extracting {len(song_containers)} songs from page {page_number}')

    for song_container in song_containers:
        song_info = extract_song_information(song_container)
        songs.append(song_info)

    df = pd.DataFrame.from_dict(data=songs, orient='columns')
    df = df.assign(page=page_number)

    for col in df.columns:
        df.loc[:, col] = df.loc[:, col].astype('string')

    path = ph.get_object_partition_dir(state_name='raw', object_name='songs')

    df.to_parquet(path=path, partition_cols=['page'])

    print(f'Ended extracting {len(song_containers)} songs from page {page_number}')


if __name__ == '__main__':
    ph.delete_object_partition(state_name='raw', object_name='songs')

    total_pages = 1347
    pages = [(page_number,) for page_number in range(1, total_pages + 1)]

    pool = mp.Pool(24)
    pool.starmap(extract_page, pages)
    pool.close()
    pool.join()
