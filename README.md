## urlExtractor

URL提取器，使用多进程的方式对目标路径下所有文件进行所描，由于Python的多线程存在资源问题，所以使用了多进程的方式，最大限度利用CPU资源，分析几千个文件只需要5秒左右

![](https://github-1302945528.cos.ap-chengdu.myqcloud.com/repPic/urlExtractor/1.png)

程序使用正则匹配的方式，可以扫描出`http、https、ftp`三种协议开头的链接并输出到文件。

## Environment

OS：All

Python：3

## Install

使用git下载

```
git clone https://github.com/Cr4y0nXX/urlExtractor.git
```

## Usage

使用`-f`或`--file`指定需要分析的项目路径，即可进行分析，并输出结果到`./output/datetime`

```
python urlExtractor.py -f D:\phpstudy
```

除此还有两个参数：

- -p  --process ：进程数，默认是本机的做大逻辑处理器数量
- -k  --keyword ：关键字，可指定关键字来提取包含该关键字的URL，可使用逗号隔开多个

```
λ python urlExtractor.py -h

             _ ______      _                  _
            | |  ____|    | |                | |
  _   _ _ __| | |__  __  _| |_ _ __ __ _  ___| |_ ___  _ __
 | | | | '__| |  __| \ \/ / __| '__/ _` |/ __| __/ _ \| '__|
 | |_| | |  | | |____ >  <| |_| | | (_| | (__| || (_) | |
  \__,_|_|  |_|______/_/\_\\__|_|  \__,_|\___|\__\___/|_|

            Author: Cr4y0n
            Version: V1.0

usage: urlExtractor.py [-h] -f FILE [-p PROCESS] [-k KEYWORD]

This is an url extract tool based on the python3.7 and created by Cr4y0n. You
can use this tool to quickly extract all URLs

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Target file or package
  -p PROCESS, --process PROCESS
                        Number of processes, default is the most of your CP: 8
  -k KEYWORD, --keyword KEYWORD
                        Include the keyword(Separate with ',': A,B,C,...)
```

当然您也可以直接改代码中的正则或re模块的匹配方式，将该工具变为一个任意字符的匹配工具，如果还能加入参数或配置文件，那就太棒了。

我这次仅想写一个提取URL的需求实现，是为了在做溯源审计时更加方便。
