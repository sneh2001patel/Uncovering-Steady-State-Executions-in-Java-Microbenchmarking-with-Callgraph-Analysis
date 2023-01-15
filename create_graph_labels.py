import rpy2
import math
import json 
from glob import glob
from kneed import KneeLocator
from outlier_detection import *
from rpy2.robjects.packages import importr, data
BOOTSTRAP_ITERATIONS = 10000

dataset = []
with open("iterDurations.txt") as f:
  content = f.readlines()
  arr = []
  count = 1
  for line in content:
    arr.append(float(line))
    if count == 1000:
      dataset.append(arr)
      arr = []
      count = 0
    count += 1  

# filter out the dataset by removing outliers
output = create_filtered(dataset)
filtered_list = output["filtered_list"]
outlier_idx = output["outlier_idx"]

utils = importr('utils')
base = importr('base')

utils.chooseCRANmirror(ind=1)
utils.install_packages('changepoint')

# All the code beyond this point is retrived by https://github.com/SEALABQualityGroup/steady-state.git 

# Change Point Analysis 
def crops(measurements):
    cpt = importr('changepoint')
    ts = rpy2.robjects.FloatVector(measurements)
    pen_value = tuple(float(m * math.log(len(measurements))) for m in [4, 100000])
    # print(pen_value)
    crops_ = cpt.cpt_meanvar(ts, method='PELT', penalty='CROPS',
                             pen_value=rpy2.robjects.FloatVector(pen_value))
    crops_full = cpt.cpts_full(crops_)
    ncpts = []

    for i in range(1, crops_full.nrow + 1):
        ncpts.append(len([x for x in map(int, crops_full.rx(i, True)) if x > 0]))

    penalties = [x for x in cpt.pen_value_full(crops_)]
    if len(penalties) == len(ncpts) + 1:
        ncpts.append(0)

    assert (len(penalties) == len(ncpts))
    return penalties, ncpts

def find_penalty(measurements):
    penalties, ncpts = crops(measurements)
    default_pen = 15 * math.log(len(measurements))

    if len(penalties) < 2 or len(ncpts) < 2:
        return penalties[0]

    try:
        kneedle = KneeLocator(penalties[::-1], ncpts[::-1], S=1.0, curve="convex", direction="decreasing")
        penalty = kneedle.elbow if kneedle.elbow else default_pen
    except IndexError:
         penalty = default_pen

    return float(penalty)

def pelt(ts):
    penalty = find_penalty(ts)
    cpt = importr('changepoint')
    measurements = rpy2.robjects.FloatVector(ts)
    changepoints = cpt.cpt_meanvar(measurements, method='PELT', penalty='Manual',
                                   pen_value=penalty)
    # List indices in R start at 1.
    return [int(cpoint - 1) for cpoint in changepoints.slots['cpts']]


cpt_list = []

for i in range(len(filtered_list)):
  cpt = pelt(filtered_list[i])
  cpt_list.append(cpt)



def interval_fork(m1, m2, significance=0.05):
    means = [np.mean(random.choices(m1, k=len(m1)))/np.mean(random.choices(m2, k=len(m2)))
             for _ in range(BOOTSTRAP_ITERATIONS)]
    return np.quantile(means, significance/2), np.quantile(means, 1-significance/2)

def test(m1, m2, es=0.05, significance=0.05):
    ci = interval_fork(m1, m2, significance)
    return ci[1] <= 1 - es or ci[0] >= 1 + es


STEADY_STATE = "steady state"
NO_STEADY_STATE = "no steady state"
INCONSISTENT = "inconsistent"

def steady_state_starts(ts, cpts):
    cpts = [0] + cpts
    i = -2
    last_segment = ts[cpts[i] + 1:]
    while cpts[i] > 0:
        cpt = cpts[i]
        i -= 1
        prev_cpt = cpts[i]

        start = prev_cpt + 1 if prev_cpt > 0 else prev_cpt
        stop = cpt + 1
        current_segment = ts[start:stop]

        if test(last_segment, current_segment):
            return cpt

    return 0

def _classify_benchmark(forks):
    if STEADY_STATE not in forks:
        return NO_STEADY_STATE
    elif NO_STEADY_STATE in forks:
        return INCONSISTENT
    else:
        return STEADY_STATE

def classify_fork(ts, cpts):
    steady_state_starts_at = steady_state_starts(ts, cpts)
    if steady_state_starts_at <= 899:
        classification = STEADY_STATE
    else:
        classification = NO_STEADY_STATE
        steady_state_starts_at = -1
    return classification, steady_state_starts_at

def classify_benchmark(ts_list, cpts_list):
    forks = []
    steady_state_starts_at = []
    for ts, cpts in zip(ts_list, cpts_list):
        fork_class, steady_state_starts_ = classify_fork(ts, cpts)
        forks.append(fork_class)
        steady_state_starts_at.append(steady_state_starts_)

    classification = _classify_benchmark(forks)
    return {"run": classification, "forks": forks, "steady_state_starts": steady_state_starts_at}

res = classify_benchmark(filtered_list, cpt_list)

# Label the executions based on the res 
fork_labels = {}
for k in range(len(res['steady_state_starts'])):

  fork = filtered_list[k]
  print(len(fork))
  steady_statemark = res['steady_state_starts'][k]

  labels = []

  for i in range(len(fork)):
    if steady_statemark == -1:
      labels.append((i,"warm up state"))
    else:
      if i < steady_statemark:
        labels.append((i,"warm up state"))
      else:
        labels.append((i,"steady state"))
  
  fork_labels["Fork " + str(k + 1)] = labels


with open('labels.txt', 'w') as f:
  f.write(json.dumps(fork_labels))
