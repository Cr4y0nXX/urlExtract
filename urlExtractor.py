#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Author  : Cr4y0n
# @Software: PyCharm
# @Time    : 2021/03/03

import re
import os
import time
from tqdm import tqdm
from argparse import ArgumentParser
from multiprocessing import Pool, Manager, cpu_count

class URLExtractor():
    def __init__(self):
        self.banner()
        self.args = self.parseArgs()
        self.differentURLList = []  # 所有URL去重后的列表
        self.fileList = Manager().list()    # 扫描到的所有文件
        self.allURLList = Manager().list()  # 扫描到的所有url
        self.urlWithFileList = Manager().list() # 所有url及其所在文件
        self.multiRun()

    def banner(self):
        logo = r"""
             _ ______      _                  _
            | |  ____|    | |                | |
  _   _ _ __| | |__  __  _| |_ _ __ __ _  ___| |_ ___  _ __
 | | | | '__| |  __| \ \/ / __| '__/ _` |/ __| __/ _ \| '__|
 | |_| | |  | | |____ >  <| |_| | | (_| | (__| || (_) | |
  \__,_|_|  |_|______/_/\_\\__|_|  \__,_|\___|\__\___/|_|

            Author: Cr4y0n
            Version: V1.0
        """
        print("\033[31m" + logo + "\033[0m")

    def parseArgs(self):
        # 文件、进程数、关键字
        parser = ArgumentParser(description="This is an url extract tool based on the  python3.7, created by Cr4y0n.")
        parser.add_argument("-f", "--file", required=True, help="Target file or package")
        parser.add_argument("-p", "--process", required=False, type=int, default=cpu_count(), help=f"Number of processes, default is the most of your PC: {cpu_count()}")
        parser.add_argument("-k", "--keyword", required=False, action="append", help="Include the keyword(Separate with ',': A,B,C,...)")
        return parser.parse_args()

    # 加载指定路径下的所有文件
    def loadFile(self, path):
        if os.path.isfile(path):
            self.fileList.append(path)
        else:
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    fileAbsPath = os.path.join(root, name)
                    self.fileList.append(fileAbsPath)

    # 匹配单个文件中的url，存入共享列表中
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

    # 多进程对所有文件进行url扫描
    def multiRun(self):
        self.s = r"http://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]|"
        self.s += r"ftp://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]|"
        self.s += r"https://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]"
        print("Please waiting……")
        start = time.time()
        self.loadFile(self.args.file)
        pool = Pool(self.args.process)
        for file in tqdm(self.fileList):
            pool.apply_async(self.findURL, (file, ))
        pool.close()
        pool.join()
        end = time.time()
        self.timeSpent = "%.2f"%(end - start)
        self.output()

    def output(self):
        print("\n" + "-" * 20)
        print(f"scan file:  {len(self.fileList)}")
        print(f"find url:   {len(self.allURLList)}")
        print(f"spend time: {self.timeSpent} s")
        if len(self.allURLList) > 0:
            self.writeFile()
            print("-" * 20, f"\n\nThe result has been saved in ./output/{self.date}/")
        else:
            print("-" * 20, f"\n\nFind 0 url, Thank you for using.")

    def writeFile(self):
        self.date = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        if not os.path.exists(r"./output/" + self.date):
            os.mkdir(r"./output/" + self.date)
        # 带文件名统计
        outputWithFilename = r"./output/" + self.date + "/urlWithFilename.txt"
        with open(outputWithFilename, "w") as f:
            for i in self.urlWithFileList:
                for j in i:
                    f.write(j + "\n")
        # 仅统计url
        allURLList = list(set(self.allURLList))
        self.differentURLList = sorted(allURLList)    # 去重+排序
        outputOnlyURL = r"./output/" + self.date + "/url.txt"
        with open(outputOnlyURL, "w") as f:
            for i in self.differentURLList:
                f.write(i + "\n")
        # 记录项目名
        outputPorjectName = r"./output/" + self.date + "/porjectName.txt"
        with open(outputPorjectName, "w") as f:
            f.write(self.args.file + "\n")
        # 带有关键字
        if self.args.keyword:
            self.withKeyword()

    def withKeyword(self):
        url_keyword = r"./output/" + self.date + "/urlWithKeyword.txt"
        with open(url_keyword, "w") as f:
            f.write(f"keyword: {self.args.keyword}\n\n")
            for url in self.differentURLList:
                for key in self.args.keyword:
                    if key in url:
                        f.write(url + "\n")
                        break

if __name__ == "__main__":
    URLExtractor()
