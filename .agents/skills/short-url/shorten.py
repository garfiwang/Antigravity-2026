#!/usr/bin/env python3
"""
Reurl.cc 縮短網址工具
支援命令列執行、Python 模組調用、UTM 參數與自動複製剪貼簿。
"""

import sys
import os
import json
import argparse
import subprocess
import urllib.request
import urllib.error

DEFAULT_API_URL = "https://api.reurl.cc/shorten"
FALLBACK_API_KEY = "4070ff49d794e43215533b663c974755ecd4b734919304df8a38b58d65165567c4f5d6"

def get_api_key(custom_key=None):
    if custom_key:
        return custom_key
    if os.environ.get("REURL_API_KEY"):
        return os.environ["REURL_API_KEY"]
    
    # Check ~/.reurl.env
    env_path = os.path.expanduser("~/.reurl.env")
    if os.path.isfile(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("REURL_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass
            
    # Check local .env
    if os.path.isfile(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("REURL_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except Exception:
            pass

    return FALLBACK_API_KEY

def copy_to_clipboard(text):
    """將文字複製到 macOS 剪貼簿"""
    try:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, close_fds=True)
        process.communicate(input=text.encode('utf-8'))
        return True
    except Exception:
        return False

def shorten_url(url, utm=None, api_key=None, api_url=None):
    """
    縮短網址核心函式
    :param url: 原始長網址 (str)
    :param utm: UTM 字典 (dict, 選填)，例如 {"utm_source": "rich", "utm_medium": "agent"}
    :param api_key: Reurl API Key (選填)
    :param api_url: Reurl API 端點 (選填)
    :return: dict 包含 {"res": "success", "short_url": "...", "original_url": "..."}
    """
    key = get_api_key(api_key)
    endpoint = api_url or os.environ.get("REURL_API_URL", DEFAULT_API_URL)
    
    if not url:
        raise ValueError("URL 不能為空")
        
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    payload = {"url": url}
    if utm:
        # 過濾空值的 utm
        valid_utm = {k: v for k, v in utm.items() if v}
        if valid_utm:
            payload["utm"] = valid_utm

    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data_bytes,
        headers={
            "Content-Type": "application/json",
            "reurl-api-key": key,
            "User-Agent": "Antigravity-Reurl/1.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_body = response.read().decode("utf-8")
            result = json.loads(res_body)
            if result.get("res") == "success" or "short_url" in result:
                return result
            else:
                raise RuntimeError(f"Reurl API 錯誤: {result}")
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8") if e.fp else str(e)
        raise RuntimeError(f"HTTP 請求失敗 ({e.code}): {err_msg}")
    except Exception as e:
        raise RuntimeError(f"縮短網址失敗: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Reurl.cc 縮短網址工具")
    parser.add_argument("url", nargs="?", help="要縮短的原始長網址")
    parser.add_argument("--key", "-k", help="指定 API Key")
    parser.add_argument("--utm-source", help="UTM 來源 (utm_source)")
    parser.add_argument("--utm-medium", help="UTM 媒介 (utm_medium)")
    parser.add_argument("--utm-campaign", help="UTM 活動名稱 (utm_campaign)")
    parser.add_argument("--utm-term", help="UTM 關鍵字 (utm_term)")
    parser.add_argument("--utm-content", help="UTM 內容 (utm_content)")
    parser.add_argument("--copy", "-c", action="store_true", help="自動複製短網址至剪貼簿 (macOS)")
    parser.add_argument("--quiet", "-q", action="store_true", help="只輸出短網址字串")
    parser.add_argument("--json", "-j", action="store_true", help="輸出 JSON 格式結果")

    args = parser.parse_args()

    # 讀取 URL：來自參數或 stdin
    url = args.url
    if not url:
        if not sys.stdin.isatty():
            url = sys.stdin.read().strip()
        else:
            parser.print_help()
            sys.exit(1)

    utm = {}
    if args.utm_source: utm["utm_source"] = args.utm_source
    if args.utm_medium: utm["utm_medium"] = args.utm_medium
    if args.utm_campaign: utm["utm_campaign"] = args.utm_campaign
    if args.utm_term: utm["utm_term"] = args.utm_term
    if args.utm_content: utm["utm_content"] = args.utm_content

    try:
        res = shorten_url(url, utm=utm if utm else None, api_key=args.key)
        short_url = res.get("short_url")

        copied = False
        if args.copy:
            copied = copy_to_clipboard(short_url)

        if args.json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif args.quiet:
            print(short_url)
        else:
            print(f"🔗 原始網址: {res.get('original_url', url)}")
            print(f"✨ 短網址  : {short_url}")
            if args.copy:
                print(f"📋 已自動複製到剪貼簿！" if copied else "⚠️ 剪貼簿複製失敗")
    except Exception as e:
        sys.stderr.write(f"❌ 錯誤: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
