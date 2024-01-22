import json
import random
from collections import defaultdict
import time


def calc_prob(unigram_set, bigram_dicts, trigram_dicts, candidates, prev_word, prev_prev_word):
    bigram_count = bigram_dicts.get(prev_prev_word, {}).get(prev_word, 0)
    vocab_size = len(unigram_set)

    best_prob = ('', 0)
    for word in candidates:
        trigram_prob = (trigram_dicts.get(prev_prev_word, {}).get(prev_word, {}).get(word, 0) + 1) \
                      / (bigram_count + vocab_size)
        print(f'best prob:{best_prob}, ({word}: {trigram_prob})')
        if trigram_prob > best_prob[1]:
            best_prob = (word, trigram_prob)
    return best_prob[0]


def find_missing_words(cloze, candidates, unigram_set, bigram_dicts, trigram_dicts):
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
            if i == 8000000:
                break

    return unigram_set, bigram_dicts, trigram_dicts


def solve_cloze(input, candidates, lexicon, corpus):
    # todo: implement this function
    print(f'starting to solve the cloze {input} with {candidates} using {lexicon} and {corpus}')

    unigram_set, bigram_dicts, trigram_dicts = initialize_dicts(lexicon, corpus)
    result_list = find_missing_words(input, candidates, unigram_set, bigram_dicts, trigram_dicts)

    return result_list  # return your solution


if __name__ == '__main__':
    start_time = time.time()
    with open('config.json', 'r', encoding="utf8") as json_file:
        config = json.load(json_file)

    solution = solve_cloze(config['input_filename'],
                           config['candidates_filename'],
                           config['lexicon_filename'],
                           config['corpus'])

    print('cloze solution:', solution)
    end_time = time.time()
    elapsed_time = (end_time - start_time) / 60
    print('Elapsed time:', elapsed_time, 'minutes')
