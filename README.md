# 贴图库的批量上传工具

批量上传某文件夹的内容（图片）到贴图库，并将与图片URL等信息对应存储到`pver.py`相同目录。

不支持带空格的路径。



# 使用方式

在pver.py同目录下创建config.json。

```json
{
    "ACCESSKEY": "。。。",
    "SECRETKEY": "。。。",
    "aid": "1334486",
    "httptype": "1",
    "SUFFIX_LIST":"png,gif,jpg,jpeg",
    "ul_from":"file" ,
    "upurl":"http://up.imgapi.com/"
}
```

### 在命令行使用

`python pver.py <dir> <md>` 

【dir】必选。将绝对路径为dir的目录里所有后缀包含于SUFFIX_LIST的图片文件上传到你的key对应的相册里。成功和失败的结果会存储到`success.json`和`failure.json`里。

【md】可选。如果声明了md，可以将md里与上传文件同名的字符串改为markdown格式的外链。

## 内容说明

| key                  | value                                    |
| -------------------- | ---------------------------------------- |
| ACCESSKEY/ SECRETKEY | http://www.tietuku.com/manager/manager   |
| aid                  | 相册ID。http://www.tietuku.com/manager/album |
| httptype             | 1 返回的图片链接为http,2 返回的图片链接为https           |
| SUFFIX_LIST          | 图片后缀名列表，英文逗号隔开。                          |
| from                 | `from`的可填写的值只能为`web`和`file`通过URL方式上传图片必须填写为`web` |
| upurl                | 并不需要更改- =+                               |
|                      |                                          |