import json
import pickle
import os.path
from collections import defaultdict
from matplotlib import pyplot as plt
from math import log
import seaborn as sn
sn.set()


def read_data(filename):
    word2freq = defaultdict(int)

    with open(filename, 'r', encoding='utf8') as fin:
        print('reading the text file...')
        for i, line in enumerate(fin.readlines()):
            for word in line.split():
                word2freq[word] += 1
            if i % 100000 == 0:
                print(i)

    total_words = sum(word2freq.values())
    word2nfreq = {w: word2freq[w]/total_words for w in word2freq}

    return word2nfreq


def plot_zipf_law(word2nfreq):
    y = sorted(word2nfreq.values(), reverse=True)
    x = list(range(1, len(y)+1))

    product = [a * b for a, b in zip(x, y)]
    print(product[:1000])  # todo: print and note the roughly constant value

    y = [log(e, 2) for e in y]
    x = [log(e, 2) for e in x]

    plt.plot(x, y)
    plt.xlabel('log(rank)')
    plt.ylabel('log(frequency)')
    plt.title("Zipf's law")
    plt.show()

# def read_data_for_heap(filename):
#     vocabulary = defaultdict(int)
#     num_of_tokens = 0
#
#     with open(filename, 'r', encoding='utf8') as fin:
#         print('reading the text file...')
#         for i, line in enumerate(fin.readlines()):
#             for word in line.split():
#                 vocabulary[word] += 1
#                 num_of_tokens += 1
#             if i % 100000 == 0:
#                 print(i)
#     data = (vocabulary, num_of_tokens)
#     print("finished")
#     return data
#
#
# def plot_heaps_law(data):
#     vocabulary_size = len(data[0])
#     num_of_tokens = data[1]
#     step = max(1, vocabulary_size // 1000)
#     y = list(range(1, vocabulary_size + 1, step))
#     x = list(range(1, num_of_tokens + 1, step))
#
#     plt.plot(x, y)
#     plt.xlabel('N')
#     plt.ylabel('V')
#     plt.title("heaps's law")
#     plt.show()


def read_data_for_heap(filename):
    types = set()
    tokens_processed = []
    vocabulary_sizes = []

    with open(filename, 'r', encoding='utf8') as fin:
        print('reading the text file...')
        for i, line in enumerate(fin.readlines()):
            for word in line.split():
                types.add(word)
                tokens_processed.append(i + 1)
                vocabulary_sizes.append(len(types))
            if i % 100000 == 0:
                print(i)

    step = 10000
    vocabulary_sizes = vocabulary_sizes[::step]
    tokens_processed = tokens_processed[::step]
    data = (tokens_processed, vocabulary_sizes)
    return data


def plot_heaps_law(data):
    x = data[0]
    y = data[1]

    print('2')
    # step = 10000
    # y = vocabulary_sizes[::step]
    # x = tokens_processed[::step]
    print('3')
    plt.plot(x, y)
    plt.xlabel('Number of Tokens Processed')
    plt.ylabel('Vocabulary Size (Number of Types)')
    plt.title("Heap's Law")
    plt.show()


if __name__ == '__main__':
    with open('config.json', 'r', encoding='utf8') as json_file:
        config = json.load(json_file)

    if not os.path.isfile('heap2.pkl'):
        data = read_data_for_heap(config['corpus'])
        pickle.dump(data, open('heap2.pkl', 'wb'))
    print('1')
    plot_heaps_law(pickle.load(open('heap2.pkl', 'rb')))

