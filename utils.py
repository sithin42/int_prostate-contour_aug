import numpy as np

def vol_dice_score(y_pred,y_true, smooth=1e-4):

    y_pred = y_pred.flatten()
    y_true = y_true.flatten()

    wp = 1

    tp = wp * ((y_pred * y_true).sum())
    fp = (y_pred * (1 - y_true)).sum()
    fn = ((1 - y_pred) * y_true).sum()

    return (2 * tp +smooth) / (2 * tp + fp + fn + smooth)