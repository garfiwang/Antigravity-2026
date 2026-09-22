---
name: short-url
version: 1.0.0
description: 產生與管理 Reurl.cc 短網址服務。當使用者說「縮網址」、「產生短網址」、「短網址」、「把這個網址縮短」、「建立短網址」、「reurl」或提供網址要求縮短時載入。
user-invocable: true
changelog:
  - version: 1.0.0
    date: 2026-09-20
    note: 初始版本，串接 Reurl API，支援 CLI 執行、Python 模組調用、UTM 標籤追蹤與自動複製到剪貼簿。
---

# 🔗 Reurl.cc 短網址產生技能

專門透過 Reurl.cc 官方 API 為使用者將長網址快速轉換為精簡短網址（例如 `https://reurl.cc/xxxxxx`）。

---

## 🚀 觸發條件
當使用者提到以下情境時自動觸發：
- 「縮網址」、「產生短網址」、「建立短網址」、「把這個網址縮短」
- 「短網址：[URL]」
- 「reurl [URL]」
- 在產出文章、簡報、社群貼文或任何連結後，要求提供短網址版本

---

## 🛠️ 執行方式

### 方式 A：透過專屬 Python 腳本產生（推薦）

```bash
# 1. 基本縮網址（自動顯示原始網址與短網址）
python3 .agents/skills/short-url/shorten.py "https://example.com/very/long/url"

# 2. 自動複製到剪貼簿 (--copy 或 -c)
python3 .agents/skills/short-url/shorten.py "https://example.com" -c

# 3. 帶有 UTM 追蹤參數
python3 .agents/skills/short-url/shorten.py "https://example.com" \
  --utm-source "threads" \
  --utm-medium "social" \
  --utm-campaign "launch"

# 4. 只輸出短網址（方便給其他腳本串接）
python3 .agents/skills/short-url/shorten.py "https://example.com" -q
```

### 方式 B：系統終端機指令（已加入 PATH）
```bash
reurl "https://example.com" -c
```

---

## 🔑 金鑰與端點設定
- **API 端點**：`https://api.reurl.cc/shorten`
- **Header 標頭**：`reurl-api-key: [API_KEY]`
- **金鑰讀取順序**：
  1. 指令參數 `--key`
  2. 環境變數 `REURL_API_KEY`（已加入 `~/.zshrc`）
  3. 設定檔 `~/.reurl.env`
  4. 腳本內建備用金鑰

---

## 💡 輸出標準格式
產生短網址後，請向使用者清晰回報：
```markdown
🔗 **原始網址**：https://example.com/very/long/url
✨ **Reurl 短網址**：https://reurl.cc/xxxxxx
📋 **狀態**：已建立完成（已複製至剪貼簿）
```
