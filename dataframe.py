import os
import numpy as np
import matplotlib.pyplot as plt

# type DataFrame a = ([String], Map String [a])

FNULL = open(os.devnull, 'w')

class DataFrame(object):

    def __init__(self):
        self._index_to_name = []
        self._name_to_index = {}
        self._data = np.array([[]])

    def read(self, filename, with_header=True):
        data = []
        with open(filename) as f:
            for line in f:
                data.append(line.split())
        if with_header:
            header = data[0]
            data = data[1:]
        else:
            header = list(map(str, range(len(data[0]))))
        data = [list(map(float, row)) for row in data]
        data = np.transpose(np.array(data))
        cols = {name: data[i] for i, name in enumerate(header)}
        self._index_to_name = header
        self._name_to_index = {name: i for i, name in enumerate(header)}
        self._data = data

    def plot(self, x=0, ys=None, y_label=None, title=None, filename=None,
             log_x=False, log_y=False, x_range=None, y_range=None):
        if type(x) != int:
            x = self._name_to_index[x]
        ys = list(ys or range(1, self._data.shape[0]))
        for y in ys:
            if type(y) != int:
                y = self._name_to_index[y]
            plt.plot(self._data[x], self._data[y], label=self._index_to_name[y])
        box = plt.axes().get_position()
        plt.axes().set_position([box.x0, box.y0, box.width * 0.8, box.height])
        plt.axes().set_xlabel(x)
        if y_label is not None:
            plt.axes().set_ylabel(y_label)
        if title is not None:
            plt.axes().set_title(title)
        if log_x:
            plt.axes().set_xscale("log")
        if log_y:
            plt.axes().set_yscale("log")
        plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        if x_range is not None:
            plt.xlim(x_range)
        if y_range is not None:
            plt.ylim(y_range)
        if filename is None:
            plt.show()
        else:
            plt.savefig(filename)
        plt.clf()

    def remap_names(self, mapping):
        self._index_to_name = [mapping[name] for i, name in enumerate(self._index_to_name)]
        self._name_to_index = {mapping[name]: i for name, i in self._name_to_index.items()}
