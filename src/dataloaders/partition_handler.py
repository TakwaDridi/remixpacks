import os
import shutil

import pandas as pd

data_path = os.environ['DATAPATH']


def make_dir(dir_name):
    path = os.path.join(data_path, dir_name)
    os.makedirs(path, exist_ok=True)
    return path


def get_object_partition_dir(state_name,
                             object_name):
    path = make_dir(dir_name=state_name)
    path = os.path.join(path, object_name)
    return path


def get_object_partition_path(state_name,
                              object_name,
                              **kwargs):
    path = get_object_partition_dir(state_name, object_name)
    for p_name, p_value in kwargs.items():
        if p_value is not None:
            path = os.path.join(path, f'{p_name}={p_value}')

    return path


def delete_object_partition(state_name,
                            object_name,
                            **kwargs):
    path = get_object_partition_path(state_name, object_name, **kwargs)
    shutil.rmtree(path, ignore_errors=True)


def load_object_partition(state_name,
                          object_name,
                          columns=None,
                          **kwargs):

    print(f'Loading dataframe from {state_name}, object : {object_name},'
          f' partition : {kwargs}')
    
    path = get_object_partition_path(state_name, object_name, **kwargs)
    try:
        df = pd.read_parquet(path, columns=columns)
    except FileNotFoundError:
        df = pd.DataFrame(columns=columns)

    return df


if __name__ == '__main__':
    df = load_object_partition('raw', 'songs', page=1)
    print(df)
