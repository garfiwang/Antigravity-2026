#!/usr/bin/env python3
"""
信用卡電子帳單下載工具
支援：渣打、玉山、元大、台新、聯邦、中國信託、台北富邦、永豐
"""

import os
import base64
import json
import pickle
from pathlib import Path
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ── 設定 ──────────────────────────────────────────────
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# 預設把帳單下載到 Documents/checkbill/帳單
DOWNLOAD_DIR = Path("/Users/garfiwang/Documents/checkbill/帳單")
if not DOWNLOAD_DIR.parent.exists():
    # 如果 checkbill 目錄不存在，則下載到腳本同目錄下
    DOWNLOAD_DIR = Path(__file__).parent / "帳單"

# 優先讀取 checkbill/ 下的憑證與 token，避免重複授權
CREDENTIALS_FILE = Path("/Users/garfiwang/Documents/checkbill/credentials.json")
if not CREDENTIALS_FILE.exists():
    CREDENTIALS_FILE = Path(__file__).parent / "credentials.json"

TOKEN_FILE = Path("/Users/garfiwang/Documents/checkbill/token.pickle")
if not TOKEN_FILE.exists():
    TOKEN_FILE = Path(__file__).parent / "token.pickle"

# 各銀行識別關鍵字（用於命名資料夾）
BANK_MAP = {
    "esunbank.com":         "玉山銀行",
    "estmt.com.tw":         "元大銀行",
    "taishinbank.com.tw":   "台新銀行",
    "bhurecv.taishinbank":  "台新銀行",
    "ubot.com.tw":          "聯邦銀行",
    "ctbcbank.com":         "中國信託",
    "estats.ctbcbank":      "中國信託",
    "taipeifubon.com.tw":   "台北富邦",
    "bhu.taipeifubon":      "台北富邦",
    "banksinopac.com.tw":   "永豐銀行",
    "newebill.banksinopac": "永豐銀行",
    "standardchartered":    "渣打銀行",
    "sc.com":               "渣打銀行",
}

SEARCH_QUERY = (
    'subject:(帳單 OR 電子帳單 OR 信用卡帳單) '
    '(渣打 OR 玉山 OR 元大 OR 台新 OR 聯邦 OR 中國信託 OR 台北富邦 OR 永豐) '
    'has:attachment filename:pdf'
)
# ─────────────────────────────────────────────────────


def get_gmail_service():
    creds = None
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'rb') as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        except Exception as e:
            print(f"⚠️ Token refresh failed ({e}), initiating fresh login...")
            creds = None

        if not creds or not creds.valid:
            if not CREDENTIALS_FILE.exists():
                print(f"❌ 找不到 {CREDENTIALS_FILE}")
                print("請先確認 credentials.json 存在於 /Users/garfiwang/Documents/checkbill/ 中")
                raise SystemExit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as f:
            pickle.dump(creds, f)

    return build('gmail', 'v1', credentials=creds)


def get_bank_name(sender: str) -> str:
    sender_lower = sender.lower()
    for key, name in BANK_MAP.items():
        if key in sender_lower:
            return name
    return "其他銀行"


def get_email_date(headers: list) -> str:
    for h in headers:
        if h['name'] == 'Date':
            try:
                # 解析各種日期格式，統一輸出 YYYYMM
                from email.utils import parsedate_to_datetime
                dt = parsedate_to_datetime(h['value'])
                return dt.strftime('%Y%m')
            except Exception:
                pass
    return "未知日期"


def get_email_subject(headers: list) -> str:
    for h in headers:
        if h['name'] == 'Subject':
            return h['value']
    return "無主旨"


def download_attachments(service, msg_id: str, bank: str, date_str: str, subject: str):
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    parts = msg.get('payload', {}).get('parts', [])

    saved = []
    for part in parts:
        filename = part.get('filename', '')
        if not filename.lower().endswith('.pdf'):
            continue

        body = part.get('body', {})
        attachment_id = body.get('attachmentId')
        if not attachment_id:
            # 小檔案直接在 body.data
            data = body.get('data', '')
        else:
            att = service.users().messages().attachments().get(
                userId='me', messageId=msg_id, id=attachment_id
            ).execute()
            data = att.get('data', '')

        if not data:
            continue

        pdf_bytes = base64.urlsafe_b64decode(data)

        # 建立儲存資料夾：帳單/玉山銀行/
        folder = DOWNLOAD_DIR / bank
        folder.mkdir(parents=True, exist_ok=True)

        # 檔名：202602_玉山銀行_信用卡帳單.pdf
        safe_subject = subject.replace('/', '-').replace('\\', '-')[:30]
        out_path = folder / f"{date_str}_{bank}_{safe_subject}.pdf"

        # 避免重複下載
        if out_path.exists():
            print(f"  ⏭  已存在，跳過：{out_path.name}")
            continue

        out_path.write_bytes(pdf_bytes)
        saved.append(out_path)
        print(f"  ✅ {out_path.relative_to(DOWNLOAD_DIR.parent)}")

    return saved


def fetch_all_message_ids(service, query: str) -> list:
    ids = []
    page_token = None
    while True:
        kwargs = {'userId': 'me', 'q': query, 'maxResults': 500}
        if page_token:
            kwargs['pageToken'] = page_token
        result = service.users().messages().list(**kwargs).execute()
        ids.extend([m['id'] for m in result.get('messages', [])])
        page_token = result.get('nextPageToken')
        if not page_token:
            break
    return ids


def main():
    print("=" * 50)
    print("  信用卡電子帳單下載工具")
    print("=" * 50)

    service = get_gmail_service()
    print(f"\n🔍 搜尋帳單郵件中...")
    ids = fetch_all_message_ids(service, SEARCH_QUERY)
    print(f"   找到 {len(ids)} 封郵件\n")

    total_saved = 0
    for i, msg_id in enumerate(ids, 1):
        # 先取 metadata 判斷銀行與日期
        meta = service.users().messages().get(
            userId='me', id=msg_id, format='metadata',
            metadataHeaders=['From', 'Date', 'Subject']
        ).execute()
        headers = meta.get('payload', {}).get('headers', [])

        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
        bank = get_bank_name(sender)
        date_str = get_email_date(headers)
        subject = get_email_subject(headers)

        print(f"[{i}/{len(ids)}] {bank} {date_str} — {subject[:40]}")

        saved = download_attachments(service, msg_id, bank, date_str, subject)
        total_saved += len(saved)

    print(f"\n{'=' * 50}")
    print(f"  完成！共下載 {total_saved} 個 PDF 檔案")
    print(f"  儲存位置：{DOWNLOAD_DIR}")
    print("=" * 50)


if __name__ == '__main__':
    main()
