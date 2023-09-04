import pymysql
import re
db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='量词名词搭配')

cursor = db.cursor()

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
    
def create_table(cursor,table_name):
    sql = """
    CREATE TABLE `{}` (
    `noun` varchar(255) DEFAULT NULL,
    `tf` varchar(255) DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """.format(table_name)
    cursor.execute(sql)

#UPDATE `支` SET tf = tf + 1 where `支`.noun='1'
def insert_table(cursor,table_name,noun):
    try:
        sql = """
        INSERT INTO `%s` VALUES('%s',0)
        """ % (table_name,noun)
        print(sql)
        cursor.execute(sql)
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False

def update_table(cursor,table_name,)
# print(table_exists(cursor,'das'))
# create_table(cursor,'支')
# print(table_exists(cursor,'支'))

print(insert_table(cursor,'支','军队'))