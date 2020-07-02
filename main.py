from single_sample import *


getLasers = SampleMeter()

data = getLasers.compute_data_avg(channels=[1, 2])

print(data)