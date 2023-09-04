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

class QuantifierNounMI:
    def __init__(self, filepath, mipath):
        self.filepath = filepath
        self.mipath = mipath

    def build_corpus(self):
        '''
        读取语料
        :return:
        '''
        def cut_words(line):
            return [word for word in line.strip().split(':')]
        with open(self.filepath, 'r', encoding='utf-8') as f_read:
            sentences = [cut_words(line) for line in f_read]
        return sentences

    def count_words(self, sentences):
        '''
        统计词频
        :param sentences:
        :return:
        '''
        words_all = list()
        for sent in sentences:
            words_all.extend(sent)
        word_dict = {item[0]: item[1] for item in collections.Counter(words_all).most_common()}
        return word_dict, len(words_all)

    def count_cowords(self, sentences):
        '''
        统计共现的词
        :param train_data:
        :return:
        '''
        co_dict = dict()
        print(len(sentences))
        for index, data in enumerate(sentences):
            if data[0] not in co_dict:
                co_dict[data[0]] = data[1]
            else:
                co_dict[data[0]] += '@' +data[1]
        return co_dict

    def build_dict(self, words):
        return {item[0]: item[1] for item in collections.Counter(words).most_common()}

    def compute_mi(self, word_dict, co_dict, sum_tf):
        '''
        计算互信息
        :param word_dict:
        :param co_dict:
        :param sum_tf:
        :return:
        '''
        def compute_mi(p1, p2, p12):
            return math.log2(p12) - math.log2(p1) - math.log2(p2)

        mis_dict = dict()
        for word, co_words in co_dict.items():
            co_word_dict = self.build_dict(co_words.split('@'))
            mi_dict = {}
            for co_word, co_tf in co_word_dict.items():
                if co_tf >= 2: #这里过滤共现频率>=2的词
                    if co_word == word:
                        continue
                    p1 = word_dict[word] / sum_tf
                    p2 = word_dict[co_word] / sum_tf
                    p12 = co_tf / sum_tf
                    mi = compute_mi(p1, p2, p12)
                    mi_dict[co_word] = mi
            mi_dict = sorted(mi_dict.items(), key=lambda asd: asd[1], reverse=True)
            mis_dict[word] = mi_dict

        return mis_dict

    def save_mi_result(self, mis_dict):
        '''
        将共现频率>=2以及互信息>=4的量名搭配找出来
        :param mis_dict:
        :return:
        '''
        with open(self.mipath, 'w', encoding='utf-8') as f_write:
            for word, co_words in mis_dict.items():
                co_infos = [item[0] + '@' + str(item[1]) for item in co_words if item[1] >= 4] #这里过滤互信息>=4的词
                if len(co_infos) !=0:
                    f_write.write(word + '\t' + ','.join(co_infos) + '\n')

    # 运行主函数
    def calcute(self):
        print('step 1/6: 读取语料 ..........')
        sentences = self.build_corpus()

        print('step 2/6: 统计词频..........')
        word_dict, sum_tf = self.count_words(sentences)

        print('step 3/6: 统计共现词..........')
        co_dict = self.count_cowords(sentences)

        print('step 4/6: 计算互信息..........')
        mi_data = self.compute_mi(word_dict, co_dict, sum_tf)

        print('step 5/6: 保存词的互信息..........')
        self.save_mi_result(mi_data)

        print('done!.......')

if __name__ == '__main__':
    mi_corpus_path = os.path.join(os.getcwd(), 'corpus.txt')
    data_write_path = os.path.join(os.getcwd(), 'result.txt')
    quantifierNounMI = QuantifierNounMI(mi_corpus_path, data_write_path)
    quantifierNounMI.calcute()
    # fetch_quantifier_noun(os.path.join(os.getcwd(), '199801'))