"""
SPOT  (Siffer et al., 2017)
"""
import numpy as np
from scipy.stats import genpareto


class SPOT:
    def __init__(self, q=1e-3, level=0.98):
        self.q = q
        self.level = level
        self.highestVal= None
        self.peaks = None
        self.numOfValues = None
        self.GPD_shape = None   # GPD shape
        self.GPD_scale = None   # GPD scale

        pass

    def fit(self, init_data):
        """
        Takes initial raw data picks out the values
        higher than the threshold according to quantile
        Then it calcules peaks (excesses)
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
        shape, _ , scale = genpareto.fit(peaks, floc=0)
        return shape, scale

    def _compute_threshold(self):
        """
        Compute
        z_q = t + (sigma / gamma) * ((q * n / N_t) ** (-gamma) - 1)
        """
        # if shape is very close to 0,
        # the formula divides by almost zero and breaks.
        numOfPeaks = len(self.peaks)
        if abs(self.GPD_shape) < 1e-8:

        ratio = self.q * self.numOfValues / numOfPeaks
        z_q = (((ratio) ** (- self.GPD_shape))-1) * (self.GPD_scale/self.GPD_shape) + self.highestVal
        pass

    def _refit(self):
        # TODO: call _fit_gpd, then _compute_threshold, and save the results
        self.GPD_shape, self.GPD_scale = self._fit_gpd(self.peaks)
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
