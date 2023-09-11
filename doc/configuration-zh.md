# 配置说明

确保客户端的配置与服务器配置相匹配，否则服务器将忽略客户端上传请求。

## 客户端

[客户端模板](./templates/client.yaml)

- 确保客户端的 "name"、"clientId" 和 "passw" 与服务器配置相同。
- `uploadUrl` 为 'http(s):/service.address/upload'。

  例如：

  | 服务地址               | uploadUrl                       |
  | ---------------------- | ------------------------------- |
  | http://127.0.0.1:8000  | http://127.0.0.1:8000/upload    |
  | http://domain.com      | http://domain.com/upload        |
  | http://domain.com/ping | http://domain.com/ping/upload   |

- targets 必须预先在服务器配置中注册，否则该数据将被忽略。

```yaml
name: client                # 客户端名称，允许重复
clientId: 1                 # 客户端 ID，整数，不允许重复
passw: password             # 客户端密码，字符串
uploadUrl: url              # 服务器上传 URL
targets:                    # 目标列表
- id: 1                     # 目标 ID，整数，不允许重复
  name: chinanet            # 目标名称，字符串，允许重复
  port: 80                  # 目标端口，整数
  addr: ct.tz.cloudcpp.com  # 目标地址，可以是 IP 或域名
- id: 2
  name: chinaunicom
  port: 80
  addr: cu.tz.cloudcpp.com
```

## 服务器

[服务器模板](./templates/server.yaml)

注意对同一个 target, 服务端和客户端的 id 和 name 必须一致.

alias 用来快速更改 target 在前端的显示名称

```yaml
targets:               # 注册目标
  - name: chinanet     # 目标名称，字符串，允许重复
    id: 1              # 目标 ID，整数，不允许重复
    alias: china-net   # 不必填。如果存在,将显示在网页中(忽略name的值)
  - name: chinaunicom
    id: 2
  - name: chinamobile
    id: 3
clients:
  - name: client       # 客户端名称，允许重复
    label: US          # 客户端标签，字符串，将显示在网页中
    pass: password     # 客户端密码，字符串
    id: 1              # 客户端 ID，整数，不允许重复
```
