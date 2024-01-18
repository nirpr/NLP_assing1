import json
import random
from collections import defaultdict

import nltk
nltk.download('punkt')

# def create_trigram(text):
#     trigram = {}
#     words = text.split()
#
#     for i in range(len(words) - 2):
#         key = (words[i], words[i + 1])
#         value = words[i + 2]
#
#         if key in trigram:
#             trigram[key].append(value)
#         else:
#             trigram[key] = [value]
#
#     return trigram

def fill_missing_words(text, trigram_model):
    list = []
    words = nltk.word_tokenize(text)
    for i in range(len(words) - 2):
        if words[i] == "__________" and words[i + 2] == "__________":
            key = (words[i - 1], words[i])
            if key in trigram_model:
                words[i] = random.choice(trigram_model[key])
    return " ".join(words)


def update_dicts(tokens, prev_word, lex_dict, bigram_dicts):
    for word in tokens:
        word = word.lower()
        lex_dict[word] = lex_dict.get(word, 0) + 1
        if prev_word != '':
            if bigram_dicts[prev_word] not in bigram_dicts.keys():
                bigram_dicts[prev_word] = {word: 1}
            else:
                bigram_dicts[prev_word][word] = bigram_dicts[prev_word].get(word, 0) + 1
        prev_word = word

    return prev_word


def initialize_dicts(lexicon, corpus):
    lexicon_dict = {}
    bigram_dicts = {}

    with open(lexicon, 'r', encoding='utf8') as f1:
        for word in f1.readlines():  # because every line is a word in lexicon
            lexicon_dict[word.rstrip('\n')] = 0

    with open(corpus, 'r', encoding='utf-8') as f2:
        prev_word = ''
        for i, line in enumerate(f2.readlines()):
            tokens = nltk.word_tokenize(line)
            prev_word = update_dicts(tokens, prev_word, lexicon_dict, bigram_dicts)

            if i % 100000 == 0:
                print(i)
    return lexicon_dict, bigram_dicts


def solve_cloze(input, candidates, lexicon, corpus):
    # todo: implement this function
    print(f'starting to solve the cloze {input} with {candidates} using {lexicon} and {corpus}')
    lex_dict, bigram_dicts = initialize_dicts(lexicon, corpus)


    return result_list  # return your solution


if __name__ == '__main__':
    with open('config.json', 'r', encoding="utf8") as json_file:
        config = json.load(json_file)

    solution = solve_cloze(config['input_filename'],
                           config['candidates_filename'],
                           config['lexicon_filename'],
                           config['corpus'])

    print('cloze solution:', solution)
