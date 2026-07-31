import os
import json
import re

# Load the data by running the extraction logic
from generate_twelve_year_report import extract_names_and_data, contains_12_year, file_to_company, company_columns

# Collect data
folder_path = "/Users/garfiwang/Documents/Antigravity-2026/壽險佣金-2026"
files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

all_filtered_data = {}
company_max_fyc = {}
company_max_item = {}
global_max_fyc = 0.0
global_max_item = None

for filename in sorted(files):
    company_name = file_to_company[filename]
    filepath = os.path.join(folder_path, filename)
    rows = extract_names_and_data(filepath)
    
    # Filter 12-year term
    filtered_rows = [r for r in rows if contains_12_year(r["term"])]
    all_filtered_data[company_name] = filtered_rows
    
    # Find local max
    local_max = 0.0
    max_item = None
    for r in filtered_rows:
        fyc = float(r["rate"]) * 0.4
        if fyc > local_max:
            local_max = fyc
            max_item = r
        if fyc > global_max_fyc:
            global_max_fyc = fyc
            global_max_item = {
                "company": company_name,
                "name": r["name"],
                "code": r["code"],
                "fyc": fyc
            }
    company_max_fyc[company_name] = local_max
    if max_item:
        company_max_item[company_name] = {
            "name": max_item["name"],
            "code": max_item["code"],
            "fyc": local_max
        }

# Sort companies by their max fyc to display on Slide 2
sorted_companies = sorted(
    [c for c in company_max_fyc if company_max_fyc[c] > 0],
    key=lambda x: company_max_fyc[x],
    reverse=True
)

# HTML Generation
html_content = []

html_content.append("""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>十二年期壽險商品佣金率大解析</title>
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
      font-size: 0.4em;
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
    .stat-card .label { font-size: 0.4em; font-weight: bold; color: #fff; margin-top: 6px; }

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
        <h1>十二年期壽險商品<br/>佣金率大解析</h1>
        <p class="subtitle">五大壽險公司 12 年期商品首年佣金與續期利益比較</p>
        <p class="author">分析團隊：Antigravity | 報告日期：2026年7月</p>
      </div>
    </section>
""")

# Slide 2: VIZ Comparison (Dynamic Cards)
html_content.append("""
    <!-- Slide 2: VIZ Comparison -->
    <section>
      <h2>跨公司首年實際佣金率對決</h2>
      <p style="font-size: 0.45em; color: #aaa; margin-top: -10px;">初年度服務報酬率 (FYC%) = 業績換算率 × 40%</p>
      <div class="stat-row">""")

for idx, comp in enumerate(sorted_companies):
    max_data = company_max_item[comp]
    is_global_highest = (global_max_item and comp == global_max_item["company"] and abs(max_data["fyc"] - global_max_fyc) < 1e-6)
    num_class = "num highest" if is_global_highest else "num"
    comp_label = f"{comp} (最高)" if is_global_highest else comp
    
    html_content.append(f"""
        <div class="stat-card">
          <div class="company">{comp_label}</div>
          <div class="num {num_class}">{max_data['fyc']:.2f}%</div>
          <div class="label" title="{max_data['name']}">{max_data['name']}</div>
        </div>""")

html_content.append("""
      </div>""")

# Summary list for slide 2
if global_max_item:
    html_content.append(f"""
      <div style="margin-top: 1.5em; font-size: 0.48em; color: #ccc; line-height: 1.6; text-align: left; padding: 0 40px;">
        <ul>
          <li>🏆 <strong>全場最高</strong>：<span class="highlight-text">{global_max_item['company']} - {global_max_item['name']} (代號 {global_max_item['code']})</span> 實際首年佣金率達 <strong>{global_max_item['fyc']:.2f}%</strong>。</li>
          <li>📊 <strong>分析特點</strong>：本列表呈現繳費期間為 12 年期（或含 12 年期範圍）之主要壽險商品。</li>
        </ul>
      </div>
      <div class="slide-footer">問大師家族辦公室 - 十二年期壽險商品佣金率分析</div>
    </section>
""")
else:
    html_content.append("""
      <div style="margin-top: 1.5em; font-size: 0.48em; color: #ccc; line-height: 1.6; text-align: left; padding: 0 40px;">
        <ul>
          <li>⚠️ <strong>無篩選到任何符合 12 年期的商品。</strong></li>
        </ul>
      </div>
      <div class="slide-footer">問大師家族辦公室 - 十二年期壽險商品佣金率分析</div>
    </section>
""")

# Individual Company Slides
# Since there are 5 companies, we will generate slides for those that have 12-year products.
for comp in sorted(files):
    company_name = file_to_company[comp]
    rows = all_filtered_data.get(company_name, [])
    if not rows:
        continue
    
    local_max = company_max_fyc.get(company_name, 0.0)
    config = company_columns[company_name]
    
    html_content.append(f"""
    <!-- Slide: {company_name} -->
    <section>
      <h2>{company_name} 12年期商品佣金表</h2>
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
              <th>續4</th>
              <th>續5</th>
              <th>續6</th>
            </tr>
          </thead>
          <tbody>""")
          
    for r in rows:
        fyc = float(r["rate"]) * 0.4
        is_max = abs(fyc - local_max) < 1e-6 and local_max > 0
        highlight_cls = " class='highlight-row'" if is_max else ""
        text_cls = " class='highlight-text'" if is_max else ""
        
        # Extract renewals
        r_rates = r["renewal_rates"]
        renewals_vals = []
        for i in range(5): # 續2 to 續6
            if len(r_rates) > i and r_rates[i] != "-" and r_rates[i] != "":
                try:
                    renewals_vals.append(f"{float(r_rates[i]):.2f}%")
                except ValueError:
                    renewals_vals.append(r_rates[i])
            else:
                renewals_vals.append("-")
                
        html_content.append(f"""
            <tr{highlight_cls}>
              <td style='text-align: left; font-weight: bold;'>{r['name']}</td>
              <td><code>{r['code']}</code></td>
              <td>{r['start_date']}</td>
              <td>{r['age']}</td>
              <td>{r['term']}</td>
              <td{text_cls}>{float(r['rate']):.2f}%</td>
              <td{text_cls}>{fyc:.2f}%</td>
              <td>{renewals_vals[0]}</td>
              <td>{renewals_vals[1]}</td>
              <td>{renewals_vals[2]}</td>
              <td>{renewals_vals[3]}</td>
              <td>{renewals_vals[4]}</td>
            </tr>""")
            
    html_content.append(f"""
          </tbody>
        </table>
      </div>
      <div class="slide-footer">{company_name} 共 {len(rows)} 款商品，首年最高實際佣金率為 {local_max:.2f}%</div>
    </section>
""")

# Slide 6: Ending / Conclusion
conclusion_bullets = []
if global_max_item:
    conclusion_bullets.append(f"🏆 <strong>首年實際佣金率冠軍</strong>：由 <span class='highlight-text'>{global_max_item['company']} - {global_max_item['name']} ({global_max_item['fyc']:.2f}%)</span> 奪得。")
else:
    conclusion_bullets.append("⚠️ 未在 PDF 檔案中找到任何 12 年期商品。")

for comp in sorted_companies:
    max_data = company_max_item[comp]
    conclusion_bullets.append(f"💼 <strong>{comp} 最高</strong>：{max_data['name']} (實際 FYC% 達 <strong>{max_data['fyc']:.2f}%</strong>)")

html_content.append(f"""
    <!-- Slide: Conclusion -->
    <section data-background-image="images/ending.jpg" data-background-opacity="0.35" data-background-size="cover">
      <div class="end-slide">
        <h1 style="color:var(--accent2); margin-bottom: 0.5em;">家族辦公室財務洞察 (12年期)</h1>
        <div style="font-size: 0.50em; color: #ddd; text-align: left; padding: 0 50px; line-height: 1.8;">
          <ul>""")

for bullet in conclusion_bullets:
    html_content.append(f"            <li>{bullet}</li>")

html_content.append("""
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
html_dir = "/Users/garfiwang/Documents/Antigravity-2026/壽險佣金-2026/twelve-year-commissions"
if not os.path.exists(html_dir):
    os.makedirs(html_dir)
    
html_path = os.path.join(html_dir, "index.html")
with open(html_path, 'w', encoding='utf-8') as f:
    f.write("".join(html_content))

print("index.html for twelve-year-commissions created successfully!")
