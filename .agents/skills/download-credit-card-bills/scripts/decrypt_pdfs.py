#!/usr/bin/env python3
"""
解密3月帳單 PDF
執行後按提示輸入各家銀行密碼，解密後存到「帳單_解密」資料夾
"""
import getpass
import os
import fitz  # PyMuPDF
from pathlib import Path

# 優先指向 checkbill 專案目錄
BASE = Path("/Users/garfiwang/Documents/checkbill/帳單")
if not BASE.parent.exists():
    BASE = Path(__file__).parent / "帳單"

OUT  = Path("/Users/garfiwang/Documents/checkbill/帳單_解密")
if not OUT.parent.exists():
    OUT = Path(__file__).parent / "帳單_解密"

# 3月帳單清單（pdf路徑, 銀行名, 密碼說明）
BILLS = [
    (BASE / "台新銀行/202603_台新銀行_台新信用卡電子帳單 2026年3月.pdf",
     "台新銀行", "身分證字號後2碼 + 生日月日4碼（共6碼，例如 AB0102）"),

    (BASE / "中國信託/202603_中國信託_中國信託信用卡電子帳單 11503.pdf",
     "中國信託", "身分證字號（英文大寫，共10碼）"),

    (BASE / "聯邦銀行/202603_聯邦銀行_聯邦銀行信用卡電子帳單(2026年03月).pdf",
     "聯邦銀行", "身分證字號（英文大寫，共10碼）"),

    (BASE / "元大銀行/202603_元大銀行_元大銀行115年02月份『信用卡電子帳單』.pdf",
     "元大銀行", "身分證字號（英文大寫，共10碼）"),

    (BASE / "玉山銀行/202603_玉山銀行_玉山銀行2026年02月信用卡電子帳單.pdf",
     "玉山銀行", "身分證字號（英文大寫，共10碼）"),
]

OUT.mkdir(exist_ok=True)

for pdf_path, bank, hint in BILLS:
    if not pdf_path.exists():
        print(f"⚠️  找不到：{pdf_path.name}，跳過")
        continue

    print(f"\n{'='*50}")
    print(f"  銀行：{bank}")
    print(f"  密碼：{hint}")
    pw = getpass.getpass("  請輸入密碼（輸入時不顯示）：")

    doc = fitz.open(str(pdf_path))
    if doc.is_encrypted:
        if not doc.authenticate(pw):
            print(f"  ❌ 密碼錯誤，跳過 {bank}")
            doc.close()
            continue

    out_path = OUT / f"{bank}_202603_解密.pdf"
    doc.save(str(out_path))
    doc.close()
    print(f"  ✅ 已解密儲存：{out_path.name}")

print(f"\n完成！解密檔案位於：{OUT}")
