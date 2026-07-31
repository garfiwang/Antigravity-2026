# Firebase 互動元件程式碼庫 (100吋大螢幕 / 樂齡高可讀性版)

## 共用 Firebase 設定

```js
const firebaseConfig = {
  apiKey: "AIzaSyAYQhNavPSce17XtvDC5xnXyl9iUhW9KjA",
  authDomain: "teacherstudy-109ef.firebaseapp.com",
  projectId: "teacherstudy-109ef",
  storageBucket: "teacherstudy-109ef.firebasestorage.app",
  messagingSenderId: "196599230156",
  appId: "1:196599230156:web:cfe55d364df3ae1b9d5c69"
};
```

Firebase 專案：`teacherstudy-109ef`
SDK 版本：`11.0.2`（CDN：`https://www.gstatic.com/firebasejs/11.0.2/`）

**Firestore 集合命名規則：**
- 文字雲：`<簡報slug>_wordcloud`（例：`ai_course_wordcloud`）
- 投票：`<簡報slug>_poll_<頁碼>`
- 每份新簡報用不同集合，避免跨場次資料污染

---

## 元件一：即時文字雲 (樂齡大字版)

需要的 CDN（加在 `<head>` 裡）：
```html
<script src="https://cdn.jsdelivr.net/npm/wordcloud@1.2.2/src/wordcloud2.min.js"></script>
```

### Section HTML

```html
<!-- ② 互動文字雲 -->
<section id="slide-wordcloud">
  <h2 style="font-size:2.0em; margin-bottom:0.4em; color:var(--accent2);"><!-- 問題標題 --></h2>
  <div style="display:grid; grid-template-columns:360px 1fr; gap:20px; height:520px;">

    <!-- 左欄：輸入 + 排行 -->
    <div style="display:flex; flex-direction:column; gap:14px;">
      <div style="background:rgba(255,255,255,0.08); border-radius:14px; padding:18px;">
        <div style="font-size:0.75em; color:var(--warn); font-weight:800; margin-bottom:10px;">輸入你的答案</div>
        <input id="wc-input" type="text" placeholder="輸入關鍵詞…" maxlength="20"
          style="width:100%; padding:12px 16px; border-radius:10px; border:2px solid rgba(64,196,255,0.5);
                 background:rgba(255,255,255,0.12); color:#fff; font-size:18px;
                 box-sizing:border-box; font-family:inherit; outline:none;" />
        <button id="wc-btn"
          style="width:100%; margin-top:10px; padding:12px; background:var(--accent); color:#ffffff;
                 border:none; border-radius:10px; font-weight:800; font-size:18px; cursor:pointer;">
          送出 ↵
        </button>
      </div>
      <div style="background:rgba(255,255,255,0.08); border-radius:14px; padding:18px; flex:1; overflow:hidden; display:flex; flex-direction:column;">
        <div style="font-size:0.75em; color:var(--accent2); font-weight:800; margin-bottom:10px;">
          熱門答案
          <span style="display:inline-block; background:#ff4757; color:#fff; padding:3px 10px;
                       border-radius:12px; font-size:0.85em; animation:pulse 1.5s infinite;">LIVE</span>
        </div>
        <div id="wc-list" style="font-size:0.7em; overflow-y:auto; flex:1; color:#fff; font-weight:600;"></div>
        <div style="margin-top:10px; font-size:0.65em; color:#e0e0e0; border-top:1px solid rgba(255,255,255,0.15); padding-top:8px; font-weight:700;">
          總提交：<span id="wc-total" style="color:var(--accent); font-weight:900;">0</span>　
          不同答案：<span id="wc-unique" style="color:var(--accent2); font-weight:900;">0</span>
        </div>
      </div>
    </div>

    <!-- 右欄：文字雲 -->
    <div style="background:rgba(255,255,255,0.06); border-radius:16px; overflow:hidden;
                position:relative; border:2px solid rgba(255,255,255,0.12);">
      <canvas id="wc-canvas" style="width:100%; height:100%; display:block;"></canvas>
      <div id="wc-empty" style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
                                 color:#bbb; font-size:0.85em; text-align:center;
                                 pointer-events:none; line-height:2; font-weight:700;">
        請大家輸入第一個答案<br>文字雲將即時放大顯示 ✨
      </div>
    </div>
  </div>
</section>
```

### Firebase Module Script（放在 `</body>` 前）

```html
<script type="module">
  import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.0.2/firebase-app.js';
  import {
    getFirestore, collection, addDoc, onSnapshot,
    serverTimestamp, query, orderBy
  } from 'https://www.gstatic.com/firebasejs/11.0.2/firebase-firestore.js';

  const firebaseConfig = {
    apiKey: "AIzaSyAYQhNavPSce17XtvDC5xnXyl9iUhW9KjA",
    authDomain: "teacherstudy-109ef.firebaseapp.com",
    projectId: "teacherstudy-109ef",
    storageBucket: "teacherstudy-109ef.firebasestorage.app",
    messagingSenderId: "196599230156",
    appId: "1:196599230156:web:cfe55d364df3ae1b9d5c69"
  };
  const app = initializeApp(firebaseConfig);
  const fdb = getFirestore(app);
  // ⚠️ 集合名稱：<簡報slug>_wordcloud
  const wordsRef = collection(fdb, '<slug>_wordcloud');

  const COLORS = ['#40c4ff','#ff6b35','#ffd740','#69f0ae','#ce93d8','#80deea','#f48fb1'];
  let wcData = [];

  window.wcSubmit = async function() {
    const input = document.getElementById('wc-input');
    const word = input.value.trim();
    if (!word) return;
    const btn = document.getElementById('wc-btn');
    btn.disabled = true;
    try {
      await addDoc(wordsRef, { word, created_at: serverTimestamp() });
      input.value = '';
    } catch(e) { console.error(e); }
    finally { btn.disabled = false; }
  };

  document.getElementById('wc-input')?.addEventListener('keypress', e => {
    if (e.key === 'Enter') window.wcSubmit();
  });
  document.getElementById('wc-btn')?.addEventListener('click', window.wcSubmit);

  onSnapshot(query(wordsRef, orderBy('created_at', 'asc')), snap => {
    const words = [];
    snap.forEach(doc => words.push(doc.data().word));
    const counts = {};
    words.forEach(w => counts[w] = (counts[w] || 0) + 1);
    wcData = Object.entries(counts).sort((a, b) => b[1] - a[1]);

    document.getElementById('wc-total').textContent = words.length;
    document.getElementById('wc-unique').textContent = wcData.length;

    const listEl = document.getElementById('wc-list');
    listEl.innerHTML = wcData.slice(0, 10).map(([w, c]) =>
      `<div style="display:flex;justify-content:space-between;padding:8px 0;
                   border-bottom:1px solid rgba(255,255,255,0.12);">
        <span>${w}</span><span style="color:var(--accent);font-weight:900;">${c}</span>
      </div>`
    ).join('') || '<div style="color:#aaa;padding:12px 0;">尚無資料</div>';

    const empty = document.getElementById('wc-empty');
    if (empty) empty.style.display = wcData.length > 0 ? 'none' : '';
    drawWordCloud();
  });

  function drawWordCloud() {
    const canvas = document.getElementById('wc-canvas');
    if (!canvas || typeof WordCloud === 'undefined') return;
    const rect = canvas.getBoundingClientRect();
    if (rect.width < 10 || rect.height < 10) return;
    canvas.width = rect.width;
    canvas.height = rect.height;
    if (wcData.length === 0) return;
    const maxCount = wcData[0][1];
    WordCloud(canvas, {
      list: wcData.map(([w, c]) => [w, Math.max(32, Math.round((c / maxCount) * 110))]),
      gridSize: 8,
      weightFactor: 1,
      fontFamily: '"PingFang TC", "Noto Sans TC", "Microsoft JhengHei", sans-serif',
      color: () => COLORS[Math.floor(Math.random() * COLORS.length)],
      backgroundColor: 'transparent',
      rotateRatio: 0.2,
      shuffle: true,
    });
  }

  Reveal.on('slidechanged', e => {
    if (e.currentSlide?.id === 'slide-wordcloud') setTimeout(drawWordCloud, 150);
  });
</script>
```

---

## 元件二：單選投票 (樂齡巨字版)

### Section HTML

```html
<section id="slide-poll">
  <h2 style="font-size:2.1em; color:var(--accent2); margin-bottom:0.6em;"><!-- 投票問題 --></h2>
  <div id="poll-options" style="display:flex; flex-direction:column; gap:16px; margin-top:1.0em;">
    <!-- 動態生成 -->
  </div>
  <div style="font-size:0.75em; color:var(--text-sub); text-align:center; margin-top:1.2em; font-weight:700;">
    已投票：<span id="poll-total" style="color:var(--accent); font-weight:900;">0</span> 人
  </div>
</section>
```

### Firebase Module Script

```html
<script type="module">
  import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.0.2/firebase-app.js';
  import {
    getFirestore, doc, setDoc, onSnapshot,
    serverTimestamp, getDoc
  } from 'https://www.gstatic.com/firebasejs/11.0.2/firebase-firestore.js';

  const firebaseConfig = {
    apiKey: "AIzaSyAYQhNavPSce17XtvDC5xnXyl9iUhW9KjA",
    authDomain: "teacherstudy-109ef.firebaseapp.com",
    projectId: "teacherstudy-109ef",
    storageBucket: "teacherstudy-109ef.firebasestorage.app",
    messagingSenderId: "196599230156",
    appId: "1:196599230156:web:cfe55d364df3ae1b9d5c69"
  };
  const app = initializeApp(firebaseConfig);
  const fdb = getFirestore(app);

  // 選項設定（根據實際題目修改）
  const OPTIONS = [
    { id: 'a', label: '選項 A' },
    { id: 'b', label: '選項 B' },
    { id: 'c', label: '選項 C' },
  ];
  // ⚠️ 集合名稱：<簡報slug>_poll_<頁碼>
  const pollRef = doc(fdb, '<slug>_poll', 'results');

  const userId = 'user_' + Math.random().toString(36).slice(2, 9);
  let myVote = null;

  // 渲染選項
  const container = document.getElementById('poll-options');
  OPTIONS.forEach(opt => {
    const btn = document.createElement('button');
    btn.id = `poll-btn-${opt.id}`;
    btn.innerHTML = `
      <div style="display:flex;align-items:center;gap:18px;">
        <span style="flex:0 0 32px;height:32px;border-radius:50%;border:3px solid rgba(255,255,255,0.4);
                     display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:900;"
              id="poll-check-${opt.id}"></span>
        <span style="flex:1;text-align:left;font-size:0.85em;font-weight:700;">${opt.label}</span>
        <span id="poll-bar-wrap-${opt.id}"
              style="flex:0 0 200px;height:16px;background:rgba(255,255,255,0.15);border-radius:8px;overflow:hidden;">
          <div id="poll-bar-${opt.id}" style="height:100%;width:0;background:var(--accent2);border-radius:8px;transition:width 0.4s;"></div>
        </span>
        <span id="poll-pct-${opt.id}" style="flex:0 0 70px;text-align:right;font-size:0.85em;color:var(--warn);font-weight:800;">0%</span>
      </div>
    `;
    btn.style.cssText = `width:100%;padding:18px 24px;background:rgba(255,255,255,0.08);
      border:2px solid rgba(255,255,255,0.2);border-radius:14px;color:#fff;
      cursor:pointer;font-family:inherit;text-align:left;`;
    btn.onclick = () => vote(opt.id);
    container.appendChild(btn);
  });

  async function vote(optId) {
    myVote = optId;
    const data = {};
    data[`votes.${userId}`] = optId;
    data.updated_at = serverTimestamp();
    await setDoc(pollRef, data, { merge: true });
  }

  onSnapshot(pollRef, snap => {
    const data = snap.data() || {};
    const votes = data.votes || {};
    const counts = {};
    OPTIONS.forEach(o => counts[o.id] = 0);
    Object.values(votes).forEach(v => { if (counts[v] !== undefined) counts[v]++; });
    const total = Object.values(counts).reduce((a, b) => a + b, 0);

    document.getElementById('poll-total').textContent = total;
    OPTIONS.forEach(opt => {
      const pct = total > 0 ? Math.round((counts[opt.id] / total) * 100) : 0;
      document.getElementById(`poll-bar-${opt.id}`).style.width = pct + '%';
      document.getElementById(`poll-pct-${opt.id}`).textContent = pct + '%';
      const check = document.getElementById(`poll-check-${opt.id}`);
      if (myVote === opt.id) {
        check.textContent = '✓';
        check.style.background = 'var(--accent2)';
        check.style.borderColor = 'var(--accent2)';
      }
    });
  });
</script>
```
