# import necessary classes and functions
import numpy
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# "set seed for reproducibility"
seed = 7
numpy.random.seed(seed)
# load test data set
csv = pd.read_csv("test.csv", index_col="Unnamed: 0", thousands=',')
set = csv.values
# define input and output variables
x = set[:, 0:(len(csv.columns) - 1)].astype(float)
y = set[:, (len(csv.columns) - 1)]
# encode if not set to 0s and 1s already (but they will be)
encoded_y = LabelEncoder().fit(y).transform(y)


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
estimators = [('standardize', StandardScaler()),
              ('mlp', KerasClassifier(build_fn=selected_model, verbose=1))]
pipeline = Pipeline(estimators)

compile_model(pipeline, x, encoded_y)
# estimator = KerasClassifier(build_fn=based_model, epochs=100, batch_size=5, verbose=0)
