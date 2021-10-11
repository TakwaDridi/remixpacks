from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

import dataloaders.partition_handler as ph


def incode_labels(target):
    le = LabelEncoder()
    le.fit(target)
    encoded_target = le.transform(target)
    return encoded_target


def standardize(features, standardizer):
    features_scaled = standardizer.fit_transform(features)
    return features_scaled


def split_data(features, target):
    X_train, X_test, y_train, y_test = train_test_split(features,
                                                        target,
                                                        test_size=0.33,
                                                        random_state=42)
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    df = ph.load_object_partition(state_name='clean',
                                  object_name='songs')

    features = df.loc[:, ~df.columns.isin(['genre', 'title', 'artist', 'country'])]
    scaled_features = standardize(features, StandardScaler())

    target = df.genre
    enc_target = incode_labels(target)

    x_train, x_test, y_train, y_test = split_data(features, enc_target)
