#!/usr/bin/env python
import pandas as pd
import numpy as np
import glob
import os


def format_file(fn):
    annotation_dir = '../annotations/raw'
    ra = pd.read_csv(os.path.join(annotation_dir, fn), sep='\t', names=['Dimension', 'Blank', 'Start', 'End', 'Duration'], index_col=False) 
    return ra


def contiguous_blocks(df, index):
    begins_with = index
    while df.loc[index, 'End'] == df.loc[index+1, 'Start'] and index < df.shape[0] - 2:
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

    newdf = timing1D(df)
    prefix = '_'.join(['part_{0}'.format(str(part))] +
                      [val.lower() for val in dimension.split(' ')])

    start_times_present = newdf['start'].values
    np.savetxt(os.path.join("../outputs","{0}_annot_present.txt".format(prefix)), start_times_present.reshape(1, start_times_present.shape[0]),
               fmt='%4.1f')

    start_times_absent = newdf['end'].values
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

def create_new_annots(fn, part):
    annotation_dir = '../annotations/raw'
    df = pd.read_table(os.path.join(annotation_dir,fn), header=None)
    df = df.dropna(axis=1, how='all')
    df.columns = ['annot', 'start', 'end', 'dur', 'content']
    df = df.round(1)    
    # iterate through all unique annotations
    for ann in pd.unique(df.annot):
        prefix = '_'.join(['part_{}'.format(part)] + [val.lower() for val in ann.split(' ')])
        start_times = df[df.annot == ann].start.values
        durations = df[df.annot == ann].dur.values
        save_mat = []
        for p in zip(start_times, durations):
            save_mat.append('{0}:{1}'.format(p[0], p[1]))
        save_array = np.array(save_mat)
        print "saving {}".format(prefix)
        prefix += '_new.txt'
        #np.savetxt(os.path.join("../outputs", prefix), start_times.reshape(1, start_times.shape[0]), fmt='%4.1f')
        np.savetxt(os.path.join("../outputs", prefix), save_array.reshape(1, save_array.shape[0]), fmt='%s')

