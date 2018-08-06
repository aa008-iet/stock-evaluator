from __future__ import print_function
# statistical libraries
import numpy
import pandas as pd
import wrangle as wr

# keras and tensorflow and scikit-learn
from keras.models import Sequential
from keras.layers import Dropout, Dense, Activation
# from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
# from sklearn.preprocessing import StandardScaler
# from sklearn.pipeline import Pipeline

# tuning hyperparameters
from hyperopt import Trials, STATUS_OK, tpe
from hyperas import optim
from hyperas.distributions import choice, uniform

# "set seed for reproducibility"
seed = 7
numpy.random.seed(seed)


def data():
    csv = pd.read_csv("test.csv", index_col="Unnamed: 0", thousands=',')
    v = csv.values

    split_size = int(csv.shape[0]*0.8)
    x = v[:, 0:(len(csv.columns) - 1)].astype(float)
    x = wr.mean_zero(x)
    x_t, x_v = x[:split_size], x[split_size:]
    y = v[:, (len(csv.columns) - 1)]
    encoded_y = LabelEncoder().fit(y).transform(y)
    y_t, y_v = encoded_y[:split_size], encoded_y[split_size:]

    return x_t, y_t, x_v, y_v


# model with hyperparameters tuned and input in
def tuned_model(x_t, y_t, x_v, y_v):
    model = Sequential()
    model.add(Dense(72, input_dim=72, activation='relu'))
    model.add(Dropout({{uniform(0, 1)}}))
    model.add(Dense({{choice([18, 36, 54])}}))
    model.add(Activation({{choice(['relu'])}}))
    model.add(Dropout({{uniform(0, 1)}}))

    if {{choice(['three', 'four'])}} == 'four':
        model.add(Dense(18))
        model.add(Dropout(0.5))
        model.add(Activation('relu'))

    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', metrics=['accuracy'],
                  optimizer={{choice(['nadam', 'adam'])}})

    model.fit(x_t, y_t, batch_size={{choice([5, 10])}}, epochs=100, verbose=2)
    score, acc = model.evaluate(x_v, y_v, verbose=0)
    print("Test accuracy: ", acc)
    return {'loss': -acc, 'status': STATUS_OK, 'model': model}


# baseline model - evaluates w/ 49% accuracy
def based_model():
    m = Sequential()
    m.add(Dense(72, input_dim=72, kernel_initializer='normal', activation='relu'))
    m.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
    # Compile model
    m.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return m


def selected_model():
    m = Sequential()
    m.add(Dense(40, input_dim=72, kernel_initializer='normal', activation='relu'))
    m.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
    # Compile model
    m.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return m


def compile_model(l, i, o):
    # evaluate w/ standardized data set
    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
    results = cross_val_score(l, i, o, cv=kfold)
    print("Results: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))
    return results


numpy.random.seed(seed)
# estimators = [('standardize', StandardScaler()),
#               ('mlp', KerasClassifier(build_fn=selected_model, verbose=1))]
# pipeline = Pipeline(estimators)
#
# compile_model(pipeline, x, encoded_y)
# estimator = KerasClassifier(build_fn=based_model, epochs=100, batch_size=5, verbose=0)
if __name__ == '__main__':
    best_run, best_model = optim.minimize(model=tuned_model,
                                          data=data,
                                          algo=tpe.suggest,
                                          max_evals=5,
                                          trials=Trials())
    x_t, y_t, x_v, y_v = data()
    print("Evaluation of best performing model:")
    print(best_model.evaluate(x_v, y_v))
    print("Best performing model chosen hyper-parameters:")
    print(best_run)

