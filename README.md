# 企业微信群机器人测试

使用 Python 向企业微信群机器人发送一条文本消息：`hello world`。

当前实现针对**企业微信群机器人 Webhook**，不适用于普通微信群、钉钉或飞书。

## 环境要求

Python 3.9 或更高版本，仅使用标准库，无需执行 pip install。

## 使用方法

1. 在目标企业微信群中添加群机器人（或使用现有机器人），复制其 Webhook 地址。
2. 在运行脚本的同一个终端中设置环境变量。
3. 执行脚本，每次执行只发送一条 `hello world`。

### Windows PowerShell

```powershell
$env:WECOM_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=替换为你的机器人KEY"
python send_hello_world.py
```

### Windows CMD

```bat
set "WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=替换为你的机器人KEY"
python send_hello_world.py
```

### Linux / macOS

```bash
export WECOM_WEBHOOK_URL='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=替换为你的机器人KEY'
python3 send_hello_world.py
```

成功时输出：

```text
发送成功：hello world
```

## 在 PyCharm 中运行

打开 Run → Edit Configurations，选择 `send_hello_world.py` 对应的运行配置，
在 Environment variables 中添加 `WECOM_WEBHOOK_URL`，值为完整 Webhook 地址，然后运行。

## 配置与故障排查

- Webhook 地址属于凭据，请仅在本地环境变量中设置，不要提交到仓库或写入公开日志。
- 只设置环境变量即可；脚本不会自动加载 .env 文件。
- 未设置地址、地址格式错误、HTTP/网络错误、无效 JSON 或业务失败时，脚本返回退出码 1。
- 请求超时为 10 秒，不自动重试。超时后应先检查群消息，避免手动重试造成重复发送。
- 若机器人未确认成功，请检查机器人是否仍在群内、Webhook 是否有效及是否触发限流。

## 验证说明

已通过模拟请求验证 POST 消息内容、成功响应、业务失败、无效响应、网络异常和缺少配置等情况。
未配置真实 Webhook，尚未进行真实群消息发送验证。

官方接口说明：https://developer.work.weixin.qq.com/document/path/91770
