import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def scatter_plot_by_class(ax, features, target, feat_1='Component_1', feat_2='Component_2'):
    species = ['Kama', 'Rosa', 'Canadian']
    colormap = ['red', 'green', 'blue']
    target = pd.Series(target)
    for i, cls in enumerate(target.unique()):
        color = colormap[i]
        mask = target == cls
        features[mask].plot(x=feat_1, y=feat_2, label=species[i], kind='scatter', ax=ax, color=color)
        
def scatter_plot_with_decision_boundary(ax, features, target, feat_1, feat_2, model):
    X = features[[feat_1, feat_2]]
    y = target
    h = .02  # step size in the mesh

    model.fit(X, y)

    x_min, x_max = X[feat_1].min() - .5, X[feat_1].max() + .5
    y_min, y_max = X[feat_2].min() - .5, X[feat_2].max() + .5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])

    scatter_plot_by_class(ax, features, target, feat_1, feat_2)
    Z = Z.reshape(xx.shape)
    ax.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.3)

