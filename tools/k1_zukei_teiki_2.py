"""高1 数学A 図形の性質 定期考査対策 第2回（第1回 k1_zukei_teiki_1.py の別パターン・同じ並び）。
A3 横・3列・2ページ。問題 pdf/k1_zukei_teiki_2.pdf と、赤で答え・途中式を書きこんだ pdf/k1_zukei_teiki_2_ans.pdf。
  cd tools && python3 k1_zukei_teiki_2.py
図の部品・紙面のしくみは k1_zukei_teiki_1.py（Z）を使う。答えは図の座標で確かめる。
"""
import math
from pathlib import Path
from playwright.sync_api import sync_playwright
import k1_zukei_teiki_1 as Z
from k1_zukei_teiki_1 import P, add, mul, lerp, dist, unit, sub, angle_at, tri_sides, tri_angles, circumcenter, incenter, Fig, ok

NAME = "k1_zukei_teiki_2"
Z.TITLE = "数学A 図形の性質　定期考査対策 第2回"

def q1():
    figs, sols = [], []
    # (1) AP=12, PB=x(=9), AQ=8, QC=6
    A, B, C = P(1.7, 3.9), P(0, 0), P(4.4, 0); t = 12/21
    Pp, Q = lerp(A, B, t), lerp(A, C, t)
    ok("1(1)", dist(A, Pp)/dist(Pp, B), 12/9); ok("1(1)b", dist(A, Q)/dist(Q, C), 8/6)
    f = Fig(36); f.poly(A, B, C); f.seg(Pp, Q); f.par(Pp, Q); f.par(B, C)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.6)); f.name(C, "C", (1, -.6)); f.name(Pp, "P", (-1, .3)); f.name(Q, "Q", (1, .3))
    f.arc(A, Pp, "12", 1, .25); f.arc(Pp, B, "x", 1, .22); f.arc(Q, A, "8", 1, .25); f.arc(C, Q, "6", 1, .22)
    figs.append(f.svg())
    sols.append([r"$\mathrm{AP}:\mathrm{PB}=\mathrm{AQ}:\mathrm{QC}$", r"$12:x=8:6$", r"$8x=72$", r"$x=\boldsymbol{9}$"])
    # (2) AQ=4, QC=8, BC=18, PQ=x(=6)
    A, B, C = P(2.4, 4.6), P(0, 0), P(3.4, 0); t = 1/3
    Pp, Q = lerp(A, B, t), lerp(A, C, t)
    ok("1(2)", dist(Pp, Q)/dist(B, C)*18, 6)
    f = Fig(36); f.poly(A, B, C); f.seg(Pp, Q); f.par(Pp, Q); f.par(B, C)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.6)); f.name(C, "C", (1, -.6)); f.name(Pp, "P", (-1, .2)); f.name(Q, "Q", (1, .2))
    f.arc(A, Q, "4", -1, .22); f.arc(Q, C, "8", -1, .22); f.arc(C, B, "18", -1, .3); f.lab(Pp, Q, "x", -1, .3)
    figs.append(f.svg())
    sols.append([r"$\mathrm{AQ}:\mathrm{AC}=\mathrm{PQ}:\mathrm{BC}$", r"$4:12=x:18$", r"$12x=72$", r"$x=\boldsymbol{6}$"])
    # (3) 交わる形：AQ=4, AC=6, BC=9, QP=x(=6)
    A = P(0, 0); B, C = P(-1.9, -1.2), P(1.9, -1.2); Q, Pp = mul(C, -2/3), mul(B, -2/3)
    ok("1(3)", dist(Q, Pp)/dist(B, C)*9, 6)
    f = Fig(36); f.seg(Q, C); f.seg(Pp, B); f.seg(Q, Pp); f.seg(B, C); f.par(Q, Pp, .25); f.par(B, C, .3)
    f.name(A, "A", (1, 0)); f.name(B, "B", (-1, -.4)); f.name(C, "C", (1, -.4)); f.name(Q, "Q", (-1, .3)); f.name(Pp, "P", (1, .3))
    f.arc(Q, A, "4", -1, .22); f.arc(A, C, "6", 1, .22); f.arc(C, B, "9", 1, .3); f.arc(Pp, Q, "x", -1, .3)
    figs.append(f.svg())
    sols.append([r"$\mathrm{AQ}:\mathrm{AC}=\mathrm{QP}:\mathrm{CB}$", r"$4:6=x:9$", r"$6x=36$", r"$x=\boldsymbol{6}$"])
    return figs, sols

def numberline(ans):
    """A を 0、B を 4 目もり。−6〜9。P=3, Q=6, R=−4。"""
    s = 24; x0 = -6; x1 = 9; W = (x1-x0)*s + 40; y = 30
    X = lambda v: 20 + (v-x0)*s
    el = [f'<line x1="{X(x0)-8}" y1="{y}" x2="{X(x1)+8}" y2="{y}" stroke="#000" stroke-width="1.5"/>']
    for v in range(x0, x1+1):
        el.append(f'<line x1="{X(v)}" y1="{y-6}" x2="{X(v)}" y2="{y+6}" stroke="#000" stroke-width="1.2"/>')
    for v, n in ((0, "A"), (4, "B")):
        el.append(f'<text x="{X(v)}" y="{y+24}" font-size="15" text-anchor="middle" font-family="KaTeX_Main, serif">{n}</text>')
    if ans:
        for v, n in ((3, "P"), (6, "Q"), (-4, "R")):
            el.append(f'<circle cx="{X(v)}" cy="{y}" r="4" fill="#d40000"/><text x="{X(v)}" y="{y-12}" font-size="15" text-anchor="middle" fill="#d40000" font-family="KaTeX_Main, serif">{n}</text>')
    return f'<svg viewBox="0 0 {W} 60" style="width:100%;height:auto" xmlns="http://www.w3.org/2000/svg">' + "".join(el) + '</svg>'

def q3():
    A, B, C = tri_sides(10, 9, 6); D = P(4, 0)          # BC=10, CA=9, AB=6
    ok("3", angle_at(A, B, D), angle_at(A, D, C))
    f = Fig(19); f.poly(A, B, C); f.seg(A, D); f.bis_dots(A, B, D, C, .6)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.name(D, "D", (0, -1))
    f.arc(B, A, "6", -1, .3); f.arc(A, C, "9", -1, .3); f.arc(C, B, "10", -1, .62); f.arc(B, D, "x", 1, .2)
    return f.svg(), [r"$\mathrm{BD}:\mathrm{DC}=\mathrm{AB}:\mathrm{AC}=6:9=2:3$", r"$x=10\times\dfrac{2}{5}=\boldsymbol{4}$"]

def q4():
    figs, sols = [], []
    # (1) AB=12, AC=9, BC=7, BD=x(=4), DC=3
    A, B, C = tri_sides(7, 9, 12); D = P(4, 0)
    ok("4(1)", angle_at(A, B, D), angle_at(A, D, C))
    f = Fig(16); f.poly(A, B, C); f.seg(A, D); f.bis_dots(A, B, D, C, .6)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.name(D, "D", (0, -1))
    f.arc(B, A, "12", -1, .3); f.arc(A, C, "9", -1, .3); f.arc(D, B, "x", -1, .3); f.arc(C, D, "3", -1, .3)
    figs.append(f.svg())
    sols.append([r"$\mathrm{BD}:\mathrm{DC}=\mathrm{AB}:\mathrm{AC}$", r"$x:3=12:9$", r"$9x=36$", r"$x=\boldsymbol{4}$"])
    # (2) ∠B の二等分線、AB=14, BC=7, AC=12, AD=x(=8)
    A, B, C = tri_sides(7, 12, 14); D = lerp(A, C, 8/12)
    ok("4(2)", angle_at(B, A, D), angle_at(B, D, C))
    f = Fig(11); f.poly(A, B, C); f.seg(B, D); f.bis_dots(B, A, D, C, .6)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.name(D, "D", (1, .4))
    f.arc(B, A, "14", -1, .3); f.arc(A, C, "12", -1, .62); f.arc(C, B, "7", -1, .3); f.arc(A, D, "x", 1, .2)
    figs.append(f.svg())
    sols.append([r"$\mathrm{AD}:\mathrm{DC}=\mathrm{BA}:\mathrm{BC}$", r"$=14:7=2:1$", r"$x=12\times\dfrac{2}{3}=\boldsymbol{8}$"])
    # (3) ∠C の二等分線、AB=10, AC=6, BC=9, BD=x(=6)
    A, B, C = tri_sides(9, 6, 10); D = lerp(B, A, 6/10)
    ok("4(3)", angle_at(C, B, D), angle_at(C, D, A))
    f = Fig(15); f.poly(A, B, C); f.seg(C, D); f.bis_dots(C, A, D, B, .6)
    f.name(A, "A", (.3, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.name(D, "D", (-.6, 1))
    f.arc(B, A, "10", -1, .62); f.arc(A, C, "6", -1, .3); f.arc(C, B, "9", -1, .3); f.arc(B, D, "x", 1, .2)
    figs.append(f.svg())
    sols.append([r"$\mathrm{BD}:\mathrm{DA}=\mathrm{CB}:\mathrm{CA}$", r"$=9:6=3:2$", r"$x=10\times\dfrac{3}{5}=\boldsymbol{6}$"])
    return figs, sols

def q5():
    figs, sols = [], []
    # (1) AB=9, AC=6, BC=5, CD=x(=10)
    A, B, C = tri_sides(5, 6, 9); D = P(15, 0); E = add(A, mul(unit(sub(A, B)), 3.5))
    ok("5(1)", angle_at(A, E, D), angle_at(A, D, C))
    f = Fig(11.5); f.poly(A, B, C); f.seg(C, D); f.seg(A, D); f.seg(A, E, 1.2); f.bis_dots(A, E, D, C, .6)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (0, -1)); f.name(D, "D", (1, -.5))
    f.arc(B, A, "9", -1, .3); c0 = f.ctr; f.ctr = None; f.lab(A, C, "6", 1, .3); f.ctr = c0
    f.arc(C, B, "5", -1, .3); f.arc(D, C, "x", -1, .3)
    figs.append(f.svg())
    sols.append([r"$\mathrm{BD}:\mathrm{DC}=\mathrm{AB}:\mathrm{AC}=3:2$", r"$(5+x):x=3:2$", r"$3x=2(5+x)$", r"$x=\boldsymbol{10}$"])
    # (2) AB=5, AC=7, BC=6, DB=x(=15)
    A, B, C = tri_sides(6, 7, 5); D = P(-15, 0); E = add(A, mul(unit(sub(A, C)), 3))
    ok("5(2)", angle_at(A, E, D), angle_at(A, D, B))
    f = Fig(8); f.poly(A, B, C); f.seg(D, B); f.seg(A, D); f.seg(A, E, 1.2); f.bis_dots(A, E, D, B, .6)
    f.name(A, "A", (0, 1)); f.name(B, "B", (0, -1)); f.name(C, "C", (1, -.5)); f.name(D, "D", (-1, -.5))
    c0 = f.ctr; f.ctr = None; f.lab(A, B, "5", 1, .3); f.ctr = c0
    f.arc(A, C, "7", -1, .3); f.arc(C, B, "6", -1, .3); f.arc(B, D, "x", -1, .3)
    figs.append(f.svg())
    sols.append([r"$\mathrm{DC}:\mathrm{DB}=\mathrm{AC}:\mathrm{AB}=7:5$", r"$(x+6):x=7:5$", r"$7x=5(x+6)$", r"$2x=30$　$x=\boldsymbol{15}$"])
    return figs, sols

def q6():
    figs, sols = [], []
    # (1) ∠OBC=20°, ∠OCA=35°, x=∠OAB(=35°)
    A, B, C = tri_angles(70, 55); O = circumcenter(A, B, C)
    ok("6(1)a", angle_at(B, O, C), 20); ok("6(1)b", angle_at(C, O, A), 35); ok("6(1)x", angle_at(A, B, O), 35)
    f = Fig(150); f.poly(A, B, C); f.seg(O, A, 1.2); f.seg(O, B, 1.2); f.seg(O, C, 1.2); f.dot(O, r=2)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.text(add(O, (0, -16/f.s)), "O", 14)
    f.angmark(B, O, C, "20°"); f.angmark(C, O, A, "35°"); f.angmark(A, B, O, "x")
    figs.append(f.svg())
    sols.append([r"$\mathrm{OA}=\mathrm{OB}=\mathrm{OC}$ より", r"$\angle\mathrm{OBA}=x,\ \angle\mathrm{OCB}=20^\circ$", r"$\angle\mathrm{OAC}=35^\circ$", r"$2(x+20^\circ+35^\circ)=180^\circ$", r"$x=\boldsymbol{35^\circ}$"])
    # (2) ∠A=90°, O は BC の中点, ∠ACB=28°, x=∠OAB(=62°)
    A, B, C = tri_angles(90, 62); O = circumcenter(A, B, C)
    ok("6(2)O", O[1], 0); ok("6(2)x", angle_at(A, B, O), 62)
    f = Fig(150); f.poly(A, B, C); f.seg(A, O, 1.2); f.dot(O, r=2)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.name(O, "O", (0, -1))
    f.angmark(C, A, B, "28°"); f.angmark(A, B, O, "x")
    figs.append(f.svg())
    sols.append([r"O は斜辺 BC の中点で", r"$\mathrm{OA}=\mathrm{OC}$ より $\angle\mathrm{OAC}=28^\circ$", r"$\angle\mathrm{BAC}=90^\circ$ だから", r"$x=90^\circ-28^\circ=\boldsymbol{62^\circ}$"])
    # (3) O が外側。∠OBC=10°, ∠ACB=30°, x=∠ABC(=50°)
    A, B, C = tri_angles(100, 50); O = circumcenter(A, B, C)
    ok("6(3)below", O[1] < 0, True); ok("6(3)a", angle_at(B, O, C), 10); ok("6(3)x", angle_at(B, A, C), 50)
    f = Fig(150); f.poly(A, B, C); f.seg(O, B, 1.2); f.seg(O, C, 1.2); f.dot(O, r=2)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, .2)); f.name(C, "C", (1, .2)); f.name(O, "O", (0, -1))
    f.angmark(B, C, A, "x"); f.angmark(B, O, C, r=1.3); m_ = math.radians(-5.0); f.seg(add(B, (54*math.cos(m_)/f.s, 54*math.sin(m_)/f.s)), add(B, (42/f.s, -22/f.s)), .8); f.text(add(B, (34/f.s, -33/f.s)), "10°", 13); f.angmark(C, B, A, "30°")
    figs.append(f.svg())
    sols.append([r"$\angle\mathrm{OCB}=10^\circ$", r"$\angle\mathrm{OAC}=\angle\mathrm{OCA}=40^\circ$", r"$\angle\mathrm{OAB}=\angle\mathrm{OBA}=x+10^\circ$", r"$x+30^\circ+(x+10^\circ)+40^\circ=180^\circ$", r"$x=\boldsymbol{50^\circ}$"])
    return figs, sols

def q7():
    figs, sols = [], []
    # (1) ∠IBC=30°, ∠ICB=36°, x=∠IAB(=24°)
    A, B, C = tri_angles(48, 60); I = incenter(A, B, C)
    ok("7(1)", angle_at(A, B, I), 24)
    f = Fig(150); f.poly(A, B, C); f.seg(I, A, 1.2); f.seg(I, B, 1.2); f.seg(I, C, 1.2); f.dot(I, r=2)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.text(add(I, (10/f.s, 12/f.s)), "I", 14)
    f.angmark(B, I, C, "30°"); f.angmark(C, B, I, "36°"); f.angmark(A, B, I, "x")
    figs.append(f.svg())
    sols.append([r"$\angle\mathrm{IBA}=30^\circ,\ \angle\mathrm{ICA}=36^\circ$", r"$\angle\mathrm{IAC}=x$", r"$2(x+30^\circ+36^\circ)=180^\circ$", r"$x=\boldsymbol{24^\circ}$"])
    # (2) ∠BAC=64°, ∠IBC=28°, x=∠ICA(=30°)
    A, B, C = tri_angles(64, 56); I = incenter(A, B, C)
    ok("7(2)", angle_at(C, I, A), 30)
    f = Fig(150); f.poly(A, B, C); f.seg(I, B, 1.2); f.seg(I, C, 1.2); f.dot(I, r=2)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.text(add(I, (10/f.s, 12/f.s)), "I", 14)
    f.angmark(A, B, C, "64°"); f.angmark(B, I, C, "28°"); f.angmark(C, I, A, "x")
    figs.append(f.svg())
    sols.append([r"$\angle\mathrm{B}=2\times 28^\circ=56^\circ$", r"$\angle\mathrm{C}=180^\circ-64^\circ-56^\circ=60^\circ$", r"$x=60^\circ\div 2=\boldsymbol{30^\circ}$"])
    # (3) ∠BIC=118°, x=∠BAC(=56°)
    A, B, C = tri_angles(56, 64); I = incenter(A, B, C)
    ok("7(3)", angle_at(I, B, C), 118)
    f = Fig(150); f.poly(A, B, C); f.seg(I, B, 1.2); f.seg(I, C, 1.2); f.dot(I, r=2)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.text(add(I, (10/f.s, 12/f.s)), "I", 14)
    f.angmark(I, C, B, "118°"); f.angmark(A, B, C, "x")
    figs.append(f.svg())
    sols.append([r"$\angle\mathrm{IBC}+\angle\mathrm{ICB}$", r"$=180^\circ-118^\circ=62^\circ$", r"$\angle\mathrm{B}+\angle\mathrm{C}=124^\circ$", r"$x=180^\circ-124^\circ=\boldsymbol{56^\circ}$"])
    return figs, sols

def pages():
    blk, q, cells, sol, ansline = Z.blk, Z.q, Z.cells, Z.sol, Z.ansline
    ANS = Z.ANS
    f1, s1 = q1(); f3, s3 = q3(); f4, s4 = q4(); f5, s5 = q5(); f6, s6 = q6(); f7, s7 = q7()
    c1 = blk(q(1, '長さが図のように与えられていて，$\\mathrm{PQ}\\parallel\\mathrm{BC}$ のとき，$x$ を求めよ。') + cells(f1, s1, ["$9$", "$6$", "$6$"]))
    nl = (q(2, '線分 AB を $3:1$ に内分する点 P，線分 AB を $3:1$ に外分する点 Q，線分 AB を $1:2$ に外分する点 R を，それぞれ下の図にしるせ。')
          + f'<div style="margin:1mm 2mm 0">{numberline(ANS)}</div>'
          + sol([r"P：$\mathrm{AB}$ は 4 目もり。$\mathrm{AP}=4\times\dfrac{3}{4}=3$ 目もり",
                 r"Q：$\mathrm{AQ}:\mathrm{QB}=3:1$ → B の外側。$\mathrm{AQ}=4\times\dfrac{3}{2}=6$ 目もり",
                 r"R：$\mathrm{AR}:\mathrm{RB}=1:2$ → A の外側。$\mathrm{AR}=4\times\dfrac{1}{1}=4$ 目もり"]))
    c2 = blk(nl, .8) + blk(q(3, '右の図において，AD は $\\angle\\mathrm{A}$ の二等分線である。$x$ を求めよ。')
                         + f'<div class="row"><div class="cell"><div class="fig">{f3}</div>{sol(s3)}{ansline("$4$")}</div></div>', 1.2)
    c3 = blk(q(4, '下の図において，点 D は角の二等分線と辺の交点である。$x$ を求めよ。') + cells(f4, s4, ["$4$", "$8$", "$6$"]))
    d1 = (blk(q(5, '下の図において，AD は $\\triangle\\mathrm{ABC}$ の $\\angle\\mathrm{A}$ の外角の二等分線である。$x$ を求めよ。') + cells(f5, s5, ["$10$", "$15$"]))
          + blk(q(6, '下の図において，点 O は $\\triangle\\mathrm{ABC}$ の外心である。$x$ を求めよ。') + cells(f6, s6, ["$35^\\circ$", "$62^\\circ$", "$50^\\circ$"])))
    bx = lambda v: f'<span class="bx">{v if ANS else ""}</span>'
    q8 = (q(8, '右の図において，点 G は $\\triangle\\mathrm{ABC}$ の重心であり，$\\mathrm{EF}\\parallel\\mathrm{BC}$ である。$\\mathrm{BC}=24$ のとき，次のものを求めよ。<br>(1) $\\mathrm{EG}:\\mathrm{BD}$　(2) 線分 EG の長さ　(3) 線分 EF の長さ')
          + f'<div class="row"><div class="cell"><div class="fig" style="justify-content:flex-end">{Z.centroid_fig("24", 22)}</div>'
          + sol([r"(1) $\mathrm{AG}:\mathrm{GD}=2:1$，$\mathrm{EG}\parallel\mathrm{BD}$ より", r"$\mathrm{EG}:\mathrm{BD}=\mathrm{AG}:\mathrm{AD}=\boldsymbol{2:3}$",
                 r"(2) D は BC の中点で $\mathrm{BD}=12$", r"$\mathrm{EG}=12\times\dfrac{2}{3}=\boldsymbol{8}$",
                 r"(3) 同じように $\mathrm{GF}=\mathrm{DC}\times\dfrac{2}{3}=8$", r"$\mathrm{EF}=8+8=\boldsymbol{16}$"])
          + f'<div class="ansl">(1){bx("$2:3$")}　(2){bx("$8$")}　(3){bx("$16$")}</div></div></div>')
    d2 = (blk(q(7, '下の図において，点 I は $\\triangle\\mathrm{ABC}$ の内心である。$x$ を求めよ。') + cells(f7, s7, ["$24^\\circ$", "$30^\\circ$", "$56^\\circ$"]))
          + blk(q8))
    q9 = (q(9, '右の図において，点 G は $\\triangle\\mathrm{ABC}$ の重心であり，$\\mathrm{EF}\\parallel\\mathrm{BC}$ である。$\\mathrm{AG}=12$，$\\mathrm{EG}=7$ のとき，線分 GD と線分 BC の長さを求めよ。')
          + f'<div class="row"><div class="cell"><div class="fig" style="justify-content:flex-end">{Z.centroid_fig()}</div>'
          + sol([r"重心は中線を $2:1$ に分けるから", r"$\mathrm{GD}=12\div 2=\boldsymbol{6}$",
                 r"$\mathrm{EG}\parallel\mathrm{BD}$ より $\mathrm{EG}:\mathrm{BD}=\mathrm{AG}:\mathrm{AD}=2:3$", r"$\mathrm{BD}=7\times\dfrac{3}{2}=\dfrac{21}{2}$",
                 r"D は BC の中点だから $\mathrm{BC}=\dfrac{21}{2}\times 2=\boldsymbol{21}$"])
          + f'<div class="ansl">GD{bx("$6$")}　BC{bx("$21$")}</div></div></div>')
    d3 = blk(q9)
    t = lambda n: f'{Z.TITLE} &lt;No.{n}&gt;' + ('　<span style="color:#d40000">【解答】</span>' if ANS else '')
    nm = '1年(　　)組(　　)番　氏名(　　　　　　　　　　)'
    pg = lambda n, cs: (f'<div class="page"><div class="hd"><div class="t">{t(n)}</div><div class="n">{nm}</div></div>'
                        f'<div class="cols">' + "".join(f'<div class="col">{c}</div>' for c in cs) + f'</div><div class="foot">-{n}-</div></div>')
    return pg(1, [c1, c2, c3]) + pg(2, [d1, d2, d3])

if __name__ == "__main__":
    # 検算（数の確かめ）
    from fractions import Fraction as Fr
    assert Fr(4*3, 4) == 3 and Fr(4*3, 3-1) == 6 and Fr(4*1, 2-1) == 4          # ［2］P・Q・R の目もり
    assert Fr(24, 2)*Fr(2, 3) == 8 and Fr(12, 2) == 6 and Fr(7*3, 2)*2 == 21      # ［8］［9］
    bad = 0
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page()
        for ans, name in [(False, NAME), (True, NAME + "_ans")]:
            Z.ANS = ans; Z.CHK.clear()
            pg.set_content(Z.doc(pages())); pg.wait_for_timeout(400); pg.evaluate("document.fonts.ready")
            over = pg.evaluate("""()=>[...document.querySelectorAll('.col,.cell,.blk')].filter(e=>e.scrollHeight>e.clientHeight+1).map(e=>e.className+':'+e.textContent.slice(0,20))""")
            if over: bad += 1; print("!! はみ出し", name, over)
            pg.pdf(path=str(Z.OUT / f"{name}.pdf"), prefer_css_page_size=True, print_background=True)
            print(name + ".pdf", "検算", len(Z.CHK), "件OK")
        br.close()
    if bad: raise SystemExit("はみ出しあり")
