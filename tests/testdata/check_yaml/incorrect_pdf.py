from scipy.stats import lognorm, norm


def pdf_norm(params)
    # This function returns an instance of scipy.stats.norm
    # with the correct paramters
    loc_param = params[0]
    scale_param = params[1]
    return norm(loc=loc_param, scale=scale_param)


def pdf_lognorm(params):
    # This function returns an instance of scipy.stats.norm
    # with the correct paramters
    # s = sigma
    # scale = exp(mu)
    scale = params[0]
    s = params[1]
    return lognorm(s=s, scale=scale)
