# 快速设置指南

**仅测试过 Debian 系统**

要快速轻松地使用默认配置设置此项目，你可以使用开发者提供的一键脚本。但是，建议在继续之前阅读使用文档。

## 客户端

1. 下载[客户端设置脚本](../scripts/client.sh)并以root权限执行它。
2. 脚本将执行以下任务：
   - 尝试创建目录"/opt/ping-charts"。
   - 从[releases](https://github.com/eastarpen/ping-charts/releases)页面下载预编译的客户端。
   - 下载[客户端模板配置](../doc/templates/client.yaml)。
   - 将客户端systemd服务配置文件下载到"/etc/systemd/system/"。

执行脚本后，请按照以下步骤操作：

1. 根据你的服务器配置重写'/opt/ping-charts/client.yaml'文件。
2. 运行命令`systemctl start pingChartsClient.timer`启动客户端。这将每分钟对你的目标进行ping并将数据上传到服务器。
3. 如果需要，运行命令`systemctl enable pingChartsClient.timer`以使客户端在操作系统重新启动后自动启动。

**注意事项：**
- 如果你不更改服务配置文件，则客户端配置文件必须命名为'client.yaml'。

## 服务器

1. 下载[服务器设置脚本](../scripts/server.sh)并以root权限执行它。
2. 脚本将执行以下任务：
   - 尝试创建目录"/opt/ping-charts"。
   - 从[releases](https://github.com/eastarpen/ping-charts/releases)页面下载预编译的服务器。
   - 下载[服务器模板配置](../doc/templates/server.yaml)。
   - 将服务器systemd服务配置文件下载到"/etc/systemd/system/"。

执行脚本后，请按照以下步骤操作：

1. 根据你的客户端配置重写'/opt/ping-charts/server.yaml'文件。
2. 运行命令`systemctl start pingChartsServer`启动服务器。
3. 如果需要，运行命令`systemctl enable pingChartsServer`以使服务器在操作系统重启后自动启动。

**注意事项**

- 如果你不更改服务配置文件，则服务器配置文件必须命名为'server.yaml'。
- 服务器将在端口8000上运行。
- 服务将监听来自'0.0.0.0'的请求。

## 自定义

**在进行任何更改之前，请确保你理解自己在做什么。**

如果你对默认设置不满意，可以自定义服务文件以满足你的需求。

首先，确保客户端和服务器正常运行。有关更多信息，请参阅[Usage](../README.md#Usage)。

接下来，修改服务配置文件：

- 服务器："/etc/systemd/system/pingChartsServer.service"
- 客户端："/etc/systemd/system/pingChartsClient.service"和"/etc/systemd/system/pingChartsClient.timer"
