"""中1 定期テスト対策の共通部品（方程式の利用・比例と反比例）

- graph(...)        … 座標平面の SVG（−R〜R のマス目、比例の直線・反比例の曲線・点）
- t(s)              … 文の中の式（mathlib.fm と同じ書き方。x・y は KaTeX の筆記体）
- hw_notebook(...)  … 宿題（A4 1枚に2日分・答えは自学ノート）の問題とこたえ
- hw_writein(...)   … 宿題（1日1ページ・プリントに直接書く）の問題とこたえ
- worksheet(...)    … 授業・自習プリント（4ページ・1ページ左右2列×n問）の問題とこたえ

問題は dict：{"q": 問題文の HTML, "a": こたえの HTML, "fig": SVG（なくてよい）, "eq": (方程式, 答え) で SymPy 確認（なくてよい）}
"""
import re
from fractions import Fraction as Fr

import sympy as sp
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr,
                                        standard_transformations)

from mathlib import CIRC, CSS, fm, fmb, head, tex, to_tex

X = sp.Symbol("x")
TR = standard_transformations + (implicit_multiplication_application,)


def t(s):
    return fm(s)


def tb(s):
    return fmb(s)


# ------------------------------------------------------------ 確認
def solve1(eq):
    """方程式の文字列（mathlib の書き方。比例式は a:b=c:d）を解く"""
    s = eq.replace(" ", "")
    if ":" in s:                                  # 比例式 a:b=c:d → ad=bc
        L, R = s.split("=")
        a, b = L.split(":")
        c, d = R.split(":")
        s = f"({a})*({d})=({b})*({c})"
    s = re.sub(r"\{", "((", s).replace("|", ")/(").replace("}", "))")
    L, R = s.split("=")
    sol = sp.solve(sp.Eq(parse_expr(L, transformations=TR), parse_expr(R, transformations=TR)), X)
    return sol


def check_eq(eq, ans):
    sol = solve1(eq)
    assert sol == [ans], (eq, sol, ans)


def check_all(probs, tag=""):
    for p in probs:
        if p.get("eq"):
            check_eq(*p["eq"])
        for c in p.get("checks", []):
            assert c, (tag, p["q"][:40])


# ------------------------------------------------------------ グラフ
def graph(R=5, line=None, hyper=None, pts=(), size=46, labels=True, grid=True, ans_line=None, ans_hyper=None, ans_pts=()):
    """line=Fraction（比例 y=ax の a）、hyper=a（反比例 y=a/x）、pts=[(x, y, 名前)]
    ans_line・ans_hyper・ans_pts は「こたえ」にだけ赤で出る（問題では見えない：class hv）"""
    u = 10                                     # 1マス=10（viewBox）
    W = (2 * R + 2) * u
    o = W / 2

    def P(x, y):
        return o + x * u, o - y * u

    s = [f'<svg viewBox="0 0 {W} {W}" width="{size}mm" height="{size}mm" class=gr xmlns="http://www.w3.org/2000/svg">']
    if grid:
        for k in range(-R, R + 1):
            x0, _ = P(k, 0)
            _, y0 = P(0, k)
            s.append(f'<line x1="{x0}" y1="{P(0, R)[1]}" x2="{x0}" y2="{P(0, -R)[1]}" stroke="#ccc" stroke-width=".5"/>')
            s.append(f'<line x1="{P(-R, 0)[0]}" y1="{y0}" x2="{P(R, 0)[0]}" y2="{y0}" stroke="#ccc" stroke-width=".5"/>')
    ax0, ay0 = P(-R - .6, 0)
    ax1, _ = P(R + .7, 0)
    _, by0 = P(0, -R - .6)
    _, by1 = P(0, R + .7)
    s.append(f'<line x1="{ax0}" y1="{ay0}" x2="{ax1}" y2="{ay0}" stroke="#111" stroke-width="1"/>')
    s.append(f'<polygon points="{ax1},{ay0} {ax1 - 4},{ay0 - 2.2} {ax1 - 4},{ay0 + 2.2}" fill="#111"/>')
    s.append(f'<line x1="{o}" y1="{by0}" x2="{o}" y2="{by1}" stroke="#111" stroke-width="1"/>')
    s.append(f'<polygon points="{o},{by1} {o - 2.2},{by1 + 4} {o + 2.2},{by1 + 4}" fill="#111"/>')
    st = 'font-family="KaTeX_Math, serif" font-style="italic" font-size="9"'
    s.append(f'<text x="{ax1 - 2}" y="{ay0 + 9}" {st}>x</text><text x="{o + 3}" y="{by1 + 6}" {st}>y</text>')
    s.append(f'<text x="{o - 8}" y="{o + 9}" font-family="KaTeX_Math, serif" font-style="italic" font-size="8">O</text>')
    if labels:
        nt = 'font-family="KaTeX_Main, serif" font-size="6.5" fill="#333"'
        for k in range(-R, R + 1):
            if k == 0:
                continue
            x0, _ = P(k, 0)
            _, y0 = P(0, k)
            lab = str(k).replace("-", "−")
            s.append(f'<text x="{x0}" y="{o + 7.5}" text-anchor="middle" {nt}>{lab}</text>')
            s.append(f'<text x="{o - 2.5}" y="{y0 + 2.3}" text-anchor="end" {nt}>{lab}</text>')
    def curves(line, hyper, pts, col):
        out = []
        if line is not None:
            a = Fr(line)
            xs = R + .4 if abs(a) <= 1 else (R + .4) / abs(a)
            (x1, y1), (x2, y2) = P(-xs, -a * xs), P(xs, a * xs)
            out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="1.4"/>')
        if hyper is not None:
            for sgn in (1, -1):
                pts_ = []
                n = 160
                xmin = abs(hyper) / (R + .4)
                for i in range(n + 1):
                    x = sgn * (xmin + (R + .4 - xmin) * i / n)
                    pts_.append(P(x, hyper / x))
                out.append(f'<polyline fill="none" stroke="{col}" stroke-width="1.4" points="' + " ".join(f"{a:.2f},{b:.2f}" for a, b in pts_) + '"/>')
        for (x, y, name) in pts:
            cx, cy = P(x, y)
            out.append(f'<circle cx="{cx}" cy="{cy}" r="2" fill="{col}"/>')
            if name:
                out.append(f'<text x="{cx + 3}" y="{cy - 3}" font-family="Noto Sans CJK JP" font-weight="700" font-size="8" fill="{col}">{name}</text>')
        return out

    s += curves(line, hyper, pts, "#111")
    if ans_line is not None or ans_hyper is not None or ans_pts:
        s.append('<g class=hv>' + "".join(curves(ans_line, ans_hyper, ans_pts, "currentColor")) + '</g>')
    s.append("</svg>")
    return "".join(s)


# ------------------------------------------------------------ 表・座標（こたえを中に持つ）
def fs(v):
    """Fraction → 式の文字列（mathlib の書き方）"""
    v = Fr(v)
    if v.denominator == 1:
        return str(v.numerator)
    return ("-" if v < 0 else "") + "{" + str(abs(v.numerator)) + "|" + str(v.denominator) + "}"


def table(xs, fn=None):
    """x の表。fn を渡すと y のらんに答えが入る（こたえのときだけ赤で見える）"""
    h = "".join(f"<td>{t(str(v))}</td>" for v in xs)
    b = "".join(f"<td>{('<span class=hv>' + t(fs(fn(x))) + '</span>') if fn else ''}</td>" for x in xs)
    return f"<table class=tb><tr><th>{t('x')}</th>{h}</tr><tr><th>{t('y')}</th>{b}</tr></table>"


def tvals(fn, xs):
    return ", ".join(t(fs(fn(x))) for x in xs)


def coords(pts, per_line=2):
    """「A（　,　）B（　,　）」の書きこみ欄。こたえでは赤で座標が入る"""
    out = []
    for i, (x, y, name) in enumerate(pts):
        v = f"{x}, {y}".replace("-", "−")
        out.append(f"{name}（<span class=hv>{v}</span>）")
        if (i + 1) % per_line == 0 and i + 1 < len(pts):
            out.append("<br>")
        else:
            out.append("　")
    return "".join(out)


# ------------------------------------------------------------ こたえ（問題のプリントに赤で書きこんだ形・11/6 先生の希望）
FILL_CSS = """
.hv { visibility: hidden; }
"""
ANS_FILL_CSS = """
.hv { visibility: visible !important; color: #d0021b; }
.ra { color: #d0021b; font-size: 10.5pt; line-height: 1.6; margin-top: 1.2mm; }
.ra b { font-weight: 700; }
.fill { display: inline-block; min-width: 30mm; border-bottom: .8pt solid #111; color: #d0021b; font-weight: 700; text-align: center; }
.ans-tag { color: #d0021b; font-weight: 700; margin-left: 2mm; }
"""


def ans_head(title, sub):
    return head(f"{title}<span class=ans-tag>こたえ</span>", sub, name=False)


# ------------------------------------------------------------ 宿題（ノートに書く・A4 1枚に2日分）
HWN_CSS = """
.day { flex: 1; display: flex; flex-direction: column; margin-top: 3mm; min-height: 0; }
.day + .day { border-top: 1pt dashed #999; padding-top: 3mm; }
.band { display: flex; align-items: center; gap: 4mm; background: #fbefdc; color: #7a4508; border-radius: 2mm;
        padding: 1.6mm 4mm; font-weight: 700; font-size: 12pt; }
.band .sp { margin-left: auto; white-space: nowrap; font-weight: 400; font-size: 10.5pt; color: #111; }
.band .ck::before { content: ""; display: inline-block; width: 4.5mm; height: 4.5mm; border: .8pt solid #111; margin-right: 1.5mm; vertical-align: -1mm; }
.point { font-size: 10pt; margin: 1.8mm 1mm 0; }
.hq { flex: 1; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 2mm 7mm; margin-top: 2mm; }
.hq .p { font-size: 11pt; line-height: 1.7; display: flex; gap: 2mm; }
.hq .p .no { font-size: 13pt; flex: none; }
.hq .p .fig { margin-top: 1mm; }
.rule { margin-top: 2.5mm; font-size: 10pt; border: .8pt solid #111; border-radius: 2mm; padding: 1.8mm 4mm; line-height: 1.55; }
.gr { display: block; }
"""


def hw_notebook(title, days, rule, answer=False):
    """days：[(曜日, ポイント, [問題×4])]。A4 1枚に2日分。answer=True でこたえ（同じ形に赤で書きこむ）"""
    pages = []
    for d in range(0, len(days), 2):
        body = ""
        for k in range(d, min(d + 2, len(days))):
            youbi, point, probs = days[k]
            check_all(probs, f"{k + 1}日目")
            cells = ""
            for j, p in enumerate(probs):
                ra = ""
                if answer:
                    if not p.get("noa"):
                        ra = f"<div class=ra>{p['a']}</div>"
                    elif p.get("fa"):
                        ra = f"<div class=ra>答え <b>{p['fa']}</b></div>"
                fig = ("<div class=fig>" + p["fig"] + "</div>") if p.get("fig") else ""
                cells += f"<div class=p><span class=no>{CIRC[j]}</span><div>{p['q']}{ra}{fig}</div></div>"
            body += (f"<div class=day><div class=band>{k + 1}日目（{youbi}）<span class=sp><span class=ck>丸つけした</span></span></div>"
                     f"<p class=point>ポイント：{point}</p><div class=hq>{cells}</div></div>")
        sub = f"{d + 1}日目・{d + 2}日目（1日4問）" if d + 1 < len(days) else f"{d + 1}日目（1日4問）"
        hd = ans_head(title, sub) if answer else head(title, sub)
        pages.append(f"<div class=page>{hd}{rule if d == 0 else ''}{body}</div>")
    css = CSS + HWN_CSS + FILL_CSS + (ANS_FILL_CSS + ".hq .fig .gr{width:28mm;height:28mm}.hq .p{font-size:10pt;line-height:1.5}.hq{gap:1mm 6mm}" if answer else "")
    return f"<html><head><meta charset=utf-8><style>{css}</style></head><body>{''.join(pages)}</body></html>"


# ------------------------------------------------------------ こたえ（どの形にも使う）
ANS_CSS = """
.al { margin-top: 3mm; }
.al .sec { font-weight: 700; font-size: 11.5pt; margin: 2.5mm 0 1mm; border-left: 3pt solid #111; padding-left: 2mm; }
.al .r { display: grid; grid-template-columns: 7mm minmax(0, 1fr); font-size: 10.5pt; line-height: 1.6; padding: 1mm 0; border-bottom: .5pt solid #ddd; }
.al .r .x { color: #555; }
.al .r b { font-weight: 700; }
.al .two { display: grid; grid-template-columns: 1fr 1fr; column-gap: 8mm; }
"""


def answers(title, secs, per_page):
    """secs：[(見出し, [問題])]。per_page＝1ページに入れる見出しの数"""
    pages = []
    for i in range(0, len(secs), per_page):
        body = ""
        for label, probs in secs[i:i + per_page]:
            rows = "".join(f"<div class=r><span>{CIRC[j]}</span><span>{p['a']}</span></div>" for j, p in enumerate(probs))
            body += f"<div class=sec>{label}</div><div class=two>{rows}</div>"
        n = (len(secs) + per_page - 1) // per_page
        pages.append(f"<div class=page>{head(title, 'こたえ' + (f'（{i // per_page + 1}/{n}）' if n > 1 else ''), name=False)}<div class=al>{body}</div></div>")
    return f"<html><head><meta charset=utf-8><style>{CSS}{ANS_CSS}</style></head><body>{''.join(pages)}</body></html>"


# ------------------------------------------------------------ 宿題（1日1ページ・直接書く）
HWW_CSS = """
.band { display: flex; align-items: center; gap: 4mm; background: #fbefdc; color: #7a4508; border-radius: 2mm;
        padding: 2mm 4mm; font-weight: 700; font-size: 12.5pt; margin-top: 3mm; }
.band .sp { margin-left: auto; white-space: nowrap; font-weight: 400; font-size: 10.5pt; color: #111; }
.band .ck::before { content: ""; display: inline-block; width: 4.5mm; height: 4.5mm; border: .8pt solid #111; margin-right: 1.5mm; vertical-align: -1mm; }
.rule { margin-top: 2.5mm; font-size: 10pt; border: .8pt solid #111; border-radius: 2mm; padding: 1.8mm 4mm; line-height: 1.55; }
.point { font-size: 10.5pt; margin: 2mm 1mm 0; background: #f1f1f1; border-radius: 2mm; padding: 1.8mm 3.5mm; line-height: 1.6; }
.wg { flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 0 8mm; margin-top: 2mm; min-height: 0; }
.wg .w { border-bottom: .6pt solid #ccc; padding: 2.5mm 0 2mm; position: relative; font-size: 11.5pt; line-height: 1.75; overflow: hidden; }
.wg .w .no { font-size: 13pt; margin-right: 1.5mm; }
.wg .w .ab { position: absolute; right: 0; bottom: 2.5mm; font-size: 10.5pt; background: #fff; padding-left: 2mm; }
.wg .w .ab .blank { display: inline-block; width: 30mm; border-bottom: .8pt solid #111; }
.wg .full { grid-column: 1 / -1; }
.gr { display: block; margin-top: 1mm; }
table.tb { border-collapse: collapse; margin-top: 1.5mm; font-size: 11pt; }
table.tb td, table.tb th { border: .8pt solid #111; min-width: 11mm; height: 8mm; text-align: center; padding: 0 1.5mm; }
table.tb th { background: #f1f1f1; font-weight: 400; }
"""


def _ab(p, answer):
    """答えの欄。answer=True なら fa（短い答え）を赤で書きこむ"""
    albl = p.get("albl", "答え")
    if not albl:
        return ""
    if answer and p.get("fa"):
        return f"<div class=ab>{albl} <span class=fill>{p['fa']}</span></div>"
    return f"<div class=ab>{albl} <span class=blank></span></div>"


def _ra(p, answer):
    """こたえの書きこみ（式・解き方）。fa だけで足りるときや、表・図に答えが入るときは noa"""
    if not answer or p.get("noa"):
        return ""
    return f"<div class=ra>{p['a']}</div>"


def hw_writein(title, days, rule, answer=False):
    """days：[(曜日, ポイント, [問題])]。1日1ページ。問題は2列（"full": True なら横いっぱい）。answer=True でこたえ"""
    pages = []
    for k, (youbi, point, probs) in enumerate(days):
        check_all(probs, f"{k + 1}日目")
        rows = sum(1 for p in probs if p.get("full")) + (sum(1 for p in probs if not p.get("full")) + 1) // 2
        cells = ""
        for j, p in enumerate(probs):
            cells += (f"<div class='w{' full' if p.get('full') else ''}'><span class=no>{CIRC[j]}</span>{p['q']}"
                      f"{('<div>' + p['fig'] + '</div>') if p.get('fig') else ''}{_ra(p, answer)}{_ab(p, answer)}</div>")
        hd = ans_head(title, f"{k + 1}日目（{youbi}）") if answer else head(title, f"{k + 1}日目（{youbi}）", date=True)
        pages.append(f"""<div class=page>{hd}
{rule if k == 0 else ''}
<div class=band>{k + 1}日目（{youbi}）<span class=sp><span class=ck>丸つけした</span></span></div>
<div class=point>ポイント：{point}</div>
<div class=wg style="grid-template-rows: repeat({rows}, 1fr)">{cells}</div></div>""")
    css = CSS + HWW_CSS + FILL_CSS + (ANS_FILL_CSS if answer else "")
    return f"<html><head><meta charset=utf-8><style>{css}</style></head><body>{''.join(pages)}</body></html>"


# ------------------------------------------------------------ 授業・自習プリント（4ページ・1ページ左右2列×4問）
WS_CSS = """
.wg { flex: 1; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: repeat(4, 1fr); grid-auto-flow: column;
      gap: 0 6mm; margin-top: 3mm; min-height: 0; }
.wg .w { border-bottom: .6pt solid #ccc; padding: 2.5mm 0 2mm; position: relative; font-size: 11pt; line-height: 1.7; overflow: hidden; }
.wg .w:nth-child(4n) { border-bottom: none; }
.wg .w .no { font-size: 13pt; margin-right: 1.5mm; }
.wg .w .ab { position: absolute; right: 0; bottom: 2.5mm; font-size: 10.5pt; background: #fff; padding-left: 2mm; }
.wg .w .ab .blank { display: inline-block; width: 30mm; border-bottom: .8pt solid #111; }
.wg .w .sc { font-size: 10pt; color: #333; margin-top: 1mm; }
.wg .w .sc .bl { display: inline-block; width: 40mm; border-bottom: .6pt solid #999; }
.gr { display: block; margin-top: 1mm; }
"""


def worksheet(title, secs, ans_title=None):
    """secs：[(その1, 小見出し, ポイント, [問題×8])]。問題 dict は q・a・fa・eq・albl・sc（足場の HTML）・fig・noa。
    もどり値は (問題の HTML, こたえの HTML)。こたえは問題と同じ形に赤で書きこむ（11/6〜）"""
    def build(answer):
        pages = []
        n = 0
        for label, sub, tip, probs in secs:
            assert len(probs) == 8, (label, len(probs))
            check_all(probs, label)
            cells = ""
            for p in probs:
                sc = "" if answer else (('<div class=sc>' + p['sc'] + '</div>') if p.get('sc') else '')
                cells += (f"<div class=w><span class=no>{CIRC[n]}</span>{p['q']}"
                          f"{('<div>' + p['fig'] + '</div>') if p.get('fig') else ''}"
                          f"{sc}{_ra(p, answer)}{_ab(p, answer)}</div>")
                n += 1
            hd = ans_head((ans_title or title) + " " + label, sub) if answer else head(title + " " + label, sub, score=8)
            pages.append(f"<div class=page>{hd}<div class=tip>{tip}</div><div class=wg>{cells}</div></div>")
        css = CSS + WS_CSS + FILL_CSS + (ANS_FILL_CSS if answer else "")
        return f"<html><head><meta charset=utf-8><style>{css}</style></head><body>{''.join(pages)}</body></html>"
    return build(False), build(True)


def answers_numbered(title, secs, per_page):
    pages = []
    for i in range(0, len(secs), per_page):
        body = ""
        for label, probs, start in secs[i:i + per_page]:
            rows = "".join(f"<div class=r><span>{CIRC[start + j]}</span><span>{p['a']}</span></div>" for j, p in enumerate(probs))
            body += f"<div class=sec>{label}</div><div class=two style='grid-auto-flow:column;grid-template-rows:repeat({(len(probs) + 1) // 2},auto)'>{rows}</div>"
        m = (len(secs) + per_page - 1) // per_page
        pages.append(f"<div class=page>{head(title, 'こたえ' + (f'（{i // per_page + 1}/{m}）' if m > 1 else ''), name=False)}<div class=al>{body}</div></div>")
    return f"<html><head><meta charset=utf-8><style>{CSS}{ANS_CSS}</style></head><body>{''.join(pages)}</body></html>"
