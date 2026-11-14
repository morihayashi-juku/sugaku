"""中3 実力テスト⑤（高校入試形式・大問1〜5）を、大問1／単元別の PDF にする。
問題（pdf/c3_jitsu5_*.pdf）と、問題に赤字で答え・途中式を書き込んだこたえ（_ans.pdf）を同じレイアウトで出す。
部品・CSS は c3_jitsu_test.py（①）〜 c3_jitsu4_test.py（④）と共通。

  大問1 小問集合（ヒストグラム・作図つき）       c3_jitsu5_d1
  大問2 空間図形（円錐・回転体）                 c3_jitsu5_kuukan
  大問3-1(1) 文字式の利用（カレンダー）          c3_jitsu5_moji
  大問3-1(2) 確率（天気予報）                    c3_jitsu5_kakuritsu
  大問3-2 連立方程式の利用（牛乳パック）         c3_jitsu5_renritsu
  大問4 平面図形（平行線・ひし形・比）           c3_jitsu5_zukei
  大問5 比例と反比例（双曲線と面積）             c3_jitsu5_hirei

実行：cd tools && python3 c3_jitsu5_test.py
"""
from fractions import Fraction as F
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from c3_jitsu_test import A, W, BX, Q, lines, OUT  # noqa: E402
from c3_jitsu2_test import build, _pt, _arc  # noqa: E402
from c3_jitsu3_test import T, L, right_mark  # noqa: E402

# ================= 答えの確認 =================
assert -3 + 7 == 4 and F(9, 4) / F(-3, 8) == -6 and F(20) / (-4 ** 2) * (-2) ** 2 == -5
HIST = [4, 5, 8, 9, 11, 2, 1]                       # 4点〜10点（図から読んだ人数）
assert sum(HIST) == 40
MEAN = F(sum(s * c for s, c in zip(range(4, 11), HIST)), 40)
assert MEAN == F(67, 10) and MEAN < 7 < 8                    # 平均 6.7 < 中央値 7 < 最頻値 8 → ア
assert 360 * 5 // 20 == 90 and 40 // 10 == 4 and F(1, 3) * 100 * 6 - F(1, 3) * 36 * 10 == 80
assert (172 % 50, 563 % 100) == (22, 63)
MX, MY = 928, 337
assert (MX + 22) - (MY + 63) == 550 and F(MX + 22, 50) + F(MY + 63, 100) == 23
assert F(3, 12) == F(1, 4) and 14 * 24 // 4 == 84
assert 9 * F(36, 5) / (9 + F(36, 5)) == 4 and 9 - 4 - 4 == 1
assert -3 * 12 == 9 * -4 == -36 and 16 * 12 // 2 == 96 and F(1, 2) * (8 - -8) * 12 == 96

TAG = "中3　実力テスト⑤"


def header(title, page=None):
    p = f"（{page}）" if page else ""
    return (f'<div class="hd"><div class="ht"><span class="tag">{TAG}</span>{title}{p}<span class="key">解答</span></div>'
            '<div class="nm">　月　　日　名前（　　　　　　　　　）</div></div>')


# ================= 図 =================
def hist_svg():
    Lx, Tp, bw, Hh = 24, 14, 26, 128
    ys = lambda v: Tp + Hh - v / 12 * Hh
    s = T(6, 10, "(人)", "sm", "start")
    for v in range(0, 13):
        s += L((Lx, ys(v)), (Lx + 8 * bw, ys(v)), 0.5, False, "#888")
    s += f'<rect x="{Lx}" y="{Tp}" width="{8 * bw}" height="{Hh}" fill="none" stroke="#000" stroke-width="1"/>'
    for i, c in enumerate(HIST):
        x = Lx + (i + 0.5) * bw
        s += f'<rect x="{x:.1f}" y="{ys(c):.1f}" width="{bw}" height="{Hh * c / 12:.1f}" fill="#ccc" stroke="#000" stroke-width="1"/>'
        s += T(x + bw / 2, Tp + Hh + 12, str(4 + i), "sm")
    for v in (0, 5, 10):
        s += T(Lx - 4, ys(v) + 3, str(v), "sm", "end")
    s += T(Lx + 8 * bw + 4, Tp + Hh + 12, "(点)", "sm", "start")
    return f'<svg width="{Lx + 8 * bw + 30}" height="{Tp + Hh + 18}" viewBox="0 0 {Lx + 8 * bw + 30} {Tp + Hh + 18}">{s}</svg>'


def _bis(V, a1, a2, r=38, r2=32):
    """角の二等分線の作図（a1・a2 は2本の半直線の向き。度・数学の向き）。弧と、Q（二等分線上の点）を返す"""
    lo, hi = min(a1, a2), max(a1, a2)
    M, N = _pt(V, r, a1), _pt(V, r, a2)
    am = (a1 + a2) / 2
    half = r * math.sin(math.radians(abs(a2 - a1) / 2))
    d = r * math.cos(math.radians(abs(a2 - a1) / 2)) + math.sqrt(r2 * r2 - half * half)
    Qp = _pt(V, d, am)
    s = _arc(V, r, hi + 8, lo - 8)
    for P0 in (M, N):
        ang = math.degrees(math.atan2(-(Qp[1] - P0[1]), Qp[0] - P0[0]))
        s += _arc(P0, r2, ang + 14, ang - 14)
    return s, am


def roads_svg():
    A_ = (40, 190)
    C_ = _pt(A_, 205, 3)
    endB, B_ = _pt(A_, 184, 77), _pt(A_, 152, 77)
    endD, D_ = _pt(C_, 184, 96), _pt(C_, 154, 96)
    s = L(endB, A_) + L(A_, C_) + L(C_, endD)
    s += "".join(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="2.3" fill="#000"/>' for p in (A_, B_, C_, D_))
    s += T(A_[0] - 4, A_[1] + 15, "A町") + T(B_[0] - 22, B_[1] + 2, "B町") + T(C_[0] + 18, C_[1] + 4, "C町") + T(D_[0] + 20, D_[1] + 2, "D町")
    s += T(A_[0] + 2, A_[1] - 88, "道路㋐", "sm") + T((A_[0] + C_[0]) / 2, A_[1] + 14, "道路㋑", "sm") + T(C_[0] + 18, C_[1] - 96, "道路㋒", "sm")
    c1, am1 = _bis(A_, 77, 3, 32, 28)
    c2, am2 = _bis(C_, 183, 96, 32, 28)
    # 2本の二等分線の交点 P
    d1 = (math.cos(math.radians(am1)), -math.sin(math.radians(am1)))
    d2 = (math.cos(math.radians(am2)), -math.sin(math.radians(am2)))
    det = d1[0] * (-d2[1]) - d1[1] * (-d2[0])
    t = ((C_[0] - A_[0]) * (-d2[1]) - (C_[1] - A_[1]) * (-d2[0])) / det
    P = (A_[0] + t * d1[0], A_[1] + t * d1[1])
    c = c1 + c2 + L(A_, _pt(A_, t + 30, am1), 1.2) + L(C_, _pt(C_, math.dist(C_, P) + 30, am2), 1.2)
    c += f'<circle cx="{P[0]:.1f}" cy="{P[1]:.1f}" r="2.6" fill="#c00"/>' + T(P[0], P[1] - 8, "P")
    return f'<svg width="{C_[0] + 50:.0f}" height="{A_[1] + 22}" viewBox="0 0 {C_[0] + 50:.0f} {A_[1] + 22}">{s}<g class="cons">{c}</g></svg>'


def cone_svg(string=False):
    cx, top, base, rx, ry = 60, 12, 132, 38, 11
    s = (L((cx, top), (cx - rx, base)) + L((cx, top), (cx + rx, base))
         + f'<path d="M{cx - rx} {base} A{rx} {ry} 0 0 0 {cx + rx} {base}" fill="none" stroke="#000" stroke-width="1.2"/>'
         + f'<path d="M{cx - rx} {base} A{rx} {ry} 0 0 1 {cx + rx} {base}" fill="none" stroke="#000" stroke-width="1" stroke-dasharray="3,2"/>')
    s += f'<circle cx="{cx}" cy="{base}" r="1.8" fill="#000"/>' + T(cx, top - 3, "P") + T(cx - rx - 8, base + 6, "Q") + T(cx + 10, base + 14, "O")
    if not string:
        s += L((cx, top), (cx, base), 1, True) + L((cx, base), (cx - rx, base), 1, True)
        s += T(cx - 34, 70, "20cm", "sm") + T(cx + 12, 112, "5cm", "sm", "start")
    else:
        s += f'<path d="M{cx - rx} {base} Q{cx + 4} {base - 6} {cx + rx - 4} {base - 46}" fill="none" stroke="#000" stroke-width="1.6"/>'
        s += f'<path d="M{cx + rx - 4} {base - 46} Q{cx - 10} {base - 62} {cx - rx} {base}" fill="none" stroke="#000" stroke-width="1.2" stroke-dasharray="3,2"/>'
    return f'<svg width="120" height="{base + 18}" viewBox="0 0 120 {base + 18}">{s}</svg>'


def sector_opts_svg():
    r = 50

    def one(ox, lab, deg, mode):
        P = (ox + 12, 34)
        Qp = (P[0], P[1] + r)
        Q2 = _pt(P, r, -90 + deg)
        large = 1 if deg > 180 else 0
        s = f'<path d="M{P[0]} {P[1]} L{Q2[0]:.1f} {Q2[1]:.1f} A{r} {r} 0 {large} 1 {Qp[0]} {Qp[1]} Z" fill="#fff" stroke="#000" stroke-width="1.1"/>'
        if mode == "chord":
            s += L(Qp, Q2, 1.1)
        else:
            mid = ((P[0] + Q2[0]) / 2, (P[1] + Q2[1]) / 2)
            s += L(Qp, mid, 1.1) + T(mid[0] + 2, mid[1] - 6, "10cm", "sm", "start")
        if deg == 90:
            s += right_mark(P, (0, 1), (1, 0), 6)
        else:
            s += T(P[0] + 8, P[1] + 22, "60°", "sm", "start")
        bc = _pt(P, r + 15, -90 + deg / 2 - 18)
        s += f'<circle cx="{bc[0]:.1f}" cy="{bc[1]:.1f}" r="13" fill="#fff" stroke="#000" stroke-width="1"/><circle cx="{bc[0]:.1f}" cy="{bc[1]:.1f}" r="1.5"/>' + T(bc[0] + 7, bc[1] + 3, "O", "sm")
        s += T(ox, 13, lab, "b2", "start") + T(P[0] - 8, P[1] + 2, "P", "sm") + T(Qp[0] - 8, Qp[1] + 10, "Q", "sm")
        return s
    s = one(4, "ア", 90, "half") + one(122, "イ", 60, "chord") + one(240, "ウ", 90, "chord") + one(358, "エ", 120, "half")
    return f'<svg width="490" height="124" viewBox="0 0 490 124">{s}</svg>'


def roll_svg():
    s = '<ellipse cx="130" cy="58" rx="122" ry="52" fill="none" stroke="#000" stroke-width="1" stroke-dasharray="2,2"/>'
    P, top, bot = (90, 58), (190, 16), (190, 102)
    s += L(P, top) + L(P, bot) + '<ellipse cx="190" cy="59" rx="14" ry="43" fill="#fff" stroke="#000" stroke-width="1.1"/>'
    s += '<circle cx="190" cy="59" r="1.6"/>' + T(80, 62, "P") + T(198, 52, "O", "sm") + T(196, 116, "Q")
    return f'<svg width="270" height="122" viewBox="0 0 270 122">{s}</svg>'


def rst_svg():
    k = 13
    T_ = (20 + 10 * k, 12 + 6 * k)
    S_ = (20, T_[1])
    R_ = (T_[0], 12)
    s = f'<polygon points="{R_[0]},{R_[1]} {S_[0]},{S_[1]} {T_[0]},{T_[1]}" fill="none" stroke="#000" stroke-width="1.2"/>' + right_mark(T_, (-1, 0), (0, -1), 7)
    s += T(R_[0] + 8, R_[1] + 2, "R") + T(S_[0] - 6, S_[1] + 12, "S") + T(T_[0] + 8, T_[1] + 12, "T")
    return f'<svg width="{T_[0] + 22}" height="{T_[1] + 16}" viewBox="0 0 {T_[0] + 22} {T_[1] + 16}">{s}</svg>'


def cal_svg(mark):
    cw, ch, x0, y0 = 28, 19, 6, 18
    pos = lambda d: ((d + 1) % 7, (d + 1) // 7)
    s = "".join(T(x0 + cw * i + cw / 2, 12, w, "sm") for i, w in enumerate("日月火水木金土"))
    shade = {5, 7, 10} if mark == 3 else set()
    for d in range(1, 31):
        c, r = pos(d)
        if d in shade:
            s += f'<rect x="{x0 + c * cw + 1}" y="{y0 + r * ch + 1}" width="{cw - 2}" height="{ch - 2}" fill="#aaa"/>'
        s += T(x0 + c * cw + cw / 2, y0 + r * ch + 14, str(d), "sm")
    box = lambda c0, r0, c1, r1: f'<rect x="{x0 + c0 * cw}" y="{y0 + r0 * ch}" width="{(c1 - c0 + 1) * cw}" height="{(r1 - r0 + 1) * ch}" fill="none" stroke="#000" stroke-width="1.1"/>'
    if mark == 1:
        s += box(4, 1, 5, 2)
    elif mark == 2:
        s += box(2, 0, 2, 4)
    elif mark == 3:
        X = lambda c: x0 + c * cw
        Y = lambda r: y0 + r * ch
        s += f'<polygon points="{X(2)},{Y(0)} {X(7)},{Y(0)} {X(7)},{Y(2)} {X(0)},{Y(2)} {X(0)},{Y(1)} {X(2)},{Y(1)}" fill="none" stroke="#000" stroke-width="1.1"/>'
    elif mark == 4:
        s += box(0, 2, 6, 3)
    return f'<svg width="{x0 + 7 * cw + 6}" height="{y0 + 5 * ch + 4}" viewBox="0 0 {x0 + 7 * cw + 6} {y0 + 5 * ch + 4}">{s}</svg>'


def tri4_svg():
    ab, ac, cosA = 9, 7.2, 0.24
    bc = math.sqrt(ab * ab + ac * ac - 2 * ab * ac * cosA)
    ax = (ab * ab - ac * ac + bc * bc) / (2 * bc)
    ay = math.sqrt(ab * ab - ax * ax)
    k = 26
    B_, C_, A_ = (20, 20 + ay * k), (20 + bc * k, 20 + ay * k), (20 + ax * k, 20)
    lerp = lambda p, q, t: (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    E_, G_, F_ = lerp(A_, B_, 4 / 9), lerp(A_, B_, 5 / 9), lerp(A_, C_, 4 / 7.2)
    D_ = lerp(B_, C_, 9 / 16.2)
    # H＝DE と GF の交点（GF は水平）
    t = (G_[1] - D_[1]) / (E_[1] - D_[1])
    H_ = lerp(D_, E_, t)
    s = f'<polygon points="{A_[0]:.1f},{A_[1]:.1f} {B_[0]:.1f},{B_[1]:.1f} {C_[0]:.1f},{C_[1]:.1f}" fill="none" stroke="#000" stroke-width="1.2"/>'
    s += L(A_, D_) + L(D_, E_) + L(D_, F_) + L(G_, F_)
    s += T(A_[0], A_[1] - 6, "A") + T(B_[0] - 8, B_[1] + 12, "B") + T(C_[0] + 8, C_[1] + 12, "C") + T(D_[0], D_[1] + 14, "D")
    s += T(E_[0] - 8, E_[1] - 3, "E") + T(G_[0] - 10, G_[1] + 2, "G") + T(F_[0] + 9, F_[1] + 2, "F") + T(H_[0] - 2, H_[1] + 14, "H")
    return f'<svg width="{C_[0] + 24:.0f}" height="{B_[1] + 20:.0f}" viewBox="0 0 {C_[0] + 24:.0f} {B_[1] + 20:.0f}">{s}</svg>'


def hyp_svg():
    sc = 11
    ox, oy = 9 * sc + 26, 14 * sc + 14
    X = lambda x: ox + x * sc
    Y = lambda y: oy - y * sc
    s = L((X(-9), Y(0)), (X(13), Y(0)), 1) + L((X(0), Y(-11)), (X(0), Y(15)), 1)
    s += T(X(13) + 6, Y(0) + 4, '<tspan class="ax">x</tspan>', "pl") + T(X(0) + 2, Y(15) - 4, '<tspan class="ax">y</tspan>', "pl") + T(X(0) + 8, Y(0) + 13, "O", "sm")
    for xs in ([-9 + i * 0.1 for i in range(65)], [3.3 + i * 0.1 for i in range(98)]):
        pts = " ".join(f"{X(x):.1f},{Y(-36 / x):.1f}" for x in xs if -11 <= -36 / x <= 15)
        s += f'<polyline points="{pts}" fill="none" stroke="#000" stroke-width="1.2"/>'
    s += T(X(-9) - 10, Y(4) + 4, "①", "sm") + T(X(13) + 2, Y(-36 / 13) - 4, "①", "sm")
    A_, B_, C_, P_ = (-3, 12), (9, -4), (-3, -4), (0, -7)
    pp = lambda p: (X(p[0]), Y(p[1]))
    s += L(pp(A_), pp(C_)) + L(pp(C_), pp(B_)) + L(pp(A_), pp(B_)) + L(pp(A_), pp(P_)) + L(pp(P_), pp(B_))
    s += T(X(-3) - 9, Y(12) - 2, "A") + T(X(9) + 6, Y(-4) + 13, "B") + T(X(-3) - 9, Y(-4) + 12, "C") + T(X(0) - 9, Y(-7) + 12, "P")
    return f'<svg width="{X(13) + 24}" height="{Y(-11) + 6}" viewBox="0 0 {X(13) + 24} {Y(-11) + 6}">{s}</svg>'


# ================= 大問1 =================
def d1():
    c1 = Q("(1)", r"$-3+7$ を計算しなさい。", W(r"$7-3=4$"), A("4"), 2)
    c2 = Q("(2)", r"$\dfrac94\div\left(-\dfrac38\right)$ を計算しなさい。", W(r"$-\dfrac94\times\dfrac83=-6$"), A("$-6$"), 2)
    c3 = Q("(3)", r"$20\div(-4^2)\times(-2)^2$ を計算しなさい。", W(r"$-4^2=-16$、$(-2)^2=4$　$20\div(-16)\times4=-5$"), A("$-5$"), 2)
    c4 = Q("(4)", r"$a-4(a-b)+3b$ を計算しなさい。", W(r"$a-4a+4b+3b$"), A(r"$-3a+7b$"), 2)
    c5 = Q("(5)", r"方程式 $7(3x-1)=35$ を解きなさい。", W(r"両辺を7でわって $3x-1=5$　$3x=6$"), A(r"$x=2$"), 2)
    c6 = Q("(6)", "七角形の内角の和を求めなさい。", W(r"$180^\circ\times(7-2)$"), A(r"$900^\circ$"), 2)
    c7 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(7)</span>右の図は、あるクラスの生徒40人に実施したテストの結果をヒストグラムにまとめたものである。'
          'このとき、平均値、中央値、最頻値の大小関係を正しく表したものを、次のア〜エから1つ選び、記号で答えなさい。</div>'
          '<div class="ch">ア　（平均値）＜（中央値）＜（最頻値）<br>イ　（中央値）＜（平均値）＜（最頻値）<br>ウ　（最頻値）＜（平均値）＜（中央値）<br>エ　（最頻値）＜（中央値）＜（平均値）</div>'
          + W(r"人数は4点から順に 4・5・8・9・11・2・1 人。最頻値は8点。<br>中央値は20・21番目で、どちらも7点。<br>"
              r"平均値は $(16+25+48+63+88+18+10)\div40=6.7$（点）")
          + f'</div><div class="fig">{hist_svg()}</div></div><div class="al">答　{A("ア", "w20")}</div></div>')
    c8 = ('<div class="q"><div class="qt"><span class="no">(8)</span>美咲さんは、下の図で、自宅の位置を次のように説明した。</div>'
          '<div class="frame" style="margin-left:7mm">・自宅は、A町からB町を通ってのびる道路㋐と、A町とC町を結ぶ道路㋑から等しい距離にある。<br>'
          '・自宅は、A町とC町を結ぶ道路㋑と、C町からD町を通ってのびる道路㋒から等しい距離にある。</div>'
          '<div class="qt" style="margin-left:7mm">自宅の位置をPとして、点Pをコンパスと定規を使って作図しなさい。作図に用いた線は消さずに残しておくこと。ただし、図において、A町、B町、C町、D町の位置は点（・）で示してある。</div>'
          f'<div class="flex"><div class="grow">'
          + W("2本の道路から等しい距離にある点は、その2本がつくる角の二等分線上にある。<br>"
              "①A町を頂点とする、道路㋐と道路㋑の角の二等分線をひく。<br>②C町を頂点とする、道路㋑と道路㋒の角の二等分線をひく。<br>③2本の二等分線の交点がP。")
          + f'</div><div class="fig">{roads_svg()}</div></div></div>')
    return f"""<section class="page">{header("大問1　小問集合")}
<div class="lead">次の(1)〜(8)の問いに答えなさい。</div>
<div class="grid2">{c1}{c2}{c3}{c4}{c5}{c6}</div>
{c7}
{c8}
</section>"""


# ================= 大問2 空間図形 =================
def d2():
    q1a = Q("(1)", "ひもの長さが最短になるとき、展開図上のひものようすを表したものとして正しいものを、次のア〜エから1つ選び、記号で答えなさい。"
            f'<div style="margin:1mm 0 0 7mm">{sector_opts_svg()}</div>',
            W(r"側面のおうぎ形の中心角は $360^\circ\times\dfrac{5}{20}=90^\circ$。最短のひもは、展開図でQともう一方のQ（おうぎ形の両はし）を結ぶ線分。"),
            A("ウ", "w20"), 2)
    q1b = Q("(2)", "ひもによって分けられる2つの側面部分のうち、頂点Pを<b>ふくまない</b>部分の面積を求めなさい。",
            W(r"おうぎ形 $\pi\times20^2\times\dfrac{90}{360}=100\pi$ から、直角二等辺三角形 $\dfrac12\times20\times20=200$ をひく。"),
            A(r"$(100\pi-200)$ cm²", "w30"), 8)
    q2 = Q("2", "図Ⅲは、図Ⅰの円錐の母線PQを平面上に置き、頂点Pを中心として、すべることのないように転がしたものである。円錐が点線で示した円の上を1周してもとの位置にかえるまでに何回転するか求めなさい。",
           W(r"点線の円の半径は母線20cm。円周 $2\pi\times20=40\pi$、底面の円周 $2\pi\times5=10\pi$<br>$40\pi\div10\pi=4$"),
           A("4回転", "w20"), 4)
    q3 = Q("3", "図Ⅳは、辺RT＝6cm、辺ST＝10cm、∠STR＝90°の直角三角形RSTである。この三角形を、直線RTを軸として1回転させてできる立体の体積と、直線STを軸として1回転させてできる立体の体積の差を求めなさい。",
           W(r"RTが軸：底面の半径10、高さ6の円錐　$\dfrac13\pi\times10^2\times6=200\pi$<br>"
             r"STが軸：底面の半径6、高さ10の円錐　$\dfrac13\pi\times6^2\times10=120\pi$<br>$200\pi-120\pi=80\pi$"),
           A(r"$80\pi$ cm³", "w30"), 6)
    return f"""<section class="page">{header("大問2　空間図形")}
<div class="flex"><div class="grow"><div class="lead">右の図Ⅰのような円錐がある。図の円錐の頂点を点P、底面である円の中心を点O、円Oの周上の点の1つを点Qとする。また、OQ＝5cm、PQ＝20cmとする。
このとき、次の1〜3の問いに答えなさい。ただし、円周率は $\\pi$ とする。</div>
<div class="q"><div class="qt"><span class="no">1</span>右の図Ⅱは、図Ⅰの円錐で点Qから側面上を1周して、点Qにもどってくるようにひもをかけたものである。このとき、次の(1)、(2)の問いに答えなさい。</div></div></div>
<div class="fig"><b>図Ⅰ</b><br>{cone_svg()}</div><div class="fig"><b>図Ⅱ</b><br>{cone_svg(True)}</div></div>
{q1a}{q1b}
<div class="flex"><div class="grow">{q2}</div><div class="fig"><b>図Ⅲ</b><br>{roll_svg()}</div></div>
<div class="flex"><div class="grow">{q3}</div><div class="fig"><b>図Ⅳ</b><br>{rst_svg()}</div></div>
</section>"""


# ================= 大問3-1 カレンダー =================
CAL_LEAD = '<div class="lead">図Ⅰ〜Ⅳは、ある同じ月のカレンダーである。</div>'


def d3m():
    q1 = Q("①", r"図Ⅰのように、枠で囲んだ4つの数において、最小の数を $n$ とするとき、4つの数の和を、整数 $n$ を用いて表しなさい。",
           W(r"右どなりは1大きく、すぐ下は7大きいので、4つの数は $n,\ n+1,\ n+7,\ n+8$<br>和は $n+(n+1)+(n+7)+(n+8)=4n+16$"), A(r"$4n+16$", "w30"), 14)
    q2 = Q("②", r"図Ⅱの枠で囲んだ5つの数において、第 $m$ 週の数を、整数 $m$ を用いて表しなさい。",
           W(r"1、8、15、22、29 と7ずつ増える。第1週が1だから　$1+7(m-1)=7m-6$"), A(r"$7m-6$", "w30"), 14)
    return f"""<section class="page">{header("大問3-1(1)　文字式の利用")}
{CAL_LEAD}
<div class="flex" style="justify-content:space-around"><div class="fig"><b>図Ⅰ</b><br>{cal_svg(1)}</div><div class="fig"><b>図Ⅱ</b><br>{cal_svg(2)}</div></div>
<div class="q"><div class="qt"><span class="no">(1)</span></div></div>
{q1}{q2}
</section>"""


def d3k():
    q1 = Q("①", "図Ⅲの枠で囲んだ12日間における天気予報では、かげをつけた日が晴れる予報が出ている。この期間で晴れの日になる確率は何％か求めなさい。",
           W(r"かげをつけた日は5日・7日・10日の3日。$\dfrac{3}{12}=\dfrac14=0.25$"), A("25％", "w20"), 14)
    q2 = Q("②", "図Ⅳの枠で囲んだ2週間における天気予報では、雨が降る時間の確率が25％と予報している。雨が降る時間は合計何時間と考えられるか求めなさい。",
           W(r"2週間は $14\times24=336$（時間）　$336\times0.25=84$"), A("84時間", "w20"), 14)
    return f"""<section class="page">{header("大問3-1(2)　確率")}
{CAL_LEAD}
<div class="flex" style="justify-content:space-around"><div class="fig"><b>図Ⅲ</b><br>{cal_svg(3)}</div><div class="fig"><b>図Ⅳ</b><br>{cal_svg(4)}</div></div>
<div class="q"><div class="qt"><span class="no">(2)</span></div></div>
{q1}{q2}
</section>"""


# ================= 大問3-2 連立方程式 =================
def d3r():
    d = lambda who, t: f'<p class="dl"><b>{who}：</b>{t}</p>'
    kaiwa = ('<div class="frame"><b>【会話】</b>'
             + d("三郎", "回収した1L用の牛乳パックは50枚ごとに、500mL用の牛乳パックは100枚ごとに、それぞれ1たばにまとめるよ。1たばにつきトイレットペーパー1個と交換してもらえるからね。")
             + d("明子", "先月回収した1L用の牛乳パックは172枚、500mL用の牛乳パックは563枚だから、合計8個のトイレットペーパーと交換したね。でも、たばにできなかった牛乳パックが少し残っているわ。")
             + d("三郎", "今月は、先月たばにできなかった分と今月回収した分をあわせてすべてたばにすることができたから、残らずトイレットペーパーと交換することができたよ。")
             + d("明子", "先月の残りの枚数と今月回収した枚数をあわせると、1L用の牛乳パックは、500mL用の牛乳パックより550枚多かったわ。")
             + d("三郎", "今月は、合計で23個のトイレットペーパーと交換することができたね。")
             + d("明子", "今月回収した1L用の牛乳パックと500mL用の牛乳パックは、それぞれ何枚だったのかな。") + '</div>')
    q1 = Q("(1)", r"今月回収した1L用の牛乳パックを $x$ 枚、500mL用の牛乳パックを $y$ 枚とする。今月トイレットペーパーと交換した1L用の牛乳パックと500mL用の牛乳パックの枚数を、それぞれ $x,\ y$ を用いて表しなさい。",
           W(r"先月の残り：1L用 $172-50\times3=22$（枚）、500mL用 $563-100\times5=63$（枚）"),
           "1L用：" + A(r"$(x+22)$ 枚", "w30") + "　500mL用：" + A(r"$(y+63)$ 枚", "w30"), 12)
    q2 = Q("(2)", r"今月回収した1L用の牛乳パックの枚数と、500mL用の牛乳パックの枚数を、連立方程式を使って求めなさい。ただし、今月回収した1L用の牛乳パックの枚数を $x$ 枚、500mL用の牛乳パックの枚数を $y$ 枚とし、答えを求める過程がわかるように、式と計算も書きなさい。",
           W(r"枚数の差：$(x+22)-(y+63)=550$ より $x-y=591$<br>"
             r"たばの数：$\dfrac{x+22}{50}+\dfrac{y+63}{100}=23$　両辺に100をかけて $2x+44+y+63=2300$ より $2x+y=2193$<br>"
             r"2つの式をたすと　$3x=2784$　$x=928$　$y=928-591=337$<br>（1L用 950枚＝19たば、500mL用 400枚＝4たば、19＋4＝23 で問題に合う）"),
           "1L用：" + A("928枚", "w20") + "　500mL用：" + A("337枚", "w20"), 42)
    return f"""<section class="page">{header("大問3-2　連立方程式の利用")}
<div class="lead">三郎さんと明子さんが通っている中学校では、毎月牛乳パックを回収している。回収した牛乳パックは、1枚の紙になるように開き、たばにまとめて、トイレットペーパーと交換してもらう。【会話】は、2人が回収した牛乳パックと、交換したトイレットペーパーについて話し合っている場面である。
このとき、下の(1)、(2)の問いに答えなさい。<br><span style="font-size:8.5pt">（もとの問題の「回収した牛乳パック → 開く → たばねる → トイレットペーパーと交換する」の絵は省いています）</span></div>
{kaiwa}{q1}{q2}
</section>"""


# ================= 大問4 平面図形 =================
def d4():
    proof = ('<div class="frame"><b>【証明】</b><div class="rb">'
             '仮定より、　∠FAD＝∠' + BX("ア", "BAD") + '　…①<br>'
             'AB∥FD より、平行線の ' + BX("イ", "錯角") + ' は等しいから、<br>　　∠' + BX("ア", "BAD") + '＝∠ADF　…②<br>'
             '①、②より、∠FAD＝∠ADF だから、<br>　　AF＝DF　…③<br>'
             'また、BG∥DF、GF∥BD より、四角形BDFGは平行四辺形であり、<br>平行四辺形の2組の ' + BX("ウ", "対辺") + ' はそれぞれ等しいから、<br>'
             '　　' + BX("エ", "DF") + '＝BG　…④<br>③、④より、　AF＝BG</div></div>')
    q1 = Q("1", "AF＝BGであることを次のように証明した。□のア、イ、ウ、エに当てはまる記号や言葉を書きなさい。ただし、同じカタカナのところには共通するものが入る。" + proof,
           "", "ア" + A("BAD", "w20") + "　イ" + A("錯角", "w20") + "　ウ" + A("対辺", "w20") + "　エ" + A("DF", "w20"), 0)
    q2 = Q("2", r"$\angle\mathrm{CAD}=40^\circ$、$\angle\mathrm{ABC}=35^\circ$ のとき、$\angle\mathrm{GHE}$ の大きさを求めなさい。",
           W(r"$\angle\mathrm{BAC}=40^\circ\times2=80^\circ$ より $\angle\mathrm{ACB}=180^\circ-80^\circ-35^\circ=65^\circ$<br>"
             r"HG∥CB、HE∥CA（向きも同じ）なので、$\angle\mathrm{GHE}=\angle\mathrm{BCA}=65^\circ$"), A(r"$65^\circ$", "w20"), 14)
    q3 = Q("3", "AE：AB＝4：9のとき、AE：EGを最も簡単な整数の比で表しなさい。ただし、答えを求める過程がわかるように説明しなさい。",
           lines(r"AE＝4、AB＝9 とする。AE∥FD、ED∥AF より四角形AEDFは平行四辺形で、③より AF＝DF だから、ひし形。よって AF＝AE＝4<br>"
                 r"1より BG＝AF＝4 だから　AG＝AB−BG＝9−4＝5<br>EG＝AG−AE＝5−4＝1　　よって　AE：EG＝4：1", 30), "AE：EG＝" + A("4：1", "w20"), 0)
    return f"""<section class="page">{header("大問4　平面図形（平行線・比）")}
<div class="lead">下の図で、△ABCの∠BACの二等分線と辺BCとの交点をDとする。点Dを通り辺ACに平行な直線と辺ABとの交点をEとし、点Dを通り辺ABに平行な直線と辺ACとの交点をFとする。また、点Fを通り辺BCに平行な直線と辺ABとの交点をGとし、線分DEと線分GFとの交点をHとする。
このとき、下の1〜3の問いに答えなさい。ただし、AB＞ACとする。</div>
<div style="text-align:center">{tri4_svg()}</div>
{q1}{q2}{q3}
</section>"""


# ================= 大問5 比例と反比例 =================
def d5():
    q1 = Q("1", r"$a$ の値を求めなさい。", W(r"A$(-3,\ 12)$ を代入して　$12=\dfrac{a}{-3}$　$a=-36$"), A(r"$a=-36$", "w20"), 12)
    q2 = Q("2", "点Cと、原点Oについて対称な点の座標を求めなさい。",
           W(r"Cの $x$ 座標はAと同じ $-3$、$y$ 座標はBと同じ $-4$ で C$(-3,\ -4)$。原点について対称なので、符号を両方変える。"), A(r"$(3,\ 4)$", "w20"), 12)
    q3 = Q("3", "△ACBの面積を求めなさい。", W(r"AC＝$12-(-4)=16$、CB＝$9-(-3)=12$、$\angle\mathrm{ACB}=90^\circ$　$\dfrac12\times12\times16=96$"), A("96", "w20"), 12)
    q4 = Q("4", r"△APBの面積が△ACBの面積と等しくなるとき、点Pの $y$ 座標を求めなさい。",
           W(r"直線AB：傾き $\dfrac{-4-12}{9-(-3)}=-\dfrac43$、$y=-\dfrac43x+8$。$y$ 軸との交点を D$(0,\ 8)$ とする。<br>"
             r"P$(0,\ p)$ とすると　△APB＝△APD＋△BPD＝$\dfrac12\times(8-p)\times(3+9)=6(8-p)$<br>"
             r"$6(8-p)=96$　$8-p=16$　$p=-8$（負の部分にある）<br>（Cを通りABに平行な直線 $y=-\dfrac43x-8$ と $y$ 軸の交点、と考えてもよい）"),
           A("$-8$", "w20"), 26)
    return f"""<section class="page">{header("大問5　比例と反比例")}
<div class="lead">下の図で、双曲線①は $y=\\dfrac{{a}}{{x}}\\ (a<0)$ のグラフである。2点A、Bは①上の点で、座標はそれぞれ $(-3,\\ 12)$、$(9,\\ -4)$ である。点Aを通り $y$ 軸に平行な直線と、点Bを通り $x$ 軸に平行な直線との交点をCとする。また、点Pは $y$ 軸上の負の部分を動く点であり、2点P、AとP、BとA、Bをそれぞれ結ぶ。
このとき、下の1〜4の問いに答えなさい。</div>
<div class="flex"><div class="grow">{q1}{q2}{q3}</div><div class="fig">{hyp_svg()}</div></div>
{q4}
</section>"""


JOBS = [("c3_jitsu5_d1", d1), ("c3_jitsu5_kuukan", d2), ("c3_jitsu5_moji", d3m), ("c3_jitsu5_kakuritsu", d3k),
        ("c3_jitsu5_renritsu", d3r), ("c3_jitsu5_zukei", d4), ("c3_jitsu5_hirei", d5)]

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    only = sys.argv[1:]
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for name, fn in JOBS:
            if only and name not in only:
                continue
            body = fn()
            for mode, suffix in [("mondai", ""), ("kaitou", "_ans")]:
                hp = pathlib.Path(f"/tmp/{name}_{mode}.html")
                hp.write_text(build(body, mode), encoding="utf-8")
                pg = br.new_page(viewport={"width": 794, "height": 1123})
                pg.goto(f"file://{hp}")
                pg.wait_for_selector("body[data-done]")
                pg.evaluate("document.fonts.ready")
                bad = pg.evaluate("""() => { const r = []; document.querySelectorAll('.page').forEach((p, i) => {
                    if (p.scrollHeight > p.clientHeight + 1) r.push('ページ' + (i + 1) + ' はみ出し ' + (p.scrollHeight - p.clientHeight) + 'px'); }); return r; }""")
                if bad:
                    print("!!", name + suffix, bad)
                pg.pdf(path=str(OUT / f"{name}{suffix}.pdf"), format="A4", print_background=True, prefer_css_page_size=True)
                pg.close()
                print("書き出し:", f"{name}{suffix}.pdf")
        br.close()
