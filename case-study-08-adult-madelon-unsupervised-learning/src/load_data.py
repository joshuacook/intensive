import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.pipeline import make_pipeline

adult_train_data = pd.read_pickle('data/adult_train_data-joshua.p')
adult_train_labels = pd.read_pickle('data/adult_train_labels-joshua.p')
madelon_train_data = pd.read_pickle('data/madelon_train_data-joshua.p')
madelon_train_labels = pd.read_pickle('data/madelon_train_labels-joshua.p')

adult_test_data = pd.read_pickle('data/adult_test_data-joshua.p')
adult_test_labels = pd.read_pickle('data/adult_test_labels-joshua.p')
madelon_test_data = pd.read_pickle('data/madelon_test_data-joshua.p')
madelon_test_labels = pd.read_pickle('data/madelon_test_labels-joshua.p')

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

def scale(train_data, test_data):

    train_data_num = train_data[['age', 'capital-gain','capital-loss','hours-per-week']]
    test_data_num = test_data[['age', 'capital-gain','capital-loss','hours-per-week']]
    means = train_data_num.mean()
    stds = train_data_num.std()

    train_data_scaled_num = (train_data_num - means)/stds
    test_data_scaled_num = (test_data_num - means)/stds

    train_data_gelman_scaled_num = (train_data_num - means)/(2*stds)
    test_data_gelman_scaled_num = (test_data_num - means)/(2*stds)

    train_data[['age', 'capital-gain','capital-loss','hours-per-week']] = train_data_scaled_num
    test_data[['age', 'capital-gain','capital-loss','hours-per-week']] = test_data_scaled_num

    train_data_scaled = train_data.copy()
    test_data_scaled = test_data.copy()

    train_data[['age', 'capital-gain','capital-loss','hours-per-week']] = train_data_gelman_scaled_num
    test_data[['age', 'capital-gain','capital-loss','hours-per-week']] = test_data_gelman_scaled_num

    train_data_gelman_scaled = train_data.copy()
    test_data_gelman_scaled = test_data.copy()

    return train_data_scaled, train_data_gelman_scaled, test_data_scaled, test_data_gelman_scaled

data['adult']['train']['engineered'], \
    data['adult']['test']['engineered'] = adult_feature_engineering(data['adult']['train']['raw_data'].copy(),
                                                                    data['adult']['test']['raw_data'].copy())

data['adult']['train']['scaled'], \
    data['adult']['train']['gelman_scaled'], \
    data['adult']['test']['scaled'], \
    data['adult']['test']['gelman_scaled'] = scale(data['adult']['train']['engineered'].copy(),
                                                   data['adult']['test']['engineered'].copy())

scaler = StandardScaler()
data['madelon']['train']['scaled'] = pd.DataFrame(scaler.fit_transform(data['madelon']['train']['raw_data']))
data['madelon']['test']['scaled'] = pd.DataFrame(scaler.transform(data['madelon']['test']['raw_data']))


adult_final_ic = pd.read_pickle('data/adult-final-ic.pkl')
adult_final_pca = pd.read_pickle('data/adult_train_gelman_scaled_pca_df.p')
adult_final_rp = pd.read_pickle('data/adult_gelman_rp_df.p')
adult_final_sfm = pd.read_pickle('data/adult-sfm.p')
madelon_final_ic = pd.read_pickle('data/madelon-final-ic.pkl')
madelon_final_pca = pd.read_pickle('data/madelon_train_scaled_pca_df.p')
madelon_final_rp = pd.read_pickle('data/madelon_scaled_rd_df.p')
madelon_final_sfm = pd.read_pickle('data/madelon-sfm.p')
