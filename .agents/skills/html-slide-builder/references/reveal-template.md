# Reveal.js HTML 基礎模板 (100吋大螢幕 / 樂齡高可讀性版)

## 完整 HTML 骨架

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title><!-- 簡報標題 --></title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reset.css" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/night.css" />
  <!-- 若有文字雲，加這行 -->
  <!-- <script src="https://cdn.jsdelivr.net/npm/wordcloud@1.2.2/src/wordcloud2.min.js"></script> -->
  <style>
    /* === 100 吋大螢幕 / 樂齡極致高對比設計變數 === */
    :root {
      --accent:  #ff6b35;  /* 醒目明亮橘 */
      --accent2: #40c4ff;  /* 高對比天空藍 */
      --success: #69f0ae;  /* 明亮翡翠綠 */
      --warn:    #ffd740;  /* 鮮豔琥珀黃 */
      --bg-dark: #0a0d14;  /* 超深純淨背景 */
      --text-main: #ffffff;/* 滿分純白文字 */
      --text-sub:  #e0e0e0;/* 高可讀副文字 (絕不使用灰暗色) */
    }

    .reveal {
      font-family: 'PingFang TC', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif;
      color: var(--text-main);
    }
    .reveal h1, .reveal h2, .reveal h3 {
      font-family: 'PingFang TC', 'Noto Sans TC', 'Microsoft JhengHei', sans-serif;
      font-weight: 800;
      letter-spacing: -0.01em;
      line-height: 1.2;
    }
    /* 100 吋大螢幕字體巨大化 */
    .reveal h1 { font-size: 2.8em; color: var(--text-main); text-shadow: 0 4px 12px rgba(0,0,0,0.8); }
    .reveal h2 { font-size: 2.1em; color: var(--accent2); margin-bottom: 0.6em; text-shadow: 0 2px 8px rgba(0,0,0,0.8); }
    .reveal h3 { font-size: 1.5em; color: var(--warn); }
    .reveal p, .reveal li { font-size: 0.85em; line-height: 1.7; color: var(--text-sub); }

    .reveal .progress { color: var(--accent); height: 6px; }
    .reveal .fragment { opacity: 0.15; }
    .reveal .fragment.visible { opacity: 1; }

    /* === 封面 === */
    .title-slide { text-align: center; }
    .title-slide .tag {
      display: inline-block;
      background: var(--accent);
      color: #ffffff;
      padding: 8px 24px;
      border-radius: 30px;
      font-size: 0.75em;
      letter-spacing: 0.08em;
      margin-bottom: 1.2em;
      font-weight: 700;
      box-shadow: 0 4px 16px rgba(255, 107, 53, 0.4);
    }
    .title-slide .subtitle { font-size: 1.0em; color: var(--warn); margin-top: 0.8em; font-weight: 600; }
    .title-slide .author   { margin-top: 2.2em; font-size: 0.75em; color: var(--text-sub); font-weight: 500; }

    /* === 統計數字卡 (超大字) === */
    .stat-row { display: flex; gap: 28px; justify-content: center; margin-top: 1.2em; }
    .stat-card {
      background: rgba(255,255,255,0.08);
      border: 2px solid rgba(255,255,255,0.25);
      border-radius: 16px;
      padding: 28px 36px;
      text-align: center;
      flex: 1;
    }
    .stat-card .num   { font-size: 2.6em; font-weight: 900; color: var(--accent); line-height: 1.1; }
    .stat-card .label { font-size: 0.75em; color: var(--text-main); margin-top: 12px; font-weight: 700; }

    /* === 優勢卡（大卡片、大圖標、單頁最多 3 個）=== */
    .adv-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-top: 0.8em; }
    .adv-card {
      background: rgba(255,255,255,0.07);
      border-top: 6px solid var(--accent2);
      border-radius: 14px;
      padding: 24px;
      text-align: center;
    }
    .adv-card .adv-icon { margin-bottom: 14px; }
    .adv-card .adv-icon img {
      width: 96px; height: 96px; object-fit: contain;
      display: block; margin: 0 auto;
      filter: drop-shadow(0 0 16px rgba(64,196,255,0.8));
    }
    .adv-card .adv-title { font-size: 1.0em; font-weight: 800; color: var(--accent2); margin-bottom: 10px; }
    .adv-card .adv-desc  { font-size: 0.75em; color: var(--text-sub); line-height: 1.7; font-weight: 500; }

    /* === VS 對比（清晰兩對照）=== */
    .vs-grid { display: grid; grid-template-columns: 1fr 80px 1fr; gap: 12px; align-items: stretch; margin-top: 0.8em; }
    .vs-col { background: rgba(255,255,255,0.07); border-radius: 16px; padding: 24px; }
    .vs-col.left-col  { border-top: 5px solid var(--accent2); }
    .vs-col.right-col { border-top: 5px solid var(--warn); }
    .vs-label { font-size: 1.0em; font-weight: 800; margin-bottom: 14px; letter-spacing: 0.05em; }
    .vs-label.left  { color: var(--accent2); }
    .vs-label.right { color: var(--warn); }
    .vs-center { display: flex; align-items: center; justify-content: center; font-size: 2.0em; font-weight: 900; color: var(--accent); }
    .vs-col ul { font-size: 0.75em; list-style: none; padding: 0; margin: 0; }
    .vs-col ul li { padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.12); color: var(--text-main); font-weight: 600; }
    .vs-col ul li:last-child { border-bottom: none; }
    .vs-col ul li::before { content: "✦ "; color: var(--accent2); font-weight: bold; }

    /* === 時間軸（高字體放大）=== */
    .timeline { position: relative; padding-left: 48px; margin-top: 1.0em; }
    .timeline::before {
      content: ''; position: absolute; left: 18px; top: 8px; bottom: 8px;
      width: 4px; background: rgba(255,255,255,0.3);
    }
    .timeline-item { position: relative; margin-bottom: 24px; font-size: 0.75em; }
    .timeline-item::before {
      content: ''; position: absolute; left: -38px; top: 6px;
      width: 16px; height: 16px; border-radius: 50%;
      background: var(--accent); border: 3px solid #0a0d14;
    }
    .timeline-item .ti-date { color: var(--accent); font-weight: 800; font-size: 1.1em; margin-bottom: 4px; }
    .timeline-item .ti-text { color: var(--text-main); font-weight: 600; }

    /* === 引用（重點金句）=== */
    .quote-box {
      background: rgba(255,255,255,0.07);
      border-left: 8px solid var(--accent);
      border-radius: 12px;
      padding: 28px 36px;
      margin: 1.0em 0;
      font-size: 0.95em;
      color: #ffffff;
      font-weight: 600;
      line-height: 1.8;
    }
    .quote-author { font-size: 0.75em; color: var(--accent2); text-align: right; margin-top: 14px; font-weight: 700; }

    /* === 結論卡 === */
    .conclusion-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 1.0em; }
    .conclusion-card { border-radius: 16px; padding: 26px; font-size: 0.75em; }
    .conclusion-card.positive {
      background: rgba(64,196,255,0.15);
      border: 2px solid rgba(64,196,255,0.5);
    }
    .conclusion-card.caution {
      background: rgba(255,215,64,0.15);
      border: 2px solid rgba(255,215,64,0.5);
    }
    .conclusion-card .cc-title { font-size: 1.2em; font-weight: 800; margin-bottom: 12px; }
    .conclusion-card.positive .cc-title { color: var(--accent2); }
    .conclusion-card.caution  .cc-title { color: var(--warn); }
    .conclusion-card ul { list-style: none; padding: 0; margin: 0; color: var(--text-main); line-height: 1.8; font-weight: 600; }
    .conclusion-card ul li::before { content: "➜ "; color: var(--accent); font-weight: bold; }

    /* === 封底 === */
    .end-slide { text-align: center; }
    .end-slide .big { font-size: 3.5em; margin-bottom: 0.3em; }
    .end-slide .tagline { font-size: 1.0em; color: var(--warn); font-weight: 700; }

    /* === LIVE 動畫 === */
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }
  </style>
</head>
<body>
<div class="reveal">
  <div class="slides">

    <!-- 投影片從這裡開始 -->

    <!-- 封面範例 -->
    <section data-background-image="images/cover.png"
             data-background-opacity="0.15"
             data-background-size="cover">
      <div class="title-slide">
        <div class="tag"><!-- 場次標籤，如：樂齡講座 · 核心課程 --></div>
        <h1><!-- 主標題 --></h1>
        <h2 style="color:var(--accent); margin-top:0.3em;"><!-- 副標題 --></h2>
        <p class="subtitle"><!-- 說明文字 --></p>
        <p class="author"><!-- 講師 / 日期 --></p>
      </div>
    </section>

    <!-- 更多投影片... -->

  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
<script>
  Reveal.initialize({
    width: 1920,
    height: 1080,
    margin: 0.06,
    minScale: 0.2,
    maxScale: 2.0,
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

<!-- 若有互動元件，Firebase module script 加在這裡 -->

</body>
</html>
```

---

## 常用 Section 片段

### 數字統計頁 (樂齡巨字版)
```html
<section>
  <h2>關鍵數字</h2>
  <div class="stat-row fragment">
    <div class="stat-card">
      <div class="num">440<span style="font-size:0.6em">萬+</span></div>
      <div class="label">說明文字</div>
    </div>
    <div class="stat-card">
      <div class="num">8,200</div>
      <div class="label">說明文字</div>
    </div>
  </div>
</section>
```

### 3 欄優勢卡（單頁最多 3 欄，圖標放大）
```html
<section>
  <h2>三大重點</h2>
  <div class="adv-grid">
    <div class="adv-card fragment">
      <div class="adv-icon"><img src="images/icon_a.png" alt="A"></div>
      <div class="adv-title">重點 A</div>
      <div class="adv-desc">大字清晰說明...</div>
    </div>
    <!-- 最多 3 個卡片 -->
  </div>
</section>
```

### 封底
```html
<section data-background-image="images/ending.png"
         data-background-opacity="0.15"
         data-background-size="cover">
  <div class="end-slide">
    <div class="big">
      <img src="images/icon_globe.png" alt=""
           style="width:200px;height:200px;object-fit:contain;
                  filter:drop-shadow(0 0 30px rgba(64,196,255,0.9));">
    </div>
    <h1 style="color:var(--accent2);"><!-- 感謝聆聽 --></h1>
    <p class="tagline"><!-- 祝福金句 --></p>
  </div>
</section>
```
