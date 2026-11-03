/* 中1数学 教材棚 — 画面と印刷
   教材の中身は data/*.json に書く（このファイルは画面の仕組みだけ）。
   - data/common.json  … 生徒の順番・単元とステップ
   - data/library.json … プリントの一覧（1回だけ書く）
   - data/{生徒}.json  … その生徒の回（sets）・今の位置（now）・記録（log） */
"use strict";
pdfjsLib.GlobalWorkerOptions.workerSrc = "lib/pdfjs/pdf.worker.min.js";

const PRINT_DPI = 200;
const DAYS = {thu: {label: "木曜", kinds: ["thu", "hw", "teacher"]}, mon: {label: "月曜", kinds: ["mon"]}};
const $ = (s, el = document) => el.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const P = f => "pdf/" + f;
const ICON_PRINT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 9V3h12v6M6 18H4a1 1 0 0 1-1-1v-6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6a1 1 0 0 1-1 1h-2"/><rect x="6" y="14" width="12" height="7"/></svg>';
const ICON_CHEV = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>';

let D = null;                         // {common, library, s: {u: …, k: …}}
let TRACKS = [];
const ITEMS = new Map();              // file → ライブラリの項目
const STEPS = new Map();              // step id → {step, unit}
const USED = new Map();               // file → ["K①", …]

/* ------------------------------------------------------------ 保存（この端末だけ） */
const store = {
  get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} },
};
let checks = store.get("sugaku-shelf", {}) || {};
const ck = (track, set, k) => checks[`${track}/${set.id}-${k}`];
const isDone = (track, set) => D.s[track].checks.every(([k]) => ck(track, set, k));

/* ------------------------------------------------------------ データ */
async function loadData() {
  const get = n => fetch(`data/${n}.json`, {cache: "no-cache"}).then(r => {
    if (!r.ok) throw new Error(`data/${n}.json が読めません（${r.status}）`);
    return r.json();
  });
  const [common, library] = await Promise.all([get("common"), get("library")]);
  TRACKS = common.students;
  const studs = await Promise.all(TRACKS.map(get));
  D = {common, library, s: Object.fromEntries(TRACKS.map((t, i) => [t, studs[i]]))};
  for (const u of common.units) for (const st of u.steps) STEPS.set(st.id, {step: st, unit: u});
  for (const it of library.items) ITEMS.set(it.file, it);
  for (const t of TRACKS) for (const s of D.s[t].sets) for (const g of s.groups) for (const r of g.items) {
    if (!USED.has(r.file)) USED.set(r.file, []);
    const tag = D.s[t].name + s.label;
    if (!USED.get(r.file).includes(tag)) USED.get(r.file).push(tag);
  }
  $("#updated").textContent = common.updated ? `最終更新 ${common.updated.replace(/^(\d+)-0?(\d+)-0?(\d+)$/, "$1年$2月$3日")}` : "";
  // 生徒のタブを「今日の準備」と「教材ライブラリ」のあいだに入れる
  const lib = $('#tabs a[data-tab="lib"]');
  for (const t of TRACKS) lib.insertAdjacentHTML("beforebegin", `<a href="#${t}" data-tab="${t}">${esc(D.s[t].name)}</a>`);
}
const item = r => ({...(ITEMS.get(r.file) || {file: r.file, title: r.file + "（ライブラリにありません）", pages: "?"}), ...r});
const stepName = id => (STEPS.get(id) || {step: {name: id}}).step.name;
const stepFull = id => { const x = STEPS.get(id); return x ? `${x.unit.name}　${x.step.name}` : id; };
const curSet = t => D.s[t].sets.find(s => s.cur) || null;
const dayList = t => D.s[t].days || ["thu", "mon"];

/* ------------------------------------------------------------ 部品 */
function tile(it, {used = false} = {}) {
  const many = it.pages > 1 ? " stack" : "";
  const u = used && USED.get(it.file);
  return `<div class="tile${it.ans ? " ans" : ""}">
    <button type="button" class="open" data-act="view" data-file="${esc(it.file)}" aria-label="${esc(it.title)}を見る">
      <span class="thumb${many}" data-thumb="${esc(it.file)}"><span class="pg">${it.pages}p</span></span>
      <span class="t">${esc(it.title)}</span>${it.note ? `<span class="n">${esc(it.note)}</span>` : ""}
    </button>
    ${u && u.length ? `<span class="used">${u.map(x => `<span>${esc(x)}</span>`).join("")}</span>` : ""}
    <button type="button" class="btn pr" data-act="print" data-file="${esc(it.file)}">${ICON_PRINT}印刷</button>
  </div>`;
}
const stepChips = ids => (ids || []).map(id => `<a class="stepchip" href="#lib/${esc(id)}">${esc(stepName(id))}</a>`).join("");

function setCard(track, s, {open = false} = {}) {
  const T = D.s[track];
  const prog = T.checks.map(([k, l]) => `<i class="${ck(track, s, k) ? "on" : ""}" title="${esc(l)}"></i>`).join("");
  return `<details class="set${s.cur ? " cur" : ""}" id="${track}-${esc(s.id)}" data-track="${track}" data-set="${esc(s.id)}"${open ? " open" : ""}>
  <summary>
    <span class="sno">${esc(s.label)}</span>
    <span class="stitle">${esc(s.title)}</span>
    <span class="prog" aria-label="進み具合">${prog}${ICON_CHEV}</span>
    <span class="smeta">${s.cur ? '<span class="tag">今ここ</span>' : ""}${(s.steps || []).map(id => `<span>${esc(stepName(id))}</span>`).join("")}</span>
  </summary>
  <div class="sbody">
    ${s.note ? `<p class="note">${esc(s.note)}</p>` : ""}
    <div class="groups">${s.groups.map(g => `<section class="group ${esc(g.kind)}"><h3>${esc(g.label)}</h3><div class="tiles">${g.items.map(r => tile(item(r))).join("")}</div></section>`).join("")}</div>
    <div class="sfoot">
      <div class="chk">${T.checks.map(([k, l]) => `<label><input type="checkbox" data-act="check" data-key="${track}/${esc(s.id)}-${k}"${ck(track, s, k) ? " checked" : ""}>${esc(l)}</label>`).join("")}</div>
      <button type="button" class="btn primary" data-act="printset" data-track="${track}" data-set="${esc(s.id)}">${ICON_PRINT}${esc(s.label)}をまとめて印刷</button>
    </div>
  </div>
</details>`;
}

const logList = T => T.log && T.log.length
  ? `<ul class="log">${T.log.map(l => `<li><time>${esc(String(l.date).replace(/^\d+-0?(\d+)-0?(\d+)$/, "$1/$2"))}</time><span>${esc(l.text)}</span></li>`).join("")}</ul>`
  : `<p class="muted">まだ記録はありません。チャットで「${esc(T.name)}が四則混合Bを終えた・16問中12問」のように伝えると、ここに書きこみます。</p>`;

/* ------------------------------------------------------------ 画面：今日の準備 */
function autoDay() { const w = new Date().getDay(); return (w >= 2 && w <= 4) ? "thu" : "mon"; }  // 火〜木は木曜、金〜月は月曜
let prepDay = null;
function prepRows(day) {
  // 生徒ごとに、今ここの回から、その曜日に使うものを集める
  return TRACKS.map(t => {
    const T = D.s[t], s = curSet(t);
    if (!dayList(t).includes(day)) return {t, off: true};
    if (!s) return {t, none: true};
    const groups = s.groups.filter(g => DAYS[day].kinds.includes(g.kind));
    return {t, s, groups};
  });
}
function renderPrep() {
  const day = prepDay || autoDay();
  const rows = prepRows(day);
  const any = rows.some(r => r.groups && r.groups.some(g => g.items.length));
  return `
  <section class="prep-head">
    <div class="daysw" role="group" aria-label="曜日">
      ${Object.entries(DAYS).map(([k, d]) => `<button type="button" data-act="day" data-day="${k}" aria-pressed="${k === day}">${d.label}</button>`).join("")}
    </div>
    <h1>${DAYS[day].label}の準備</h1>
    <button type="button" class="btn key" data-act="printday" data-day="${day}"${any ? "" : " disabled"}>${ICON_PRINT}${DAYS[day].label}の分を全員まとめて印刷</button>
  </section>
  <div class="prep">
    ${rows.map(r => {
      const T = D.s[r.t];
      const head = `<header><a class="who" href="#${r.t}">${esc(T.name)}</a><div><b>${esc(stepFull(T.now && T.now.step))}</b>${T.now && T.now.text ? `<small>${esc(T.now.text)}</small>` : ""}</div></header>`;
      if (r.off) return `<article class="stu off">${head}<p class="muted">${DAYS[day].label}は来ない日です（宿題の日）。</p></article>`;
      if (r.none) return `<article class="stu">${head}<p class="empty">まだ教材がありません。作ったらここに出ます。</p></article>`;
      return `<article class="stu">${head}
        <p class="cur"><span class="tag">今ここ</span> <a href="#${r.t}/${esc(r.s.id)}">${esc(r.s.label)}　${esc(r.s.title)}</a></p>
        ${r.groups.length ? `<div class="groups">${r.groups.map(g => `<section class="group ${esc(g.kind)}"><h3>${esc(g.label)}</h3><div class="tiles">${g.items.map(x => tile(item(x))).join("")}</div></section>`).join("")}</div>`
          : `<p class="empty">この回には${DAYS[day].label}の教材がありません。</p>`}
      </article>`;
    }).join("")}
  </div>`;
}

/* ------------------------------------------------------------ 画面：生徒 */
let filter = store.get("sugaku-filter", {});
function renderTrack(track) {
  const T = D.s[track];
  const sets = [...T.sets].reverse();
  const cur = curSet(track);
  const f = filter[track] || "all";
  const shown = sets.filter(s => f === "all" || !isDone(track, s));
  return `
  <section class="now" aria-label="今の位置">
    <span class="lab">今ここ　${esc(T.longName)}</span>
    <span class="no">${cur ? esc(cur.label) : "—"}</span>
    <div><h1>${cur ? esc(cur.title) : esc(stepFull(T.now && T.now.step))}</h1>
      <div class="nu">${T.now ? `<a href="#lib/${esc(T.now.step)}">${esc(stepFull(T.now.step))}</a>${T.now.text ? "　" + esc(T.now.text) : ""}` : ""}</div></div>
    ${cur ? `<div class="acts">
      <button type="button" class="btn key" data-act="printset" data-track="${track}" data-set="${esc(cur.id)}">${ICON_PRINT}${esc(cur.label)}をまとめて印刷</button>
      <a class="btn" href="#${track}/${esc(cur.id)}">${esc(cur.label)}の教材を見る</a>
    </div>` : ""}
  </section>
  <div class="layout">
    <div>
      ${sets.length ? `<div class="filters" role="group" aria-label="しぼりこみ">
        ${[["all", "すべて"], ["todo", "まだ終わっていない"]].map(([k, l]) => `<button type="button" data-act="filter" data-track="${track}" data-f="${k}" aria-pressed="${f === k}">${l}</button>`).join("")}
      </div>` : ""}
      <div class="sets">${shown.map(s => setCard(track, s, {open: s === cur})).join("") || `<p class="empty">${sets.length ? "この条件の回はありません。" : "まだ教材がありません。作ったらここに①②…と並びます。"}</p>`}</div>
    </div>
    <aside class="side">
      ${T.about ? `<div class="panel"><h2>${esc(T.longName)}</h2>${T.about.map(p => `<p>${esc(p)}</p>`).join("")}</div>` : ""}
      <div class="panel"><h2>記録</h2>${logList(T)}</div>
    </aside>
  </div>`;
}

/* ------------------------------------------------------------ 画面：教材ライブラリ */
function renderLib() {
  const units = D.common.units;
  const here = id => TRACKS.filter(t => D.s[t].now && D.s[t].now.step === id).map(t => `<a class="here" href="#${t}">${esc(D.s[t].name)} 今ここ</a>`).join("");
  return `
  <p class="lead">プリントは単元・ステップごとに1回だけ置いてあります。どの生徒のどの回で使ったかはタイルの下に出ます。</p>
  <nav class="unav" aria-label="単元">${units.map(u => {
    const n = u.steps.reduce((a, st) => a + D.library.items.filter(i => i.step === st.id && !i.ans).length, 0);
    return `<a href="#lib/${esc(u.id)}">${esc(u.name)}${n ? `<small>${n}</small>` : ""}</a>`;
  }).join("")}</nav>
  ${units.map(u => `<section class="unit" id="lib-${esc(u.id)}">
    <h2>${esc(u.name)}</h2>
    <div class="steps">${u.steps.map((st, i) => {
      const its = D.library.items.filter(x => x.step === st.id).sort((a, b) => (a.ans ? 1 : 0) - (b.ans ? 1 : 0));
      return `<section class="stepsec${its.length ? "" : " none"}" id="lib-${esc(st.id)}">
        <h3><span class="sn">${i + 1}</span>${esc(st.name)}${here(st.id)}</h3>
        ${its.length ? `<div class="tiles">${its.map(x => tile(x, {used: true})).join("")}</div>` : `<p class="muted">まだプリントはありません。</p>`}
      </section>`;
    }).join("")}</div>
  </section>`).join("")}`;
}

/* ------------------------------------------------------------ 画面の切りかえ */
function route() {
  const [tab, sub] = (location.hash.replace(/^#/, "") || "junbi").split("/");
  const t = ["junbi", "lib", ...TRACKS].includes(tab) ? tab : "junbi";
  document.querySelectorAll(".tabs a").forEach(a => {
    if (a.dataset.tab === t) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
  });
  $("#app").innerHTML = t === "junbi" ? renderPrep() : t === "lib" ? renderLib() : renderTrack(t);
  document.title = (t === "junbi" ? "今日の準備" : t === "lib" ? "教材ライブラリ" : D.s[t].name) + " | 中1数学 教材棚";
  if (sub) {
    const el = t === "lib" ? $("#lib-" + CSS.escape(sub)) : $(`#${t}-${CSS.escape(sub)}`);
    if (el) {
      if (el.tagName === "DETAILS") el.open = true;
      el.scrollIntoView({block: "start"}); window.scrollBy(0, -64);
      if (el.classList.contains("stepsec")) { el.classList.add("flash"); setTimeout(() => el.classList.remove("flash"), 1600); }
    }
  } else window.scrollTo(0, 0);
  observeThumbs();
}

/* ------------------------------------------------------------ PDF を読む・描く */
const docs = new Map();
function getDoc(file) {
  if (!docs.has(file)) {
    const p = pdfjsLib.getDocument({url: P(file)}).promise;
    p.catch(() => docs.delete(file));
    docs.set(file, p);
  }
  return docs.get(file);
}
async function drawPage(file, n, cssWidth, ratio) {
  const doc = await getDoc(file);
  const page = await doc.getPage(n);
  const base = page.getViewport({scale: 1});
  const vp = page.getViewport({scale: (cssWidth * ratio) / base.width});
  const c = document.createElement("canvas");
  c.width = Math.ceil(vp.width); c.height = Math.ceil(vp.height);
  const ctx = c.getContext("2d");
  ctx.fillStyle = "#fff"; ctx.fillRect(0, 0, c.width, c.height);
  await page.render({canvasContext: ctx, viewport: vp}).promise;
  return c;
}

const thumbQueue = []; let thumbBusy = 0;
const thumbIO = "IntersectionObserver" in window ? new IntersectionObserver(es => {
  for (const e of es) if (e.isIntersecting) { thumbIO.unobserve(e.target); thumbQueue.push(e.target); }
  pumpThumbs();
}, {rootMargin: "200px"}) : null;
function observeThumbs() {
  document.querySelectorAll(".thumb[data-thumb]:not([data-done])").forEach(el => thumbIO ? thumbIO.observe(el) : thumbQueue.push(el));
  if (!thumbIO) pumpThumbs();
}
function pumpThumbs() {
  while (thumbBusy < 2 && thumbQueue.length) {
    const el = thumbQueue.shift();
    if (el.dataset.done) continue;
    el.dataset.done = "1"; thumbBusy++;
    drawPage(el.dataset.thumb, 1, el.clientWidth || 118, Math.min(window.devicePixelRatio || 1, 2))
      .then(c => el.prepend(c)).catch(() => { el.insertAdjacentHTML("afterbegin", '<span class="muted" style="padding:6px;display:block">読めません</span>'); })
      .finally(() => { thumbBusy--; pumpThumbs(); });
  }
}
document.addEventListener("toggle", e => { if (e.target.matches && e.target.matches("details[open]")) observeThumbs(); }, true);

/* ------------------------------------------------------------ ビューア */
const viewer = $("#viewer");
let viewing = null, viewIO = null;
async function openViewer(file) {
  const it = ITEMS.get(file) || {file, title: file, pages: "?"};
  viewing = it;
  $("#v-title").textContent = it.title;
  $("#v-pages").textContent = "";
  $("#v-open").href = P(file);
  const body = $("#v-body");
  body.innerHTML = "";
  if (!viewer.open) viewer.showModal();
  body.scrollTop = 0;
  try {
    const doc = await getDoc(file);
    if (viewing !== it) return;
    $("#v-pages").textContent = `${doc.numPages}ページ`;
    if (viewIO) viewIO.disconnect();
    viewIO = new IntersectionObserver(es => {
      for (const e of es) if (e.isIntersecting && !e.target.dataset.done) {
        e.target.dataset.done = "1";
        drawPage(file, +e.target.dataset.n, e.target.clientWidth, Math.min(window.devicePixelRatio || 1, 2) * 1.25)
          .then(c => e.target.prepend(c)).catch(() => {});
      }
    }, {root: body, rootMargin: "400px"});
    for (let i = 1; i <= doc.numPages; i++) {
      const d = document.createElement("div");
      d.className = "v-page"; d.dataset.n = i; d.setAttribute("aria-label", `${i}ページ目`);
      body.append(d); viewIO.observe(d);
    }
  } catch (e) {
    body.innerHTML = `<p class="v-err">このPDFを開けませんでした（pdf/${esc(file)}）。ファイル名がまちがっていないか確認してください。</p>`;
  }
}
$("#v-close").addEventListener("click", () => viewer.close());
$("#v-print").addEventListener("click", () => viewing && printJob(viewing.title, [{file: viewing.file, copies: 1}]));
viewer.addEventListener("close", () => { if (viewIO) viewIO.disconnect(); $("#v-body").innerHTML = ""; viewing = null; });

/* ------------------------------------------------------------ まとめて印刷（1つの回／その曜日の全員分） */
const sp = $("#setprint");
let spRows = [];
function openPrintList(title, sections) {
  // sections: [{label, kind, items:[item]}]
  $("#sp-title").textContent = title;
  spRows = [];
  let html = "";
  for (const sec of sections) {
    html += `<li class="g ${esc(sec.kind || "")}">${esc(sec.label)}</li>`;
    for (const it of sec.items) {
      const i = spRows.push({it, on: (it.copies ?? 1) > 0, copies: Math.max(it.copies ?? 1, 1)}) - 1;
      html += `<li><input type="checkbox" id="sp${i}" data-i="${i}"${spRows[i].on ? " checked" : ""}>
        <label class="nm" for="sp${i}">${esc(it.title)}<small>${it.pages}ページ${it.note ? "　" + esc(it.note) : ""}</small></label>
        <span class="step"><button type="button" data-i="${i}" data-d="-1" aria-label="${esc(it.title)}の部数をへらす">−</button><span id="spc${i}">${spRows[i].copies}部</span><button type="button" data-i="${i}" data-d="1" aria-label="${esc(it.title)}の部数をふやす">＋</button></span></li>`;
    }
  }
  $("#sp-list").innerHTML = html;
  spTotal();
  sp.dataset.title = title.replace(/をまとめて印刷$|を全員まとめて印刷$/, "");
  sp.showModal();
}
function openSetPrint(track, id) {
  const T = D.s[track], s = T.sets.find(x => x.id === id);
  if (!s) return;
  openPrintList(`${T.name} ${s.label}「${s.title}」をまとめて印刷`,
    s.groups.map(g => ({label: g.label, kind: g.kind, items: g.items.map(item)})));
}
function openDayPrint(day) {
  const secs = [];
  const seen = new Set();                 // 先生用（こたえ）は2人で同じものなら1部だけ
  for (const r of prepRows(day)) if (r.groups) for (const g of r.groups) {
    const items = g.items.filter(x => g.kind !== "teacher" || !seen.has(x.file));
    if (g.kind === "teacher") items.forEach(x => seen.add(x.file));
    if (items.length) secs.push({label: `${D.s[r.t].name}　${g.label}`, kind: g.kind, items: items.map(item)});
  }
  if (secs.length) openPrintList(`${DAYS[day].label}の分を全員まとめて印刷`, secs);
}
function spTotal() {
  const n = spRows.reduce((a, r) => a + (r.on ? r.it.pages * r.copies : 0), 0);
  $("#sp-total").textContent = `合計 ${n}ページ`;
  $("#sp-go").disabled = n === 0;
  $("#sp-go").textContent = n ? `${n}ページを印刷する` : "印刷する";
}
$("#sp-list").addEventListener("change", e => { const i = e.target.dataset.i; if (i != null) { spRows[i].on = e.target.checked; spTotal(); } });
$("#sp-list").addEventListener("click", e => {
  const b = e.target.closest("button[data-d]"); if (!b) return;
  const r = spRows[b.dataset.i];
  r.copies = Math.min(9, Math.max(1, r.copies + +b.dataset.d)); r.on = true;
  $("#spc" + b.dataset.i).textContent = r.copies + "部"; $("#sp" + b.dataset.i).checked = true; spTotal();
});
$("#sp-cancel").addEventListener("click", () => sp.close());
$("#sp-go").addEventListener("click", () => {
  const jobs = spRows.filter(r => r.on).map(r => ({file: r.it.file, copies: r.copies}));
  sp.close();
  printJob(sp.dataset.title, jobs);
});

/* ------------------------------------------------------------ 印刷のしくみ
   PDF をページごとに画像にして #print-root にならべ、ブラウザの印刷を呼ぶ。 */
const pageImg = new Map();
const progress = $("#progress");
let printing = false;
async function renderForPrint(file, n) {
  const k = file + "#" + n;
  if (pageImg.has(k)) return pageImg.get(k);
  const doc = await getDoc(file);
  const page = await doc.getPage(n);
  const base = page.getViewport({scale: 1});
  const c = await drawPage(file, n, base.width, PRINT_DPI / 72);
  const url = await new Promise(res => c.toBlob(b => res(URL.createObjectURL(b)), "image/png"));
  c.width = c.height = 0;
  pageImg.set(k, url);
  return url;
}
async function printJob(title, jobs) {
  if (printing || !jobs.length) return;
  printing = true;
  if (viewer.open) viewer.close();
  $("#pg-title").textContent = "印刷の準備をしています";
  $("#pg-btns").hidden = true; $("#pg-again").hidden = false; $("#pg-bar").style.width = "0"; $("#pg-text").textContent = "";
  progress.showModal();
  const root = $("#print-root");
  root.innerHTML = "";
  try {
    const docsN = await Promise.all(jobs.map(j => getDoc(j.file).then(d => d.numPages)));
    const total = docsN.reduce((a, n) => a + n, 0);
    const sheets = docsN.reduce((a, n, i) => a + n * jobs[i].copies, 0);
    let done = 0;
    const urls = [];
    for (let j = 0; j < jobs.length; j++) {
      const list = [];
      for (let n = 1; n <= docsN[j]; n++) {
        list.push(await renderForPrint(jobs[j].file, n));
        done++;
        $("#pg-bar").style.width = (100 * done / total) + "%";
        $("#pg-text").textContent = `${done} / ${total} ページ（印刷するのは全部で ${sheets} ページ）`;
      }
      for (let c = 0; c < jobs[j].copies; c++) urls.push(...list);
    }
    const frag = document.createDocumentFragment();
    const imgs = urls.map(u => { const d = document.createElement("div"); d.className = "sheet"; const im = new Image(); im.src = u; im.alt = ""; d.append(im); frag.append(d); return im; });
    root.append(frag);
    await Promise.all(imgs.map(im => im.decode ? im.decode().catch(() => {}) : null));
    progress.close();
    doPrint(title);
    $("#pg-title").textContent = "印刷画面を開きました";
    $("#pg-text").textContent = `全部で ${sheets} ページ。部数は印刷画面ではなく、ここでえらんだ部数になっています。`;
    $("#pg-btns").hidden = false;
    progress.showModal();
  } catch (e) {
    $("#pg-title").textContent = "印刷の準備ができませんでした";
    $("#pg-text").textContent = "PDF が読めませんでした。ページを読みこみなおして、もう一度ためしてください。";
    $("#pg-btns").hidden = false; $("#pg-again").hidden = true;
  } finally { printing = false; }
}
function doPrint(title) {
  const old = document.title;
  document.title = title || old;
  try { window.print(); } finally { setTimeout(() => { document.title = old; }, 500); }
}
$("#pg-again").addEventListener("click", () => { progress.close(); doPrint(); progress.showModal(); });
$("#pg-close").addEventListener("click", () => { progress.close(); $("#pg-again").hidden = false; });
window.__sugakuPrintJob = printJob;          // 動作確認用

/* ------------------------------------------------------------ 操作 */
document.addEventListener("click", e => {
  const b = e.target.closest("[data-act]");
  if (!b || b.tagName === "INPUT") return;
  const act = b.dataset.act;
  if (act === "view") openViewer(b.dataset.file);
  else if (act === "print") { const it = ITEMS.get(b.dataset.file); printJob(it ? it.title : b.dataset.file, [{file: b.dataset.file, copies: 1}]); }
  else if (act === "printset") { e.preventDefault(); openSetPrint(b.dataset.track, b.dataset.set); }
  else if (act === "printday") openDayPrint(b.dataset.day);
  else if (act === "day") { prepDay = b.dataset.day; $("#app").innerHTML = renderPrep(); observeThumbs(); }
  else if (act === "filter") {
    filter[b.dataset.track] = b.dataset.f; store.set("sugaku-filter", filter);
    $("#app").innerHTML = renderTrack(b.dataset.track); observeThumbs();
  }
});
document.addEventListener("change", e => {
  const k = e.target.dataset && e.target.dataset.key;
  if (!k) return;
  checks[k] = e.target.checked; store.set("sugaku-shelf", checks);
  const card = e.target.closest("details.set");
  if (card) {
    const t = card.dataset.track, T = D.s[t];
    card.querySelectorAll(".prog i").forEach((i, n) => i.classList.toggle("on", !!checks[`${t}/${card.dataset.set}-${T.checks[n][0]}`]));
  }
});
window.addEventListener("hashchange", route);

loadData().then(route).catch(err => {
  $("#app").innerHTML = `<p class="v-err">教材の一覧を読みこめませんでした：${esc(err.message)}</p>`;
});
