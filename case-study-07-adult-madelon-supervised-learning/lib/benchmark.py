import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from time import time

#from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from tqdm import tqdm


from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer

def run_model(model, model_name, n_pcnt, data, labels):
    X_train, X_test, y_train, y_test = train_test_split(data, labels, random_state=42, stratify=labels)
    n = X_train.shape[0]*n_pcnt//100
    X_samp, y_samp = X_train[:n], y_train[:n]
    start = time()
    model.fit(X_samp, y_samp)
    fit_time = time() - start

    start = time()
    train_pred = model.predict(X_samp)
    train_pred_time = time() - start

    start = time()
    test_pred = model.predict(X_test)
    test_pred_time = time() - start
    return {
            'model_name' : model_name,
            'n_pcnt' : n_pcnt,
            'n' : n,
            'f1_train_score' : f1_score(y_samp, train_pred),
            'f1_test_score' : f1_score(y_test, test_pred),
            'accuracy_train_score' : model.score(X_samp, y_samp),
            'accuracy_test_score' : model.score(X_test, y_test),
            'fit_time' : fit_time,
            'train_pred_time' : train_pred_time,
            'test_pred_time' : test_pred_time}

def run_experiment(data, dataset='adult', tests=None):
    result_dict = {}

    if dataset == 'madelon':
        data, labels = data['madelon']['train']['raw_data'],\
                       data['madelon']['train']['labels']
    else:
        data, labels = data['adult']['train']['engineered'], \
                       data['adult']['train']['labels']

    percentages = [1, 2, 3, 4, 5, 7, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100]

    if tests is None:
        tests = [('svm', 'basic', pipeline_basic(SVC)),
                 ('svm', 'scaled', pipeline_scale(SVC)),
                 ('svm', 'deskewed', pipeline_deskew(SVC)),
                 ('knn', 'basic', pipeline_basic(KNeighborsClassifier)),
                 ('knn', 'scaled', pipeline_scale(KNeighborsClassifier)),
                 ('knn', 'deskewed', pipeline_deskew(KNeighborsClassifier)),
                 ('neural_net', 'basic', pipeline_basic(MLPClassifier)),
                 ('neural_net', 'scaled', pipeline_scale(MLPClassifier)),
                 ('neural_net', 'deskewed', pipeline_deskew(MLPClassifier)),
                 ('boosting', 'basic', pipeline_basic(AdaBoostClassifier)),
                 ('boosting', 'scaled', pipeline_scale(AdaBoostClassifier)),
                 ('boosting', 'deskewed', pipeline_deskew(AdaBoostClassifier)),
                 ('decision tree', 'basic', pipeline_basic(DecisionTreeClassifier)),
                 ('decision tree', 'scaled', pipeline_scale(DecisionTreeClassifier)),
                 ('decision tree', 'deskewed', pipeline_deskew(DecisionTreeClassifier)),
                ]

    for t in tests:
        for n in tqdm(percentages):
            test_name = "{} {} {}".format(t[0], t[1], n)
            model = t[2]
            result_dict[test_name] = run_model(model, test_name, n, data, labels)

    results = pd.DataFrame(result_dict).T.sort_values('n')

    # return the tests so we can plot with them
    return results, tests


def plot_results(test_results, tests, models, num_experiments = 5, ylim=(0.4,0.8), train=False):
    fig = plt.figure(figsize=(20, 8))

    for i, m in enumerate(models):
        fig.add_subplot(2, num_experiments, 1+i)

        for t in [(t[0]+' '+t[1]) for t in tests if m in t[0]]:

            test = test_results.loc[test_results.index.str.contains(t)]

            if train:
                label = t + "_test"
            else:
                label = t
            plt.plot(test.n_pcnt, test.f1_test_score, label=label)
            if train:
                label = t + "_train"
                plt.plot(test.n_pcnt, test.f1_train_score, label=label)

        plt.ylim(*ylim)
        plt.legend()
        plt.title(m)

        #### Time it here
        fig.add_subplot(2, num_experiments, num_experiments+1+i)

        for time in ['fit_time', 'test_pred_time', "train_pred_time"]:

            #test = test_results.loc[test_results.index.str.contains(t)]
            plt.plot(test.n_pcnt, test[time], label=time)
            plt.ylim(0, 50)
            plt.yscale('log')

        #plt.ylim(0.5,0.7)
        plt.legend()
        plt.title(m+" deskewed")


def pipeline_basic(model, args=None):
    if args is None:
        return model()
    return model(**args)

def pipeline_scale(model, args=None):
    if args is None:
        return make_pipeline(StandardScaler(), model())
    return make_pipeline(StandardScaler(), model(**args))


def pipeline_deskew(model, args=None):
    if args is None:
        return make_pipeline(MinMaxScaler((10, 11)), FunctionTransformer(np.log),
                             StandardScaler(), model())
    return make_pipeline(MinMaxScaler((10, 11)), FunctionTransformer(np.log),
                             StandardScaler(), model(**args))
