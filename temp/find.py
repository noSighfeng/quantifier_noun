import re

class Find():
    def __init__(self,path_quantifier,path_num):
        self.quantifier = []
        self.num = []
        self.noun_quantifier_dict = {}
        self.path_quantifier = path_quantifier
        self.path_num = path_num
    
    # 量词词典初始化
    def init_data(self,path_quantifier,path_num):
        with open(path_quantifier, encoding='utf-8') as f:
            for l in f.readlines():
                data = l.strip().split(' ')
                self.quantifier.append(data[0])
                del(data[0])
                for i in data:
                    if i not in self.noun_quantifier_dict.keys():
                        self.noun_quantifier_dict[i] = []
                    self.noun_quantifier_dict[i].append(self.quantifier[-1])
        with open(path_num,encoding='utf-8') as f:
            self.num = f.readlines()

    # 构建正则表达式
    def init_pattern(self):
        num_pattern = '[' + "".join("".join(self.num).split('\n')) + ']'
        quantifier_pattern = '[' + "".join("".join(self.quantifier).split('\n')) + ']'
        # (?:(?<=num_pattern)(quantifier_pattern{1})([\u4e00-\u9fa5]{0,}))
        # pattern = "(?:({}+)({})([\u4e00-\u9fa5]{{0,10}}))".format(num_pattern,quantifier_pattern)
        pattern = "(?:({}+)({})([\x20\u4e00-\u9fa5]*))".format(num_pattern,quantifier_pattern)
        return pattern
    

    # 使用正则查找
    def find(self,sentence):
        '''
         sentence 这里三百七十五个东西用来帮助他，这是很重要的一件事
         return [[('个', '东西用来帮助他'), (7, 15)], [('件', '事'), (23, 25)], '这里三百七十五个东西用来帮助他，这是很重要的一件事。']
        '''
        self.init_data(self.path_quantifier,self.path_num)
        pattern = self.init_pattern()
        # print(re.findall(pattern,sentence))
        return re.findall(pattern,sentence)
        # f = re.finditer(pattern,sentence)
        # res = []
        # for i in f:
        #     # print(i.groups())
        #     # print(i.span())
        #     # res.append([i.groups(),i.span()])
        #     res.append(i.groups())
        # return res

s = Find('./data_txt/quantifier.txt','./data_txt/num.txt')
print(s.find('这里三百七十五个东西 用来帮助他，这是很重要的一件事。'))
