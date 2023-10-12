"""
# Author   : Wu Linlin
# coding=utf-8
# @version : 1.0
# @Time    : 2022/5/31 16:00
# @File    : chat_mysql.py
# @Software: PyCharm
# @describe: 数据库相关操作
"""

import pymysql


db_config = {}
db_config["host"] = "bj-cynosdbmysql-grp-94se5i3c.sql.tencentcdb.com"
db_config["port"] = 21559
db_config["user"] = "root"
db_config["passwd"] = "BJUT@java"
db_config["db_name"] = "黄鸣奕20068109"


def db_query(sql):
    """
    查询数据库操作
    @param sql: 数据操作对应的SQL语句
    """
    # 1. 连接数据库
    db = pymysql.connect(host=db_config["host"],
                         port=db_config["port"],
                         user=db_config["user"],
                         passwd=db_config["passwd"],
                         db=db_config["db_name"],
                         charset='utf8', use_unicode=True)
    # 2. 创建游标对象
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        # 3. 获取所有记录列表
        results = cursor.fetchall()
    except Exception as ex:
        print("<ERROR> --数据库操作失败:" + str(ex) + "--")
    # 4. 关闭数据库连接
    db.close()
    return results


def db_insert(sql, args):
    """
    插入数据库操作
    @param sql: 数据操作对应的SQL语句
    """
    # 1. 连接数据库
    db = pymysql.connect(host=db_config["host"],
                         port=db_config["port"],
                         user=db_config["user"],
                         passwd=db_config["passwd"],
                         db=db_config["db_name"],
                         charset='utf8', use_unicode=True)
    # 2. 创建游标对象
    cursor = db.cursor()
    try:
        cursor.execute(sql, args)
        # 3. 提交到数据库执行
        db.commit()
    except Exception as ex:
        print("<ERROR> --数据库操作失败:" + str(ex) + "--")
        # 4. 如果发生错误则回滚
        db.rollback()
        return False
    # 5. 关闭数据库连接
    db.close()
    return True


class LogInformation(object):
    # 检查用户名及密码是否匹配
    def login_check(user_name, password):
        try:
            sql = "SELECT * FROM users"
            result = db_query(sql)
            if (user_name, password) in result:
                return True
            else:
                return False
        except:
            return False

    # 创建新用户
    def create_new_user(user_name, password):
        try:
            sql = "INSERT INTO users VALUES (%s, %s);"
            args = (user_name, password)
            db_insert(sql, args)
            print("插入成功")
            return "0"
        except:
            print("数据库出错")

    # 检查用户名是否已存在
    def select_user_name(user_name):
        try:
            flg = 0
            sql = "SELECT * FROM users"
            result = db_query(sql)
            n = len(result)
            for i in range(n):
                if user_name == result[i][0]:
                    flg = 1
            if flg == 1:
                return "1"
            else:
                return "0"
        except:
            print("数据库出错")
