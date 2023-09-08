import re
import os
import jieba
import jieba.posseg as posseg
jieba.load_userdict("data_txt/jieba_dict_custom.txt")
class correct:
    def __init__(self,noun_list:set,quantifier_list:list,num_list:list,quantifier_noun_dict:dict) -> None:
        self.noun_list = noun_list
        self.quantifier_list = quantifier_list
        self.num_list = num_list
        self.quantifier_noun_dict = quantifier_noun_dict
        self.pattern = ''
    
    def init_pattern(self):
        # 数字 量词 名词
        self.pattern = ('([\d{}]+)' + '({})' + '(?:.*?)').format(''.join(self.num_list)
                                                       ,'|'.join(self.quantifier_list))
    def find(self,sentence):
        res = []
        self.init_pattern()
        # 分词后根据定义的字典提取可能的名词
        words = [word for word,flag in posseg.lcut(sentence) if flag in ['n']]
        # 查找这些名词所搭配的[数词量词名词]
        self.pattern = self.pattern + '([{}]+)'.format(''.join(words))
        return re.finditer(self.pattern,sentence)

    def correct(self,sentence:str): # [('一', '篇', '话')]
        if sentence ==' ' or len(sentence)==0: return 
        mybe = self.find(sentence)
        # if len(mybe) == 0 : print('没找到数词量词名词搭配') # 没找到数词量词名词搭配
        errors_span_rights = [] # [(error,index,right)] # 错误列表error[('一', '篇', '话')]  错误范围span  过错后的词right
        sentence_right = '' # 改错后的句子
        for i in mybe:
            span = i.span()
            i = list(i.groups())
            res = []
            try:
                if i[2] not in self.quantifier_noun_dict[i[1]]: # 如果名词不在所搭配的量词词典中
                    print('存在错误 {}  '.format(i),end='\t')
                    for k,v in self.quantifier_noun_dict.items(): # 遍历词典找到名词词可搭配的量词
                        if i[2] in v:
                            res.append(k)
                    #print(i[0] + '[%s]' % '|'.join(res) + i[2],end='\t') 
                    errors_span_rights.append((i,span,(i[0] , '[%s]' % '|'.join(res) , i[2])))
                    #print(span)
                    #print('正确句子：{}'.format(sentence.replace(''.join(i),i[0] + '[%s]' % '|'.join(res) + i[2])))
                else: 
                    # print('暂无错误 {}'.format(i))
                    print
            except Exception:
            # 存在非量词
                print('['+''.join(i) + ']句子中的[' + i[1] + ']不是量词')
                for k,v in self.quantifier_noun_dict.items():
                        if i[2] in v:
                            res.append(k)
                print(i[0] + '[%s]' % '|'.join(res) + i[2]) 
        print(errors_span_rights)

quantifier_list = [] # 量词列表
num_list = [] 
noun_list = set() # 名词列表
quantifier_noun_dict = {} # {'句' : ('话')}

# 加载数据
def init_list():

    num_path = os.path.join(os.getcwd(),'data_txt/num.txt')
    with open(num_path,'r',encoding='utf-8') as f:
        for line in f:
            num_list.append(line.strip())

    # 初始化量词列表，名词列表，量词-名词词典
    quantifier_noun_dict_path = os.path.join(os.getcwd(),'data_txt/result.txt')
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
    
    # 加载第二份量词-名词词典
    with open('data_txt/2_quan_noun.txt','r',encoding='utf-8') as f:
        for line in f:
            line_spl = line.strip().split(' ')
            quan = line_spl[0]
            # 量词列表
            if quan not in quantifier_list:
                quantifier_list.append(quan)
            # 名词列表
            noun_list.update(line_spl[1:])
            # 量词-名词词典
            if quan not in quantifier_noun_dict.keys():
                quantifier_noun_dict[quan] = set()
            quantifier_noun_dict[quan].update(line_spl[1:])

    
    

    # 初始化自定义词典
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

    
    # 名词列表写入jieba自定义词典
    with open('data_txt/jieba_dict_custom.txt','w',encoding='utf-8') as f:
        for i in noun_list:
            f.write(i + ' 10 ' + 'n' + '\n')

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
    text = [
        '这篇文章的每一则话表达了作者这三种月以来的颠沛流离',
        '表达了作者一个强烈的情感',
        '一项情感',
        '一各漂亮的苹果',
        '每到中秋节，家家户户都会吃一轮圆圆的月饼',
        '我的衣柜里有六件衣服，四件裤子和两件帽子',
        '墙上挂着一副画',
        '一对眼镜',
        '她发现自己头上有一条白头发'
    ]
    for i in text:
        co.correct(i)





    

