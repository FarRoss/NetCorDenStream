#!/usr/bin/python3
# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] January, 25th 2020.

# Import libraries
import json
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from utils import *

gs1 = gridspec.GridSpec(2, 1, wspace=0.0, hspace=0.32, top=.95, bottom=0.16, left=0.1, right=0.97)

config = json.load(open('config.json'))

SHOW_PLOT_FLAG = True
plot_id = '13'
plot_name = '01_Exec_Time_Bravo'

stream_length_1 = [50e3, 100000, 150000, 200000, 250000]
stream_length_2 = [700000, 900000, 1100000, 1300000, 1500000]

exec_time_1 = [1.0961229801177979, 2.040371894836426, 3.1530189514160156, 3.3261799812316895, 5.050731182098389]

exec = [0.7051229476928711, 1.5547709465026855, 2.372032880783081, 3.2650840282440186, 4.061100006103516]
exec_time_2 = [13.166262149810791, 16.943597078323364, 20.465559005737305, 25.29185676574707, 32.274441957473755]

fig = plt.figure(figsize=(5, 2.5))


def plotFunction(time, stream_length, flag):
    ax = plt.subplot(gs1[flag])

    ax.set_xticks(stream_length)

    # ax.set_ylabel('Execution Time (in seconds)')
    if flag == 0:
        ax.set_yticks([i for i in range(6)])
        left, width = -0.07, .5
        bottom, height = -0.42, .5
        right = left + width
        top = bottom + height
        ax.text(left, 0.5 * (bottom + top), 'Execution Time (in seconds)',
                horizontalalignment='right',
                verticalalignment='center',
                rotation='vertical',
                transform=ax.transAxes)
    if flag == 1:
        ax.set_yticks([t for t in range(0, 36, 5)])
        left, width = .36, .5
        bottom, height = -0.46, .6
        right = left + width
        top = bottom + height
        ax.text(left, bottom, 'Length of Stream',
                horizontalalignment='left',
                verticalalignment='bottom',
                transform=ax.transAxes)
    ax.plot(stream_length, time, marker='s', linewidth=1, color='blue', alpha=0.6,
            label='MDT Data counter' if flag == 1 else '')
    return


plotFunction(exec_time_1, stream_length_1, 0)
plotFunction(exec_time_2, stream_length_2, 1)

plotme(plt, plot_id, plot_name, show_flag=SHOW_PLOT_FLAG, png_only=False)
