"""
Functions for the lognormal distribtution.
"""
from scipy.stats import lognorm


def pdf_lognorm(params):
    """
    This function returns an instance of scipy.stats.norm
    with the correct paramters
    s = sigma
    scale = exp(mu)
    """
    scale = params[0]
    s = params[1]
    return lognorm(s=s, scale=scale)
