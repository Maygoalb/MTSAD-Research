"""
calculates precision, recall, and F1 scores
"""
import numpy as np

def confusion_counts(flags, labels):
    #TP: flagged and a real attack:
    TP = np.sum(flags & labels)
    #FP: flagged but normal:
    FP = np.sum(flags & ~labels)
    #FN: missed attack:
    FN = np.sum(~flags & labels)
    #TN: not flagged and normal:
    TN = np.sum(~flags & ~labels)

    return TP, FP, FN, TN

def precision_recall_f1(TP, FP, FN):
    # start at 0, so a zero denominator gives a score of 0 and not an error
    precision = 0
    recall = 0
    F1 = 0

    if (TP + FP) != 0:
        precision = TP / (TP + FP)
    if (TP + FN) != 0:
        recall = TP / (TP + FN)
    if (precision + recall) != 0:
        F1 = 2 * precision * recall / (precision + recall)

    return precision, recall, F1
