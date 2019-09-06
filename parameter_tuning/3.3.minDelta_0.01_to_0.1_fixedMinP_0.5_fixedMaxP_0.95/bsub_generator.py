import numpy as np

fixedMinP=0.5
fixedMaxP=0.95
fraction=0.01 

startDelta=0.01
endDelta=min(0.1, 0.4*(fixedMaxP-fixedMinP))

dataset="tweet-2472"
min_deltas=np.arange(startDelta, endDelta+fraction, fraction)
print(min_deltas)
