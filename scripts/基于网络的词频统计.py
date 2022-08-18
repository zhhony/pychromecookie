import pandas
import os
import jieba
import jieba.analyse as analyse
import jieba.posseg as posseg
import paddle
import re
from pathlib import Path
from zhon.hanzi import punctuation
from typing import *
import wordcloud
import cv2
from time import sleep

pandas.set_option('display.unicode.east_asian_width', True)
pandas.set_option('display.unicode.ambiguous_as_wide', True)

AUTHOR = {2000: '朱镕基', 2001: '朱镕基', 2002: '朱镕基', 2003: '朱镕基', 2004: '温家宝', 2005: '温家宝', 2006: '温家宝', 2007: '温家宝', 2008: '温家宝', 2009: '温家宝', 2010: '温家宝',
          2011: '温家宝', 2012: '温家宝', 2013: '温家宝', 2014: '李克强', 2015: '李克强', 2016: '李克强', 2017: '李克强', 2018: '李克强', 2019: '李克强', 2020: '李克强', 2021: '李克强', 2022: '李克强'}

FLAG = {'vi': '不及物动词', 's': '处所词', 'r': '代词', 'ns': '地名', 'v': '动词', 'vg': '动词性语素', 'f': '方位词', 'ict': '副词', 'vd': '副动词', 'ad': '副形词', 'k': '后缀', 'nt': '机构团体名', 'uj': '结构助词1', 'uv': '结构助词2', 'p': '介词', 'c': '连词', 'q': '量词', 'n': '名词', 'ng': '名词性语素', 'vn': '名动词', 'an': '名形词', 'nz': '其它专名', 'h': '前缀', 'b': '区别词',
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
    addList = [('防沙治沙', 'l'), ('转移支付', 'l'), ('新型冠状病毒', 'l'), ('新冠', 'l'), ('换林换草', 'l'), ('平均', 'v'), ('妥善', 'a'), ('成果丰硕', 'a'), ('汪洋大海', 'n'), ('孟中印缅', 'n'), ('陆海统筹', 'l'), ('人命关天', 'a'), ('山水林田湖', 'l'), ('化蛹成蝶', 'v'), ('枝繁叶茂', 'a'),
               ('十二五', 'l'), ('拥政爱民', 'a'), ('天然林', 'n'), ('退耕还林还草', 'l'), ('惠民生', 'v'), ('蔚然成风', 'a'), ('于法有据', 'a')]
    for x, y in addList:
        jieba.suggest_freq(x, tune=True)
        jieba.add_word(word=x, tag=y)

    return posseg.lcut(text, HMM=False, use_paddle=False)


if __name__ == '__main__':

    LOCAL_USER_PROFILE = os.environ['USERPROFILE']

    inPath = LOCAL_USER_PROFILE + '/Desktop/新建文件夹/'
    outPath = LOCAL_USER_PROFILE + '/Desktop/输出文件夹/'

    image = cv2.imread('../resource//map_pin.jpg')

    color = wordcloud.ImageColorGenerator(image)
    wordcloud_ = wordcloud.WordCloud(font_path='../resource/simhei.ttf', mask=image, color_func=color, max_font_size=120, repeat=True, min_font_size=2,
                                     max_words=25000, background_color=None, mode='RGBA', relative_scaling=0)

    # 获取path内的文件
    fileList = [i for i in Path(inPath).glob('**/*.txt')]

    # 存储每个文件的词频dataframe
    fileFrequencyList = []
    for file in fileList:

        FILE_NAME = file.name
        FILE_YEAR = file.name[:4]

        with open(file=file, mode='r') as f:
            # 获取词频清单
            wordFrequency = lcut_(f)

        flags = list(set([j for i, j in wordFrequency]))
        flagReleaseList = ['不及物动词', '动词性语素', '状态词', '形容词', '人名', '区别词', '简称略称', '方位词', '副词', '副动词', '动词', '副形词', '后缀',  '结构助词1', '结构助词2',  '介词', '连词',  '量词',  '前缀', '助词', '名词性语素', '代词', '时间词', '数词', '数量词名词',
                           '时间词性语素', '时态助词1',  '时态助词2',  '叹词', '形容词性语素', '助词', '字符串',  '副语素', '外语', '语素', '结构助词3', '时态助词3', '其他']

        flags = [i for i in flags if FLAG[i] not in flagReleaseList]

        for flag in flags:
            word = ' '.join(
                [i for i, j in wordFrequency if i != '~' and j == flag])
            ciyunImage = wordcloud_.generate(word)

            if Path(outPath + FLAG[flag]).exists() == False:
                Path(outPath + FLAG[flag]).mkdir()
            ciyunImage.to_file(outPath + FLAG[flag] + '/' + FILE_YEAR + '.png')
            sleep(1.5)
        sleep(1)
