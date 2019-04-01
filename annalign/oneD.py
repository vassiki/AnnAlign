import pandas as pd
import numpy as np
import glob
import os


def format_file(fn):
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


def timingfile(df, dimension):

    """
    df is formatted dataframe for an RA
    dimension is the one we want to extract time stamps for
    """

    # clearly, the dimension has to contain strings
    df[dimension] = df[dimension].str.lower()

    # 'no' in dimension of interest
    not_present_df = df[df[dimension].str.contains('no', na=True)]

    present_indices = [idx for idx in range(len(df)) if idx not in non_face_df.index]

    present_df = df.iloc(present_indices)

    prefix = '_'.join([val.lower() for val in dimension.split(' ')])

    start_times_present = np.round(present_df["Start"]).values

    np.savetxt("{0}_annot_present.txt".format(prefix), start_times_present.reshape(1, start_times_present.shape[0]),
               fmt='%4.1f')

    start_times_absent = np.round(not_present_df["Start"]).values

    np.savetxt("{0}_annot_absent.txt".format(prefix), start_times_absent.reshape(1, start_times_absent.shape[0]),
               fmt='%4.1f')


