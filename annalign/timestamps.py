import pandas as pd
import numpy as np
import os
import glob

def make_df(fn, part):
    annotation_dir = '../annotations/raw'
    df = pd.read_table(os.path.join(annotation_dir, fn), header=None)
    df = df.dropna(axis=1, how='all')
    df = df.round(1)
    df.columns = ['dim', 'start', 'end', 'dur', 'content']
    return df


def merge(df, idx):
    start_at = idx
    dur = df.loc[idx, 'dur']
    #while df.loc[idx, 'end'] == df.loc[idx+1, 'start'] and idx < df.shape[0] - 1:
    while idx+1 in df.index and df.loc[idx, 'end'] == df.loc[idx+1, 'start']:
        dur += df.loc[idx, 'dur']
        idx += 1
    end_at = idx
    return start_at, end_at, dur


def get_new_df(df):
    row_num = 0
    new_df = pd.DataFrame(columns=['start', 'end', 'dur'])
    while row_num < df.shape[0] - 1:
        s, e, d = merge(df, row_num)
        row = pd.DataFrame([[df.loc[s, 'start'], df.loc[e, 'end'], d]], columns=['start', 'end', 'dur'])
        new_df = new_df.append(row)
        row_num = e+1
    if row_num == df.shape[0] - 1:
        row = pd.DataFrame([[df.loc[row_num, 'start'], df.loc[row_num, 'end'], df.loc[row_num, 'dur']]], columns=['start', 'end', 'dur'])
        new_df = new_df.append(row)
    new_df.index = np.arange(new_df.shape[0])
    return new_df


def oneDfy(df):
    return ['{0}:{1}'.format(df.loc[i, 'start'], df.loc[i, 'dur']) for i in range(df.shape[0])]


def save_one_d(data, name):
    filename = os.path.join('../outputs', name)
    np.savetxt(filename+'.1D', data.reshape(1, data.shape[0]), fmt='%s')
    

def get_timestamps(fn, part):
    df = make_df(fn, part)
    present_df = get_new_df(df)
    absent_df = pd.DataFrame(columns=present_df.columns)
    for i in range(present_df.shape[0]):
        if i+1 in present_df.index:
            start = present_df.loc[i, 'end']
            dur = present_df.loc[i+1, 'start'] - start
            end = start + dur
            row = pd.DataFrame([[start, end, dur]], columns = absent_df.columns)
            absent_df = absent_df.append(row)
    absent_df.index = np.arange(absent_df.shape[0])
    present_times = np.array(oneDfy(present_df))
    absent_times = np.array(oneDfy(absent_df))

    prefix_present = 'face_present_part{}'.format(part)
    prefix_absent = 'face_absent_part{}'.format(part)

    save_one_d(present_times, prefix_present)
    save_one_d(absent_times, prefix_absent)    
    
    return present_df, absent_df


def run_all_parts():
    parts = range(2, 7)
    for part in parts:
        fn = 'Budapest_pt{0}_face_present.txt'.format(str(part))
        get_timestamps(fn, part)


def concat_parts():
    type_runs = ['face_present', 'face_absent']
    base_path = '../outputs/'
    for type in type_runs:
        all_parts = glob.glob(os.path.join(base_path, type+'*.1D'))
        fn = os.path.join(base_path, type + '.1D')
        with open(fn, 'w') as outfile:
            for fname in all_parts:
                with open(fname, 'r') as infile:
                    outfile.write(infile.read())

def test_concatenation():
    first = np.hstack((np.linspace(0, 10, 5), np.linspace(11, 20, 5)))
    second = np.hstack((np.linspace(first[1], 10+first[1], 5), np.linspace(20, 30, 5)))
    df = pd.DataFrame({'start' : first, 'end' : second})
    df['dur'] = df.end - df.start
    ndf = get_new_df(df)
    assert ndf.shape[0] == 6




