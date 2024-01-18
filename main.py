import json
import random
from collections import defaultdict
import time



def calc_bigram_prob(bigram_dicts, lex_dict, candidates, prev_word):
    unigram_count = lex_dict[prev_word]
    best_prob = ('', 0)

    for word in candidates:
        bigram_prob = bigram_dicts[prev_word][word] / unigram_count # problem here: /
        # bigram_prob = bigram_dicts[prev_word].get(word, 0) / unigram_countAttributeError: /
        # 'int' object has no attribute 'get'
        if bigram_prob > best_prob[1]:
            best_prob = (word, bigram_prob)

    return best_prob[0]


def find_missing_words(cloze, candidates, bigram_dicts, lex_dict):
    list = []
    with open(cloze, 'r', encoding='utf8') as f1:
        text = f1.read()
    with open(candidates, 'r', encoding='utf8') as f2:
        candidates_text = f2.read()

    words = text.split()
    candidates_lst = candidates_text.split()  # new change
    candidate = ''
    for i in range(len(words)):
        if i == 0 and words[i] == "__________":
            candidate = max(lex_dict)
        elif words[i] == "__________":
            candidate = calc_bigram_prob(bigram_dicts, lex_dict, candidates_lst, words[i-1])
    list.append(candidate)
    candidates_lst.remove(candidate)
    return list


def update_dicts(tokens, prev_word, lex_dict, bigram_dicts):
    # for word in tokens:
    #     word = word.lower()
    #     lex_dict[word] = lex_dict.get(word, 0) + 1
    #     if prev_word != '':
    #         if prev_word not in bigram_dicts:
    #             bigram_dicts[prev_word] = {word: 1}
    #         else:
    #             bigram_dicts[prev_word][word] = bigram_dicts[prev_word].get(word, 0) + 1
    #     prev_word = word

    for word in tokens: # new change
        word = word.lower()
        lex_dict[word] = lex_dict.get(word, 0) + 1
        bigram_dicts[prev_word][word] = bigram_dicts[prev_word].get(word, 0) + 1
        prev_word = word

    return prev_word


def initialize_dicts(lexicon, corpus):
    lexicon_dict = {}
    bigram_dicts = defaultdict(dict) # new change

    with open(lexicon, 'r', encoding='utf8') as f1:
        for word in f1.readlines():  # because every line is a word in lexicon
            lexicon_dict[word.rstrip('\n')] = 0

    with open(corpus, 'r', encoding='utf-8') as f2:
        prev_word = ''
        for i, line in enumerate(f2.readlines()):
            tokens = line.split()  # change
            prev_word = update_dicts(tokens, prev_word, lexicon_dict, bigram_dicts)
            if i % 100000 == 0:
                print(i)
    return lexicon_dict, bigram_dicts


def solve_cloze(input, candidates, lexicon, corpus):
    # todo: implement this function
    print(f'starting to solve the cloze {input} with {candidates} using {lexicon} and {corpus}')
    lex_dict, bigram_dicts = initialize_dicts(lexicon, corpus)
    result_list = find_missing_words(input, candidates, bigram_dicts, lex_dict)

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