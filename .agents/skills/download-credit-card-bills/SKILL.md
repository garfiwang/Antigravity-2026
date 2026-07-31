---
name: download-credit-card-bills
description: 下載並解密您的各家銀行信用卡電子帳單。當使用者說「下載信用卡帳單」或「下載帳單」時載入。
---

# 信用卡電子帳單下載與解密技能

當使用者想要下載或整理信用卡電子帳單時，使用此技能自動處理 Gmail 帳單下載與 PDF 解密。

## 1. 核心流程與指令

### 第一階段：下載帳單
1. **確認憑證**：腳本會自動讀取 `/Users/garfiwang/Documents/checkbill/` 下的 `credentials.json` 與 `token.pickle` 進行 Gmail 唯讀授權。
2. **執行下載指令**：
   ```bash
   python3 .agents/skills/download-credit-card-bills/scripts/download_statements.py
   ```
3. **儲存位置**：下載的加密 PDF 會自動依照銀行分類，存放在 `file:///Users/garfiwang/Documents/checkbill/帳單/` 中。

### 第二階段：解密帳單（可選）
1. **說明**：若使用者需要查看或分析帳單內容，需對下載下來的加密 PDF 進行解密。
2. **執行解密指令**：
   ```bash
   python3 .agents/skills/download-credit-card-bills/scripts/decrypt_pdfs.py
   ```
3. **密碼提示與輸入**：解密過程會依據各銀行提示（例如：身份證字號或生日）請使用者在終端機中安全地輸入密碼。
4. **解密後存檔**：解密後的 PDF 檔案會儲存在 `file:///Users/garfiwang/Documents/checkbill/帳單_解密/` 中。

---

## 2. 疑難排解 (Troubleshooting)

* **憑證失效或遺失**：若出現 `credentials.json` 錯誤，請使用者確認檔案是否在 `file:///Users/garfiwang/Documents/checkbill/credentials.json` 中。
* **首次授權**：如果是第一次執行，或是 `token.pickle` 失效，腳本會在本地開啟瀏覽器進行 Google 登入驗證，請按照終端機提示操作。
