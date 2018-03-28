# -*- coding: UTF-8 -*-
import math


# get info of any possible words from an article string, including suffixes, frequency
# load info into a dict with format like:
# {'追求':[21, ['经', 14], ['的', 3], ['包', 1], ['质', 3]]}
def get_word_dict(article, max_len, dict):
    length = len(article)
    for i in range(length):
        for j in range(i + 1, min(i + max_len + 1, length + 1)):
            word = article[i:j]
            suffix = article[j:j + 1]
            if word in dict:
                dict[word][0] += 1
                has_suffix = False
                for k in dict[word][1:]:
                    if suffix == k[0]:
                        k[1] += 1
                        has_suffix = True
                        break
                if not has_suffix:
                    dict[word].append([suffix, 1])
            else:
                dict[word] = [1, [suffix, 1]]
    return dict


def col_word_dict(sentence_list, max_len):
    global dict1, dict2, dict3, length
    dict1, dict2, dict3, length = {}, {}, {}, 0
    for sentence in sentence_list:
        dict1 = get_word_dict(sentence, max_len, dict1)
        rev_sentence = sentence[::-1]
        dict2 = get_word_dict(rev_sentence, max_len, dict2)
        length += len(sentence)
    for word in dict2:
        dict3[word[::-1]] = dict2[word]
    return dict1, dict3


# calculate the possibility of a string to be a word by mutual information
# I(A,B) = log(P(A,B)/(P(A)*P(B)))
def cohesion(word):
    global length, dict1
    cohesion_list = []
    if len(word) == 1:
        return 100
    else:
        for i in range(1, len(word)):
            word1 = word[:i]
            word2 = word[i:]
            cohesion = (dict1[word][0] * length) / (dict1[word1][0] * dict1[word2][0])
            cohesion_list.append(cohesion)
        cohesion = min(cohesion_list)
        return cohesion


# calculate the possibility of a string to be a word by entropy of its prefixes and suffixes
# H(x) = -∑P(xi)log(2,P(xi))
# considering the small corpus, add the contribution of word being beginning or end of a sentence as an extra parameter
def flex(word):
    global dict1, dict3
    left_flex = 0
    sum = dict1[word][0]
    right_bound = 0
    left_bound = 0
    for i in dict3[word][1:]:
        freq = i[1] / sum
        left_flex -= freq * math.log(freq)
        if i[0] == '':
            left_bound += i[1]
    right_flex = 0
    for i in dict1[word][1:]:
        freq = i[1] / sum
        right_flex -= freq * math.log(freq)
        if i[0] == '':
            right_bound += i[1]
    flex = min([right_flex, left_flex])
    temp = 0
    if right_bound != 0 and left_bound != 0:
        temp = 0.2 * min((right_bound + left_bound), 10)
    elif right_bound != 0:
        if left_flex != 0:
            temp = 0.1 * min(right_bound, 5)
    elif left_bound != 0:
        if right_flex != 0:
            temp = 0.1 * min(left_bound, 5)
    flex += temp
    return flex
