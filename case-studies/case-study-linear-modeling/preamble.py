import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def initialize_2d_plot(x_min=-1, x_max=8, y_min=-1, y_max=8, figsize=(12,6)):
    """Default values: x_min=-1, x_max=8, y_min=-1, y_max=8"""
    fig = plt.figure(figsize=figsize)
    plt.xlim([x_min,x_max])
    plt.ylim([y_min,y_max])
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    
def draw_vector(np_array, tail=np.array([0,0]), kwargs=None):
    """Pass a vector of dimension 2 and a figure.
       Optionally, specify a start point. Defaults to the origin.
       """
    u_1 = np_array[0]
    u_2 = np_array[1]
    tail_1 = tail[0]
    tail_2 = tail[1]
    if kwargs:
        if 'head_width' in kwargs.keys():
            plt.arrow(tail_1,tail_2,u_1,u_2, **kwargs)
        else:
            plt.arrow(tail_1,tail_2,u_1,u_2, **kwargs, head_width=0.25, head_length=0.25)
    else:
        plt.arrow(tail_1,tail_2,u_1,u_2, head_width=0.25, head_length=0.25)    
    
xx = np.linspace(-3,3,7)
inverse = np.linalg.inv
a = np.array((-1,2))
b = np.array((3,5))
c = a + b
d = np.array((-1.5,1.3))
e = 3*d
f = np.array((-1,1))
g = np.array((2,-1))
h = 2*f + 3*g
as_row_vectors_df = pd.DataFrame([a,b,c,d,e,f,g,h], columns=['x','y'], index=['a','b','c','d','e','f','g','h'])
as_col_vectors_df = as_row_vectors_df.T
