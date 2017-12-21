# _*_ coding:utf-8 _*_
import socket
# import uuid  # 通用唯一识别码
import time
import sqlite3
import os
import hashlib
import pickle
# Notes：
'''
测试时需要修改22行的目录，修改成本地计算机的某个目录即可。
'''

def get_file_hash(filename):
    with open(filename, 'rb') as f:
        sha256obj = hashlib.sha256()
        sha256obj.update(f.read())
        hash256 = sha256obj.hexdigest()
    return hash256

# 将相关数据保存至文本
browserDownload = open('browserDownload.txt', 'w')
for root, dirs , files in os.walk('D:\\browserDowload', topdown=False):
    for i in files:
        # print('%s in %s'% (files, root))
        # print(i,root)
        filename= os.path.join(root,i)
        # print(filename)
        # file_name = os.path.join(root, files)
        fileinfo = os.stat(filename)
        ctime = time.strftime('%Y%m%d%H%M%S',time.localtime(fileinfo.st_ctime ))
        atime = time.strftime('%Y%m%d%H%M%S', time.localtime(fileinfo.st_atime))
        mtime = time.strftime('%Y%m%d%H%M%S', time.localtime(fileinfo.st_mtime))
        # print(atime)
        hash256 = get_file_hash(filename)
        browserDownload.write('%s\t%s\t%s\t%s\t%s\t%s\n'
                              % (os.path.basename(filename), ctime, atime, mtime, hash256, root))
browserDownload.close()

# 将这个txt文件备份一下
pickle_file_name = 'browserDownload' + '_' + time.strftime("%Y-%m-%d",time.localtime()) + '.pkl'
pickle_file = open(pickle_file_name,'wb')


# 获取数据库名字
myname1 = socket.getfqdn(socket.gethostname())
table_create_time = time.strftime('%Y%m%d', time.localtime())
database_name = myname1 + '-' + table_create_time
# 生成以主机识别码+创建时间为名字的数据库
conn = sqlite3.connect(database_name + '.db')

# print(curdir)
# create a table named by curdir
cursor = conn.cursor()

cursor.execute('create table if not exists file_monitor ('
               'rowid int not null, '
               'file_name text NOT NULL, '
               'ctime text not null,'
               'atime text not null,'
               'mtime text not null,'
               'file_hash CHAR(64) not null,'
               # 'file_type int not null,'
               'parrent_path text not null)')
conn.commit()
print('database and table are created successfully!')

fr = open('browserDownload.txt','r')
i = 0
for line in fr.readlines():
    i +=1
    line_list = line.split('\t')
    sql = "insert into file_monitor(rowid, file_name, ctime, atime, mtime, file_hash, parrent_path) " \
          "values (%d, '%s', %s, %s, %s, '%s', '%s')" % (
        i, line_list[0], line_list[1], line_list[2], line_list[3], line_list[4], line_list[5]
    )
    cursor.execute(sql)
conn.commit()
print('data inserted successfully!')
conn.close()

# 查询数据库中数据
conn = sqlite3.connect('dufan-THINK-20171217.db')
cursor = conn.cursor()
cursor.execute('select * from file_monitor')
print(cursor.fetchall())
print('data query completed.')