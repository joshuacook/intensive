import numpy as np
import pandas as pd
from urllib.request import urlopen

BASE_URL = 'https://archive.ics.uci.edu/ml/machine-learning-databases/'
DATASET_URI = 'breast-cancer-wisconsin/unformatted-data'
FULL_URL = BASE_URL + DATASET_URI

BC_COLUMNS = [
    'Sample_code_number',
    'Clump_Thickness',
    'Uniformity_of_Cell_Size',
    'Uniformity_of_Cell_Shape',
    'Marginal_Adhesion',
    'Single_Epithelial_Cell_Size',
    'Bare_Nuclei',
    'Bland_Chromatin',
    'Normal_Nucleoli',
    'Mitoses',
    'Diagnosis',
    'group'
]

def read_string(data):
    return data.readline().decode()

def read_file_to_list_of_groups(data):
    
    groups = []
    tmp = []
    line = read_string(data)
    while line:
        if 'Group' in line:
            groups.append(tmp)
            tmp = []
        if line != '\n':
            tmp.append(line)
        line = read_string(data)
    groups.append(tmp)  
    
    return groups

def remove_commented_lines(groups):
    groups = [
        [line for line in group if '#####' not in line]
        for group in groups
    ]
    return groups

def group_to_df(group, group_name):
    group = [(line.replace('\n','')
                    .split(',')) for line in group]
    group = np.array(group, dtype=int)
    group_df = pd.DataFrame(group)
    group_df['group'] = group_name
    group_df.columns = BC_COLUMNS
    return group_df

if __name__ == '__main__':

    data = urlopen(FULL_URL)
    assert data.status == 200
    groups = read_file_to_list_of_groups(data)
    groups = remove_commented_lines(groups)
    
    group_1_df = group_to_df(groups[1], 'group_1')
    group_2_df = group_to_df(groups[2], 'group_2')
    group_3_df = group_to_df(groups[3], 'group_3')
    group_4_df = group_to_df(groups[4], 'group_4')
    group_5_df = group_to_df(groups[5], 'group_5')
    group_6_df = group_to_df(groups[7], 'group_6')
    group_7_df = group_to_df(groups[8], 'group_7')
    group_8_df = group_to_df(groups[9], 'group_8')
    
    breast_cancer_df = pd.concat([group_1_df, group_2_df, 
                                  group_3_df, group_4_df, 
                                  group_5_df, group_6_df, 
                                  group_7_df, group_8_df])