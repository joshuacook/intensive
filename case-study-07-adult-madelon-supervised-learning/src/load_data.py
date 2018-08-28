import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.pipeline import make_pipeline

adult_train_data = pd.read_pickle('data/adult_train_data.p')
adult_train_labels = pd.read_pickle('data/adult_train_labels.p')
madelon_train_data = pd.read_pickle('data/madelon_train_data.p')
madelon_train_labels = pd.read_pickle('data/madelon_train_labels.p')

adult_test_data = pd.read_pickle('data/adult_test_data.p')
adult_test_labels = pd.read_pickle('data/adult_test_labels.p')
madelon_test_data = pd.read_pickle('data/madelon_test_data.p')
madelon_test_labels = pd.read_pickle('data/madelon_test_labels.p')

import sys

data = {
    'adult' : {
        'train' : {
            'raw_data' : adult_train_data,
            'labels' : adult_train_labels
        },
        'test' : {
            'raw_data' : adult_test_data,
            'labels' : adult_test_labels
        }
    },

    'madelon' : {
        'train' : {
            'raw_data' : madelon_train_data,
            'labels' : madelon_train_labels
        },
        'test' : {
            'raw_data' : madelon_test_data,
            'labels' : madelon_test_labels
        }
    }
}

def adult_feature_engineering(train_data, test_data):

    train_data = train_data.drop('education-num', axis=1)
    test_data = test_data.drop('education-num', axis=1)

    train_data = train_data.drop('fnlwgt', axis=1)
    test_data = test_data.drop('fnlwgt', axis=1)

    train_data = pd.get_dummies(train_data)
    test_data = pd.get_dummies(test_data)

    test_data['native-country_ Holand-Netherlands'] = np.zeros_like(test_data.age)

    # ensure column order of test is exactly the same as train
    test_data = test_data.reindex(columns = train_data.columns)

    return train_data, test_data

# def standard_scale(train_data, test_data, numeric_only=True):
#     scaler = StandardScaler()

#     numerical_features = train_data.select_dtypes([int, float]).columns

#     if numeric_only:
#         train_num = pd.DataFrame(scaler.fit_transform(train_data[numerical_features]),
#                                  columns=numerical_features,
#                                  index=train_data.index)
#         test_num = pd.DataFrame(scaler.transform(test_data[numerical_features]),
#                                 columns=numerical_features,
#                                 index=test_data.index)
#         train_data[numerical_features] = train_num
#         test_data[numerical_features] = test_num
#     else:
#         train_data = pd.DataFrame(scaler.fit_transform(train_data),
#                                   columns=train_data.columns,
#                                   index=train_data.index)
#         test_data = pd.DataFrame(scaler.transform(test_data),
#                                  columns=test_data.columns,
#                                  index=test_data.index)

#     return train_data, test_data

# def skew_normalize(train_data, test_data, numeric_only=True):
#     numerical_features = train_data.select_dtypes([int, float]).columns

#     mmscaler = MinMaxScaler((1,2))
#     boxcox_transformer = BoxCoxTransformer()
#     sscaler = StandardScaler()

#     pipeline = make_pipeline(
#       MinMaxScaler((1,2)),
#       BoxCoxTransformer(),
#       StandardScaler()
#     )

#     if numeric_only:
#         train_num = pd.DataFrame(pipeline.fit_transform(train_data[numerical_features]),
#                                  columns=numerical_features,
#                                  index=train_data.index)
#         test_num = pd.DataFrame(pipeline.transform(test_data[numerical_features]),
#                                 columns=numerical_features,
#                                 index=test_data.index)
#         train_data[numerical_features] = train_num
#         test_data[numerical_features] = test_num
#     else:
#         train_data = pd.DataFrame(pipeline.fit_transform(train_data),
#                                   columns=train_data.columns,
#                                   index=train_data.index)
#         test_data = pd.DataFrame(pipeline.transform(test_data),
#                                  columns=train_data.columns,
#                                  index=test_data.index)

#     return train_data, test_data

data['adult']['train']['engineered'], \
    data['adult']['test']['engineered'] = adult_feature_engineering(data['adult']['train']['raw_data'].copy(),
                                                                    data['adult']['test']['raw_data'].copy())

# data['adult']['train']['scaled_numeric'], \
#     data['adult']['test']['scaled_numeric'] = standard_scale(data['adult']['train']['basic'].copy(),
#                                                      data['adult']['test']['basic'].copy())

# data['adult']['train']['skew_normalized_numeric'], \
#     data['adult']['test']['skew_normalized_numeric'] = skew_normalize(data['adult']['train']['basic'].copy(),
#                                                                       data['adult']['test']['basic'].copy())

# data['adult']['train']['scaled_all'], \
#     data['adult']['test']['scaled_all'] = standard_scale(data['adult']['train']['basic'].copy(),
#                                                          data['adult']['test']['basic'].copy(),
#                                                          numeric_only=False)

# data['adult']['train']['skew_normalized_all'], \
#     data['adult']['test']['skew_normalized_all'] = skew_normalize(data['adult']['train']['basic'].copy(),
#                                                               data['adult']['test']['basic'].copy(),
#                                                               numeric_only=False)
# data['madelon']['train']['scaled'], \
#     data['madelon']['test']['scaled'] = standard_scale(data['madelon']['train']['raw_data'].copy(),
#                                                        data['madelon']['test']['raw_data'].copy())

# data['madelon']['train']['skew_normalized'], \
#     data['madelon']['test']['skew_normalized'] = skew_normalize(data['madelon']['train']['raw_data'].copy(),
#                                                                 data['madelon']['test']['raw_data'].copy())
