# -*- coding: utf-8 -*-
import collections
import math
import os


def fetch_quantifier_noun(data_path):
    '''
    从语料中获取量名搭配词对
    fetch quantifier noun from corpus
    :param data_path:
    :return:
    '''
    noun_list = ['n', 'ns', 'nr', 'nt', 'nz', 'vn']
    punctuation_pattern = list('，？！。：；')

    for root, dirs, files in os.walk(data_path):
        for file in files:
            with open(os.path.join(root, file), 'r', encoding='utf-8') as file_read:
                for line in file_read:
                    line = line.strip()
                    cut_tokens = line.split()
                    sents = []
                    sent = []
                    for token in cut_tokens:
                        # word, pos = token.split('/')
                        word = token.split('/')[0]
                        pos = token.split('/')[1]
                        if word not in punctuation_pattern:
                            sent.append(token)
                        else:
                            sents.append(sent)
                            sent = []
                    sents.append(sent)
                    for sent in sents:
                        words_list = [word.split('/')[0] for word in sent]
                        pos_list = [word.split('/')[1] for word in sent]
                        index = 0
                        while index < len(words_list):
                            word = words_list[index]
                            pos = pos_list[index]
                            if (pos == 'q') and ((index + 1) < len(words_list)):
                                right_word = words_list[index + 1]
                                right_pos = pos_list[index + 1]
                                if right_pos != 'c' or right_word != '、':
                                    if '的' in words_list[index:]:
                                        if right_pos in ['d', 'v', 'p', 'c', 'm', 'a']:
                                            de_index = words_list[index + 1:].index('的')
                                            de_index += (index + 1)
                                            pos_index = de_index + 1
                                            while pos_index < len(pos_list):
                                                q_right_pos = pos_list[pos_index]
                                                if q_right_pos in noun_list:
                                                    right_pos = q_right_pos
                                                    right_word = words_list[pos_index]
                                                    pos_index += 1
                                                else:
                                                    break
                                            if right_pos in noun_list:
                                                write_to_file(word,right_word)
                                                print('{}:{}'.format(word, right_word))
                                        else:
                                            pos_index = index + 1
                                            while pos_index < len(pos_list):
                                                q_right_pos = pos_list[pos_index]
                                                if q_right_pos in noun_list:
                                                    right_pos = q_right_pos
                                                    right_word = words_list[pos_index]
                                                    pos_index += 1
                                                else:
                                                    break
                                            if right_pos in noun_list:
                                                write_to_file(word,right_word)
                                                print('{}:{}'.format(word, right_word))
                                    elif (right_pos not in ['p', 'd', 'v', 'm']) and (right_word != '地'):
                                        pos_index = index + 1
                                        while pos_index < len(pos_list):
                                            q_right_pos = pos_list[pos_index]
                                            if q_right_pos in noun_list:
                                                right_pos = q_right_pos
                                                right_word = words_list[pos_index]
                                                pos_index += 1
                                            else:
                                                break
                                        if right_pos in noun_list:
                                            write_to_file(word,right_word)
                                            print('{}:{}'.format(word, right_word))
                            index += 1

def write_to_file(word,right_word):
    f = open('corpus.txt','a',encoding='utf-8')
    f.write('{}:{}\n'.format(word, right_word))
    f.close()

if __name__ == '__main__':
    fetch_quantifier_noun(os.path.join(os.getcwd(), '199801'))