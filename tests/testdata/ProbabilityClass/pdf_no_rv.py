"""
Functions to test checks for wrong format for PDFs.
"""
from scipy.stats import norm


def pdf_no_rv(params):
    """
    This function just returns a list of parameters.
    """

    return params


def pdf_no_frozen_rv(params):
    """
    This function returns an rv_continuous object but not frozen.
    """
    return norm
