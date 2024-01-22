import json
import random
from collections import defaultdict
import time


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

    best_prob = ('', 0)
    for word in candidates:
        trigram_prob = (trigram_dicts.get(prev_prev_word, {}).get(prev_word, {}).get(word, 0) + 1) \
                      / (bigram_count + vocab_size)
        if trigram_prob > best_prob[1]:
            best_prob = (word, trigram_prob)
    return best_prob[0]


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
    list = []
    with open(cloze, 'r', encoding='utf8') as f1:
        text = f1.read()
    with open(candidates, 'r', encoding='utf8') as f2:
        candidates_text = f2.read()

    words = text.split()
    candidates_lst = candidates_text.split()
    random.shuffle(candidates_lst)
    candidate = ''
    for i in range(len(words)):
        if i == 0 and words[i] == "__________":
            candidate = candidates_lst[0]
            list.append(candidate)
        elif words[i] == "__________":
            candidate = calc_prob(unigram_set, bigram_dicts, trigram_dicts
                                  , candidates_lst, words[i-1].lower(), words[i-2].lower())
            list.append(candidate)
        if candidate in candidates_lst:
            candidates_lst.remove(candidate)
    return list


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
            if i % 100000 == 0:
                print(i)
            # if i == 8000000:
            #     break

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
    print(calc_success_percentage(solution, config['candidates_filename']))
    end_time = time.time()
    elapsed_time = (end_time - start_time) / 60
    print('Elapsed time:', elapsed_time, 'minutes')