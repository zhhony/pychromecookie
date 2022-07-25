import threading
from urllib.parse import *
from urllib.request import *
from typing import *


class Downunit():
    def __init__(self, url: str, path: str, threadnum: int = 3) -> None:
        self.url = url
        self.path = path
        self.threadnum = threadnum
        self.CONTENT_LENGTH = 0
        self.headers = {}

    def Download(self):
        request = Request(url=self.url, headers=self.headers)
        self.file = urlopen(request)
        self.CONTENT_LENGTH = int(dict(
            self.file.headers).get('Content-Length', 0))
        self.file.close()

        unitBox = self.CONTENT_LENGTH//self.threadnum + 1  # 每个线程所负责的下载大小

        for i in range(self.threadnum):
            os_Start = i * unitBox  # 下载的起点

            f = open(self.path, 'wb')
            f.seek(os_Start, 0)
            td = DownThread(self.url, self.headers, f, os_Start, unitBox)
            td.start()


class DownThread(threading.Thread):
    def __init__(self, url, headers, file, os_Start, unitBox) -> None:
        super().__init__()
        self.url = url
        self.headers = headers
        self.file = file
        self.os_Start = os_Start
        self.unitBox = unitBox

    def run(self):
        request = Request(url=self.url, headers=self.headers)
        f = urlopen(request)

        # 移动光标到下载开始的位置
        for i in range(self.os_Start):
            f.read(1)

        lenth = 0
        while lenth < self.unitBox:
            page = f.read(1024)
            if page is None or len(page) <= 0:
                break
            self.file.write(page)
            lenth += len(page)
        f.close()
        self.file.close()
