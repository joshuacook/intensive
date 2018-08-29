import pandas as pd
import numpy as np
import scipy.stats as st
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display
from sklearn.preprocessing import StandardScaler
from collections import Counter
from sklearn.decomposition import PCA

def feature_outliers(dataframe, col, param=1.5):
    Q1 = np.percentile(dataframe[col], 25)
    Q3 = np.percentile(dataframe[col], 75)
    tukey_window = param*(Q3-Q1)
    less_than_Q1 = (dataframe[col] < Q1 - tukey_window)
    greater_than_Q3 = (dataframe[col] > Q3 + tukey_window)
    tukey_mask = (less_than_Q1 | greater_than_Q3)
    return dataframe.loc[tukey_mask]

def multiple_outliers(dataframe, count=2):
    raw_outliers = []
    for col in dataframe:
        outlier_df = feature_outliers(dataframe, col)
        raw_outliers += list(outlier_df.index)

    outlier_count = Counter(raw_outliers)
    outliers = [k for k,v in outlier_count.items() if v >= count]
    return outliers

X = pd.read_csv('Wholesale_customers_data.csv')
X.drop(['Channel', 'Region'], axis=1, inplace=True)

scaler = StandardScaler()
scaler.fit(X)
Z = scaler.transform(X)
Z = pd.DataFrame(Z, columns=X.columns)

scaler = StandardScaler()
log_X = np.log(X + 1)
scaler.fit(log_X)
Z_log = scaler.transform(log_X)
Z_log = pd.DataFrame(Z_log, columns=X.columns)

boxcox_X = pd.DataFrame()
for col in X.columns:
    transformed_data, optimal_lambda = st.boxcox(X[col])
    box_cox_trans = transformed_data
    boxcox_X[col] = pd.Series(box_cox_trans)

scaler = StandardScaler()
scaler.fit(boxcox_X)
Z_bc = scaler.transform(boxcox_X)
Z_bc = pd.DataFrame(Z_bc, columns=X.columns)

z_log_outlier_indices = multiple_outliers(Z_log)
z_bc_outlier_indices = multiple_outliers(Z_bc)
Z_log_rmo = Z_log.drop(z_log_outlier_indices)
Z_bc_rmo = Z_bc.drop(z_bc_outlier_indices)