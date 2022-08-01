# pychromecookie

## modules模组文件夹

### conn.py

用于定义针对SQlite数据库的上下文连接器，可以调用with语句方便管理数据库连接。

- **Conn类**    继承自sqlite3.Connection类，需指定SQlite文件`Cookies`的位置。如果是windows系统一般默认放在 `%LOCALAPPDATA%`内的 `\Google\Chrome\User Data\Default\network\`文件夹下。具备两个内置方法：

  - **`__enter__`**   调用with进入上下文管理器，并返回Connection.cursor()对象；
  - **`__exit__`**    退出上下文管理器；
  - **范例：**

    ```python
    dbCookies = os.environ['LOCALAPPDATA'] + r'\Google\Chrome\User Data\Default\network\Cookies'
    KEY_WORD = r'%bailuzhiku%'
    with Conn(dbCookies) as cur:
        sql = """select creation_utc,host_key,name,encrypted_value,path from cookies where host_key like '%s'""" % KEY_WORD
        cur.execute(sql)
        valCookiesWithEncode = cur.fetchall()
    # 上述范例是一个从指定位置获取cookie的完整过程。最终所返回的valCookiesWithEncode是一个多维列表，存储了cookie的若干参数，比如有效时间、域名、key、value等。需要注意的是，这里获取的value是加密的。
    ```

### decode.py

用于获取密钥、以及解开被加密的cookie参数。有如下函数：

- 函数:

  - **DecodeKey**    用于将密钥解析出来。需指定密钥文件Local state的位置。如果是Windows系统，它默认是存储在 `%LOCALAPPDATA%`下的 `Google\Chrome\User Data`文件夹下。
  - **DecodeValue**    用于将cookie中加密的value解密出来。需指定待解密的字符串以及密钥。
  - **范例**：

    ```python
    fileLocalState = os.environ['LOCALAPPDATA'] + r'\Google\Chrome\User Data\Local State'
    key = DecodeKey(fileLocalState)
    value = DecodeValue('!@#$%%^^&$', key)
    ```

### cookie.py

用于生成cookie文件。需提供解密后的cookie内容。

- **Cookie类**    生成cookie的类，需提供解密后的cookie内容。有如下几个生成方法：

  - **getOne**    将生成的cookie封装成一个cookie生成器并返回；
  - **getAll**    将所有生成的cookie条目打印到控制台；
  - **getOutFile**    将生成的cookie输出到指定路径中；
  - **范例：**

    ```python
        valCookiesWithDecode = [('aaaa','bbbb','cccc','dddd','eeee')]
        cookies = Cookie(valCookiesWithDecode)
        cookies.getOutFile()
    ```

### download.py

用于下载文件。

- **Downunit类**
用于实现下载文件的类。需要指定资源路径，输出文件的路径和名称，以及需要启用的线程数量（默认为3）。有如下方法：

  - Download    执行下载任务；

- **DownThread类**
用于实现派送线程任务的类。有如下方法：

  - run    建立一个执行下载任务的线程；
