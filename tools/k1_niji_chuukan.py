# -*- coding: utf-8 -*-
"""高1 数学Ⅰ 2次関数「2学期中間考査型テスト」 A〜G パターン（A3・2ページ）

各パターンについて、問題 pdf/k1_chuukan_exam_{P}.pdf と、
問題プリントに赤で答え・途中式・グラフを書きこんだこたえ pdf/k1_chuukan_exam_{P}_ans.pdf を
同じレイアウトで出す（11/6 先生の希望「こたえは問題に赤で書きこんだ形」）。
大問1＝答えのみ（解答欄に記入）／大問2〜4＝頂点・軸の表＋グラフに放物線／大問5〜7＝記述欄に途中式。
答えは SymPy で検算。実行： cd tools && python3 k1_niji_chuukan.py
"""
import math, pathlib, sys
import sympy as sp

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from texlib import _dist
KATEX = _dist()
OUT = pathlib.Path(__file__).resolve().parent.parent / "pdf"
x = sp.Symbol('x')
R = sp.Rational

# ---------------- データ（PDF から抽出・全問 SymPy 検算済み） ----------------
PAT = {
 'A': dict(N=3, f=(1,-4,3), fa=(2,-1),
    q13=[(1,-8,3),(4,-8,11),(-1,-8,2),(-2,6,-1)],
    q2=[(3,-3),(-1,1)], q3=[(2,2),(-2,-1)], q4v=(2,1,-3), q4g=(-2,-4,1),
    q5=[(2,1,3),(-1,-2,-1)], q6=(1,-6,5),
    q7=[(1,-4,7,0,3),(-2,8,-3,0,1),(1,2,4,-3,0),(-1,6,-4,1,5)]),
 'B': dict(N=4, f=(1,-6,5), fa=(3,-2),
    q13=[(1,-10,4),(4,16,9),(-1,-6,4),(-2,10,-3)],
    q2=[(2,-3),(-1,3)], q3=[(2,-1),(-3,1)], q4v=(2,-2,-3), q4g=(-1,4,-1),
    q5=[(3,2,1),(-2,-1,4)], q6=(1,6,4),
    q7=[(1,-6,10,0,4),(-2,12,-13,1,2),(1,4,7,-4,-1),(-1,6,-5,1,5)]),
 'C': dict(N=5, f=(1,-8,7), fa=(4,-1),
    q13=[(1,-12,5),(4,-24,11),(-1,10,-3),(-2,-6,5)],
    q2=[(3,-2),(-2,2)], q3=[(3,2),(-2,-2)], q4v=(3,1,-2), q4g=(-2,8,-5),
    q5=[(2,3,2),(-3,-1,2)], q6=(1,-8,12),
    q7=[(1,-2,5,0,3),(-2,4,1,2,3),(1,6,11,-5,-2),(-1,2,3,-1,3)]),
 'D': dict(N=6, f=(1,-4,-5), fa=(3,-2),
    q13=[(1,-14,6),(4,8,7),(-1,8,-1),(-2,14,-5)],
    q2=[(2,-4),(-3,3)], q3=[(2,3),(-3,-1)], q4v=(2,-1,-4), q4g=(-1,-6,-7),
    q5=[(3,-2,1),(-2,1,5)], q6=(1,4,-1),
    q7=[(1,-4,6,0,3),(-2,-4,1,-3,-2),(1,-6,11,1,2),(-1,-2,2,-3,1)]),
 'E': dict(N=2, f=(1,2,-8), fa=(2,-3),
    q13=[(1,4,-6),(4,-16,9),(-1,-4,7),(-2,2,-5)],
    q2=[(1,-3),(-2,-1)], q3=[(2,1),(-2,2)], q4v=(2,2,-3), q4g=(-2,-8,-5),
    q5=[(2,-3,2),(-3,2,4)], q6=(1,-2,-5),
    q7=[(1,-6,7,1,4),(-1,2,2,2,4),(2,8,5,-1,1),(-1,-4,-1,-4,0)]),
 'F': dict(N=7, f=(1,-2,-3), fa=(4,-2),
    q13=[(1,8,3),(4,-8,1),(-1,6,2),(-2,-10,-7)],
    q2=[(3,-1),(-1,2)], q3=[(2,-2),(-3,1)], q4v=(2,3,-1), q4g=(-1,2,2),
    q5=[(2,1,3),(-2,-2,1)], q6=(1,2,-2),
    q7=[(1,-8,13,2,5),(-2,8,-3,3,4),(1,2,4,1,3),(-1,4,-2,0,4)]),
 'G': dict(N=3, f=(1,4,3), fa=(2,-4),
    q13=[(1,-2,-7),(4,24,31),(-1,-8,1),(-2,6,-5)],
    q2=[(2,-4),(-3,2)], q3=[(3,-1),(-2,2)], q4v=(3,2,-2), q4g=(-2,4,1),
    q5=[(3,1,2),(-2,3,5)], q6=(1,-4,1),
    q7=[(1,-4,1,0,3),(-2,12,-15,4,5),(1,4,6,-1,2),(-1,-6,-6,-5,-1)]),
}

# ---------------- 式の整形 ----------------
def ntex(v):
    v = R(v)
    if v.denominator == 1:
        return str(v.numerator)
    s = "-" if v < 0 else ""
    return f"{s}\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"

def mono(a):
    return "x^2" if a == 1 else ("-x^2" if a == -1 else f"{a}x^2")

def lin(b):
    if b == 0: return ""
    s = "+" if b > 0 else "-"; ab = abs(b)
    return f"{s}{'x' if ab==1 else str(ab)+'x'}"

def con(c):
    return "" if c == 0 else f"{'+' if c>0 else '-'}{abs(c)}"

def gen(a, b, c):
    return mono(a) + lin(b) + con(c)

def fact(a, p):            # a(x-p)^2
    pre = "" if a == 1 else ("-" if a == -1 else str(a))
    if p == 0: return f"{pre}x^2"
    sg = "-" if p > 0 else "+"
    return f"{pre}(x{sg}{abs(p)})^2"

def vform(a, p, q):        # a(x-p)^2 (+q)
    return fact(a, p) + con(q)

def basic_tex(a, p, q):    # 平方完成の結果（p,q は分数可）
    pre = "" if a == 1 else ("-" if a == -1 else str(a))
    if p == 0:
        body = f"{pre}x^2"
    else:
        sg = "-" if p > 0 else "+"
        body = f"{pre}(x{sg}{ntex(abs(p))})^2"
    if q != 0:
        body += ("+" if q > 0 else "-") + ntex(abs(q))
    return body

def vertex(a, b, c):
    p = R(-b, 2 * a); q = sp.nsimplify(c - R(b * b, 4 * a))
    return a, p, q

def coord(p, q):
    return f"({ntex(p)},\\,{ntex(q)})"

def M(s):
    return f"${s}$"

def A(s):                  # 赤の答え（下線つき）
    return f'<span class="ans">{s}</span>'

def W(s):                  # 赤の途中式
    return f'<div class="work">{s}</div>'

# ---------------- 検算 ----------------
def solve_dom(a, b, c, lo, hi):
    e = a * x**2 + b * x + c
    _, p, q = vertex(a, b, c)
    f = lambda t: int(e.subs(x, t))
    cs = [lo, hi] + ([p] if lo <= p <= hi else [])
    vals = {t: f(t) for t in cs}
    mx = max(vals.values()); mn = min(vals.values())
    amx = sorted(t for t, v in vals.items() if v == mx)
    amn = sorted(t for t, v in vals.items() if v == mn)
    inside = (lo <= p <= hi)
    return dict(p=p, q=q, lo=lo, hi=hi, flo=f(lo), fhi=f(hi),
                mx=mx, mn=mn, amx=amx, amn=amn, inside=inside, a=a)

def verify():
    for P, d in PAT.items():
        for (a, b, c) in d['q13']:
            aa, p, q = vertex(a, b, c)
            assert sp.expand(a*(x-p)**2 + q - (a*x**2+b*x+c)) == 0, (P, a, b, c)
        for (a, b, c, lo, hi) in d['q7']:
            s = solve_dom(a, b, c, lo, hi)
            assert sp.expand(a*(x-s['p'])**2 + s['q'] - (a*x**2+b*x+c)) == 0
    print("検算 OK（全7パターン）")

# ---------------- グラフ（軸のみ・方眼/目盛りなし。答えは放物線を赤で） ----------------
def win(a, p, q):
    p = int(p); q = int(q)
    xmin = min(0, p - 3); xmax = max(0, p + 3)
    if a > 0:
        ymin = math.floor((q - 2) / 2) * 2; ymax = ymin + 12
    else:
        ymax = math.ceil((q + 2) / 2) * 2; ymin = ymax - 12
    return xmin, xmax, ymin, ymax

def graph(a, b, c, p, q, draw):
    xmin, xmax, ymin, ymax = win(a, p, q)
    u, pad = 12, 11
    Wd = (xmax - xmin) * u + 2 * pad
    Ht = (ymax - ymin) * u + 2 * pad
    ox = pad + (0 - xmin) * u
    oy = pad + (ymax - 0) * u
    SX = lambda v: pad + (v - xmin) * u
    SY = lambda v: pad + (ymax - v) * u
    e = []
    e.append(f'<line x1="{pad-3}" y1="{oy:.1f}" x2="{Wd-pad+7}" y2="{oy:.1f}" stroke="#2b2b2b" stroke-width="1.2"/>')
    e.append(f'<line x1="{ox:.1f}" y1="{Ht-pad+3}" x2="{ox:.1f}" y2="{pad-7}" stroke="#2b2b2b" stroke-width="1.2"/>')
    e.append(f'<path d="M{Wd-pad+7:.1f},{oy:.1f} l-6,-3.2 l0,6.4 z" fill="#2b2b2b"/>')
    e.append(f'<path d="M{ox:.1f},{pad-7:.1f} l-3.2,6 l6.4,0 z" fill="#2b2b2b"/>')
    e.append(f'<text x="{ox-9:.1f}" y="{oy+11:.1f}" font-size="9" fill="#2b2b2b">O</text>')
    e.append(f'<text x="{Wd-pad+3:.1f}" y="{oy+12:.1f}" class="ax">x</text>')
    e.append(f'<text x="{ox+4:.1f}" y="{pad+1:.1f}" class="ax">y</text>')
    if draw:
        pts = []
        t = xmin
        while t <= xmax + 1e-9:
            yv = a * t * t + b * t + c
            if ymin - 0.4 <= yv <= ymax + 0.4:
                pts.append(f"{SX(t):.1f},{SY(yv):.1f}")
            t += 0.1
        if pts:
            e.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#c00" stroke-width="1.8"/>')
        if ymin <= q <= ymax and xmin <= p <= xmax:
            e.append(f'<circle cx="{SX(p):.1f}" cy="{SY(q):.1f}" r="2.4" fill="#c00"/>')
    return (f'<svg class="grf" viewBox="0 0 {Wd:.0f} {Ht:.0f}" width="{Wd:.0f}" '
            f'height="{Ht:.0f}" xmlns="http://www.w3.org/2000/svg">' + "".join(e) + "</svg>")

def vtable(p=None, q=None, draw=False):
    v = A(M(coord(p, q))) if draw else ""
    ax = A(M(f"x={ntex(p)}")) if draw else ""
    return (f'<table class="vt"><tr><td class="lbl">頂点</td><td class="ec">{v}</td></tr>'
            f'<tr><td class="lbl">軸</td><td class="ec">{ax}</td></tr></table>')

# ---------------- ヘッダ・部品 ----------------
def exhead(P, no):
    return ('<div class="exhead"><span class="t">２学期中間考査　数学【探究標準コース】　前段'
            f'〔{P}〕</span><span class="no">No.{no}</span>'
            '<span class="name">（<span class="u"></span>）組（<span class="u"></span>）番　名前'
            '（<span class="nm"></span>）<span class="pt">点</span></span></div>')

def qh(num, title, pts):
    p = f'<span class="pts">{pts}</span>' if pts else ""
    return f'<div class="qh"><span class="bx">{num}</span><span class="ti">{title}</span>{p}</div>'

INSTR = ('「答えのみ」以外の問題は必ず途中式を書くこと。答案は必ず枠内に記入せよ。'
         '計算スペースが足りない場合は、答案用紙の裏面を使用しても良い。'
         'ただし、裏面および枠外は採点対象としないので注意すること。')

# ---------------- 大問1 ----------------
def q1_block(d, ans):
    N = d['N']; fa = d['f']; (x1, x2) = d['fa']
    lst = ('<div class="qlist">'
           f'<div class="li">(1) 横が縦より \\({N}\\,\\mathrm{{cm}}\\) 長い長方形について，縦の長さを '
           '\\(x\\,\\mathrm{cm}\\)，面積を \\(y\\,\\mathrm{cm^2}\\) とするとき</div>'
           '<div class="li sm">① \\(x\\) と \\(y\\) の関係式を求めよ。　　② \\(x\\) の定義域を求めよ。</div>'
           f'<div class="li">(2) 2次関数 \\(f(x)={gen(*fa)}\\) において，次の値を求めよ。</div>'
           f'<div class="li sm">① \\(f({x1})\\)　　② \\(f({x2})\\)　　③ \\(f(a+1)\\)</div>'
           '<div class="li">(3) 次の2次式を平方完成せよ。</div>'
           f'<div class="li sm">① \\({gen(*d["q13"][0])}\\)　　② \\({gen(*d["q13"][1])}\\)</div>'
           f'<div class="li sm">③ \\({gen(*d["q13"][2])}\\)　　④ \\({gen(*d["q13"][3])}\\)</div>'
           '</div>')
    # 答え
    a_, b_, c_ = fa
    f1 = sp.expand(a_*x1**2 + b_*x1 + c_); f2 = sp.expand(a_*x2**2 + b_*x2 + c_)
    fa1 = sp.expand(a_*(sp.Symbol('a')+1)**2 + b_*(sp.Symbol('a')+1) + c_)
    def cell(s): return A(M(s)) if ans else ""
    bf = [basic_tex(*vertex(*t)) for t in d['q13']]
    tbl = ('<table class="ans1">'
           f'<tr><td class="k">(1)</td><td class="n">①</td><td class="v">{cell("y="+gen(1,N,0))}</td>'
           f'<td class="n">②</td><td class="v">{cell("x>0")}</td></tr>'
           f'<tr><td class="k">(2)</td><td class="n">①</td><td class="v">{cell("f("+str(x1)+")="+sp.latex(f1))}</td>'
           f'<td class="n">②</td><td class="v">{cell("f("+str(x2)+")="+sp.latex(f2))}</td></tr>'
           f'<tr><td class="k"></td><td class="n">③</td><td class="v" colspan="3">{cell("f(a+1)="+sp.latex(fa1))}</td></tr>'
           f'<tr><td class="k" rowspan="4">(3)</td><td class="n">①</td><td class="v" colspan="3">{cell(bf[0])}</td></tr>'
           f'<tr><td class="n">②</td><td class="v" colspan="3">{cell(bf[1])}</td></tr>'
           f'<tr><td class="n">③</td><td class="v" colspan="3">{cell(bf[2])}</td></tr>'
           f'<tr><td class="n">④</td><td class="v" colspan="3">{cell(bf[3])}</td></tr>'
           '</table>')
    return qh('1', '次の各問いに答え、解答欄に答えのみ記入せよ。', '知・技 各3点×9問＝27点') + lst, tbl

# ---------------- 大問2・3・4 ----------------
def q234(d, ans):
    def pair(title, items):
        h = qh(items[0], title, '知・技 各6点')
        rows = ""
        for (lb, disp, a, b, c) in items[1]:
            aa, p, q = vertex(a, b, c)
            rows += (f'<div class="sub"><span class="lb">{lb}</span>\\({disp}\\)</div>'
                     f'<div class="tg">{vtable(p, q, ans)}{graph(a, b, c, p, q, ans)}</div>')
        return h + rows
    # 大問2： y=ax^2+c
    a1, c1 = d['q2'][0]; a2, c2 = d['q2'][1]
    q2 = pair('次の2次関数の頂点と軸を求め、グラフをかけ。',
              ('2', [('(1)', gen(a1, 0, c1), a1, 0, c1), ('(2)', gen(a2, 0, c2), a2, 0, c2)]))
    # 大問3： y=a(x-p)^2
    a1, p1 = d['q3'][0]; a2, p2 = d['q3'][1]
    q3 = pair('次の2次関数の頂点と軸を求め、グラフをかけ。',
              ('3', [('(1)', fact(a1, p1), a1, -2*a1*p1, a1*p1*p1),
                     ('(2)', fact(a2, p2), a2, -2*a2*p2, a2*p2*p2)]))
    # 大問4： (1) 頂点形  (2) 一般形
    av, pv, qv = d['q4v']; ag, bg, cg = d['q4g']
    q4 = pair('次の2次関数の頂点と軸を求め、グラフをかけ。',
              ('4', [('(1)', vform(av, pv, qv), av, -2*av*pv, av*pv*pv+qv),
                     ('(2)', gen(ag, bg, cg), ag, bg, cg)]))
    return q2 + q3 + q4

# ---------------- 大問5・6・7 の記述解答 ----------------
def sol5(a, p, q):
    conv = "下に凸" if a > 0 else "上に凸"
    if a > 0:
        return [M(f"軸\\ x={p}，{conv}"), M(f"x={p}\\ で最小値\\ {q}"), "最大値はない"]
    return [M(f"軸\\ x={p}，{conv}"), M(f"x={p}\\ で最大値\\ {q}"), "最小値はない"]

def sol6(a, b, c):
    aa, p, q = vertex(a, b, c)
    return [M(f"y={gen(a,b,c)}={basic_tex(a,p,q)}"),
            M(f"x={p}\\ で最小値\\ {q}"), "最大値はない"]

def sol7(a, b, c, lo, hi):
    s = solve_dom(a, b, c, lo, hi)
    p, q = s['p'], s['q']
    conv = "下に凸" if a > 0 else "上に凸"
    pos = "定義域内" if s['inside'] else ("定義域の左外" if p < lo else "定義域の右外")
    lines = [M(f"y={gen(a,b,c)}={basic_tex(a,p,q)}"),
             M(f"軸\\ x={p}（{pos}），{conv}")]
    endp = f"f({lo})={s['flo']},\\ f({hi})={s['fhi']}"
    if s['inside']:
        endp += f"，\\ f({p})={q}"
    lines.append(M(endp))
    amx = ",\\ ".join(f"x={t}" for t in s['amx'])
    amn = ",\\ ".join(f"x={t}" for t in s['amn'])
    lines.append(M(f"最大値\\ {s['mx']}\\ ({amx})"))
    lines.append(M(f"最小値\\ {s['mn']}\\ ({amn})"))
    return lines

def box(lb, disp, sol, ans, mh):
    lab = f'<span class="lb">{lb}</span>' if lb else ""
    body = "".join(f'<div class="wl">{t}</div>' for t in sol) if ans else ""
    return (f'<div class="bx" style="min-height:{mh}"><div class="fx">{lab}\\({disp}\\)</div>'
            f'<div class="sol">{body}</div></div>')

def page2_cols(d, ans):
    av1, pv1, qv1 = d['q5'][0]; av2, pv2, qv2 = d['q5'][1]
    q5 = (qh('5', '次の2次関数に最大値，最小値があれば，それを求めよ。', '思・判・表 各4点')
          + box('(1)', vform(av1, pv1, qv1), sol5(av1, pv1, qv1), ans, "58mm")
          + box('(2)', vform(av2, pv2, qv2), sol5(av2, pv2, qv2), ans, "58mm"))
    q6 = (qh('6', '次の2次関数に最大値，最小値があれば，それを求めよ。', '思・判・表 4点')
          + box('', gen(*d['q6']), sol6(*d['q6']), ans, "74mm"))
    g7 = d['q7']
    def q7disp(t):
        a, b, c, lo, hi = t
        return f"y={gen(a,b,c)}\\quad({lo}\\le x\\le {hi})"
    q7a = (qh('7', '次の関数の最大値，最小値を求めよ。', '思・判・表 各6点')
           + box('(1)', q7disp(g7[0]), sol7(*g7[0]), ans, "118mm"))
    left = f'<div class="col">{q5}{q6}{q7a}</div>'
    q7b = (box('(2)', q7disp(g7[1]), sol7(*g7[1]), ans, "120mm")
           + box('(3)', q7disp(g7[2]), sol7(*g7[2]), ans, "120mm")
           + box('(4)', q7disp(g7[3]), sol7(*g7[3]), ans, "120mm"))
    right = f'<div class="col">{q7b}</div>'
    return left + right

# ---------------- ページ ----------------
def build(P, ans):
    d = PAT[P]
    q1top, q1tbl = q1_block(d, ans)
    page1 = ('<section class="sheet">' + exhead(P, 1)
             + f'<div class="instr">{INSTR}</div><div class="cols">'
             + f'<div class="col">{q1top}<div class="sp"></div>{q1tbl}</div>'
             + f'<div class="col">{q234(d, ans)}</div></div>'
             + f'<div class="foot">２学期中間考査 数学【探究標準コース】 前段〔{P}〕 No.1</div></section>')
    page2 = ('<section class="sheet">' + exhead(P, 2)
             + f'<div class="cols">{page2_cols(d, ans)}</div>'
             + f'<div class="foot">２学期中間考査 数学【探究標準コース】 前段〔{P}〕 No.2</div></section>')
    return page1 + page2

CSS = """
@page { size: A3 portrait; margin: 9mm 9mm 8mm; }
*{box-sizing:border-box;} html,body{margin:0;padding:0;}
body{font-family:"Noto Sans CJK JP",sans-serif;color:#1a1a1a;font-size:10pt;}
.sheet{page-break-after:always;}
.sheet:last-child{page-break-after:auto;}
.exhead{display:flex;align-items:flex-end;border-bottom:2px solid #000;padding-bottom:3px;margin-bottom:5px;}
.exhead .t{font-size:11pt;font-weight:700;white-space:nowrap;}
.exhead .no{font-size:11pt;font-weight:700;margin:0 10px;}
.exhead .name{flex:1;display:flex;align-items:flex-end;justify-content:flex-end;gap:4px;font-size:10.5pt;}
.exhead .u{display:inline-block;border-bottom:1px solid #666;min-width:34px;}
.exhead .nm{display:inline-block;border-bottom:1px solid #666;min-width:120px;}
.exhead .pt{border:1px solid #000;padding:2px 6px;margin-left:10px;font-size:9pt;}
.instr{border:1px solid #000;padding:5px 8px;font-size:8.6pt;line-height:1.5;margin-bottom:7px;}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:7mm;min-height:372mm;}
.col{display:flex;flex-direction:column;min-height:0;}
.sp{flex:1 1 auto;}
.qh{display:flex;align-items:baseline;gap:6px;margin:5px 0 4px;}
.qh .bx{border:1.4px solid #000;font-weight:700;font-size:10.5pt;padding:0 5px;line-height:1.35;}
.qh .ti{font-size:10pt;font-weight:600;}
.qh .pts{margin-left:auto;font-size:8.2pt;color:#333;white-space:nowrap;border:0.8px solid #999;padding:0 4px;border-radius:2px;}
.qlist{font-size:10pt;line-height:1.9;}
.qlist .li{margin:2px 0;}
.qlist .sm{margin-left:1.4em;}
.sub{font-size:10pt;margin:4px 0 2px;}
.sub .lb{font-weight:600;margin-right:6px;}
.tg{display:flex;align-items:center;gap:10px;margin:1px 0 4px;}
table.vt{border-collapse:collapse;}
table.vt td{border:1px solid #000;height:26px;}
table.vt td.lbl{width:44px;text-align:center;font-size:9.5pt;background:#f4f6f9;}
table.vt td.ec{width:118px;padding:0 4px;}
svg.grf{display:block;}
.ax{font-style:italic;font-family:"KaTeX_Math",serif;font-size:12px;fill:#2b2b2b;}
table.ans1{border-collapse:collapse;width:100%;margin-top:6px;}
table.ans1 td{border:1px solid #000;padding:3px 4px;font-size:9.5pt;}
table.ans1 td.k{width:24px;text-align:center;background:#f4f6f9;}
table.ans1 td.n{width:20px;text-align:center;color:#333;}
table.ans1 td.v{height:30px;}
.bx{border:1px solid #000;padding:6px 8px;}
.bx .fx{font-size:10.5pt;margin-bottom:3px;}
.bx .lb{font-weight:600;margin-right:6px;}
.sol{color:#c00;}
.sol .wl{font-size:9.3pt;line-height:1.8;}
.sol .katex{color:#c00;}
.ans{color:#c00;font-weight:700;}
.ans .katex{color:#c00;}
.foot{margin-top:6px;font-size:8pt;color:#8a97a4;text-align:right;}
"""

HTML = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
        f'<link rel="stylesheet" href="file://{KATEX}/katex.min.css">'
        f'<script src="file://{KATEX}/katex.min.js"></script>'
        f'<script src="file://{KATEX}/contrib/auto-render.min.js"></script>'
        f'<style>{CSS}</style></head><body>__BODY__'
        '<script>renderMathInElement(document.body,{delimiters:[{left:"$",right:"$",display:false},'
        '{left:"\\\\(",right:"\\\\)",display:false}],'
        'throwOnError:true});document.body.setAttribute("data-done","1");</script></body></html>')

def main():
    verify()
    OUT.mkdir(exist_ok=True)
    from playwright.sync_api import sync_playwright
    jobs = []
    for P in "ABCDEFG":
        jobs.append((build(P, False), f"k1_chuukan_exam_{P}.pdf"))
        jobs.append((build(P, True), f"k1_chuukan_exam_{P}_ans.pdf"))
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for body, name in jobs:
            hp = pathlib.Path(f"/tmp/{name}.html")
            hp.write_text(HTML.replace("__BODY__", body), encoding="utf-8")
            pg = br.new_page()
            pg.goto(f"file://{hp.resolve()}")
            pg.wait_for_selector("body[data-done]")
            pg.evaluate("document.fonts.ready")
            bad = pg.evaluate("""() => {const r=[];document.querySelectorAll('.sheet').forEach((s,i)=>{
              if(s.scrollHeight>s.clientHeight+2) r.push('p'+(i+1));});return r;}""")
            pg.pdf(path=str(OUT / name), format="A3", print_background=True, prefer_css_page_size=True)
            pg.close()
            print("書き出し:", name, ("!! はみ出し "+str(bad)) if bad else "")
        br.close()

if __name__ == "__main__":
    main()
