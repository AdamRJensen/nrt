import numpy as np
import pytest

import nrt.fit_methods as fm
import nrt.stats as st


def test_rirls(X_y_intercept_slope):
    """
    Compare against implementation in yatsm
    https://github.com/ceholden/yatsm/blob/
    8e328f366c8fd94d5cc57cd2cc42080c43d1f391/yatsm/regression/robust_fit.py
    """
    X, y, intercept, slope = X_y_intercept_slope
    beta, residuals = fm.rirls(X, y, M=st.bisquare, tune=4.685,
               scale_est=st.mad, scale_constant=0.6745, update_scale=True,
               maxiter=50, tol=1e-8)

    np.testing.assert_allclose(beta, np.array([[intercept, intercept],
                                               [slope, slope]]))
    #np.testing.assert_allclose(np.dot(X, beta), y)


# @pytest.mark.parametrize(('X', 'y'), [
#     (np.random.rand(n, n), np.random.rand(n))
#     for n in range(1, 10)
# ])
# def test_RLM_issue88(X, y):
#     """ Issue 88: Numeric problems when n_obs == n_reg/k/p/number of regressors
#     The regression result will be garbage so we're not worrying about the
#     coefficients. However, it shouldn't raise an exception.
#     """
#     beta, residuals = fm.rirls(X, y, M=st.bisquare, tune=4.685,
#                scale_est=st.mad, scale_constant=0.6745, update_scale=True,
#                maxiter=50, tol=1e-8)


@pytest.fixture
def X_y_intercept_slope(request):
    np.random.seed(0)
    slope, intercept = 2., 5.
    X = np.c_[np.ones(10), np.arange(10)]
    y = np.array([slope * X[:, 1] + intercept,
                  slope * X[:, 1] + intercept])

    # Add noise
    y[0,9] = 0
    y[1,0] = 10
    return X, y.T, intercept, slope