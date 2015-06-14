# coding=utf-8
import sys
import os
import subprocess

"""
    git 提交大的文件夹时会报错, 无法提交
    该程序用于把大文件夹分成小份多次提交
"""

# 总大小
TOTAL_SIZE = 0

# 每次 push 到服务器 总文件大小 单位M
PER_PUSH_SIZE = 10 

def main():
    sp = subprocess.Popen(['git', 'status'], stdout=subprocess.PIPE)
    
    for line in sp.stdout.readlines():
        line = line.strip()
        if os.path.isfile(line):
            gitadd(line)
        elif os.path.isdir(line):
            gitadddir(line)

    commit_and_push()

def gitadddir(dirname):
    '''
        文件夹文件批量 git add
    '''
    for i in os.listdir(dirname):
        npath = '%s/%s' % (dirname, i)
        if os.path.isfile(npath):
            gitadd(npath)
        elif os.path.isdir(npath):
            gitadddir(npath)

    print 'add dir %s finish' % dirname

def getsize(dirname):
    '''
        获取文件或文件夹的大小
    '''
    sp = subprocess.Popen(['du', '-sk', dirname], stdout=subprocess.PIPE)
    t = sp.stdout.readline().split('\t')
    return int(t[0].strip())

def gitadd(filename):
    '''
        git add 单个文件
    '''
    global TOTAL_SIZE
    global PER_PUSH_SIZE

    size = getsize(filename)
    TOTAL_SIZE = TOTAL_SIZE + size

    print 'git add %s' % filename
    os.system('git add %s' % filename)

    if TOTAL_SIZE > PER_PUSH_SIZE * 1024:
        print '====size %dk =====' % TOTAL_SIZE
        TOTAL_SIZE = 0
        commit_and_push()

def commit_and_push():
    '''
        提交 and 推送
    '''
    print 'commit_and_push'
    os.system("git commit -m 'init'")
    os.system("git push origin master")

if __name__ == '__main__':

    main()


