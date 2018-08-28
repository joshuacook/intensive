import numpy as np
from scipy import stats
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils import check_array
from sklearn.externals import six
from sklearn.externals.joblib import Parallel, delayed
from sklearn.utils.validation import check_is_fitted, FLOAT_DTYPES

def _transform_selected(X, transform, selected="all", copy=True,
                        retain_ordering=False):
    """Apply a transform function to portion of selected features
    Parameters
    ----------
    X : {array-like, sparse matrix}, shape [n_samples, n_features]
        Dense array or sparse matrix.
    transform : callable
        A callable transform(X) -> X_transformed
    copy : boolean, optional
        Copy X even if it could be avoided.
    selected : "all" or array of indices or mask
        Specify which features to apply the transform to.
    retain_ordering : boolean, default False
        Specify whether the initial order of features has
        to be maintained in the output
    Returns
    -------
    X : array or sparse matrix, shape=(n_samples, n_features_new)
    """
    X = check_array(X, accept_sparse='csc', copy=copy, dtype=FLOAT_DTYPES)

    if isinstance(selected, six.string_types) and selected == "all":
        return transform(X)

    if len(selected) == 0:
        return X

    n_features = X.shape[1]
    ind = np.arange(n_features)
    sel = np.zeros(n_features, dtype=bool)
    sel[np.asarray(selected)] = True
    not_sel = np.logical_not(sel)
    n_selected = np.sum(sel)

    if n_selected == 0:
        # No features selected.
        return X
    elif n_selected == n_features:
        # All features selected.
        return transform(X)
    else:
        X_sel = transform(X[:, ind[sel]])
        X_not_sel = X[:, ind[not_sel]]

        if retain_ordering:
            # As of now, X is expected to be dense array
            X[:, ind[sel]] = X_sel
            return X
        if sparse.issparse(X_sel) or sparse.issparse(X_not_sel):
            return sparse.hstack((X_sel, X_not_sel))
        else:
            return np.hstack((X_sel, X_not_sel))

def _boxcox(X, i, lambda_x=None):
    x = X[:, i]
    if lambda_x is None:
        x, lambda_x = stats.boxcox(x, lambda_x)
        return x, lambda_x
    else:
        x = stats.boxcox(x, lambda_x)
        return x


def boxcox(X, copy=True):
    """BoxCox transform to the input data
    Apply boxcox transform on individual features with lambda
    that maximizes the log-likelihood function for each feature
    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
        The data to be transformed. Should contain only positive data.
    copy : boolean, optional, default=True
        Set to False to perform inplace transformation and avoid a
        copy (if the input is already a numpy array or a scipy.sparse
        CSR matrix and if axis is 1).
    Returns
    -------
    X_tr : array-like, shape (n_samples, n_features)
        The transformed data.
    References
    ----------
    G.E.P. Box and D.R. Cox, "An Analysis of Transformations", Journal of the
    Royal Statistical Society B, 26, 211-252 (1964).
    """
    X = check_array(X, ensure_2d=True, dtype=FLOAT_DTYPES, copy=copy)
    if np.any(X <= 0):
        raise ValueError("BoxCox transform can only be applied "
                         "on positive data")
    n_features = X.shape[1]
    outputs = Parallel(n_jobs=-1)(delayed(_boxcox)(X, i, lambda_x=None)
                                  for i in range(n_features))
    output = np.concatenate([o[0][..., np.newaxis] for o in outputs], axis=1)
    return output


class BoxCoxTransformer(BaseEstimator, TransformerMixin):
    """BoxCox transformation on individual features.
    Boxcox transform wil be applied on each feature (each column of
    the data matrix) with lambda evaluated to maximise the log-likelihood
    Parameters
    ----------
    transformed_features : "all" or array of indices or mask
        Specify what features are to be transformed.
        - "all" (default): All features are to be transformed.
        - array of int: Array of feature indices to be transformed..
        - mask: Array of length n_features and with dtype=bool.
    copy : boolean, optional, default=True
        Set to False to perform inplace computation.
    Attributes
    ----------
    transformed_features_ : array of int
        The indices of the features to be transformed
    lambdas_ : array of float, shape (n_transformed_features,)
        The parameters of the BoxCox transform for the selected features.
    n_features_ : int
        Number of features in input during fit
    Notes
    -----
    The Box-Cox transform is given by::
        y = (x ** lmbda - 1.) / lmbda,  for lmbda > 0
            log(x),                     for lmbda = 0
    ``boxcox`` requires the input data to be positive.
    """
    def __init__(self, transformed_features="all", n_jobs=1, copy=True):
        self.transformed_features = transformed_features
        self.n_jobs = n_jobs
        self.copy = copy

    def fit(self, X, y=None):
        """Estimate lambda for each feature to maximise log-likelihood
        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The data to fit by apply boxcox transform,
            to each of the features and learn the lambda.
        y : ignored
        Returns
        -------
        self : object
            Returns self.
        """
        X = check_array(X, ensure_2d=True, dtype=FLOAT_DTYPES)
        self.n_features_ = X.shape[1]
        if self.transformed_features is "all":
            self.transformed_features_ = np.arange(self.n_features_)
        else:
            self.transformed_features_ = np.copy(self.transformed_features)
            if self.transformed_features_.dtype == np.bool:
                self.transformed_features_ = \
                    np.where(self.transformed_features_)[0]
        if np.any(X[:, self.transformed_features_] <= 0):
            raise ValueError("BoxCox transform can only be applied "
                             "on positive data")
        out = Parallel(n_jobs=self.n_jobs)(delayed(_boxcox)(X, i,
                                           lambda_x=None)
                                           for i in self.transformed_features_)
        self.lambdas_ = np.array([o[1] for o in out])
        return self

    def transform(self, X):
        """Transform each feature using the lambdas evaluated during fit time
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The data to apply boxcox transform.
        Returns
        -------
        X_tr : array-like, shape (n_samples, n_features)
            The transformed data.
        """
        X = check_array(X, ensure_2d=True, dtype=FLOAT_DTYPES, copy=self.copy)
        if any(np.any(X[:, self.transformed_features_] <= 0, axis=0)):
            raise ValueError("BoxCox transform can only be applied "
                             "on positive data")
        if X.shape[1] != self.n_features_:
            raise ValueError("X has a different shape than during fitting.")
        X_tr = _transform_selected(X, self._transform,
                                   self.transformed_features_,
                                   copy=False, retain_ordering=True)
        return X_tr

    def _transform(self, X):
        outputs = Parallel(n_jobs=self.n_jobs)(
            delayed(_boxcox)(X, i, self.lambdas_[i])
            for i in range(len(self.transformed_features_)))
        output = np.concatenate([o[..., np.newaxis] for o in outputs], axis=1)
        return output

    def inverse_transform(self, X):
        """Inverse transform each feature using the lambdas evaluated during fit time
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The transformed data after boxcox transform.
        Returns
        -------
        X_inv : array-like, shape (n_samples, n_features)
            The original data.
        Notes
        -----
        The inverse Box-Cox transform is given by::
        y = log(x * lmbda + 1.) / lmbda,  for lmbda > 0
            exp(x),                       for lmbda = 0
        """

        X = check_array(X, ensure_2d=True, dtype=FLOAT_DTYPES, copy=self.copy)
        if X.shape[1] != self.n_features_:
            raise ValueError("X has a different shape than during fitting.")
        X_inv = _transform_selected(X, self._inverse_transform,
                                    self.transformed_features_, copy=False,
                                    retain_ordering=True)
        return X_inv

    def _inverse_transform(self, X):
        X_inv = X.copy()

        mask = self.lambdas_ != 0
        mask_lambdas = self.lambdas_[mask]
        Xinv_mask = X_inv[:, mask]
        Xinv_mask *= mask_lambdas
        np.log1p(Xinv_mask, out=Xinv_mask)
        Xinv_mask /= mask_lambdas
        np.exp(Xinv_mask, out=Xinv_mask)
        X_inv[:, mask] = Xinv_mask

        mask = self.lambdas_ == 0
        X_inv[:, mask] = np.exp(X_inv[:, mask])
        return X_inv