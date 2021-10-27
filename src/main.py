import multiprocessing as mp

from dataloaders import partition_handler as ph
from preprocess.clean import clean as cl
from preprocess.extract import extract as ex

if __name__ == '__main__':
    # ================= crawling and extracting data =================
    ph.delete_object_partition(state_name='raw', object_name='songs')
    print('Started crawling website')
    total_pages = 1347
    pages = [(page_number,) for page_number in range(1, total_pages + 1)]

    pool = mp.Pool(24)
    pool.starmap(ex.extract_page, pages)
    pool.close()
    pool.join()

    # ======================= cleaning data ==========================
    ph.delete_object_partition(state_name='clean',
                               object_name='songs')

    df = ph.load_object_partition(state_name='raw',
                                  object_name='songs')

    df = cl.clean_data(df)

    path = ph.get_object_partition_dir(state_name='clean',
                                       object_name='songs')

    df.to_parquet(path=path, partition_cols=['page'])

    # ======================= loading data ==========================
    print('Loading clean data')
    df = ph.load_object_partition(state_name='clean',
                                  object_name='songs')

    print(df.sample(10))

    # to get the insight figure, run the main in file insights/insights.py
