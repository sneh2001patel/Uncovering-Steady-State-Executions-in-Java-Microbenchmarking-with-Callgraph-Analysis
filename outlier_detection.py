import numpy as np

# Play around with this to increase/decrease number of outliers in the dataset
ALPHA = 0.01 # 0.01, 
BETA = 0.99 # 0.99
TURKEY = 1.5 

def isoutlier(series, value):
    median = np.median(series)
    p1, p99 = [np.quantile(series, q) for q in [ALPHA, BETA]]
    return value > (median + TURKEY * (p99 - p1)) or value < (median - TURKEY * (p99 - p1))


def create_filtered(series):
  arr = []
  outlier_idx = []
  for seri in series:
    out = []
    a = []
    for idx in range(len(seri)):
      if not isoutlier(seri, seri[idx]):
        out.append(seri[idx])
      else:
        a.append(idx)
        
    outlier_idx.append(a)
    arr.append(out)
  
  return {"filtered_list": arr, "outlier_idx": outlier_idx}