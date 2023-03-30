import cv2
import numpy as np

def WTHE(src):
    rows, cols, channels = src.shape
    total_pixels = rows * cols

    L = None
    if channels == 1:
        L = src.copy()
    else:
        YUV = cv2.cvtColor(src, cv2.COLOR_BGR2YUV)
        YUV_channels = cv2.split(YUV)
        L = YUV_channels[0]

    histsize = 256
    range = [0, 256]
    histRanges = [range]
    bins = 256
    hist = cv2.calcHist([L], [0], None, [histsize], range, True, False)

    total_pixels_inv = 1.0 / total_pixels
    P = hist.copy()
    for i in range(256):
        P[i] = P[i] * total_pixels_inv

    Pwt = P.copy()
    minP, maxP, _, _ = cv2.minMaxLoc(P)
    Pu = v * maxP
    Pl = minP
    for i in range(256):
        Pi = P[i]
        if Pi > Pu:
            Pwt[i] = Pu
        elif Pi < Pl:
            Pwt[i] = 0
        else:
            Pwt[i] = pow((Pi - Pl) / (Pu - Pl), r) * Pu

    Cwt = Pwt.copy()
    cdf = 0
    for i in range(256):
        cdf += Pwt[i]
        Cwt[i] = cdf

    Wout = 255.0
    Madj = 0.0
    table = np.zeros(256, dtype=np.uint8)
    for i in range(256):
        table[i] = cv2.saturate_cast(np.uint8, Wout * Cwt[i] + Madj)

    dst = cv2.LUT(L, table)

    if channels == 1:
        dst = dst.copy()
    else:
        YUV_channels[0] = dst
        dst = cv2.merge(YUV_channels)
        dst = cv2.cvtColor(dst, cv2.COLOR_YUV2BGR)

    return dst