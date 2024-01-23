import json
import random
from collections import defaultdict
import time

import numpy as np


def calc_prob(unigram_set, bigram_dicts, trigram_dicts, candidates, prev_word, prev_prev_word):
    """
    The function calculates the best probability for a word from the candidate words
    :param unigram_set: a set with all the lexicon words
    :param bigram_dicts: dictionary of dictionaries with bi-grams
    :param trigram_dicts: same as bigrams but with one more level back
    :param candidates: list of tokenized candidates
    :param prev_word: the previous word
    :param prev_prev_word: the previous word of the previous word
    :return: string: best probability
    """
    bigram_count = bigram_dicts.get(prev_prev_word, {}).get(prev_word, 0)
    vocab_size = len(unigram_set)
    probabilities = []

    for word in candidates:
        trigram_prob = (trigram_dicts.get(prev_prev_word, {}).get(prev_word, {}).get(word, 0) + 1) \
                      / (bigram_count + vocab_size)
        probabilities.append((word, trigram_prob))
    return probabilities


def calc_final_res(prob_matrix):
    res_lst_with_index = []

    while any(value != -1 for row in prob_matrix for _, value in row):
        max_value, max_row, max_col = max(
            (value, i, j) for i, row in enumerate(prob_matrix) for j, (_, value) in enumerate(row) if value != -1)
        # Append tuple[0] to res_lst
        res_lst_with_index.append((prob_matrix[max_row][max_col][0], max_row))
        # Change the indexing of the entire row and column to -1
        for i in range(len(prob_matrix)):
            prob_matrix[i][max_col] = (prob_matrix[i][max_col][0], -1)
        prob_matrix[max_row] = [(item[0], -1) for item in prob_matrix[max_row]]
    # Sort the result list by the row index
    res_lst_with_index.sort(key=lambda x: x[1])
    # Extract only the words from the sorted result list
    res_lst = [item[0] for item in res_lst_with_index]

    return res_lst


def find_missing_words(cloze, candidates, unigram_set, bigram_dicts, trigram_dicts):
    """
    The function finds the missing words in a cloze.
    :param cloze: the text with missing words
    :param candidates: the text with the candidates
    :param unigram_set: a set with all the lexicon words
    :param bigram_dicts: dictionary of dictionaries with bi-grams
    :param trigram_dicts: same as bigrams but with one more level back
    :return: list of missing words by order
    """
    res_lst = []
    with open(cloze, 'r', encoding='utf8') as f1:
        text = f1.read()
    with open(candidates, 'r', encoding='utf8') as f2:
        candidates_text = f2.read()

    prob_matrix, probabilities = [], []
    words = text.split()
    candidates_lst = candidates_text.split()
    random.shuffle(candidates_lst)
    for i in range(len(words)):
        if (i == 0 or i == 1) and words[i] == "__________":
            probabilities = [(word, random.uniform(0, 1)) for word in candidates_lst]
            prob_matrix.append(probabilities)
        elif words[i] == "__________":
            probabilities = calc_prob(unigram_set, bigram_dicts, trigram_dicts
                                      , candidates_lst, words[i-1].lower(), words[i-2].lower())
            prob_matrix.append(probabilities)

    res_lst = calc_final_res(prob_matrix)

    return res_lst


def update_dicts(tokens, prev_word, prev_prev_word, unigram_set, bigram_dicts, trigram_dicts):
    """
    This function updates all the dictionaries
    :param tokens: a tokenized list of a sentence
    :param prev_word: the previous word
    :param prev_prev_word: the previous word of the previous word
    :param unigram_set: a set with all the lexicon words
    :param bigram_dicts: dictionary of dictionaries with bi-grams
    :param trigram_dicts: same as bigrams but with one more level back
    :return: prev_prev_word, prev_word
    """
    for word in tokens:
        if word in unigram_set:
            word = word.lower()
            if prev_word != '':
                bigram_dicts[prev_word][word] = bigram_dicts[prev_word].get(word, 0) + 1
                if prev_prev_word != '':
                    trigram_dicts[prev_prev_word][prev_word][word] = \
                        trigram_dicts[prev_prev_word][prev_word].get(word, 0) + 1
            prev_prev_word = prev_word
            prev_word = word

    return prev_prev_word, prev_word


def initialize_dicts(lexicon, corpus):
    """
    Init function
    :param lexicon: text of the lexicon
    :param corpus: text of the corpus
    :return: set of the lexicon and two dictionaries representing bi-grams and tri-grams.
    """
    unigram_set = set()
    bigram_dicts = defaultdict(dict)
    nested_defaultdict = lambda: defaultdict(lambda: defaultdict(int))
    trigram_dicts = defaultdict(nested_defaultdict)

    with open(lexicon, 'r', encoding='utf8') as f1:
        for word in f1.readlines():  # because every line is a word in lexicon
            unigram_set.add(word.rstrip('\n'))

    with open(corpus, 'r', encoding='utf-8') as f2:
        prev_word = ''
        prev_prev_word = ''
        for i, line in enumerate(f2.readlines()):
            tokens = line.split()
            prev_prev_word, prev_word = \
                update_dicts(tokens, prev_word, prev_prev_word, unigram_set, bigram_dicts, trigram_dicts)
            if i == 8000000:
                break

    return unigram_set, bigram_dicts, trigram_dicts


def solve_cloze(input, candidates, lexicon, corpus):
    """

    :param input: the cloze
    :param candidates: text with candidates
    :param lexicon: text of the lexicon
    :param corpus: text of the corpus
    :return: the list with missing words by order.
    """
    print(f'starting to solve the cloze {input} with {candidates} using {lexicon} and {corpus}')

    unigram_set, bigram_dicts, trigram_dicts = initialize_dicts(lexicon, corpus)
    result_list = find_missing_words(input, candidates, unigram_set, bigram_dicts, trigram_dicts)

    return result_list  # return your solution


def calc_success_percentage(solution_lst, candidates_file):
    """
    The function calculates the success prec
    :param solution_lst: a list with the chosen words
    :param candidates_file: text with candidates
    :return:the success percentage.
    """
    with open(candidates_file, 'r', encoding='utf8') as f:
        candidates_text = f.read()
    candidates_lst = candidates_text.split()
    correct_pred = 0
    for i, j in zip(solution_lst, candidates_lst):
        if i == j:
            correct_pred += 1
    return (correct_pred / len(solution_lst)) * 100


if __name__ == '__main__':
    start_time = time.time()
    with open('config.json', 'r', encoding="utf8") as json_file:
        config = json.load(json_file)

    solution = solve_cloze(config['input_filename'],
                           config['candidates_filename'],
                           config['lexicon_filename'],
                           config['corpus'])

    print('cloze solution:', solution)
    percentage = calc_success_percentage(solution, config['candidates_filename'])
    print(f'success rate:{percentage}%')
    end_time = time.time()
    elapsed_time = (end_time - start_time) / 60
    print('Elapsed time:', elapsed_time, 'minutes')