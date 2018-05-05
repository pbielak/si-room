"""
Draw plot of aggregated summary files
"""
from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt
import numpy as np


def get_all_files(parent_dir):
    files = [join(parent_dir, f) for f in listdir(parent_dir) if isfile(join(parent_dir, f))]
    return files


def get_summaries_from_file(filepath):
    with open(filepath, 'r') as in_file:
        avg = list(map(lambda x: float(x), in_file.readline().split(' ')))
        best = list(map(lambda x: float(x), in_file.readline().split(' ')))

    return np.array(avg), np.array(best)


def main():
    files = get_all_files('out_files')

    total_avg = np.array([])
    total_best = np.array([])

    for f in files:
        avg, best = get_summaries_from_file(f)

        if len(total_avg) == 0:
            total_avg = avg
        else:
            total_avg += avg

        if len(total_best) == 0:
            total_best = best
        else:
            total_best += best

    total_avg = total_avg / len(files)
    total_best = total_best / len(files)

    xs = np.arange(0, len(total_avg))

    plt.figure()
    plt.title('Aggregated summary from %d runs' % len(files))
    plt.plot(xs, total_avg,
             color='g',
             label='Avg')
    plt.plot(xs, total_best,
             color='r',
             linestyle='--',
             label='Best')

    plt.xlabel('Iteration')
    plt.ylabel('Fitness')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
