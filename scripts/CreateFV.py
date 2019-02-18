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


def round_ms(f):
    decimal = f - np.fix(f)
    # val = 0
    if decimal <= 0.5:
        val = 0.5
    else:
        val = 1.0
    return np.fix(f) + val


def annotation_timestamps(dim, temporal_resolution):
    file = 'ra2_part2.txt'
    ra = format_annotation_file(file)

    df = ra[["Start", "End", dim]]
    print("Dimensions before dropping are {}".format(df.shape))
    df = df.dropna(subset=[dim])
    print("Dimensions after dropping are {}".format(df.shape))

    df["Start"] = df.apply(lambda row: round_ms(row["Start"]), axis=1)
    df["End"] = df.apply(lambda row: round_ms(row["End"]), axis=1)

    s = np.array([])
    for i in df.index:
        # print("index is {}".format(i))
        x = np.arange(df.loc[i, 'Start'], df.loc[i, 'End'], temporal_resolution)
        s = np.append(s, x)

    return np.unique(s)


# df = annotation_timestamps("Face Present", 0.5)
# def movie_part_lengths(part):
#     part_lengths = {'part2': 9.37, 'part3': 7.57, 'part4': 8.35, 'part5': 9.58, 'part6': 13.03}

