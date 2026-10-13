"""
SPOT  (Siffer et al., 2017)
"""
import numpy as np
import math
from scipy.stats import genpareto
from open_SMAP import load_smap_data as ld


class SPOT:
    def __init__(self, q=1e-3, level=0.98):
        self.q = q
        self.level = level
        self.highestVal= None
        self.peaks = None
        self.numOfValues = None
        self.GPD_shape = None   # GPD shape
        self.GPD_scale = None   # GPD scale
        self.z_q = None


    def fit(self, init_data):
        """
        Takes initial raw data picks out the values
        higher than the threshold according to quantile
        Then it calcules peaks (excesses)
        """
        initial_data = np.array(init_data, dtype=float)
        # t
        self.highestVal = np.quantile(initial_data, self.level)
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

        numOfPeaks = len(self.peaks)
        ratio = self.q * self.numOfValues / numOfPeaks
        # if shape is very close to 0,
        # the formula divides by almost zero and breaks.
        # Then z_q = t - {scale} * ln({ratio})
        if abs(self.GPD_shape) < 1e-8:
            z_q = self.highestVal - self.GPD_scale * math.log(ratio)
        else:
            z_q = (((ratio) ** (- self.GPD_shape))-1) * (self.GPD_scale/self.GPD_shape) + self.highestVal

        return z_q

    def _refit(self):
        # TODO: call _fit_gpd, then _compute_threshold, and save the results
        self.GPD_shape, self.GPD_scale = self._fit_gpd(self.peaks)
        self.z_q = self._compute_threshold()


    def step(self, x):
        if x > self.z_q:
            anomaly = True
        # new peak found
        elif x > self.highestVal:
            self.peaks.append(x - self.highestVal)
            self.numOfValues += 1
            # update the cut off
            self._refit()
            anomaly = False
        else:
            self.numOfValues +=1
            anomaly = False
        return anomaly




    def run(self, stream):
        flags = []
        thresholds = []
        for x in stream:
            flags.append(self.step(x))
            thresholds.append(self.z_q)
        threshold_np = np.array(thresholds)
        flags_np = np.array(flags)
        return  flags_np, threshold_np


if __name__ == "__main__":
    first_1000 = ld()[:1000]
    stream = ld()[1000:]
    spot = SPOT(q=1e-3).fit(first_1000)
    flags, thresholds = spot.run(stream)
