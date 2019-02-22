import os
import pandas as pd
import numpy as np


def format_annotation_file(fn):
    annotation_dir = '../annotations/raw'
    ra = pd.read_csv(os.path.join(annotation_dir, fn), sep='\t', skiprows=1)
    if 'ra1' in fn:
        ra.rename(
            columns={"Begin Time - ss.msec": "Start", "End Time - ss.msec": "End", "Duration - ss.msec": "Duration",
                     "Face(s) present": "Face Present"}, inplace=True)
    else:
        ra.rename(
            columns={"Begin Time - ss.msec": "Start", "End Time - ss.msec": "End", "Duration - ss.msec": "Duration",
                     "Face present": "Face Present"}, inplace=True)

    return ra


def round_ms(f, temporal_resolution):
    decimal = f - np.fix(f)
    if decimal <= 0.5:
        val = 0.0
    else:
        val = temporal_resolution
    return np.fix(f) + val


def annotation_timestamps(dim, temporal_resolution):
    file = 'ra2_part2.txt'
    ra = format_annotation_file(file)

    df = ra[["Start", "End", dim]]
    df = df.dropna(subset=[dim])

    df["Start"] = df.apply(lambda row: round_ms(row["Start"], temporal_resolution), axis=1)
    df["End"] = df.apply(lambda row: round_ms(row["End"], temporal_resolution), axis=1)

    s = np.array([])
    for i in df.index:
        x = np.arange(df.loc[i, 'Start'], df.loc[i, 'End'], temporal_resolution)
        s = np.append(s, x)

    return np.unique(s)


