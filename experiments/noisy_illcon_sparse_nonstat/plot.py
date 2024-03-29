import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import numpy as np
import seaborn as sns
import os

sns.set()
sns.set_style("whitegrid", {'grid.linestyle': '--'})

plt.rc('font', family='serif')
plt.rc('text', usetex=True)

SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=6) #SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=6) #SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

def make_subplots(rows=4, cols=5):
    ax1 = plt.subplot(rows, cols, 1)
    ax2 = plt.subplot(rows, cols, 2)

    axes = [ax1, ax2]
    # axes = [(ax1, (0,0), 1, False), (ax2, (0, 1), 2, True)]

    i = 0
    for r in range(rows):
        for c in range(cols):
            i += 1
            if r == 0 and c == 0:
                continue
            if r == 0 and c == 1:
                continue

            share = False #[r, c] not in [[0,0], [2,0]] and c != 0
            print ("Share: ", r, c, share)
            if share:
                ax = plt.subplot(rows, cols, i, sharex=ax2)
            else:
                ax = plt.subplot(rows, cols, i)

            axes.append(ax) #(ax, (r, c), i, share))

    return axes




def plot(tag='quadratic', bs=10, subtag='test', file='data', seed=0):
    try:
        os.makedirs("results/"+str(tag)+"/plots/" + subtag)
    except:
        pass

    nonstat = 'true'
    iters = 100

    axes = make_subplots(4, 5)

    print (axes)
    axes_shaped = []
    axes_shaped.append(axes[0:5])
    axes_shaped.append(axes[5:10])
    axes_shaped.append(axes[10:15])
    axes_shaped.append(axes[15:20])
    axes = axes_shaped
    # print (axes)
    # input("")
    # f, axes = plt.subplots(4, 5, sharex=True) #, sharey='row')

    axes[1][0].axis('off')
    axes[3][0].axis('off')

    # axes[0,0].get_shared_x_axes().remove(axes[0,0])
    # axes[2,0].get_shared_x_axes().remove(axes[2,0])

    # for r in range(4):
    #     for c in range(5):
    #         # if [r,c] not in [[0,0], [2,0]]:
    #         axes[r,c].get_shared_x_axes().remove(axes[2,0])
    #         axes[r,c].get_shared_x_axes().remove(axes[0,0])
    #
    #         axes[0,0].get_shared_x_axes().remove(axes[r,c])
    #         axes[2,0].get_shared_x_axes().remove(axes[r,c])

    eigs_cond1 = np.load("results/quadratic/eigs_cond_1.0.npy")
    axes[0][0].hist(eigs_cond1, bins=10, density=True)
    axes[0][0].set_xticks(np.arange(0.1, 1.2, 0.2))

    eigs_cond100 = np.load("results/quadratic/eigs_cond_100.0.npy")
    axes[2][0].hist(eigs_cond100, bins=10, density=True)
    axes[2][0].set_xticks(np.arange(0, 101, 20))

    noise = [(0.0, 0.0), (0.0, 0.1), (0.4, 0.0), (0.4, 0.1)]

    lines = []

    axes[0][0].set_title("Eigenvalue distribution")
    axes[0][1].set_title("Noise 0.0, Sparsity 0.0")
    axes[0][2].set_title("Noise 0.0, Sparsity 0.1")
    axes[0][3].set_title("Noise 0.4, Sparsity 0.0")
    axes[0][4].set_title("Noise 0.4, Sparsity 0.1")

    axes[3][1].set_xlabel("Steps")
    axes[3][2].set_xlabel("Steps")
    axes[3][3].set_xlabel("Steps")
    axes[3][4].set_xlabel("Steps")

    i = 1
    for n, s in noise:
        fname = "results/"+str(tag)+"/batch_size_"+str(bs)+"/iters_"+str(iters)+"/dimension_100/condition_1.0/noise_"+str(n)+"/grad_sparsity_"+str(s)+"/rotate_false/adaptive_false/"+str(seed)+"/data.npy"
        newton = np.load(fname)[:,1]

        fname = "results/"+str(tag)+"/batch_size_"+str(bs)+"/iters_"+str(iters)+"/dimension_100/condition_1.0/noise_"+str(n)+"/grad_sparsity_"+str(s)+"/rotate_false/adaptive_true/"+str(seed)+"/data.npy"
        newton_adap = np.load(fname)[:,1]

        ax = axes[0][i]

        ax.semilogy(newton, color='#2F4F4F', ls='dashed', label='Newton', zorder=1000)
        ax.semilogy(newton_adap, color='xkcd:fuchsia', label='AdaCurv\nNewton')
        ax.tick_params(axis='x', colors='white')
        ax.set_xlim((0, 100))

        if i == 4:
            ax.yaxis.set_label_position("right")
            ax.set_ylabel("Aligned", rotation=270, labelpad=10)

        i+= 1
        if i == 0:
            lines.extend([l1, l2])


    i = 1
    for n, s in noise:
        fname = "results/"+str(tag)+"/batch_size_"+str(bs)+"/iters_"+str(iters)+"/dimension_100/condition_1.0/noise_"+str(n)+"/grad_sparsity_"+str(s)+"/rotate_true/adaptive_false/"+str(seed)+"/data.npy"
        newton = np.load(fname)[:,1]

        fname = "results/"+str(tag)+"/batch_size_"+str(bs)+"/iters_"+str(iters)+"/dimension_100/condition_1.0/noise_"+str(n)+"/grad_sparsity_"+str(s)+"/rotate_true/adaptive_true/"+str(seed)+"/data.npy"
        newton_adap = np.load(fname)[:,1]

        ax = axes[1][i]
        ax.semilogy(newton, color='#2F4F4F', ls='dashed', zorder=1000)
        ax.semilogy(newton_adap, color='xkcd:fuchsia')
        ax.tick_params(axis='x', colors='white')
        ax.set_xlim((0, 100))

        if i == 4:
            ax.yaxis.set_label_position("right")
            ax.set_ylabel("Rotated", rotation=270, labelpad=10)

        i += 1

    i = 1
    for n, s in noise:
        fname = "results/"+str(tag)+"/batch_size_"+str(bs)+"/iters_"+str(iters)+"/dimension_100/condition_100.0/noise_"+str(n)+"/grad_sparsity_"+str(s)+"/rotate_false/adaptive_false/"+str(seed)+"/data.npy"
        newton = np.load(fname)[:,1]

        fname = "results/"+str(tag)+"/batch_size_"+str(bs)+"/iters_"+str(iters)+"/dimension_100/condition_100.0/noise_"+str(n)+"/grad_sparsity_"+str(s)+"/rotate_false/adaptive_true/"+str(seed)+"/data.npy"
        newton_adap = np.load(fname)[:,1]

        ax = axes[2][i]

        ax.semilogy(newton, color='#2F4F4F', ls='dashed', zorder=1000)
        ax.semilogy(newton_adap, color='xkcd:fuchsia')
        ax.tick_params(axis='x', colors='white')
        ax.set_xlim((0, 100))

        if i == 4:
            ax.yaxis.set_label_position("right")
            ax.set_ylabel("Aligned", rotation=270, labelpad=10)

        i+= 1


    i = 1
    for n, s in noise:
        fname = "results/"+str(tag)+"/batch_size_"+str(bs)+"/iters_"+str(iters)+"/dimension_100/condition_100.0/noise_"+str(n)+"/grad_sparsity_"+str(s)+"/rotate_true/adaptive_false/"+str(seed)+"/data.npy"
        newton = np.load(fname)[:,1]

        fname = "results/"+str(tag)+"/batch_size_"+str(bs)+"/iters_"+str(iters)+"/dimension_100/condition_100.0/noise_"+str(n)+"/grad_sparsity_"+str(s)+"/rotate_true/adaptive_true/"+str(seed)+"/data.npy"
        newton_adap = np.load(fname)[:,1]

        ax = axes[3][i]
        ax.semilogy(newton, color='#2F4F4F', ls='dashed', zorder=1000)
        ax.semilogy(newton_adap, color='xkcd:fuchsia')
        ax.set_xlim((0, 100))
        # ax.set_xticks([0, 50, 100, 150, 200, 250, 300]) #, 350, 400, 450, 500])

        if i == 4:
            ax.yaxis.set_label_position("right")
            ax.set_ylabel("Rotated", rotation=270, labelpad=10)

        i += 1


    sns.despine()

    handles, labels = axes[0][1].get_legend_handles_labels()
    # plt.gcf().legend(handles, labels, bbox_to_anchor=(1.0, 0.0), loc="lower left", borderaxespad=0)
    f = plt.gcf()
    f.legend(handles, labels, loc="lower left", bbox_to_anchor=(0.07, 0.13), borderaxespad=0)
    # plt.show()

    f.subplots_adjust(hspace=0.1, wspace=0.4)

    f.set_figwidth(10)
    f.set_figheight(5)


# f, axes = plt.subplots(1, 4, sharey=True)
# tag='quadratic_exactstep'
# tag='quadratic_nonstat'
# tag='quadratic_comp'
tag='quadratic'

subtag='test'

# for b, ax in zip(batch_sizes, axes):
plot(tag=tag, bs=10, subtag='test', seed=0) #, fig_ax=(f, ax))

# Legends: https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot/27355247#27355247


# plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
#           ncol=3, fancybox=True, shadow=True)
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig("results/"+str(tag)+"/plots/"+ subtag +"/full.pdf", bbox_inches='tight')
