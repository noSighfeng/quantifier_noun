import re
import os
import jieba
class correct:
    def __init__(self,noun_list,quantifier_list,num_list,quantifier_noun_dict) -> None:
        self.noun_list = noun_list
        self.quantifier_list = quantifier_list
        self.num_list = num_list
        self.quantifier_noun_dict = quantifier_noun_dict
        self.pattern = ''
    
    def init_pattern(self):
        # 数字 量词 名词
        self.pattern = ('([\d{}]+)' + '({}|.*)' + '({})').format(''.join(self.num_list)
                                                       ,'|'.join(self.quantifier_list)
                                                       ,'|'.join(self.noun_list))
        # self.pattern = ('([{}]+)' + '(.*)' + '(年)').format(''.join(self.num_list))
    def find(self,sentence):
        res = []
        self.init_pattern()
        # print(re.findall(self.pattern,sentence))
        return re.findall(self.pattern,sentence)

    def correct(self,sentence): # (['','',''])
        mybe = self.find(sentence)
        if len(mybe) == 0 : print('存在错别字')
        for i in mybe:
            res = []
            try:
                if i[2] not in self.quantifier_noun_dict[i[1]]: # 如果名词不在所搭配的量词词典中
                    print('存在错误 {}  '.format(i))
                    for k,v in self.quantifier_noun_dict.items():
                        if i[2] in v:
                            res.append(k)
                    print(i[0] + '[%s]' % '|'.join(res) + i[2]) 
                else: print('暂无错误 {}'.format(i))
            except Exception:
            # 存在非量词
                print('['+''.join(i) + ']句子中的[' + i[1] + ']不是量词')
                for k,v in self.quantifier_noun_dict.items():
                        if i[2] in v:
                            res.append(k)
                print(i[0] + '[%s]' % '|'.join(res) + i[2]) 

    


quantifier_list = [] # 量词列表
num_list = [] 
noun_list = set() # 名词列表
quantifier_noun_dict = {} # {'句' : ('话')}
def init_list():

    num_path = os.path.join(os.getcwd(),'data_txt/num.txt')
    with open(num_path,'r',encoding='utf-8') as f:
        for line in f:
            num_list.append(line.strip())

    # 初始化量词列表，名词列表，量词-名词词典
    quantifier_noun_dict_path = os.path.join(os.getcwd(),'data_txt/1_quan_noun.txt')
    with open(quantifier_noun_dict_path,'r',encoding='utf-8') as f:
        for line in f:
            line_spl = line.strip().split(' ')
            quan = line_spl[0]
            # 量词列表
            quantifier_list.append(quan)
            # 名词列表
            for i in line_spl[1:]:
                noun_list.add(i)
            # 量词-名词词典
            quantifier_noun_dict[quan] = set(line_spl[1:])
    
    # 初始化用户词典
    dict_custom_path = os.path.join(os.getcwd(),'data_txt/dict_custom.txt')
    with open(dict_custom_path,'r',encoding='utf-8') as f:
        for line in f:
            line_spl = line.strip().split(' ')
            quan = line_spl[0]
            # 量词列表
            if quan not in quantifier_list:
                quantifier_list.append(quan)
            # 名词列表
            noun_list.add(line_spl[1])
            # 量词-名词词典
            if quan not in quantifier_noun_dict.keys():
                quantifier_noun_dict[quan] = set()
            quantifier_noun_dict[quan].add(line_spl[1])

    
    # 纠正错误词典 错误类型：量词错误搭配
    dict_error_path = os.path.join(os.getcwd(),'data_txt/dict_error.txt')
    with open(dict_error_path,'r',encoding='utf-8') as f:
        for line in f:
            line_spl = line.strip().split(' ')
            error_quan , error_noun = line_spl[0] , line_spl[1]
            quantifier_noun_dict[error_quan].discard(error_noun)
            
            
if __name__ == '__main__':
    init_list()
    co = correct(noun_list,quantifier_list,num_list,quantifier_noun_dict)
    co.correct('这篇文章中的这一篇话抒发了表达了作者这三各月以来的颠沛流离')





    

