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

AUTHOR = {2000: '朱镕基', 2001: '朱镕基', 2002: '朱镕基', 2003: '朱镕基', 2004: '温家宝', 2005: '温家宝', 2006: '温家宝', 2007: '温家宝', 2008: '温家宝', 2009: '温家宝', 2010: '温家宝',
          2011: '温家宝', 2012: '温家宝', 2013: '温家宝', 2014: '李克强', 2015: '李克强', 2016: '李克强', 2017: '李克强', 2018: '李克强', 2019: '李克强', 2020: '李克强', 2021: '李克强', 2022: '李克强'}

FLAG = {'vi': '不及物动词', 's': '处所词', 'r': '代词', 'ns': '地名', 'v': '动词', 'vg': '动词性语素', 'f': '方位词', 'd': '副词', 'vd': '副动词', 'ad': '副形词', 'k': '后缀', 'nt': '机构团体名', 'uj': '结构助词1', 'uv': '结构助词2', 'p': '介词', 'c': '连词', 'q': '量词', 'n': '名词', 'ng': '名词性语素', 'vn': '名动词', 'an': '名形词', 'nz': '其它专名', 'h': '前缀', 'b': '区别词',
        'nr': '人名', 't': '时间词', 'tg': '时间词性语素', 'ul': '时态助词1', 'uz': '时态助词2', 'm': '数词', 'mq': '数量词名词', 'e': '叹词', 'a': '形容词', 'ag': '形容词性语素', 'u': '助词', 'z': '状态词', 'x': '字符串', 'df': '副语素', 'eng': '外语', 'g': '语素', 'i': '成语', 'j': '简称略称', 'l': '习用语', 'nrfg': '古近现代人名', 'nrt': '英译名', 'ud': '结构助词3', 'ug': '时态助词3', 'zg': '其他'}


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


def lcut_(fp: IO) -> list:
    '''用于统计文件中的词频，返回词语和词性'''

    # 替换文本
    text = replace_(fp.read())

    # 切割词语
    paddle.enable_static()
    jieba.enable_paddle()

    # 定义展示的词语
    addList = [('防沙治沙', 'n'), ('新型冠状病毒', 'n'), ('新冠', 'n'), ('换林换草', 'v'), ('平均', 'v'), ('妥善', 'a'), ('成果丰硕', 'a'), ('汪洋大海', 'n'), ('孟中印缅', 'n'), ('陆海统筹', 'n'), ('人命关天', 'a'), ('山水林田湖', 'n'), ('化蛹成蝶', 'v'), ('枝繁叶茂', 'a'),
               ('十二五', 'n'), ('拥政爱民', 'a'), ('天然林', 'n'), ('退耕还林还草', 'v'), ('惠民生', 'v'), ('蔚然成风', 'a'), ('于法有据', 'a')]
    for x, y in addList:
        jieba.suggest_freq(x, tune=True)
        jieba.add_word(word=x, tag=y)

    return posseg.lcut(text, HMM=False, use_paddle=False)


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
            wordFrequency = lcut_(f)

        wordDict = dict()
        for word, flag in wordFrequency:
            wordDict.update(
                {word: [wordDict.setdefault(word, [0, flag])[0]+1, flag]})

        # 按词频降序排序
        wordDictList = [(keyword, [value[0], FLAG.get(value[1]), AUTHOR.get(
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
