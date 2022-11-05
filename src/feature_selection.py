import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import VarianceThreshold, SelectKBest, SelectPercentile, RFECV, SequentialFeatureSelector
import dvc.api


base_estimator = SVC(kernel="linear")
selectors = {
    'variance': VarianceThreshold(),
    'kbest': SelectKBest(),
    'percentile': SelectPercentile(),
    'rfecv': RFECV(
            estimator=base_estimator,
            step=1,
            cv=StratifiedKFold(2),
            scoring="accuracy",
            min_features_to_select=1,
        ),
    'forward': SequentialFeatureSelector(
            estimator=base_estimator,
            n_features_to_select=10,
            direction='forward'
    ),
    'backward': SequentialFeatureSelector(
            estimator=base_estimator,
            n_features_to_select=10,
            direction='backward'
    )
}



def select(X_train, y_train, X_test, selector):
    selector.fit(X_train, np.ravel(y_train))
    print(X_train.columns[[x for x in selector.get_support()]])
    X_train = pd.DataFrame(selector.transform(X_train), columns=X_train.columns[selector.get_support()])
    X_test = pd.DataFrame(selector.transform(X_test), columns=X_test.columns[selector.get_support()])
    return X_train, X_test

def main():
    X_test = pd.read_csv('data/X_test_all_features.csv')
    X_train = pd.read_csv('data/X_train_all_features.csv')
    y_train = pd.read_csv('data/y_train.csv')

    params = dvc.api.params_show()['feature_selection']
    
    for method in params['methods']:
        if method in selectors:
            print("Applying method" + method)
            X_train, X_test = select(X_train, y_train, X_test, selectors[method])

    X_train.to_csv('data/X_train.csv', index=False)
    X_test.to_csv('data/X_test.csv', index=False)

if __name__ == '__main__':
    main()