## urlExtractor

------

### 介绍

URL提取器，使用多进程的方式对目标路径下所有文件进行所描，提取其中的URL并输出到文件，可以扫描出`http、https、ftp`三中协议开头的链接

![https://github-1302945528.cos.ap-chengdu.myqcloud.com/repPic/urlExtractor/2.png]()

由于Python的多线程存在资源问题，所以使用了多进程的方式，最大限度利用CPu资源，分析几千个文件只需要5秒左右

![https://github-1302945528.cos.ap-chengdu.myqcloud.com/repPic/urlExtractor/1.png]()

### 使用

