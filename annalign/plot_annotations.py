import numpy as np
import matplotlib.pyplot as plt
import os

def read_data(fn):
    info = []
    with open(fn, 'r') as f:
        info.append(f.read())
    return info[0].split('\n')[0].split(' ')
    

def get_axes(l):
    start_times = [float(val.split(':')[0]) for val in l]
    durations = [float(val.split(':')[1]) for val in l]
    last_tp = start_times[-1] + durations[-1]
    all_timepoints = np.arange(0, last_tp, 0.1)
    on_timepoints = np.array([])
    
    for s, d in zip(start_times, durations):
        on_timepoints = np.hstack((on_timepoints, np.arange(s, s+d, 0.1)))
    
    on_values = np.zeros(all_timepoints.shape[0])

    for idx, tp in enumerate(all_timepoints):
        if np.any(np.isclose(on_timepoints, tp)):
            on_values[idx] = 1
    return on_timepoints, all_timepoints, on_values


def make_run_fig(part):
    present = '../outputs/face_present_part{}.1D'.format(part)
    absent = '../outputs/face_absent_part{}.1D'.format(part)
    present_timestamps = read_data(present)
    absent_timestamps = read_data(absent) 

    _, p_x_data, p_y_data = get_axes(present_timestamps)
    _, a_x_data, a_y_data = get_axes(absent_timestamps)

    fig, axs = plt.subplots(3, 1)
    axs[0].plot(p_x_data, p_y_data, 'r')
    axs[0].set_xlim(0, p_x_data[-1])
    axs[0].set_ylim(0, 1.25)
    axs[0].set_xlabel('Time stamps in the run (s)')
    axs[0].set_ylabel('Face present annotations')
    
    axs[1].plot(a_x_data, a_y_data, 'b')
    axs[1].set_xlim(0, a_x_data[-1])
    axs[1].set_ylim(0, 1.25)
    axs[1].set_xlabel('Time stamps in the run (s)')
    axs[1].set_ylabel('Face absent nnotations')

    axs[2].plot(p_x_data, p_y_data, 'r', a_x_data, a_y_data, 'b')
    axs[2].set_xlim(0, a_x_data[-1])
    axs[2].set_ylim(0, 1.25)
    axs[2].set_xlabel('Time stamps in the run (s)')
    axs[2].set_ylabel('Overlap')
    
    fig.suptitle('Annotations for part {0} of Budapest'.format(part)) 
    fig.set_size_inches(18.5, 10.5, forward=True)
    fig.savefig(os.path.join('../outputs/', 'part{0}_annotations.png'.format(part)))
