import pandas
import os
import jieba
import jieba.analyse as analyse
import json
from pathlib import Path
from simplejson import loads
from yaml import load
from zhon.hanzi import punctuation
from datetime import datetime
from yonghong.script.port import EntryPoint, ResourceType
from typing import *


pandas.set_option('display.unicode.east_asian_width', True)
pandas.set_option('display.unicode.ambiguous_as_wide', True)

LOCAL_USER_PROFILE = os.environ['USERPROFILE']

path = Path(LOCAL_USER_PROFILE + '/Desktop/新建文件夹')


def replace_(text: str) -> str:
    replaceList = ['\n', '\r', '\xa0', '/', '和', '的',
                   '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    [replaceList.append(i) for i in punctuation]
    for i in replaceList:
        text = text.replace(i, '')
    return text


fileList = [i for i in path.glob('**/*')]

f = open('C:/Users/zhhony/Desktop/新建文件夹/2000年政府工作报告.log.txt', 'r')
t = f.read()
f.close()


def lcut(fp: IO) -> pandas.DataFrame:
    text = replace_(fp.read())
    wordList = jieba.lcut(text)
    wordDict = dict()
    for word in wordList:
        wordDict.update({word: wordDict.setdefault(word, 0)+1})

    # 按词频降序排序
    wordDictList = [(key, value) for (key, value) in wordDict.items()]
    wordDictList.sort(key=lambda x: x[1], reverse=True)
    wordDict = dict(wordDictList)

    # 封装成dataframe
    df = pandas.DataFrame(data=wordDict, index=['数值'])
    df = df.transpose().reset_index()
    df.columns = ['名词', '数值']

    return df


entry = EntryPoint()
entry.output.dataset = ...
