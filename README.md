# 邮件转发服务
## 支持邮件内容展示格式
### 1. json
### 2. html 
## json格式api接口说明
### 请求地址
http://127.0.0.1:8080/xxxxxx/v1/email
### 请求方法
POST
### 请求参数
名称|类型|必填项|描述|
---|---|---|---
smtp_server|string|Y|公司smtp服务域名
smtp_user|string|Y|发件人smtp用户名
smtp_password|string|Y|发件人smtp用户密码
from_addr|string|Y|发件人smtp邮箱	
to_addr|list|Y|收件人smtp邮箱列表
subject|string|Y|邮件主题
content|dict|Y|邮件内容
content_type|string|Y|邮件内容展示格式


```
# 示例
 {
       "smtp_server": "smtp.xxx.com",
        "smtp_user": "xxx",
        "smtp_password": "xxxxxx",
        "from_addr": "xxxxxx<xxx@xxx.com>",
        "to_addr": ["xxxxxx<xxx@xxx.com>"],
        "subject": "test",
        "content": {
        			"key1": "value1",
        			"key2": "value2"
        				},
        "content_type":"json"
    }
```

## html格式api接口说明
### 请求地址
http://127.0.0.1:8080/xxxxxx/v1/email/{service}
### 请求方法
POST
### 请求参数
名称|类型|必填项|描述|
---|---|---|---
smtp_server|string|Y|公司smtp服务域名
smtp_user|string|Y|发件人smtp用户名
smtp_password|string|Y|发件人smtp用户密码
from_addr|string|Y|发件人smtp邮箱	
to_addr|list|Y|收件人smtp邮箱列表
subject|string|Y|邮件主题
content|dict|Y|邮件内容
content_type|string|Y|邮件内容展示格式

```
# 示例
 {
       "smtp_server": "smtp.xxx.com",
        "smtp_user": "xxx",
        "smtp_password": "xxxxxx",
        "from_addr": "xxxxxx<xxx@xxx.com>",
        "to_addr": ["xxxxxx<xxx@xxx.com>"],
        "subject": "test",
        "content": "<html></html>",
        "content_type":"html"
    }
```
>提示：html格式需添加html模板，如有需要请联系我，谢谢！

