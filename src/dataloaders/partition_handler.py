import os
import shutil

import pandas as pd

data_path = os.environ['DATAPATH']


def make_dir(dir_name):
    '''
    this function creates a directory in the data_path location.

    :param dir_name: name of the directory to be created
    :return:
    '''
    path = os.path.join(data_path, dir_name)
    os.makedirs(path, exist_ok=True)
    return path


def get_object_partition_dir(state_name,
                             object_name):
    '''
    this function creates a directory state_name in the path
    data_path, returns a path to the object_name located under state_name.

    :param state_name: name of the parent directory to be created
    :param object_name: name of the subdirectory/file
    :return: absolute path to object_name
    '''
    path = make_dir(dir_name=state_name)
    path = os.path.join(path, object_name)
    return path


def get_object_partition_path(state_name,
                              object_name,
                              **kwargs):
    '''
    This function returns the path to the object partition.
    Partitions are used to store parquet files
    :param state_name:
    :param object_name:
    :param kwargs:
    :return: path to partition
    '''
    path = get_object_partition_dir(state_name, object_name)
    for p_name, p_value in kwargs.items():
        if p_value is not None:
            path = os.path.join(path, f'{p_name}={p_value}')

    return path


def delete_object_partition(state_name,
                            object_name,
                            **kwargs):
    '''
    this function generates the path to a partition then deletes it.

    :param state_name: parent directory
    :param object_name: subdirectory
    :param kwargs: partition name
    :return:
    '''
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


