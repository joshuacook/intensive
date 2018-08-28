import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt


from IPython.display import display

from sklearn.preprocessing import StandardScaler
import scipy.stats as st
from collections import Counter

from sklearn.decomposition import PCA

def feature_outliers(dataframe, col, param=1.5):
    Q1 = np.percentile(dataframe[col], 25)
    Q3 = np.percentile(dataframe[col], 75)
    tukey_window = param*(Q3-Q1)
    less_than_Q1 = dataframe[col] < Q1 - tukey_window
    greater_than_Q3 = dataframe[col] > Q3 + tukey_window
    tukey_mask = (less_than_Q1 | greater_than_Q3)
    return dataframe[tukey_mask]

def multiple_outliers(dataframe, count=2):
    raw_outliers = []
    for col in dataframe:
        outlier_df = feature_outliers(dataframe, col)
        raw_outliers += list(outlier_df.index)

    outlier_count = Counter(raw_outliers)
    outliers = [k for k,v in outlier_count.items() if v >= count]
    return outliers



customers = pd.read_csv('Wholesale_customers_data.csv')
customers.Region = customers.Region.astype('category')
customers.Channel = customers.Channel.astype('category')
customer_features = customers.select_dtypes(exclude=['category'])

scaler = StandardScaler()
customer_sc = scaler.fit_transform(customer_features)
customer_sc_df = pd.DataFrame(customer_sc, columns=customer_features.columns)

customer_log_df = np.log(1+customer_features)
scaler.fit(customer_log_df)
customer_log_sc = scaler.transform(customer_log_df)
customer_log_sc_df = pd.DataFrame(customer_log_sc, columns=customer_features.columns)

customer_box_cox_df = pd.DataFrame()
for col in customer_features.columns:
    box_cox_trans = st.boxcox(customer_features[col])[0]
    customer_box_cox_df[col] = pd.Series(box_cox_trans)

del box_cox_trans

scaler.fit(customer_box_cox_df)
customer_box_cox_sc = scaler.transform(customer_box_cox_df)
customer_box_cox_sc_df = pd.DataFrame(customer_box_cox_sc, columns=customer_features.columns)

customer_features_outliers_removed = customer_features.drop(multiple_outliers(customer_features))
customer_sc_df_outliers_removed = customer_sc_df.drop(multiple_outliers(customer_sc_df))
customer_log_sc_df_outliers_removed = customer_log_sc_df.drop(multiple_outliers(customer_log_sc_df))
customer_box_cox_sc_df_outliers_removed = customer_box_cox_sc_df.drop(multiple_outliers(customer_box_cox_sc_df))

channel_original_outliers_removed = np.array(customers.Channel.loc[customer_features_outliers_removed.index].values) - 1
channel_scaled_outliers_removed = np.array(customers.Channel.loc[customer_sc_df_outliers_removed.index].values) - 1
channel_log_outliers_removed = np.array(customers.Channel.loc[customer_log_sc_df_outliers_removed.index].values) - 1
channel_box_cox_outliers_removed = np.array(customers.Channel.loc[customer_box_cox_sc_df_outliers_removed.index].values) - 1

customer_features_pca_2 = PCA(2).fit_transform(customer_features)
customer_sc_pca_2 = PCA(2).fit_transform(customer_sc_df)
customer_log_sc_pca_2 = PCA(2).fit_transform(customer_log_sc_df)
customer_box_cox_sc_pca_2 = PCA(2).fit_transform(customer_box_cox_sc_df)
customer_features_outliers_removed_pca_2 = PCA(2).fit_transform(customer_features_outliers_removed)
customer_sc_outliers_removed_pca_2 = PCA(2).fit_transform(customer_sc_df_outliers_removed)
customer_log_sc_outliers_removed_pca_2 = PCA(2).fit_transform(customer_log_sc_df_outliers_removed)
customer_box_cox_sc_outliers_removed_pca_2 = PCA(2).fit_transform(customer_box_cox_sc_df_outliers_removed)

customer_features_pca_3 = PCA(3).fit_transform(customer_features)
customer_sc_pca_3 = PCA(3).fit_transform(customer_sc_df)
customer_log_sc_pca_3 = PCA(3).fit_transform(customer_log_sc_df)
customer_box_cox_sc_pca_3 = PCA(3).fit_transform(customer_box_cox_sc_df)
customer_features_outliers_removed_pca_3 = PCA(3).fit_transform(customer_features_outliers_removed)
customer_sc_outliers_removed_pca_3 = PCA(3).fit_transform(customer_sc_df_outliers_removed)
customer_log_sc_outliers_removed_pca_3 = PCA(3).fit_transform(customer_log_sc_df_outliers_removed)
customer_box_cox_sc_outliers_removed_pca_3 = PCA(3).fit_transform(customer_box_cox_sc_df_outliers_removed)


customer_features = customer_features.values
customer_sc = customer_sc_df.values
customer_log_sc = customer_log_sc_df.values
customer_box_cox_sc = customer_box_cox_sc_df.values
customer_features_outliers_removed = customer_features_outliers_removed.values
customer_sc_outliers_removed = customer_sc_df_outliers_removed.values
customer_log_sc_outliers_removed = customer_log_sc_df_outliers_removed.values
customer_box_cox_sc_outliers_removed = customer_box_cox_sc_df_outliers_removed.values