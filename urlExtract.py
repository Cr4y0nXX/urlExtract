#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2021/03/03

import re
import os
import time
# from datetime import datetime
from argparse import ArgumentParser
from multiprocessing import Pool, Manager

class URLExtract():
    def __init__(self, file):
        # self.args = self.parseArgs()
        self.differentURLList = []
        self.fileList = Manager().list()
        self.allURLList = Manager().list()
        self.urlWithFileList = Manager().list()
        self.s = r"http://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]|"
        self.s += r"ftp://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]|"
        self.s += r"https://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]"
        self.file = file
        print("Please waiting……")
        self.multiRun()

    def parseArgs(self):
        """
        文件、进程数、包含关键字、不包含关键字、输出结果到文件、
        :return:
        """
        parser = ArgumentParser()
        parser.add_argument("-f", "--file", required=True, help="Target file or package")
        parser.add_argument("-p", "--process", required=False, type=int, default=4, help="Number of processes, default 4, -1 means the most ")
        parser.add_argument("-k", "--keyword", required=False, type=str, default="", help="include keyword('key1&&key2' is include both key1 and key2, 'key1||key2' is include key1 or key2)")
        parser.add_argument("-ek", "--process", required=False, type=int, default=4, help="Number of processes, default 4, -1 means the most ")
        parser.add_argument("-rA", "--randomAgent", required=False, action="store_true", help="random request User-Agent")
        return parser.parse_args()

    def loadFile(self, path):
        if os.path.isfile(path):
            self.fileList.append(path)
        else:
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    fileAbsPath = os.path.join(root, name)
                    self.fileList.append(fileAbsPath)

    def findURL(self, file):
        string = ""
        with open(file, encoding="utf8") as f:
            for line in f.readlines():
                line = line.strip()
                string += line
        oneFileResult = list(set(re.findall(self.s, string)))
        self.allURLList += oneFileResult
        oneFileResult.sort()
        if len(oneFileResult) != 0:
            oneFileResult.insert(0, "------" + file + "------")
            self.urlWithFileList.append(oneFileResult)
        # print(self.urlWithFileList)

    def multiRun(self):
        start = time.time()
        self.loadFile(self.file)
        # print(self.fileList)
        pool = Pool()
        for file in self.fileList:
            pool.apply_async(self.findURL, (file, ))
        pool.close()
        pool.join()
        end = time.time()
        self.timeSpent = "%.2f"%(end - start)
        self.output()
        self.writeFile()

    def output(self):

        # for i in self.differentURLList:
        #     print(i)
        print("-" * 20)
        print(f"find url:   {len(self.allURLList)}")
        print(f"scan file:  {len(self.fileList)}")
        print(f"time spend: {self.timeSpent} s")
        print("-" * 20, "\nThe result has been saved in ./output/")

    def writeFile(self):
        # porjectName = self.args.filename
        date = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        if not os.path.exists(r"./output/" + date):
            os.mkdir(r"./output/" + date)
        # 带文件名统计
        outputWithFilename = r"./output/" + date + "/urlWithFilename.txt"
        with open(outputWithFilename, "w") as f:
            for i in self.urlWithFileList:
                for j in i:
                    f.write(j + "\n")
        # 仅统计url
        allURLList = list(set(self.allURLList))
        self.differentURLList = sorted(allURLList)    # 去重+排序
        outputOnlyURL = r"./output/" + date + "/url.txt"
        with open(outputOnlyURL, "w") as f:
            for i in self.differentURLList:
                f.write(i + "\n")
        # 记录项目名
        outputPorjectName = r"./output/" + date + "/porjectName.txt"
        with open(outputPorjectName, "w") as f:
            f.write(self.file + "\n")

if __name__ == "__main__":
    file = r"E:/"
    # file = r"./1.html"
    URLExtract(file)
