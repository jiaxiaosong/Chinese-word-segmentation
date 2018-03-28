#encoding=utf-8
#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      Administrator
#
# Created:     22/12/2016
# Copyright:   (c) Administrator 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re
#-----------------seg_sentence--------------------------------------------------
def find_sentence(section,punctuation,current_sentence):
    section=section.replace(" ","")
    section=section.replace("\n","")
    section=section.replace("“","")
    section=section.replace("”","")
    list_sec=list(section)
    if list_sec[-1] not in punctuation:
        section+='。'
        return find_sentence(section,punctuation,current_sentence)
    else:
        for i in range(len(list_sec)):
            if list_sec[i] in punctuation:
                for num in range(i+1):
                    current_sentence+=list_sec[num]
                section = ''
                for num in range(i+1,len(list_sec)):
                    section+=list_sec[num]
                break
        return[section,current_sentence]
def seg_sentence(section):
    try:
        punctuation=['，','。','？','?','!','！',',','……','、']
        well_seg=''
        while section!='':
            well_seg+=find_sentence(section,punctuation,'')[1]+'\n'
            section=find_sentence(section,punctuation,'')[0]
        return well_seg
    except:
        return ''


#--------------inverse_seg------------------------------------------------------
def find_word_inverse(sentence,dict_inverse,rest_sentence):
    list_sen=list(sentence)
    len1=len(list_sen)
    if len1>10:
        len1=10
    if len1==1:
        if sentence.isdigit()==True:
            return[sentence,rest_sentence]
        elif ord(sentence)>64 and ord(sentence)<91:
            return[sentence,rest_sentence]
        elif ord(sentence)>96 and ord(sentence)<123:
            return[sentence,rest_sentence]
        else:
            return['|'+sentence+'|',rest_sentence]
    else:
        if sentence in dict_inverse:
            return['|'+sentence+'|',rest_sentence]
        else:
            list_sen1=list_sen[0:len1-1]
            rest_sentence=''.join(list_sen[len1-1:])+rest_sentence
            sentence1=''
            for i in range(len1-1):
                sentence1+=list_sen1[i]
            return find_word_inverse(sentence1,dict_inverse,rest_sentence)
def seg_inverse(sentence,dict_inverse):
    sentence = sentence[::-1]
    well_seg=''
    while sentence!='':
        well_seg+=find_word_inverse(sentence,dict_inverse,'')[0]
        sentence=find_word_inverse(sentence,dict_inverse,'')[1]
    well_seg=re.sub('\|+','|',well_seg)
    return well_seg[::-1]

#---------------forward_seg-----------------------------------------------------
def find_word_forward(sentence,dictionary,rest_sentence):
    list_sen=list(sentence)
    len1=len(list_sen)
    if len1>10:
        len1=10
    if len1==1:
        if sentence.isdigit()==True:
            return[sentence,rest_sentence]
        elif ord(sentence)>64 and ord(sentence)<91:
            return[sentence,rest_sentence]
        elif ord(sentence)>96 and ord(sentence)<123:
            return[sentence,rest_sentence]
        else:
            return['|'+sentence+'|',rest_sentence]
    else:
        if sentence in dictionary:
            return[sentence+'|',rest_sentence]
        else:
            list_sen1=list_sen[0:len1-1]
            rest_sentence=''.join(list_sen[len1-1:])+rest_sentence
            sentence1=''
            for i in range(len1-1):
                sentence1+=list_sen1[i]
            return find_word_forward(sentence1,dictionary,rest_sentence)
def seg_forward(sentence,dictionary):
    well_seg=''
    while sentence!='':
        well_seg+=find_word_forward(sentence,dictionary,'')[0]
        sentence=find_word_forward(sentence,dictionary,'')[1]
    well_seg=re.sub('\|+','|',well_seg)
    return well_seg

