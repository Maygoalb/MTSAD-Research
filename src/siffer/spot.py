"""
SPOT  (Siffer et al., 2017)
"""
import numpy as np


class SPOT:
    def __init__(self, q=1e-3, level=0.98):
        self.level = level
        self.highestVal= None
        self.peaks = None
        self.numOfValues = None

        pass

    def fit(self, init_data):
        """

        """
        initial_data = np.array(init_data, dtype=float)
        self.highestVal = np.quantile(init_data, self.level)
        self.peaks = []
        for i in  initial_data:
            if i > self.highestVal:
                self.peaks.append(i-self.highestVal)
        self.numOfValues = len(initial_data)
        self._refit()
        return self

    def _fit_gpd(self, peaks):
        # TODO: fit a GPD to the peaks
        # TODO: return gamma, sigma
        pass

    def _compute_threshold(self):
        # TODO: implement
        #   z_q = t + (sigma / gamma) * ((q * n / N_t) ** (-gamma) - 1)
        # TODO: handle the special case gamma close to 0
        pass

    def _refit(self):
        # TODO: call _fit_gpd, then _compute_threshold, and save the results
        pass


    def step(self, x):
        # TODO: if x > z_q            -> anomaly, return True
        # TODO: elif x > t            -> add to peaks, n += 1, refit
        # TODO: else                  -> normal value, n += 1
        # TODO: return False if not an anomaly
        pass

    def run(self, stream):
        # TODO: loop over stream, call step(), collect flags and thresholds
        # TODO: return flags, thresholds
        pass
