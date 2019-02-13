import os
import pandas as pd
import numpy as np

annotation_dir = '../annotations/raw'
ra1 = pd.read_csv(os.path.join(annotation_dir, 'ra1_part2.txt'), sep='\t', skiprows=1)
ra1.rename(columns={"Begin Time - ss.msec": "Start", "End Time - ss.msec": "End", "Duration - ss.msec": "Duration",
                    "Face(s) present": "Face Present"}, inplace=True)
df = ra1[["Start", "End", "Face Present"]]
df = df.dropna(subset=["Face Present"])
# for i in range(df.shape[0]):


def round_ms(f):
    decimal = f - np.fix(f)
    val = 0
    if decimal <= 0.5:
        val = 0.5
    else:
        val = 1.0
    return np.fix(f) + val


df["Start"] = df.apply(lambda row: round_ms(row["Start"]), axis=1)
df["End"] = df.apply(lambda row: round_ms(row["End"]), axis=1)
temporal_resolution = 0.5
s = np.array([])
for i in range(5):
    x = np.arange(df.loc[i, 'Start'], df.loc[i, 'End'], temporal_resolution)
    s = np.append(s, x)

# ToDo:
# [] For ra1, remove the rows containing no faces present
# [] Generalize for all rows
#print(s)
print(df.loc[:2])