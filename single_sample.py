import ctypes
import numpy as np
from picosdk.pl1000 import pl1000 as pl
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok


class SampleMeter:
    def __init__(self):
        self.iterations = 1000
        self._initialize_picolog()

    def _initialize_picolog(self):
        # Create chandle and status ready for use
        self.chandle = ctypes.c_int16()
        self.status = {}

    def _open_picolog_comm(self):
        # Open PicoLog 1000 device
        self.status['openUnit'] = pl.pl1000OpenUnit(ctypes.byref(self.chandle))
        assert_pico_ok(self.status['openUnit'])

    def _close_picolog_comm(self):
        # Close PicoLog 1000 device
        self.status['closeUnit'] = pl.pl1000CloseUnit(self.chandle)
        assert_pico_ok(self.status['closeUnit'])

    def get_raw_data(self, channels=[1, 2]):
        channel_data = {'channels_enum': channels,
                        'channel_a_raw': [], 'channel_b_raw': [],
                        'channel_a_avg': [], 'channel_b_avg': [],
                        'channel_a_std': [], 'channel_b_std': []}
        single_value_channel_a = ctypes.c_int16()
        single_value_channel_b = ctypes.c_int16()
        # Open PicoLog 1000
        self._open_picolog_comm()
        for _ in range(self.iterations):
            # Get a single ADC count value from channel A
            self.status['getSingle'] = pl.pl1000GetSingle(self.chandle,
                                                          pl.PL1000Inputs['PL1000_CHANNEL_' + str(channels[0])],
                                                          ctypes.byref(single_value_channel_a))
            # Get a single ADC count value from channel B
            self.status['getSingle'] = pl.pl1000GetSingle(self.chandle,
                                                          pl.PL1000Inputs['PL1000_CHANNEL_' + str(channels[1])],
                                                          ctypes.byref(single_value_channel_b))
            assert_pico_ok(self.status['getSingle'])
            channel_data['channel_a_raw'].append(single_value_channel_a.value)
            channel_data['channel_b_raw'].append(single_value_channel_b.value)

        # Close PicoLog 1000
        self._close_picolog_comm()

        # Assert correct closure of PicoLog 1000
        assert_pico_ok(self.status['closeUnit'])
        return channel_data

    def compute_data_avg(self, channels=[1, 2]):
        channel_data = self.get_raw_data(channels)
        # We need to check for outliers

        # Compute mean of raw data
        channel_data['channel_a_avg'] = np.mean(channel_data['channel_a_raw'])
        channel_data['channel_b_avg'] = np.mean(channel_data['channel_b_raw'])
        # Compute standard deviation of raw data
        channel_data['channel_a_std'] = np.std(channel_data['channel_a_raw'])
        channel_data['channel_b_std'] = np.std(channel_data['channel_b_raw'])

        return channel_data
