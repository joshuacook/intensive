import numpy as np
from sklearn.linear_model import LinearRegression

def fit_and_plot_poly_to_degree(xx, yy, degree, ax, scatter=False):
    lr = LinearRegression()
    X = []
    for i in range(degree):
        X.append(xx**(i+1))
    X = np.array(X).T
    lr.fit(X, yy)
    if scatter:
        ax.scatter(xx, lr.predict(X), label="p = {}".format(degree))
    else:
        ax.plot(xx, lr.predict(X), label="p = {}".format(degree))