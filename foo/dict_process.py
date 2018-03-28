# -*- coding: UTF-8 -*-
import re


# load the dictionary, return a dict with words as keys and their frequencies as values
# e.g. {'一个':818357166}
def load_dict(filename='word_dict.txt'):
    with open(filename,'r',encoding='utf-8') as f:
        word_dict = {}
        data = f.readlines()
        for i in data:
            word = re.findall(u'([\u4e00-\u9fa5]+)',i)[0]
            num = int(re.findall('[0-9]+',i)[0])
            word_dict[word] = num
    return word_dict


# add words into dict, input words to be added and word dict, output confirm info and changed dict
# change dict loaded and dict file simultaneously
# format of the input words:
# words only: '一个' (default frequency = 1)  words with frequency: '一个 818357166' or '一个818357166'
def add_words(str,dict,filename='word_dict.txt'):
    word_list = re.findall(r'[\u4e00-\u9fa5]+\s*[0-9]*',str)
    if not word_list:
        confirm_info = 'Please input at least one chinese character.'
        return confirm_info, dict
    add_list = ['The following word(s) have been added into the dict.']
    add_component = '\n'
    for i in word_list:
        temp = re.search('[0-9]+',i)
        num = temp and temp.group(0) or 1
        word = re.findall('[\u4e00-\u9fa5]+',i)[0]
        if word not in dict:
            dict[word] = num
            add_component += '{:<10}{}'.format(word,num) + '\n'
            add_list.append('{:<10}{}'.format(word, num))
        else:
            add_list.append('{:<10}{}'.format(word, num) + '\nThe word "{}" has been in the dict.'.format(word))
    confirm_info = '\n'.join(add_list)
    with open(filename,'a',encoding='utf-8') as f2:
        f2.write(add_component[:-1])
    return confirm_info,dict


# delete words from dict, input words to be deleted and word dict, output confirm info and changed dict
# change dict loaded and dict file simultaneously
# format of the input words:
# '一个 大佬' (words separated by space)
def delete_words(str,dict,filename='word_dict.txt'):
    word_set = set(re.findall(r'[\u4e00-\u9fa5]+',str))
    if not word_set:
        confirm_info = 'Please input at least one chinese character.'
        return confirm_info,dict
    delete_list = ['The following word(s) have been deleted from the dict.']
    with open(filename,'r',encoding='utf-8') as f:
        data = f.readlines()
        for i in word_set:
            in_dict = False
            for j in data:
                if i == j.split()[0]:
                    data.remove(j)
                    del dict[i]
                    delete_list.append(i)
                    in_dict = True
                    break
            if not in_dict:
                delete_list.append('The word {} is not in the dict.'.format(i))
        confirm_info = '\n'.join(delete_list)
    with open(filename,'w',encoding='utf-8') as f:
        temp = ''.join(data)
        data = temp[-1] == '\n' and temp[:-1] or temp
        f.write(data)
    return confirm_info,dict


# revise words in the dict, input origin word in the dict, new word and dict, output confirm info and changed dict
# change dict loaded and dict file simultaneously
def revise_words(origin_word,new_word,dict,filename='word_dict.txt'):
    if origin_word == new_word:
        confirm_info = 'The origin word and the new word are the same word!'
        return confirm_info,dict
    elif re.findall('[\u4e00-\u9fa5]+',new_word) == [] or re.findall('[\u4e00-\u9fa5]+',new_word)[0] != new_word:
        confirm_info = 'Please input new word with only chinese characters.'
        return confirm_info,dict
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.readlines()
        new_data = []
        new_in_dict = False
        ori_in_dict = False
        for i in data:
            if new_word == i.split()[0]:
                new_in_dict = True
                break
        for j in range(len(data)):
            word_in_dict = data[j].split()[0]
            if origin_word == word_in_dict and new_in_dict == False:
                new_data.append(data[j].replace(origin_word,new_word))
                dict[new_word] = dict[origin_word]
                del dict[origin_word]
                ori_in_dict = True
            elif origin_word == word_in_dict and new_in_dict == True:
                del dict[origin_word]
                ori_in_dict = True
            else:
                new_data.append(data[j])
        if not ori_in_dict:
            confirm_info = 'The word you want to edit is not in the dict.'
        else:
            if new_in_dict:
                confirm_info = 'The new word "{}" has been in the dict,so the origin word "{}" is deleted from the dict.'.format(new_word,origin_word)
            else:
                confirm_info = 'The word "{}" has been changed into "{}"'.format(origin_word,new_word)
    with open(filename, 'w', encoding='utf-8') as f:
        temp = ''.join(new_data)
        new_data = temp[-1] == '\n' and temp[:-1] or temp
        f.write(new_data)
    return confirm_info,dict
