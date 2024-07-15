## 一、项目配置相关信息
### 更新数据库  
`alembic init alembic`  
`alembic revision --autogenerate`  
`alembic upgrade head`   
`pip freeze > requirements.txt`

### 数据库配置参考
    https://blog.csdn.net/zyl495843236/article/details/135870949?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522172016836116800226543694%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=172016836116800226543694&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-135870949-null-null.142^v100^control&utm_term=fastapi%20alembic&spm=1018.2226.3001.4187
    https://blog.csdn.net/weixin_53999905/article/details/132433250?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522172018248716800211513462%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=172018248716800211513462&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-132433250-null-null.142^v100^control&utm_term=fastapi%20alembic&spm=1018.2226.3001.4187







## 二、后端接口说明文档
### 1、用户部分
用户名和email不可重复  
验证码5分钟自动过期

* 注册接口:`http://0.0.0.0:8080/api/user/register/{captcha}`  
参数:
```json
{
  "name": "string",
  "password":"string",
  "email": "1153592594@qq.com"

}
```
返回:
```json
{
    "code": 200,
    "msg": "请求成功",
    "data": {
        "name": "chen77",
        "password": "password",
        "email": "1153592594@qq.com",
        "role": 1000
    }
}
```
或者  
```json
{
    "code": 400,
    "msg": "请求错误",
    "data": "注册失败,用户名重复"
}
```
  
  
  
* 登录接口:`http://0.0.0.0:8080/api/user/login`  
参数:  
```json
{
  "name": "chen77",
  "password":"password"
}

```

返回值:
```json
{
    "code": 200,
    "msg": "请求成功",
    "data": {
      "username":"czy",
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNoZW4iLCJleHAiOjE3MjA2ODc1NzZ9.PCkfhzKwRH46HDUAYCUxYbcPog5FjZeDvcGzCfOpAso"
    }
}
```
或者  
```json
{
    "code": 400,
    "msg": "请求错误",
    "data": "用户名或密码错误"
}
```

* 创建俱乐部接口:`http://0.0.0.0:8080/api/user/createClub`  
参数:
```json
{
  "name": "chemistry united",
  "avatar":1
}
```
返回值:  
```json
{
    "code": 400,
    "msg": "请求错误",
    "data": "创建俱乐部失败"
}
```  
或者:  
```json
{
    "code": 200,
    "msg": "请求成功",
    "data": {
        "name": "chemistry united",
        "id": 10,
        "captain": 1
    }
}
```

* 发送验证码接口:`http://0.0.0.0:8080/api/user/sendEmail/{toaddr}`
返回:  
```json
{
    "code": 200,
    "msg": "请求成功",
    "data": "验证码已发送"
}
```
或者:
```json
{
    "code": 400,
    "msg": "请求错误",
    "data": "邮箱格式不正确"
}
```

* 更新用户信息接口:`http://0.0.0.0:8080/api/user/update`
参数:  
```json
{
  "name": "string",
  "password": "string",
  "role": 0,
  "email": "string",
  "avatar": 0
}
```
返回:  
```json
{
    "code": 200,
    "msg": "请求成功",
    "data": "修改成功"
}
```
或者:
```json
{
    "code": 400,
    "msg": "请求错误",
    "data": "邮箱格式不正确"
}
```
```json
{
    "detail": "Token无效或已过期"
}
```
* 更新用户头像接口:`http://0.0.0.0:8080/api/user/updateAvatar`
参数:  
```json
{
    "avatar":7
}
```
返回:  
```json
{
    "code": 200,
    "msg": "请求成功",
    "data": "修改成功"
}
```
或者:
```json
{
    "code": 400,
    "msg": "请求错误",
    "data": "邮箱格式不正确"
}
```

* 更新用户密码接口:`http://0.0.0.0:8080/api/user/reset/{captcha}`
参数:  
```json
{
  "password":"password1"
}
```
返回:  
```json
{
    "code": 200,
    "msg": "请求成功",
    "data": "修改成功"
}
```
或者:
```json
{
    "code": 400,
    "msg": "请求错误",
    "data": "邮箱格式不正确"
}
```

* 获取头像列表接口:`http://0.0.0.0:8080/api/user/avatar`
返回:  
```json
{
    "code": 200,
    "msg": "请求成功",
    "data": {
      "1": "*********"
    }
}
```