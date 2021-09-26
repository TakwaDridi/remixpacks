from dataloaders import partition_handler as ph

if __name__ == '__main__':
    df = ph.load_object_partition(state_name='clean',
                                  object_name='songs')
    print(df.sample(10))
