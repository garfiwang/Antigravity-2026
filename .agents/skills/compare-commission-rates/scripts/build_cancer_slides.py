import os
import re
import pdfplumber

folder_path = "/Users/garfiwang/Documents/Antigravity-2026/壽險佣金-2026"
files = [
    "保誠人壽-20260626.pdf",
    "元大人壽-20260626.pdf",
    "全球人壽-20260626.pdf",
    "安達人壽 - 202605.pdf",
    "富邦人壽 - 20260703.pdf",
    "遠雄人壽-20260626.pdf"
]

date_pattern = re.compile(r'\d{4}/\d{2}/\d{2}')

def is_float(val):
    try:
        if '.' not in val:
            return False
        float(val.replace('%', '').strip())
        return True
    except ValueError:
        return False

def clean_rate(rate_str):
    if not rate_str or rate_str == "-":
        return 0.0
    try:
        return float(str(rate_str).replace('%', '').strip())
    except ValueError:
        return 0.0

# 提取除了富邦人壽以外的其他五家公司
def extract_other_companies(filepath):
    code_to_name = {}
    data_rows = []
    insurance_keywords = ["壽險", "保險", "附約", "年金", "健康", "傷害", "定期", "終身", "防癌", "醫療", "養老"]
    
    with pdfplumber.open(filepath) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
            lines = text.split('\n')
            
            standalone_names = []
            data_lines = []
            
            for line_idx, line in enumerate(lines):
                parts = line.split()
                if not parts:
                    continue
                
                has_date = any(date_pattern.match(p) for p in parts)
                has_chinese = any(any('\u4e00' <= char <= '\u9fff' for char in word) for word in parts)
                has_float = any(is_float(p) for p in parts)
                
                if not has_date and not has_float and has_chinese:
                    candidate_name = " ".join(parts).strip()
                    if any(k in candidate_name for k in insurance_keywords):
                        if not any(h in candidate_name for h in ["險種名稱", "製表日期", "初年度", "續年度", "特別報酬率", "業績換算率", "人壽商品"]):
                            standalone_names.append((line_idx, candidate_name))
                
                if has_date:
                    date_idx = -1
                    for idx, part in enumerate(parts):
                        if date_pattern.match(part):
                            date_idx = idx
                            break
                    
                    if date_idx > 0:
                        code = parts[date_idx - 1]
                        name_parts = parts[:date_idx - 1]
                        name = " ".join(name_parts).strip()
                        data_lines.append((line_idx, code, name))
            
            for line_idx, code, name in data_lines:
                if name and any('\u4e00' <= char <= '\u9fff' for char in name) and not any(h in name for h in ["險種名稱", "險種代號"]):
                    code_to_name[code] = name
                else:
                    for s_idx, s_name in standalone_names:
                        if abs(s_idx - line_idx) <= 2:
                            code_to_name[code] = s_name
                            break
                            
    with pdfplumber.open(filepath) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue
            lines = text.split('\n')
            
            for line_idx, line in enumerate(lines):
                parts = line.split()
                if not parts:
                    continue
                
                has_date = any(date_pattern.match(p) for p in parts)
                if not has_date:
                    continue
                
                float_idx = -1
                for idx, part in enumerate(parts):
                    if is_float(part):
                        float_idx = idx
                        break
                
                if float_idx > 0:
                    term = parts[float_idx - 1]
                    rate = parts[float_idx]
                    
                    date_idx = -1
                    for idx, part in enumerate(parts[:float_idx]):
                        if date_pattern.match(part):
                            date_idx = idx
                            break
                    
                    if date_idx > 0:
                        code = parts[date_idx - 1]
                        start_date = parts[date_idx]
                        
                        middle_parts = parts[date_idx + 1: float_idx - 1]
                        
                        end_date = "-"
                        age = "-"
                        other_conditions = "-"
                        
                        for p in middle_parts:
                            if date_pattern.match(p):
                                end_date = p
                            elif re.match(r'(\d+~\d+|\d+~|~\d+)', p):
                                age = p
                            elif p != "-":
                                other_conditions = p
                                
                        name = code_to_name.get(code, "")
                        
                        data_rows.append({
                            "name": name,
                            "code": code,
                            "start_date": start_date,
                            "end_date": end_date,
                            "age": age,
                            "other_conditions": other_conditions,
                            "term": term,
                            "rate": rate,
                        })
                        
    return data_rows

# 提取富邦人壽
def extract_fubon(filepath):
    data_rows = []
    with pdfplumber.open(filepath) as pdf:
        for page_idx, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            if not tables:
                continue
            table = tables[0]
            for r_idx, row in enumerate(table):
                if r_idx < 5:
                    continue
                if len(row) > 7:
                    term = row[6]
                    if not term or term == "年期" or term == "繳費\n年期" or term == "年度\n繳費\n年期":
                        continue
                    
                    name = row[0]
                    if not name:
                        curr_idx = r_idx - 1
                        while curr_idx >= 0 and not table[curr_idx][0]:
                            curr_idx -= 1
                        if curr_idx >= 0:
                            name = table[curr_idx][0]
                    
                    if not name or "險種名稱" in name:
                        continue
                        
                    code = row[1]
                    start_date = row[2]
                    end_date = row[3]
                    age = row[4]
                    other = row[5]
                    rate = row[7]
                    
                    data_rows.append({
                        "name": name.replace('\n', '').strip() if name else "",
                        "code": code.replace('\n', '').strip() if code else "",
                        "start_date": start_date.replace('\n', '').strip() if start_date else "",
                        "end_date": end_date.replace('\n', '').strip() if end_date else "",
                        "age": age.replace('\n', '').strip() if age else "",
                        "other_conditions": other.replace('\n', '').strip() if other else "",
                        "term": term.replace('\n', '').strip() if term else "",
                        "rate": rate.replace('\n', '').strip() if rate else "0.0",
                    })
    return data_rows

print("Collecting all products data...")
all_products = []
for filename in files:
    filepath = os.path.join(folder_path, filename)
    company_name = filename.split('-')[0].split(' ')[0].strip()
    
    if "富邦" in company_name:
        rows = extract_fubon(filepath)
    else:
        rows = extract_other_companies(filepath)
        
    for r in rows:
        r["company"] = company_name
        if company_name == "元大人壽":
            if r["code"] == "A2":
                r["name"] = "真安心保本防癌保險"
            elif r["code"] == "HC":
                r["name"] = "終身防癌健康保險"
        all_products.append(r)

# Filter cancer products
cancer_products = []
for p in all_products:
    name = p["name"]
    code = p["code"]
    is_cancer = False
    if name and any(k in name for k in ["防癌", "癌", "癌症", "腫瘤"]):
        is_cancer = True
    if code and any(k in code.upper() for k in ["CANCER"]):
        is_cancer = True
        
    if is_cancer:
        rate_val = clean_rate(p["rate"])
        fyc_val = rate_val * 0.4
        p["rate_val"] = rate_val
        p["fyc_val"] = fyc_val
        cancer_products.append(p)

cancer_products.sort(key=lambda x: x["fyc_val"], reverse=True)

# Find local max for each company
company_max = {}
global_max = 0.0
for p in cancer_products:
    comp = p["company"]
    fyc = p["fyc_val"]
    if comp not in company_max or fyc > company_max[comp]:
        company_max[comp] = fyc
    if fyc > global_max:
        global_max = fyc

# Start writing index.html
html = []
html.append("""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>癌症與防癌保險商品佣金率大解析</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reset.css" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/night.css" />
  <style>
    :root {
      --accent:  #ff5252;   /* 鮮紅高亮 */
      --accent2: #4fc3f7;   /* 青色 */
      --success: #81c784;   /* 綠色 */
      --warn:    #ffb74d;   /* 橘黃 */
      --dark-bg: #0f1015;
    }

    .reveal {
      font-family: 'Segoe UI', 'Noto Sans TC', sans-serif;
    }
    .reveal h1, .reveal h2, .reveal h3 {
      font-family: 'Segoe UI', 'Noto Sans TC', sans-serif;
      font-weight: 700;
      letter-spacing: -0.01em;
      text-transform: none;
    }
    .reveal h1 { font-size: 1.8em; line-height: 1.25; color: #fff; }
    .reveal h2 { font-size: 1.3em; color: var(--accent2); margin-bottom: 0.4em; }
    .reveal h3 { font-size: 0.95em; color: #fff; margin-bottom: 0.3em; }
    .reveal .progress { color: var(--accent); }
    
    /* === Tables style === */
    .reveal table {
      font-size: 0.38em;
      border-collapse: collapse;
      width: 100%;
      margin: 0 auto;
    }
    .reveal table th {
      background: rgba(79, 195, 247, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: var(--accent2);
      font-weight: bold;
      text-align: center;
      padding: 6px 10px;
    }
    .reveal table td {
      border: 1px solid rgba(255, 255, 255, 0.1);
      padding: 4px 8px;
      text-align: center;
    }
    .reveal table tr:nth-child(even) {
      background: rgba(255, 255, 255, 0.02);
    }
    
    /* === Highlighting === */
    .highlight-row {
      background: rgba(255, 82, 82, 0.1) !important;
    }
    .highlight-text {
      color: var(--accent) !important;
      font-weight: bold !important;
    }
    
    /* === Cover === */
    .title-slide { text-align: center; }
    .title-slide .tag {
      display: inline-block;
      background: var(--accent);
      color: #fff;
      padding: 4px 14px;
      border-radius: 20px;
      font-size: 0.45em;
      letter-spacing: 0.08em;
      margin-bottom: 1.0em;
      font-weight: 600;
    }
    .title-slide .subtitle { font-size: 0.6em; color: #ccc; margin-top: 0.5em; }
    .title-slide .author { margin-top: 1.8em; font-size: 0.4em; color: #888; }
    
    /* === Stat cards === */
    .stat-row { display: flex; gap: 10px; justify-content: center; margin-top: 0.5em; flex-wrap: wrap; }
    .stat-card {
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 8px;
      padding: 8px 12px;
      text-align: center;
      min-width: 130px;
      flex: 1;
    }
    .stat-card .num { font-size: 1.3em; font-weight: 800; color: var(--accent2); line-height: 1.1; }
    .stat-card .num.highest { color: var(--accent); }
    .stat-card .company { font-size: 0.35em; color: #aaa; margin-top: 2px; }
    .stat-card .label { font-size: 0.35em; font-weight: bold; color: #fff; margin-top: 4px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; max-width: 140px; }

    /* === Slide footer/header === */
    .slide-footer {
      position: absolute;
      bottom: 20px;
      left: 30px;
      font-size: 0.3em;
      color: #666;
    }
    
    .scrollable-slide-container {
      max-height: 480px;
      overflow-y: auto;
      padding-right: 5px;
    }
    /* Scrollbar style */
    .scrollable-slide-container::-webkit-scrollbar {
      width: 6px;
    }
    .scrollable-slide-container::-webkit-scrollbar-track {
      background: rgba(255,255,255,0.01);
    }
    .scrollable-slide-container::-webkit-scrollbar-thumb {
      background: rgba(79, 195, 247, 0.25);
      border-radius: 3px;
    }
  </style>
</head>
<body>
<div class="reveal">
  <div class="slides">

    <!-- Slide 1: Cover -->
    <section data-background-gradient="linear-gradient(135deg, #1e1f29 0%, #0f1015 100%)">
      <div class="title-slide">
        <div class="tag">問大師家族辦公室 · 財務規劃專題</div>
        <h1>癌症與防癌保險商品<br/><span style="color:var(--accent);">首年佣金率</span>大解析</h1>
        <p class="subtitle">六大壽險公司 癌症商品首年佣金率（FYC%）全面比較</p>
        <p class="author">分析團隊：Antigravity | 報告日期：2026年7月</p>
      </div>
    </section>

    <!-- Slide 2: Exec Summary -->
    <section data-background-gradient="linear-gradient(135deg, #151620 0%, #0f1015 100%)">
      <h2>各公司癌症商品最高佣金率對決</h2>
      <p style="font-size: 0.4em; color: #aaa; margin-top: -10px;">首年實際佣金率 (FYC%) = 業績換算率 × 40%</p>
      <div class="stat-row">
        <div class="stat-card">
          <div class="company">保誠人壽 (最高)</div>
          <div class="num highest">25.60%</div>
          <div class="label">誠心防癌2.0 (20年)</div>
        </div>
        <div class="stat-card">
          <div class="company">元大人壽 (最高)</div>
          <div class="num highest">25.60%</div>
          <div class="label">真安心保本 (20年/15~歲)</div>
        </div>
        <div class="stat-card">
          <div class="company">富邦人壽</div>
          <div class="num">24.80%</div>
          <div class="label">溢起防癌 (1年期)</div>
        </div>
        <div class="stat-card">
          <div class="company">遠雄人壽</div>
          <div class="num">24.80%</div>
          <div class="label">愛無限B / 愛無懼B (20年)</div>
        </div>
        <div class="stat-card">
          <div class="company">全球人壽</div>
          <div class="num">24.00%</div>
          <div class="label">臻心85附約 (30年)</div>
        </div>
        <div class="stat-card">
          <div class="company">安達人壽</div>
          <div class="num">11.20%</div>
          <div class="label">愛醫靠/達文西 (1年期)</div>
        </div>
      </div>
      <div style="margin-top: 1.0em; font-size: 0.42em; color: #ccc; line-height: 1.5; text-align: left; padding: 0 40px;">
        <ul>
          <li>🏆 <strong>全場冠軍</strong>：<span class="highlight-text">保誠 ACCRTB1 (20年)</span> 與 <span class="highlight-text">元大 A2 (20年/15歲+)</span> 以 <strong>25.60%</strong> 的首年實際佣金率並列第一。</li>
          <li>⚡ <strong>一年期黑馬</strong>：<span style="color:var(--accent2);">富邦人壽 PCC5 (1年期)</span> 以 <strong>24.80%</strong> 的超高佣金率強勢奪得全場第三，是極具競爭力的短年期商品。</li>
          <li>📊 <strong>年期特點</strong>：大部分商品的佣金率隨繳費年期拉長而增加，20 年期是長年期商品的佣金高峰。</li>
        </ul>
      </div>
    </section>

    <!-- Slide 3: Leaderboard -->
    <section data-background-gradient="linear-gradient(135deg, #151620 0%, #0f1015 100%)">
      <h2>🏆 全場癌症商品佣金率 Top 12 排行榜</h2>
      <p style="font-size: 0.4em; color: #aaa; margin-top: -10px; margin-bottom: 10px;">Top 12 癌症商品首年實際佣金率皆高於 22.40%</p>
      <div class="scrollable-slide-container">
        <table>
          <thead>
            <tr>
              <th>排名</th>
              <th>保險公司</th>
              <th>商品名稱</th>
              <th>代號</th>
              <th>年期</th>
              <th>換算率</th>
              <th>首年實際(FYC%)</th>
              <th>年齡限制</th>
            </tr>
          </thead>
          <tbody>""")

# Add Top 12 rows
for idx, p in enumerate(cancer_products[:12]):
    is_max = abs(p["fyc_val"] - global_max) < 1e-6
    row_cls = " class='highlight-row'" if is_max else ""
    text_cls = " class='highlight-text'" if is_max else ""
    
    html.append(f"""
            <tr{row_cls}>
              <td><strong>{idx+1}</strong></td>
              <td>{p['company']}</td>
              <td style='text-align: left; font-weight: bold;'>{p['name']}</td>
              <td><code>{p['code']}</code></td>
              <td>{p['term']}</td>
              <td{text_cls}>{p['rate_val']:.2f}%</td>
              <td{text_cls}>{p['fyc_val']:.2f}%</td>
              <td>{p['age']}</td>
            </tr>""")

html.append("""
          </tbody>
        </table>
      </div>
    </section>
""")

# Slide 4: Prudential & Yuanta
html.append("""
    <!-- Slide 4: Prudential & Yuanta -->
    <section>
      <h2>保誠人壽 & 元大人壽 癌症商品佣金表</h2>
      <p style="font-size: 0.4em; color: #aaa; margin-top: -10px; margin-bottom: 10px;">保誠 ACCRTB1 與 元大 A2 為兩大公司的主力高佣商品</p>
      <div class="scrollable-slide-container">
        <h3 style="text-align: left; color: var(--accent2);">保誠人壽</h3>
        <table>
          <thead>
            <tr>
              <th>商品名稱</th>
              <th>代號</th>
              <th>年期</th>
              <th>換算率</th>
              <th>首年實際(FYC%)</th>
              <th>年齡限制</th>
            </tr>
          </thead>
          <tbody>""")

pru_prods = [p for p in cancer_products if p["company"] == "保誠人壽"]
pru_max = company_max["保誠人壽"]
for p in pru_prods:
    is_max = abs(p["fyc_val"] - pru_max) < 1e-6
    row_cls = " class='highlight-row'" if is_max else ""
    text_cls = " class='highlight-text'" if is_max else ""
    html.append(f"""
            <tr{row_cls}>
              <td style='text-align: left; font-weight: bold;'>{p['name']}</td>
              <td><code>{p['code']}</code></td>
              <td>{p['term']}</td>
              <td{text_cls}>{p['rate_val']:.2f}%</td>
              <td{text_cls}>{p['fyc_val']:.2f}%</td>
              <td>{p['age']}</td>
            </tr>""")

html.append("""
          </tbody>
        </table>

        <h3 style="text-align: left; margin-top: 15px; color: var(--accent2);">元大人壽</h3>
        <table>
          <thead>
            <tr>
              <th>商品名稱</th>
              <th>代號</th>
              <th>年期</th>
              <th>換算率</th>
              <th>首年實際(FYC%)</th>
              <th>年齡限制</th>
            </tr>
          </thead>
          <tbody>""")

yt_prods = [p for p in cancer_products if p["company"] == "元大人壽"]
yt_max = company_max["元大人壽"]
for p in yt_prods:
    is_max = abs(p["fyc_val"] - yt_max) < 1e-6
    row_cls = " class='highlight-row'" if is_max else ""
    text_cls = " class='highlight-text'" if is_max else ""
    html.append(f"""
            <tr{row_cls}>
              <td style='text-align: left; font-weight: bold;'>{p['name']}</td>
              <td><code>{p['code']}</code></td>
              <td>{p['term']}</td>
              <td{text_cls}>{p['rate_val']:.2f}%</td>
              <td{text_cls}>{p['fyc_val']:.2f}%</td>
              <td>{p['age']}</td>
            </tr>""")

html.append("""
          </tbody>
        </table>
      </div>
    </section>
""")

# Slide 5: Fubon & Farglory
html.append("""
    <!-- Slide 5: Fubon & Farglory -->
    <section>
      <h2>富邦人壽 & 遠雄人壽 癌症商品佣金表</h2>
      <p style="font-size: 0.4em; color: #aaa; margin-top: -10px; margin-bottom: 10px;">富邦 PCC5 一年期佣金達 24.80%，遠雄主力商品集中在 CE4 / HY4 (24.80%)</p>
      <div class="scrollable-slide-container">
        <h3 style="text-align: left; color: var(--accent2);">富邦人壽</h3>
        <table>
          <thead>
            <tr>
              <th>商品名稱</th>
              <th>代號</th>
              <th>年期</th>
              <th>換算率</th>
              <th>首年實際(FYC%)</th>
              <th>備註 / 年齡</th>
            </tr>
          </thead>
          <tbody>""")

fb_prods = [p for p in cancer_products if p["company"] == "富邦人壽"]
fb_prods_filtered = [p for p in fb_prods if p["rate_val"] >= 30.0]
fb_max = company_max["富邦人壽"]
for p in fb_prods_filtered:
    is_max = abs(p["fyc_val"] - fb_max) < 1e-6
    row_cls = " class='highlight-row'" if is_max else ""
    text_cls = " class='highlight-text'" if is_max else ""
    html.append(f"""
            <tr{row_cls}>
              <td style='text-align: left; font-weight: bold;'>{p['name']}</td>
              <td><code>{p['code']}</code></td>
              <td>{p['term']}</td>
              <td{text_cls}>{p['rate_val']:.2f}%</td>
              <td{text_cls}>{p['fyc_val']:.2f}%</td>
              <td>{p['age']}</td>
            </tr>""")

html.append("""
          </tbody>
        </table>

        <h3 style="text-align: left; margin-top: 15px; color: var(--accent2);">遠雄人壽</h3>
        <table>
          <thead>
            <tr>
              <th>商品名稱</th>
              <th>代號</th>
              <th>年期</th>
              <th>換算率</th>
              <th>首年實際(FYC%)</th>
              <th>年齡限制</th>
            </tr>
          </thead>
          <tbody>""")

fg_prods = [p for p in cancer_products if p["company"] == "遠雄人壽"]
fg_prods_filtered = [p for p in fg_prods if p["rate_val"] >= 30.0]
fg_max = company_max["遠雄人壽"]
for p in fg_prods_filtered:
    is_max = abs(p["fyc_val"] - fg_max) < 1e-6
    row_cls = " class='highlight-row'" if is_max else ""
    text_cls = " class='highlight-text'" if is_max else ""
    html.append(f"""
            <tr{row_cls}>
              <td style='text-align: left; font-weight: bold;'>{p['name']}</td>
              <td><code>{p['code']}</code></td>
              <td>{p['term']}</td>
              <td{text_cls}>{p['rate_val']:.2f}%</td>
              <td{text_cls}>{p['fyc_val']:.2f}%</td>
              <td>{p['age']}</td>
            </tr>""")

html.append("""
          </tbody>
        </table>
      </div>
    </section>
""")

# Slide 6: TransGlobe & Chubb
html.append("""
    <!-- Slide 6: TransGlobe & Chubb -->
    <section>
      <h2>全球人壽 & 安達人壽 癌症商品佣金表</h2>
      <p style="font-size: 0.4em; color: #aaa; margin-top: -10px; margin-bottom: 10px;">全球最高為 XCE (24.00%)，安達以一年期 OCE001 / OCF001 (11.20%) 為主</p>
      <div class="scrollable-slide-container">
        <h3 style="text-align: left; color: var(--accent2);">全球人壽</h3>
        <table>
          <thead>
            <tr>
              <th>商品名稱</th>
              <th>代號</th>
              <th>年期</th>
              <th>換算率</th>
              <th>首年實際(FYC%)</th>
              <th>年齡限制</th>
            </tr>
          </thead>
          <tbody>""")

tg_prods = [p for p in cancer_products if p["company"] == "全球人壽"]
tg_prods_filtered = [p for p in tg_prods if p["rate_val"] >= 30.0]
tg_max = company_max["全球人壽"]
for p in tg_prods_filtered:
    is_max = abs(p["fyc_val"] - tg_max) < 1e-6
    row_cls = " class='highlight-row'" if is_max else ""
    text_cls = " class='highlight-text'" if is_max else ""
    html.append(f"""
            <tr{row_cls}>
              <td style='text-align: left; font-weight: bold;'>{p['name']}</td>
              <td><code>{p['code']}</code></td>
              <td>{p['term']}</td>
              <td{text_cls}>{p['rate_val']:.2f}%</td>
              <td{text_cls}>{p['fyc_val']:.2f}%</td>
              <td>{p['age']}</td>
            </tr>""")

html.append("""
          </tbody>
        </table>

        <h3 style="text-align: left; margin-top: 15px; color: var(--accent2);">安達人壽</h3>
        <table>
          <thead>
            <tr>
              <th>商品名稱</th>
              <th>代號</th>
              <th>年期</th>
              <th>換算率</th>
              <th>首年實際(FYC%)</th>
              <th>年齡限制</th>
            </tr>
          </thead>
          <tbody>""")

ch_prods = [p for p in cancer_products if p["company"] == "安達人壽"]
ch_max = company_max["安達人壽"]
for p in ch_prods:
    is_max = abs(p["fyc_val"] - ch_max) < 1e-6
    row_cls = " class='highlight-row'" if is_max else ""
    text_cls = " class='highlight-text'" if is_max else ""
    html.append(f"""
            <tr{row_cls}>
              <td style='text-align: left; font-weight: bold;'>{p['name']}</td>
              <td><code>{p['code']}</code></td>
              <td>{p['term']}</td>
              <td{text_cls}>{p['rate_val']:.2f}%</td>
              <td{text_cls}>{p['fyc_val']:.2f}%</td>
              <td>{p['age']}</td>
            </tr>""")

html.append("""
          </tbody>
        </table>
      </div>
    </section>
""")

# Slide 7: Conclusion
html.append("""
    <!-- Slide 7: Conclusion -->
    <section data-background-gradient="linear-gradient(135deg, #1e1f29 0%, #0f1015 100%)">
      <div class="end-slide">
        <h1 style="color:var(--accent2); margin-bottom: 0.4em;">癌症商品配置策略總結</h1>
        <div style="font-size: 0.52em; color: #ddd; text-align: left; padding: 0 50px; line-height: 1.7;">
          <ul>
            <li>💎 <strong>高長年期佣金率選擇</strong>：若以首年佣金為主要考量，<span class="highlight-text">保誠 誠心防癌2.0 (20年 - 25.60%)</span> 與 <span class="highlight-text">元大 真安心保本 (20年/15歲以上 - 25.60%)</span> 最為優異。</li>
            <li>⚡ <strong>高一年期佣金率選擇</strong>：若希望資金靈活配置，<span class="highlight-text">富邦人壽 溢起防癌 PCC5 (1年期 - 24.80%)</span> 的佣金表現傲視群雄。</li>
            <li>📊 <strong>投保年齡細節</strong>：元大 A2 與 遠雄 CI4 均有明顯的投保年齡佣金率分級，規劃時須特別留意保戶年齡所對應的換算率落點。</li>
          </ul>
        </div>
        <p class="tagline" style="margin-top: 1.5em; font-size: 0.55em; color: #777;">— 精準配置 · 穩健傳承 —</p>
      </div>
    </section>

  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
<script>
  Reveal.initialize({
    hash: true,
    transition: 'slide',
    transitionSpeed: 'default',
    backgroundTransition: 'fade',
    center: true,
    progress: true,
    controls: true,
    slideNumber: 'c/t',
    plugins: []
  });
</script>
</body>
</html>
""")

# Create directory
output_dir = "/Users/garfiwang/Documents/Antigravity-2026/壽險佣金-2026/cancer-commissions"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Write HTML
output_file = os.path.join(output_dir, "index.html")
with open(output_file, "w", encoding="utf-8") as f:
    f.write("".join(html))

print(f"Slides generated successfully: {output_file}")
