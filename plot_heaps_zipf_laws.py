import json
import random
from collections import defaultdict

import nltk
from nltk import word_tokenize, ngrams


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
    words = word_tokenize(text)
    for i in range(len(words) - 2):
        if words[i] == "__________" and words[i + 2] == "__________":
            key = (words[i - 1], words[i])
            if key in trigram_model:
                words[i] = random.choice(trigram_model[key])
    return " ".join(words)


def solve_cloze(input, candidates, lexicon, corpus):
    # todo: implement this function
    print(f'starting to solve the cloze {input} with {candidates} using {lexicon} and {corpus}')

    with open(corpus, 'r', encoding='utf-8') as f1:
        wiki = f1.read()
    with open(input, 'r', encoding='utf-8') as f2:
        text = f2.read()

    # trigram = create_trigram(text)

    tokens = word_tokenize(wiki) #need to seperate wiki's lines
    trigrams = list(ngrams(tokens, 3))
    trigram_model = defaultdict(list)

    for a_trigram in trigrams:
        trigram_model[(a_trigram[0], a_trigram[1])].append(a_trigram[2])

    result_list = fill_missing_words(text, trigram_model)

    return result_list  # return your solution


if __name__ == '__main__':
    with open('config.json', 'r', encoding="utf8") as json_file:
        config = json.load(json_file)

    solution = solve_cloze(config['input_filename'],
                           config['candidates_filename'],
                           config['lexicon_filename'],
                           config['corpus'])

    print('cloze solution:', solution)
