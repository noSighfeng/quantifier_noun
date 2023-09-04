from multiprocessing import Process 
from temp.find import Find
from jieba_fast import posseg
from functools import partial
import collections
import pymysql
import re
import time

db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='量词名词搭配')
cursor = db.cursor()
def chunked_file_reader(file, block_size=1024 * 1024):
    """生成器函数：分块读取文件内容，使用 iter 函数
    """
    # 首先使用 partial(fp.read, block_size) 构造一个新的无需参数的函数
    # 循环将不断返回 fp.read(block_size) 调用结果，直到其为 '' 时终止
    for chunk in iter(partial(file.read, block_size), ''):
        yield chunk

def write_to_file(res:dict):
    f = open('res.txt','a')
    for k,v in res.items():
        print(k)
        # for i in v:
        #     words.extend([x.word for x in posseg.cut(i) if 'n' in x.flag])
        f.write(str(k) + ' ' + " ".join(collections.Counter([i.word for i in posseg.lcut("".join(v),HMM=False) if i.flag in ['n']])) + '\n')
    f.close()
    res.clear()

def create_table(cursor,table_name):
    sql = """
    CREATE TABLE `{}` (
    `noun` varchar(255) NOT NULL,
    `tf` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`noun`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """.format(table_name)
    cursor.execute(sql)

def table_exists(con,table_name):        #这个函数用来判断表是否存在
    sql = "show tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]
    if table_name in table_list:
        return 1        #存在返回1
    else:
        return 0        #不存在返回

def insert_table(cursor,table_name,data):
    try:
        sql = """
        INSERT INTO `{}` VALUES(%s,%s)
        ON DUPLICATE KEY UPDATE tf = tf + 1
        """.format(table_name) 
        # print(sql)
        cursor.executemany(sql,data)
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False

def write_to_mysql(res:dict):
    print("?")
    for k,v in res.items():
        print(k)
        if not table_exists(cursor,k):
            create_table(cursor,k)
        lcut = posseg.lcut("".join(v))
        insert_table(cursor,k,[(i.word,0) for i in lcut if i.flag in ['n']])

    res.clear()
    return True



if __name__ == "__main__":
    s = Find('./data_txt/quantifier.txt','./data_txt/num.txt')
    filePath = 'C:\\Users\\y\\Desktop\\1_jieba_seg.txt'
    
    res = {}
    total = 0 
    
    with open(filePath,encoding='utf-8') as fp:
        for chunk in chunked_file_reader(fp):
            total += 1
            print('\r',"{}G {}M".format(total>>10,total),end='',flush=True)
            if total%100==0:
                write_to_mysql(res)
                #write_to_file(res)

            data = s.find(chunk)
            if len(data) != 0 :
                for i in data:
                    if i[1] not in res.keys():
                        res[i[1]] = []
                    res[i[1]].append(i[2])
        
    #write_to_file(res)

    