# pychromecookie

## <font color = blue>modules</font>模组文件夹

获取cookie，解密cookie、输出cookie、下载文件

### <font color = red>conn.py</font>

用于定义SQlite数据库上下文管理器，通过with语句管理对cookie文件的访问。

- **Conn类**    继承自sqlite3.Connection类，需指定cookie件位置。Windows系统默认放在 %LOCALAPPDATA%内的 \Google\Chrome\User Data\Default\network\文件夹下，名为Cookies。具备两个内置方法：

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

### <font color = red>decode.py</font>

用于获取密钥和解密。包含如下函数：

- 函数:

  - **DecodeKey**    用于获取密钥。需指定密钥的位置。Windows系统默认放在 `%LOCALAPPDATA%`下的 `Google\Chrome\User Data`文件夹下,名为Local state。
  - **DecodeValue**    用于解密。需指定待解密的字符串以及密钥。
  - **范例**：

    ```python
    fileLocalState = os.environ['LOCALAPPDATA'] + r'\Google\Chrome\User Data\Local State'
    key = DecodeKey(fileLocalState)
    value = DecodeValue('!@#$%%^^&$', key)
    ```

### <font color = red>cookie.py</font>

用于生成cookie文件。

- **Cookie类**    生成cookie的类。有如下几个生成方法：

  - **getOne**    将生成的cookie封装成一个cookie生成器并返回；
  - **getAll**    将所有生成的cookie条目打印到控制台；
  - **getOutFile**    将生成的cookie输出到指定路径中；
  - **范例：**

    ```python
    # 注意Cookies的加密参数必须解密，否则生成的文件不能用
    valCookiesWithDecode = [('aaaa','bbbb','cccc','dddd','eeee')]
    cookies = Cookie(valCookiesWithDecode)
    cookies.getOutFile()
    ```

### <font color = red>download.py</font>

用于下载文件。

- **Downunit类**    实现下载的类，依托于DownThread类。需要指定资源url、输出文件的路径和名称，以及需要启用的线程数量（默认为3）。有如下方法：

  - Download    执行下载任务；
- **DownThread类**    实现派送线程的类。有如下方法：

  - run    建立一个线程,用于下载；

## <font color = blue>resource</font>资源文件夹

存储一些参数

### <font color = red>config</font>

这是生成cookie的必要配置文件。从chrome获取的cookie共5个参数，但是实际生成cookie需要7个，额外的2个存在这里。参数值是bool形式的，具体是True还是False是试出来的，目前没找到对应的含义和规律。

### <font color = red>map_pin.jpg</font>

这是衍生工程：中国政府词频报告所用的模板，可以无视。

### <font color = red>simhei.ttf</font>

这是衍生工程：中国政府词频报告所用的字体，可以无视。

## <font color = blue>scripts</font>脚本文件夹

放的是一些衍生工程
