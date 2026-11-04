"""使用企业微信群机器人发送一条 hello world（仅依赖 Python 标准库）。"""

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit
from urllib.request import Request, urlopen


def send_hello_world(webhook_url):
    """发送一次消息，超时或失败不自动重试，避免重复推送。"""
    webhook_url = webhook_url.strip()
    url = urlsplit(webhook_url)
    if (
        url.scheme != "https"
        or url.netloc != "qyapi.weixin.qq.com"
        or url.path != "/cgi-bin/webhook/send"
        or not any(parse_qs(url.query).get("key", []))
        or url.fragment
    ):
        raise ValueError("请配置有效的企业微信群机器人 Webhook 地址。")

    payload = {"msgtype": "text", "text": {"content": "hello world"}}
    request = Request(
        webhook_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"HTTP 请求失败，状态码：{exc.code}") from None
    except (URLError, TimeoutError, OSError):
        raise RuntimeError("网络请求失败或超时，请检查网络后确认群内是否已收到消息。") from None
    except (ValueError, UnicodeError):
        raise RuntimeError("机器人返回的内容不是有效的 JSON。") from None

    if not isinstance(result, dict) or result.get("errcode") != 0:
        # 不输出原始响应，避免日志意外包含 Webhook 密钥。
        raise RuntimeError("机器人未确认发送成功，请检查 Webhook 是否有效或是否触发限流。")
    return result


def main():
    webhook_url = os.environ.get("WECOM_WEBHOOK_URL", "").strip()
    if not webhook_url:
        print("请先设置环境变量 WECOM_WEBHOOK_URL。", file=sys.stderr)
        return 1
    try:
        send_hello_world(webhook_url)
    except (ValueError, RuntimeError) as exc:
        print(f"发送失败：{exc}", file=sys.stderr)
        return 1
    print("发送成功：hello world")
    return 0


if __name__ == "__main__":
    sys.exit(main())
