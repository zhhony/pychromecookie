import pandas
import os
import jieba
import jieba.analyse as analyse
import jieba.posseg as posseg
import paddle
from pathlib import Path
from zhon.hanzi import punctuation
from yonghong.script.port import EntryPoint, ResourceType
from typing import *


pandas.set_option('display.unicode.east_asian_width', True)
pandas.set_option('display.unicode.ambiguous_as_wide', True)


def replace_(text: str, *args) -> str:
    '''用于将文本中多余的字符去掉，*args支持自定义添加'''

    # 构建替换关键字
    replaceList = ['\n', '\r', '\xa0', '/']
    for i in range(10):
        replaceList.append(str(i))
    for i in punctuation:
        replaceList.append(i)
    for i in args:
        replaceList.append(i)

    # 替换文本
    for i in replaceList:
        text = text.replace(i, '')
    return text


def lcut(fp: IO) -> list:
    '''用于统计文件中的词频，返回词语和词性'''

    # 替换文本
    text = replace_(fp.read(), '和', '的')

    # 切割词语
    paddle.enable_static()
    jieba.enable_paddle()
    return posseg.lcut(text, use_paddle=True)


if __name__ == '__main__':

    LOCAL_USER_PROFILE = os.environ['USERPROFILE']

    path = Path(LOCAL_USER_PROFILE + '/Desktop/新建文件夹')

    # 获取path内的文件
    fileList = [i for i in path.glob('**/*.txt')]

    # 存储每个文件的词频dataframe
    fileFrequencyList = []
    for file in fileList:

        FILE_NAME = file.name

        with open(file=file, mode='r') as f:
            # 获取词频清单
            wordFrequency = lcut(f)

        wordDict = dict()
        for word, flag in wordFrequency:
            wordDict.update(
                {word: [wordDict.setdefault(word, [0, flag])[0]+1, flag]})

        # 按词频降序排序
        wordDictList = [(key, value) for (key, value) in wordDict.items()]
        wordDictList.sort(key=lambda x: x[1], reverse=True)
        wordDict = dict(wordDictList)

        # 封装成dataframe
        df = pandas.DataFrame(data=wordDict)
        df = df.transpose().reset_index()
        df.columns = ['词语', '数值', '词性']
        fileFrequencyList.append(df)

        with pandas.ExcelWriter('abc.xlsx', mode='a') as xlsx:
            df.to_excel(xlsx, sheet_name=FILE_NAME)
            xlsx.save()

    print(fileFrequencyList)
