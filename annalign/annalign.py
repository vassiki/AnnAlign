import numpy as np
import pandas as pd


def downsample(f, temporal_resolution):
    """
    Function to make a float adhere to the distribution
    specified by the temporal resolution

    Parameters
    ----------
    f : float to downsample
    temporal_resolution : step for the distribution

    Returns
    -------
    downsampled float
    """
    window = np.arange(f - np.mod(f, temporal_resolution), f + 2 * temporal_resolution, temporal_resolution)
    diff = np.abs(window - f)
    return window[np.argmin(diff)]


def annotation_timestamps(start_times, end_times, dim, temporal_resolution):
    """
    Function to create intervals for the annotation timestamps

    Parameters
    ----------
    start_times : annotation start times
    end_times : annotation end times
    dim: dimension, or column of interest
    temporal_resolution: steps of the intervals

    Returns
    -------
    timestamps : np array with all time stamps that have annotations
        for the desired dimension
    """
    df = pd.DataFrame({"Start": start_times, "End": end_times})

    df["Start"] = df.apply(lambda row: downsample(row["Start"], temporal_resolution), axis=1)
    df["End"] = df.apply(lambda row: downsample(row["End"], temporal_resolution), axis=1)

    annots = np.array([])
    for i in df.index:
        annot_window = np.arange(df.loc[i, 'Start'], df.loc[i, 'End'], temporal_resolution)
        annots = np.append(annots, annot_window)

    red_annots = np.unique(annots)
    min_ts, max_ts = 0, np.max(df['End'])
    ts = np.arange(min_ts, max_ts, temporal_resolution)
    timestamps = np.zeros(len(ts))
    for idx, val in enumerate(ts):
        if val in red_annots:
            timestamps[idx] = 1

    return timestamps, ts




