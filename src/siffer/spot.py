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
   if __name__ == "__main__":
    train_data = ld('SMAP_train.npy')      # normal data only, used for fit
    stream = ld('SMAP_test.npy')           # the whole test column, used for run
    labels_LD = ld('SMAP_test_label.npy')  # labels belong to the test file
    labels = labels_LD                     # same length as stream, so no slicing

    print("unique values in train:", np.unique(train_data).size)
    print("train min/max:", train_data.min(), train_data.max())
    print("train 98th percentile:", np.quantile(train_data, 0.98))
    print("values above it:", (train_data > np.quantile(train_data, 0.98)).sum())
    print("shapes:", stream.shape, labels.shape)

    spot = SPOT(q=1e-3).fit(train_data)
    flags, thresholds = spot.run(stream)
    labels = labels.astype(bool)

    TP = np.sum(flags & labels)      # flagged, and a real anomaly
    FP = np.sum(flags & ~labels)     # flagged, but normal (false alarm)
    FN = np.sum(~flags & labels)     # not flagged, but a real anomaly (missed)
    TN = np.sum(~flags & ~labels)    # not flagged, and normal

    precision = TP / (TP + FP) if (TP + FP) else 0
    recall    = TP / (TP + FN) if (TP + FN) else 0
    f1        = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
    accuracy  = (TP + TN) / (TP + TN + FP + FN)

    print(f"TP={TP} FP={FP} FN={FN} TN={TN}")
    print(f"precision={precision:.3f} recall={recall:.3f} f1={f1:.3f} accuracy={accuracy:.3f}")
    print(f"Flags: {flags.sum()}, threshold[0]: {thresholds[0]}, threshold[-1]: {thresholds[-1]}")
