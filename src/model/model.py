import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import dataloaders.partition_handler as ph


def encode_labels(target):
    enc_target = pd.get_dummies(target, columns=['genre'])
    return enc_target, enc_target.columns


def standardize(features, standardizer):
    features_scaled = standardizer.fit_transform(features)
    return features_scaled


def split_data(features, target):
    X_train, X_test, y_train, y_test = train_test_split(features,
                                                        target,
                                                        test_size=0.33,
                                                        random_state=42)
    return X_train, X_test, y_train, y_test


def create_model(input_size, categories, X_train, y_train):
    model = Sequential()
    model.add(Dense(units=64,
                    activation='relu',
                    input_dim=input_size))
    model.add(Dense(units=100,
                    activation='relu'))
    model.add(Dense(units=categories,
                    activation='softmax'))
    # compile the model
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    # build the model
    model.fit(X_train, y_train, epochs=150)

    return model


def evaluate_model(final_model, x_train, y_train, x_test, y_test):
    pred_train = final_model.predict(x_train)
    scores = final_model.evaluate(x_train, y_train, verbose=0)
    print('Accuracy on training data: {}% \n Error on training data: {}'.format(scores[1], 1 - scores[1]))

    pred_test = final_model.predict(x_test)
    scores2 = final_model.evaluate(x_test, y_test, verbose=0)
    print('Accuracy on test data: {}% \n Error on test data: {}'.format(scores2[1], 1 - scores2[1]))


if __name__ == "__main__":
    df = ph.load_object_partition(state_name='clean',
                                  object_name='songs')

    features = df.loc[:, ~df.columns.isin(['genre', 'title', 'artist', 'country'])]
    scaled_features = standardize(features, StandardScaler())

    target = df.genre

    enc_target, classes = encode_labels(target)

    classes_size = len(classes)
    features_size = scaled_features.shape[1]

    x_train, x_test, y_train, y_test = split_data(features, enc_target)

    trained_model = create_model(features_size, classes_size, x_train, y_train)
    evaluate_model(trained_model, x_train, y_train, x_test, y_test)
