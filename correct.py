import re
import os
class correct:
    def __init__(self,noun_list,quantifier_list,num_list,quantifier_noun_dict) -> None:
        self.noun_list = noun_list
        self.quantifier_list = quantifier_list
        self.num_list = num_list
        self.quantifier_noun_dict = quantifier_noun_dict
        self.pattern = ''
    
    def init_pattern(self):
        # 数字 量词 名词
        self.pattern = ('([{}]+)' + '([{}])' + '({})').format(''.join(self.num_list)
                                                       ,''.join(self.quantifier_list)
                                                       ,''.join(self.noun_list))
    
    def find(self,sentence):
        self.init_pattern()
        print(re.findall(self.pattern,sentence))
        return re.findall(self.pattern,sentence)

    def correct(self,sentence):
        mybe = self.find(sentence)[0]
        res = []
        if mybe[2] not in self.quantifier_noun_dict[mybe[1]]:
            print('存在错误')
            for k,v in self.quantifier_noun_dict.items():
                if mybe[2] in v:
                    res.append(k)
            return mybe[0] + '[%s]' % '|'.join(res) + mybe[2]
        else: return '暂无错误'

    


quantifier_list = []
num_list = []
noun_list = []
quantifier_noun_dict = {} # {'句' : ('话')}
def init_list():

    num_path = os.path.join(os.getcwd(),'data_txt/num.txt')
    with open(num_path,'r',encoding='utf-8') as f:
        for line in f:
            num_list.append(line.strip())


    quantifier_path = os.path.join(os.getcwd(),'data_txt/quantifier.txt')
    with open(quantifier_path,'r',encoding='utf-8') as f:
        for line in f:
            quantifier_list.append(line.strip())


    noun_path = os.path.join(os.getcwd(),'data_txt/noun.txt')
    with open(noun_path,'r',encoding='utf-8') as f:
        global noun_list
        noun_list = f.readlines()

    quantifier_noun_dict_path = os.path.join(os.getcwd(),'data_txt\\quan_noun.txt')
    with open(quantifier_noun_dict_path,'r',encoding='utf-8') as f:
        for line in f:
            line_spl = line.split(' ')
            quan = line_spl[0]
            quantifier_noun_dict[quan] = set(line_spl[1:])

    
    



if __name__ == '__main__':
    init_list()
    co = correct(noun_list,quantifier_list,num_list,quantifier_noun_dict)
    print(co.correct('这里有一棵树'))





    

