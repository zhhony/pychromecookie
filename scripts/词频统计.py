import pandas
import os
import jieba
import jieba.analyse as analyse
import jieba.posseg as posseg
import paddle
import re
from pathlib import Path
from zhon.hanzi import punctuation
from yonghong.script.port import EntryPoint, ResourceType
from typing import *


pandas.set_option('display.unicode.east_asian_width', True)
pandas.set_option('display.unicode.ambiguous_as_wide', True)

AUTHOR = {2000: '朱镕基', 2001: '朱镕基', 2002: '朱镕基', 2003: '朱镕基', 2004: '温家宝', 2005: '温家宝', 2006: '温家宝',
          2007: '温家宝', 2008: '温家宝', 2009: '温家宝', 2010: '温家宝', 2011: '温家宝', 2012: '温家宝', 2013: '温家宝', 2014: '李克强', 2015: '李克强', 2016: '李克强', 2017: '李克强', 2018: '李克强', 2019: '李克强', 2020: '李克强', 2021: '李克强', 2022: '李克强'}


def replace_(text: str, *args) -> str:
    '''用于将文本中多余的字符替换成空格，*args支持自定义添加'''

    # 构建替换关键字
    replaceList = ['\n', '\r', '\t', '\xa0', '/', '\\', '!', '@', '\#', '$', '%', '^', '&', '+', '‰', '-',
                   '*', '(', ')', '<', '>', '?', '[', ']', '{', '}', ';', "'", ':', '"', ',', '.', ' ', '．', '０', '１', '２', '３', '４', '５', '６', '７', '８', '９']
    for i in range(10):
        replaceList.append(str(i))
    for i in punctuation:
        replaceList.append(i)
    for i in args:
        replaceList.append(i)

    # 替换为空格
    for i in replaceList:
        text = text.replace(i, ' ')

    # 将多个空格合并成一个
    pattern = re.compile(r' +')
    text = pattern.sub('~~~', text)

    return text


def lcut(fp: IO) -> list:
    '''用于统计文件中的词频，返回词语和词性'''

    # 替换文本
    text = replace_(fp.read())

    # 切割词语
    paddle.enable_static()
    jieba.enable_paddle()

    # 定义展示的词语
    addList = [('防沙治沙', 'n', '1000000000000'), ('新型冠状病毒', 'n', '1000000000000'), ('新冠', 'n', '1000000000000'), ('换林换草', 'v', '1000000000000'), ('平均', 'v', '1000000000000'), ('妥善', 'a', '1000000000000'), ('成果丰硕', 'a', '1000000000000'), ('汪洋大海', 'n', '1000000000000'), ('孟中印缅', 'n', '1000000000000'), ('陆海统筹', 'n', '1000000000000'), ('人命关天', 'a', '1000000000000'), ('山水林田湖', 'n', '100000000000'), ('化蛹成蝶', 'v', '1000000000000'), ('枝繁叶茂', 'a', '1000000000000'),
               ('十二五', 'n', '1000000000000'), ('拥政爱民', 'a', '100000000000'), ('天然林', 'n', '1000000000000'), ('退耕还林还草', 'v', '1000000000000'), ('惠民生', 'v', '1000000000000'), ('蔚然成风', 'a', '1000000000000'), ('于法有据', 'a', '1000000000000')]
    for x, y, z in addList:
        jieba.suggest_freq(x, tune=True)
        jieba.add_word(word=x, tag=y, freq=z)

    return posseg.lcut(text, HMM=False, use_paddle=True)


if __name__ == '__main__':

    LOCAL_USER_PROFILE = os.environ['USERPROFILE']

    path = Path(LOCAL_USER_PROFILE + '/Desktop/新建文件夹')

    # 获取path内的文件
    fileList = [i for i in path.glob('**/*.txt')]

    # 存储每个文件的词频dataframe
    fileFrequencyList = []
    for file in fileList:

        FILE_NAME = file.name
        FILE_YEAR = int(file.name[:4])

        with open(file=file, mode='r') as f:
            # 获取词频清单
            wordFrequency = lcut(f)

        wordDict = dict()
        for word, flag in wordFrequency:
            wordDict.update(
                {word: [wordDict.setdefault(word, [0, flag])[0]+1, flag]})

        # 按词频降序排序
        wordDictList = [(keyword, [value[0], value[1], AUTHOR.get(
            FILE_YEAR), FILE_YEAR]) for keyword, value in wordDict.items()]
        wordDictList.sort(key=lambda x: x[1], reverse=True)
        wordDict = dict(wordDictList)

        # 封装成dataframe
        df = pandas.DataFrame(data=wordDict)
        df = df.transpose().reset_index()
        df.columns = ['关键词', '数值', '词性', '作者', '年份']
        fileFrequencyList.append(df)

    df = pandas.concat(fileFrequencyList).reset_index(drop=True)
    df = df.astype({'数值': 'int64', '年份': 'int64'})

    entry = EntryPoint()
    entry.output.dataset = df
    print(entry.output.dataset)
