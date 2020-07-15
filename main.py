from single_sample import *

if __name__ == '__main__':
    # Class constructor
    getLasers = SampleMeter()
    # Obtain averaged data from meter duet
    data = getLasers.compute_data_avg(channels=[1, 2])
