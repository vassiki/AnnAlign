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

    return ra


def contiguous_blocks(df, index):
    begins_with = index
    while df.loc[index, 'End'] == df.loc[index+1, 'Start']:
        index += 1
    return begins_with, index


def timing1D(df):
    df = df.round(1)
    newdf = pd.DataFrame(columns=['start', 'end'])
    # start with index 0
    index = 0
    while index < df.shape[0] -1:
        start, end = contiguous_blocks(df, index)
        row = pd.DataFrame([[df.loc[start, 'Start'], df.loc[end, 'End']]], columns=['start', 'end'])
        newdf = newdf.append(row)
        index = end+1

    return newdf


def timing_file(df, part, dimension):

    """
    df is formatted dataframe for an RA
    dimension is the one we want to extract time stamps for
    """

    #df[dimension] = df[dimension].str.lower()
    #df['Start'] = np.round(df['Start'], 1)
    #df = df.drop_duplicates(['Start'])
    # df = df.sort_values(by=['Start'])
    # not_present_df = df[df[dimension].isnull()]
    # present_df = df[~df['Face Present'].isnull()]
    newdf = timing1D(df)
    prefix = '_'.join(['part_{0}'.format(str(part))] +
                      [val.lower() for val in dimension.split(' ')])

    start_times_present = newdf['start'].values
    print(type(start_times_present))
    #start_times_present = present_df["Start"].values
    np.savetxt(os.path.join("../outputs","{0}_annot_present.txt".format(prefix)), start_times_present.reshape(1, start_times_present.shape[0]),
               fmt='%4.1f')

    start_times_absent = newdf['end'].values
    #start_times_absent = not_present_df["Start"].values
    np.savetxt(os.path.join("../outputs","{0}_annot_absent.txt".format(prefix)), start_times_absent.reshape(1, start_times_absent.shape[0]),
               fmt='%4.1f')
    return start_times_present, start_times_absent


def concat_run_timings(sub, dimension, type_data):
    run_files = glob.glob('sub-sid000{0}*_{1}.txt'.format(sub, type_data))
    out_file = 'sub-sid000{0}_{1}_{2}_allruns.txt'.format(sub, dimension, type_data)
    with open(out_file, 'w') as outfile:
        for fname in run_files:
            with open(fname) as infile:
                outfile.write(infile.read())
