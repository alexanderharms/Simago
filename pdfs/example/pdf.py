from scipy.stats import norm

def pdf_norm(params):
    # This function returns an instance of scipy.stats.norm
    # with the correct paramters
    loc_param = params[0]
    scale_param = params[1]
    return norm(loc=loc_param, scale=scale_param)

