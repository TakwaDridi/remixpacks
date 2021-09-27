from dataloaders import partition_handler as ph

if __name__ == '__main__':
    df = ph.load_object_partition(state_name='clean',
                                  object_name='songs')
    #print(df.columns)
    df.drop(['page'], axis=1, inplace=True)

    df_deep_house = df.loc[df.genre =='deep house']
    print(df.groupby(['genre'])['a major'].count())