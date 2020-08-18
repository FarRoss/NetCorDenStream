#!/usr/bin/python3
# ------------------------------------------------------------------
# [Author] Rostand
# [ Data ] January, 25th 2020.

# Import libraries
import json
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from utils import *
from matplotlib.patches import Circle

gs1 = gridspec.GridSpec(2, 1, wspace=0.0, hspace=0.2, top=.85, bottom=0.15, left=0.08, right=0.98)

config = json.load(open('config.json'))

SHOW_PLOT_FLAG = False
plot_id = '13'
plot_name = '01_TP_k_delta'

stream_length_1 = [1, 1, 0, 1, 0, 0, 0, 1]
stream_length_2 = [1, 0, 0, 1, 1, 0, 0, 1]

# exec_time_1 = ['t_1', 't_2', 't_3', 't_4', 't_5', 't_6', 't_7']
exec_time_1 = [1, 2, 3, 4, 5, 6, 7, 8]
exec_time_2 = [1, 2, 3, 4, 5, 6, 7, 8]

fig = plt.figure(figsize=(5, 2.5))

labels = [0, 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8']


def plotFunction(time, stream_length, flag):
    ax = plt.subplot(gs1[flag])

    # ax.set_ylabel('Execution Time (in seconds)')

    def circle(x, y, color, radius=0.1):
        circle = Circle((x, y), radius, clip_on=False, zorder=10, linewidth=1,
                        edgecolor=color, linestyle='--', facecolor='none', lw=2,
                        )
        ax.add_artist(circle)

    def text(x, y, text):
        plt.text(x, y, text, ha="center", va="center",
                 fontsize=12, )

    if flag == 0:
        ax.set_xticklabels(labels='')
        ax.set_yticks([-1, 0, 1, 2])
        left, width = -0.035, .5
        bottom, height = 0.27, .5
        right = left + width
        top = bottom + height
        ax.text(left, 0.5 * (bottom + top), '$n_1$ Alarms',
                horizontalalignment='right',
                verticalalignment='center',
                rotation='vertical',
                fontsize=11,
                transform=ax.transAxes)
        plt.text(1, 1, ' ', ha="center", va="center", fontsize=20,
                 bbox=dict(facecolor='none', linestyle='--', edgecolor='red', boxstyle="circle, pad=-0.2",
                           lw=2, pad=0.2))
        plt.text(2, 1, ' ', ha="center", va="center", fontsize=20,
                 bbox=dict(facecolor='none', linestyle='--', edgecolor='purple', boxstyle="circle, pad=-0.2",
                           lw=2, pad=0.2))
        plt.text(4, 1, ' ', ha="center", va="center", fontsize=20,
                 bbox=dict(facecolor='none', linestyle='--', edgecolor='black', boxstyle="circle, pad=-0.2",
                           lw=2, pad=0.2))
        plt.text(4, 1, ' ', ha="center", va="center", fontsize=20,
                 bbox=dict(facecolor='none', linestyle='--', edgecolor='black', boxstyle="circle, pad=-0.2",
                           lw=2, pad=0.2))
        plt.text(4, 1, ' ', ha="center", va="center", fontsize=20,
                 bbox=dict(facecolor='none', linestyle='--', edgecolor='orange', boxstyle="circle, pad=0",
                           lw=2, pad=0.2))
        plt.text(8, 1, ' ', ha="center", va="center", fontsize=20,
                 bbox=dict(facecolor='none', linestyle='--', edgecolor='green', boxstyle="circle, pad=-0.2",
                           lw=2, pad=0.2))
        ax.annotate("",
                    xy=(4.2, 0.9), xycoords='data',
                    xytext=(5.2, 0.6), textcoords='data',
                    arrowprops=dict(arrowstyle="->",
                                    connectionstyle="arc3", ), horizontalalignment='center', verticalalignment='top')
        # plt.text(2.5, 1.25, '$\delta = 4$, $k=1$', fontproperties='monospace',
        #          ha="center", va="center",
        #          fontsize=10, bbox=dict(boxstyle="round,pad=0.2", fc="lime", alpha=.15),)

        circle(3.8, 1.35, 'black')
        circle(4.1, 1.35, 'red')
        circle(4.4, 1.35, 'orange')
        circle(4.7, 1.35, 'green')
        circle(5.0, 1.35, 'purple')

        text(6.2, 1.35, "= $TP_{k\delta}$ Alarms")
        text(2.5, 1.35, ' $ \delta = 4 $, $ k = 1 $, ')
        plt.text(4.5, 1.35, '                                                   '
                            '                   ', ha="center", va="center",
                 fontsize=12, bbox=dict(boxstyle="round,pad=0.2", fc="lime", alpha=.15), )
        plt.text(6.1, 0.5, ' $TP_{k\delta}$ Alarms\n counted \ntwice', ha="center", va="center",
                 fontsize=11, bbox=dict(boxstyle="round,pad=0.1", fc="lime", alpha=.15), )

    if flag == 1:
        ax.set_xticklabels(labels=labels)
        ax.set_yticks([-1, 0, 1, 2])
        left, width = -0.035, .5
        bottom, height = 0.27, .5
        right = left + width
        top = bottom + height
        ax.text(left, 0.5 * (bottom + top), '$n_2$ Alarms',
                horizontalalignment='right',
                verticalalignment='center',
                fontsize=11,
                rotation='vertical',
                transform=ax.transAxes)

        left, width = .36, .5
        bottom, height = -0.46, 0.7
        right = left + width
        top = bottom + height
        ax.text(left, bottom, 'Length of Stream',
                horizontalalignment='left',
                verticalalignment='bottom',
                fontsize=11,
                transform=ax.transAxes)
        plt.text(1, 1, ' ', ha="center", va="center", fontsize=20,
                 bbox=dict(facecolor='none', linestyle='--', edgecolor='black', boxstyle="circle,pad=-0.2", lw=2,
                           pad=0.2))
        plt.text(4, 1, ' ', ha="center", va="center", fontsize=20,
                 bbox=dict(facecolor='none', linestyle='--', edgecolor='red', boxstyle="circle, pad=-0.2", lw=2,
                           pad=0.2))
        plt.text(8, 1, ' ', ha="center", va="center", fontsize=20,
                 bbox=dict(facecolor='none', linestyle='--', edgecolor='orange', boxstyle="circle, pad=-0.2", lw=2,
                           pad=0.2))
        plt.text(4, 1, ' ', ha="center", va="center", fontsize=20,
                 bbox=dict(facecolor='none', linestyle='--', edgecolor='green', boxstyle="circle, pad=0", lw=2,
                           pad=0.2))
        # plt.text(5, 0.2, ' Anomalies counted \ntwice', ha="center", va="center",
        #          bbox=dict(boxstyle="round,pad=0.2", fc="lime", alpha=.15))

        ax.annotate("",
                    xy=(4.2, 1.05), xycoords='data',
                    xytext=(5.2, 1.7), textcoords='data',
                    arrowprops=dict(arrowstyle="->",
                                    connectionstyle="arc3", ), horizontalalignment='center', verticalalignment='top')
    ax.plot(stream_length, time, marker='s', ms=3, linewidth=1, color='blue', alpha=0.6)
    # red_patch = mpatches.Patch(label='$\delta = 4$, $k = 1$')
    # plt.legend(handles=[red_patch])
    ax.figure.legend(bbox_to_anchor=(0.5, 2.5), ncol=2, loc=9, bbox_transform=ax.transAxes)
    return


plotFunction(stream_length_1, exec_time_1, 0)
plotFunction(stream_length_2, exec_time_2, 1)

plotme(plt, plot_id, plot_name, show_flag=SHOW_PLOT_FLAG, png_only=False)
