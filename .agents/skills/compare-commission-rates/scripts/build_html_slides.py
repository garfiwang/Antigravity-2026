import os
import json
import re

# Load the data by running the extraction logic
from generate_three_year_report import extract_names_and_data, contains_3_year, file_to_company, company_columns

# Collect data
folder_path = "/Users/garfiwang/Documents/Antigravity-2026/壽險佣金-2026"
files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

all_filtered_data = {}
company_max_fyc = {}

for filename in sorted(files):
    company_name = file_to_company[filename]
    filepath = os.path.join(folder_path, filename)
    rows = extract_names_and_data(filepath)
    
    # Filter 3-year term
    filtered_rows = [r for r in rows if contains_3_year(r["term"])]
    # Filter out Farglory excluded codes
    if company_name == "遠雄人壽":
        filtered_rows = [r for r in filtered_rows if r["code"] not in ["HB4", "HZ1", "HA4", "MC1"]]
        
    all_filtered_data[company_name] = filtered_rows
    
    # Find local max
    local_max = 0.0
    for r in filtered_rows:
        fyc = float(r["rate"]) * 0.4
        if fyc > local_max:
            local_max = fyc
    company_max_fyc[company_name] = local_max

# HTML Generation
html_content = []

html_content.append("""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>三年期壽險商品佣金率大解析</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reset.css" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/night.css" />
  <style>
    :root {
      --accent:  #e8643a;   /* 橘紅 */
      --accent2: #4fc3f7;   /* 青色 */
      --success: #81c784;   /* 綠色 */
      --warn:    #ffb74d;   /* 琥珀色 */
      --highlight: #ff5252; /* 鮮紅高亮 */
    }

    .reveal {
      font-family: 'Segoe UI', 'Noto Sans TC', sans-serif;
    }
    .reveal h1, .reveal h2, .reveal h3 {
      font-family: 'Segoe UI', 'Noto Sans TC', sans-serif;
      font-weight: 700;
      letter-spacing: -0.01em;
    }
    .reveal h1 { font-size: 2.0em; line-height: 1.2; }
    .reveal h2 { font-size: 1.4em; color: var(--accent2); margin-bottom: 0.5em; }
    .reveal h3 { font-size: 1.0em; color: #fff; }
    .reveal .progress { color: var(--accent); }
    
    /* === Tables style === */
    .reveal table {
      font-size: 0.45em;
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
      background: rgba(255, 255, 255, 0.03);
    }
    
    /* === Highlighting === */
    .highlight-row {
      background: rgba(255, 82, 82, 0.1) !important;
    }
    .highlight-text {
      color: var(--highlight) !important;
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
      font-size: 0.5em;
      letter-spacing: 0.08em;
      margin-bottom: 1.0em;
      font-weight: 600;
    }
    .title-slide .subtitle { font-size: 0.7em; color: #ccc; margin-top: 0.5em; }
    .title-slide .author { margin-top: 1.8em; font-size: 0.45em; color: #999; }
    
    /* === Stat cards === */
    .stat-row { display: flex; gap: 15px; justify-content: center; margin-top: 0.6em; }
    .stat-card {
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 10px;
      padding: 12px 18px;
      text-align: center;
      flex: 1;
    }
    .stat-card .num { font-size: 1.5em; font-weight: 800; color: var(--accent2); line-height: 1.1; }
    .stat-card .num.highest { color: var(--highlight); }
    .stat-card .company { font-size: 0.4em; color: #aaa; margin-top: 4px; }
    .stat-card .label { font-size: 0.45em; font-weight: bold; color: #fff; margin-top: 6px; }

    /* === Slide footer/header === */
    .slide-footer {
      position: absolute;
      bottom: 20px;
      left: 30px;
      font-size: 0.35em;
      color: #777;
    }
    
    .scrollable-slide-container {
      max-height: 520px;
      overflow-y: auto;
      padding-right: 5px;
    }
    /* Scrollbar style */
    .scrollable-slide-container::-webkit-scrollbar {
      width: 6px;
    }
    .scrollable-slide-container::-webkit-scrollbar-track {
      background: rgba(255,255,255,0.02);
    }
    .scrollable-slide-container::-webkit-scrollbar-thumb {
      background: rgba(79, 195, 247, 0.3);
      border-radius: 3px;
    }
  </style>
</head>
<body>
<div class="reveal">
  <div class="slides">

    <!-- Slide 1: Cover -->
    <section data-background-image="images/cover.jpg" data-background-opacity="0.35" data-background-size="cover">
      <div class="title-slide">
        <div class="tag">問大師家族辦公室 · 財務規劃專題</div>
        <h1>三年期壽險商品<br/>佣金率大解析</h1>
        <p class="subtitle">五大壽險公司 3 年期商品首年佣金與續期利益比較</p>
        <p class="author">分析團隊：Antigravity | 報告日期：2026年7月</p>
      </div>
    </section>

    <!-- Slide 2: VIZ Comparison -->
    <section>
      <h2>跨公司首年實際佣金率對決</h2>
      <p style="font-size: 0.45em; color: #aaa; margin-top: -10px;">初年度服務報酬率 (FYC%) = 業績換算率 × 40%</p>
      <div class="stat-row">
        <div class="stat-card">
          <div class="company">元大人壽 (最高)</div>
          <div class="num highest">13.20%</div>
          <div class="label">百富美元利變壽險</div>
        </div>
        <div class="stat-card">
          <div class="company">全球人壽</div>
          <div class="num">11.60%</div>
          <div class="label">尊榮37 / 豪美368</div>
        </div>
        <div class="stat-card">
          <div class="company">安達人壽</div>
          <div class="num">10.80%</div>
          <div class="label">美利紅美元分紅壽險</div>
        </div>
        <div class="stat-card">
          <div class="company">保誠人壽</div>
          <div class="num">9.20%</div>
          <div class="label">鑫美傳家 / 鑫傳家</div>
        </div>
        <div class="stat-card">
          <div class="company">遠雄人壽</div>
          <div class="num">4.80%</div>
          <div class="label">富貴鑽美利</div>
        </div>
      </div>
      <div style="margin-top: 1.5em; font-size: 0.48em; color: #ccc; line-height: 1.6; text-align: left; padding: 0 40px;">
        <ul>
          <li>🏆 <strong>全場最高</strong>：<span class="highlight-text">元大人壽 - 百富美元利率變動型終身壽險</span> 實際首年佣金率達 <strong>13.20%</strong>。</li>
          <li>📊 <strong>分佈特性</strong>：前四家壽險最高費率皆在 9.20% ~ 13.20% 區間，競爭激烈；遠雄人壽在剔除豁免保單後，最高首年實際佣金率為 <strong>4.80%</strong>。</li>
        </ul>
      </div>
      <div class="slide-footer">問大師家族辦公室 - 三年期壽險商品佣金率分析</div>
    </section>
""")

# Slide 3: Prudential (保誠人壽)
prudential_rows = all_filtered_data["保誠人壽"]
p_max = company_max_fyc["保誠人壽"]

html_content.append("""
    <!-- Slide 3: Prudential -->
    <section>
      <h2>保誠人壽 3年期商品佣金表</h2>
      <div class="scrollable-slide-container">
        <table>
          <thead>
            <tr>
              <th>商品名稱</th>
              <th>代號</th>
              <th>起賣日</th>
              <th>年齡</th>
              <th>年期</th>
              <th>業績換算率</th>
              <th>首年實際(FYC%)</th>
              <th>續2</th>
              <th>續3</th>
            </tr>
          </thead>
          <tbody>""")

for r in prudential_rows:
    fyc = float(r["rate"]) * 0.4
    is_max = abs(fyc - p_max) < 1e-6
    highlight_cls = " class='highlight-row'" if is_max else ""
    text_cls = " class='highlight-text'" if is_max else ""
    
    # Check if renewal has values
    r2 = f"{float(r['renewal_rates'][0]):.2f}%" if len(r['renewal_rates']) > 0 and r['renewal_rates'][0] != "-" else "-"
    r3 = f"{float(r['renewal_rates'][1]):.2f}%" if len(r['renewal_rates']) > 1 and r['renewal_rates'][1] != "-" else "-"
    
    html_content.append(f"""
            <tr{highlight_cls}>
              <td style='text-align: left; font-weight: bold;'>{r['name']}</td>
              <td><code>{r['code']}</code></td>
              <td>{r['start_date']}</td>
              <td>{r['age']}</td>
              <td>{r['term']}</td>
              <td{text_cls}>{float(r['rate']):.2f}%</td>
              <td{text_cls}>{fyc:.2f}%</td>
              <td>{r2}</td>
              <td>{r3}</td>
            </tr>""")

html_content.append("""
          </tbody>
        </table>
      </div>
      <div class="slide-footer">保誠人壽共 14 款 3年期商品，其中紅標項目最高佣金率達 9.20%</div>
    </section>
""")

# Slide 4: Yuanta (元大人壽)
yuanta_rows = all_filtered_data["元大人壽"]
y_max = company_max_fyc["元大人壽"]

html_content.append("""
    <!-- Slide 4: Yuanta -->
    <section>
      <h2>元大人壽 3年期商品佣金表</h2>
      <div class="scrollable-slide-container">
        <table>
          <thead>
            <tr>
              <th>商品名稱</th>
              <th>代號</th>
              <th>起賣日</th>
              <th>年齡</th>
              <th>年期</th>
              <th>業績換算率</th>
              <th>首年實際(FYC%)</th>
              <th>續2</th>
              <th>續3</th>
            </tr>
          </thead>
          <tbody>""")

for r in yuanta_rows:
    fyc = float(r["rate"]) * 0.4
    is_max = abs(fyc - y_max) < 1e-6
    highlight_cls = " class='highlight-row'" if is_max else ""
    text_cls = " class='highlight-text'" if is_max else ""
    
    r2 = f"{float(r['renewal_rates'][0]):.2f}%" if len(r['renewal_rates']) > 0 and r['renewal_rates'][0] != "-" else "-"
    r3 = f"{float(r['renewal_rates'][1]):.2f}%" if len(r['renewal_rates']) > 1 and r['renewal_rates'][1] != "-" else "-"
    
    html_content.append(f"""
            <tr{highlight_cls}>
              <td style='text-align: left; font-weight: bold;'>{r['name']}</td>
              <td><code>{r['code']}</code></td>
              <td>{r['start_date']}</td>
              <td>{r['age']}</td>
              <td>{r['term']}</td>
              <td{text_cls}>{float(r['rate']):.2f}%</td>
              <td{text_cls}>{fyc:.2f}%</td>
              <td>{r2}</td>
              <td>{r3}</td>
            </tr>""")

html_content.append("""
          </tbody>
        </table>
      </div>
      <div class="slide-footer">元大人壽共 9 款商品，百富美元壽險 (0~74歲) 實際首年佣金率 13.20% 為全公司及全場最高</div>
    </section>
""")

# Slide 5: TransGlobe, Chubb & Farglory (全球人壽、安達人壽、遠雄人壽)
transglobe_rows = all_filtered_data["全球人壽"]
tg_max = company_max_fyc["全球人壽"]

chubb_rows = all_filtered_data["安達人壽"]
ch_max = company_max_fyc["安達人壽"]

farglory_rows = all_filtered_data["遠雄人壽"]
fg_max = company_max_fyc["遠雄人壽"]

html_content.append("""
    <!-- Slide 5: TransGlobe, Chubb & Farglory -->
    <section>
      <h2>全球、安達、遠雄 3年期商品佣金表</h2>
      <div class="scrollable-slide-container">
        <!-- TransGlobe -->
        <h3 style="text-align: left; margin-top: 10px; color: var(--accent2);">全球人壽</h3>
        <table>
          <thead>
            <tr>
              <th>商品名稱</th>
              <th>代號</th>
              <th>起賣日</th>
              <th>年期</th>
              <th>業績換算率</th>
              <th>首年實際(FYC%)</th>
              <th>續2</th>
              <th>續3</th>
            </tr>
          </thead>
          <tbody>""")

for r in transglobe_rows:
    fyc = float(r["rate"]) * 0.4
    is_max = abs(fyc - tg_max) < 1e-6
    highlight_cls = " class='highlight-row'" if is_max else ""
    text_cls = " class='highlight-text'" if is_max else ""
    r2 = f"{float(r['renewal_rates'][0]):.2f}%" if len(r['renewal_rates']) > 0 and r['renewal_rates'][0] != "-" else "-"
    r3 = f"{float(r['renewal_rates'][1]):.2f}%" if len(r['renewal_rates']) > 1 and r['renewal_rates'][1] != "-" else "-"
    html_content.append(f"""
            <tr{highlight_cls}>
              <td style='text-align: left; font-weight: bold;'>{r['name']}</td>
              <td><code>{r['code']}</code></td>
              <td>{r['start_date']}</td>
              <td>{r['term']}</td>
              <td{text_cls}>{float(r['rate']):.2f}%</td>
              <td{text_cls}>{fyc:.2f}%</td>
              <td>{r2}</td>
              <td>{r3}</td>
            </tr>""")

html_content.append("""
          </tbody>
        </table>

        <!-- Chubb -->
        <h3 style="text-align: left; margin-top: 20px; color: var(--accent2);">安達人壽</h3>
        <table>
          <thead>
            <tr>
              <th>商品名稱</th>
              <th>代號</th>
              <th>起賣日</th>
              <th>年期</th>
              <th>業績換算率</th>
              <th>首年實際(FYC%)</th>
              <th>續2</th>
              <th>續3</th>
            </tr>
          </thead>
          <tbody>""")

for r in chubb_rows:
    fyc = float(r["rate"]) * 0.4
    is_max = abs(fyc - ch_max) < 1e-6
    highlight_cls = " class='highlight-row'" if is_max else ""
    text_cls = " class='highlight-text'" if is_max else ""
    r2 = f"{float(r['renewal_rates'][0]):.2f}%" if len(r['renewal_rates']) > 0 and r['renewal_rates'][0] != "-" else "-"
    r3 = f"{float(r['renewal_rates'][1]):.2f}%" if len(r['renewal_rates']) > 1 and r['renewal_rates'][1] != "-" else "-"
    html_content.append(f"""
            <tr{highlight_cls}>
              <td style='text-align: left; font-weight: bold;'>{r['name']}</td>
              <td><code>{r['code']}</code></td>
              <td>{r['start_date']}</td>
              <td>{r['term']}</td>
              <td{text_cls}>{float(r['rate']):.2f}%</td>
              <td{text_cls}>{fyc:.2f}%</td>
              <td>{r2}</td>
              <td>{r3}</td>
            </tr>""")

html_content.append("""
          </tbody>
        </table>

        <!-- Farglory -->
        <h3 style="text-align: left; margin-top: 20px; color: var(--accent2);">遠雄人壽 (已剔除豁免商品)</h3>
        <table>
          <thead>
            <tr>
              <th>商品名稱</th>
              <th>代號</th>
              <th>起賣日</th>
              <th>年期</th>
              <th>業績換算率</th>
              <th>首年實際(FYC%)</th>
              <th>續2</th>
              <th>續3</th>
            </tr>
          </thead>
          <tbody>""")

for r in farglory_rows:
    fyc = float(r["rate"]) * 0.4
    is_max = abs(fyc - fg_max) < 1e-6
    highlight_cls = " class='highlight-row'" if is_max else ""
    text_cls = " class='highlight-text'" if is_max else ""
    r2 = f"{float(r['renewal_rates'][0]):.2f}%" if len(r['renewal_rates']) > 0 and r['renewal_rates'][0] != "-" else "-"
    r3 = f"{float(r['renewal_rates'][1]):.2f}%" if len(r['renewal_rates']) > 1 and r['renewal_rates'][1] != "-" else "-"
    html_content.append(f"""
            <tr{highlight_cls}>
              <td style='text-align: left; font-weight: bold;'>{r['name']}</td>
              <td><code>{r['code']}</code></td>
              <td>{r['start_date']}</td>
              <td>{r['term']}</td>
              <td{text_cls}>{float(r['rate']):.2f}%</td>
              <td{text_cls}>{fyc:.2f}%</td>
              <td>{r2}</td>
              <td>{r3}</td>
            </tr>""")

html_content.append("""
          </tbody>
        </table>
      </div>
      <div class="slide-footer">各公司旗下最高佣金率項目均以紅字高亮標記</div>
    </section>
""")

# Slide 6: Ending / Conclusion
html_content.append("""
    <!-- Slide 6: Conclusion -->
    <section data-background-image="images/ending.jpg" data-background-opacity="0.35" data-background-size="cover">
      <div class="end-slide">
        <h1 style="color:var(--accent2); margin-bottom: 0.5em;">家族辦公室財務洞察</h1>
        <div style="font-size: 0.55em; color: #ddd; text-align: left; padding: 0 50px; line-height: 1.8;">
          <ul>
            <li>💎 <strong>首年佣金率冠軍</strong>：<span class="highlight-text">元大人壽 百富 (13.20%)</span> 與 <span class="highlight-text">全球人壽 尊榮37/豪美368 (11.60%)</span> 最具競爭力。</li>
            <li>💼 <strong>多元化選擇</strong>：<span style="color:var(--accent2);">保誠人壽</span> 提供最多 3 年期短年期選擇（達 14 款），方便規劃不同資金周期的保險信託。</li>
            <li>🛡️ <strong>豁免保單分析</strong>：剔除豁免類商品後，遠雄人壽以富貴鑽美利利變增額還本壽險（實際佣金 4.80%）為 3年期唯一儲蓄主力。</li>
          </ul>
        </div>
        <p class="tagline" style="margin-top: 1.5em; font-size: 0.6em; color: #999;">— 精準配置 · 穩健傳承 —</p>
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

# Write HTML to project folder
html_path = "/Users/garfiwang/Documents/Antigravity-2026/壽險佣金-2026/three-year-commissions/index.html"
with open(html_path, 'w', encoding='utf-8') as f:
    f.write("".join(html_content))

print("index.html created successfully!")
