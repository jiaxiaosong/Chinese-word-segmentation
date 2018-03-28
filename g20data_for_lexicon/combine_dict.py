# -*- coding: UTF-8 -*-
import re


def load_dict(title):
    with open('{}.txt'.format(title), 'r', encoding='utf-8') as f:
        word_dict = {}
        data = f.readlines()
        for i in data:
            word = re.findall(u'([\u4e00-\u9fa5]+)',i)[0]
            num = int(re.findall('[0-9]+',i)[0])
            word_dict[word] = num
    return word_dict


def combine(original_name,new_name,app_name):
    original_dict,new_dict,app_dict = load_dict(original_name), load_dict(new_name), load_dict(app_name)
    add_list = []
    add_set = set()
    diff_set = set()
    for i in new_dict:
        if i in app_dict:
            add_set |= {i}
        else:
            diff_set |= {i}
    for j in app_dict:
        if j not in new_dict:
            diff_set |= {j}
    for k in diff_set:
        if k not in original_dict:
            add_set |= {k}
    for t in add_set:
        if t in new_dict:
            add_list.append('{:<10}{}'.format(t,new_dict[t]))
        else:
            add_list.append('{:<10}{}'.format(t, app_dict[t]))
    add_list = sorted(add_list,key=lambda i:int(re.findall('[0-9]+',i)[0]),reverse=1)
    with open('{}.txt'.format(app_name),'w',encoding='utf-8') as f:
        f.write('\n'.join(add_list))

combine('test1','test2','test3')