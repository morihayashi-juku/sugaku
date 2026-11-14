"""実力テスト 令和4年度 3年・9月（大問1〜5）を、大問1／単元別の PDF にする。
問題（pdf/c3_jitsu_r409_*.pdf）と、問題に赤字で答え・途中式を書き込んだこたえ（_ans.pdf）を同じレイアウトで出す。
部品・CSS は c3_jitsu_test.py などと共通。common.json の jitsu.tests の id は r4-3-09。

  大問1 小問集合（度数分布表・垂線の作図）       c3_jitsu_r409_d1
  大問2-1 確率（さいころと玉の移動）             c3_jitsu_r409_kakuritsu
  大問2-2 連立方程式の利用（道のり・速さ）       c3_jitsu_r409_renritsu
  大問3 比例と反比例（y＝12/x と直線）           c3_jitsu_r409_hirei
  大問4 平面図形（二等辺三角形・合同・長さ）     c3_jitsu_r409_zukei
  大問5 空間図形（三角柱・四角錐）               c3_jitsu_r409_kuukan

実行：cd tools && python3 c3_jitsu_r409.py
"""
from fractions import Fraction as F
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from c3_jitsu_test import A, W, BX, Q, lines, OUT  # noqa: E402
from c3_jitsu2_test import build, _arc  # noqa: E402
from c3_jitsu3_test import T, L, right_mark  # noqa: E402

# ================= 答えの確認 =================
assert 7 - (-4) == 11 and F(-8) / F(4, 5) == -10 and F(2 * 8 * 135, 360) == 6
C1, C2 = [3, 6, 8, 6, 1, 1], [2, 9, 6, 5, 1, 2]          # ハンドボール投げ（10m から 5m ごと）
assert sum(C1) == sum(C2) == 25 and sum(C1[3:]) == sum(C2[3:]) == 8
assert C1.index(max(C1)) == 2 and C2.index(max(C2)) == 1              # 最頻値 22.5 > 17.5
N_BLACK = sum(1 for x in range(1, 7) for y in range(1, 7) if 7 - y > 1 + x)
assert F(N_BLACK, 36) == F(5, 18) and 8 - 3 + 4 == 9
assert 780 + 420 == 1200 and F(780, 60) + F(420, 140) == 16
assert 12 / -6 == -2 and 12 / 4 == 3 and F(3 - -2, 4 - -6) == F(1, 2)
assert (-6 + 6, -2 + -3) == (0, -5) and (4 + 6, 3 + -3) == (10, 0)    # AP＝BQ のベクトル (6, −3)
assert 180 - 2 * 2 * (90 - 64) == 76 and F(1, 2) * 10 + F(1, 2) * 12 == 11 and F(48, 11) * 11 == 48
assert F(1, 2) * 12 * 9 * 20 == 1080 and 2 * 54 + (12 + 9 + 15) * 20 == 828
assert F(1, 3) * 12 * F(20 + 8, 2) * 9 == 504 and 54 + 54 + 90 + 90 == 288

TAG = "令和4年度　3年・9月"


def header(title, page=None):
    p = f"（{page}）" if page else ""
    return (f'<div class="hd"><div class="ht"><span class="tag">{TAG}</span>{title}{p}<span class="key">解答</span></div>'
            '<div class="nm">　月　　日　名前（　　　　　　　　　）</div></div>')


def arc_at(c, r, p, w=10):
    ang = math.degrees(math.atan2(-(p[1] - c[1]), p[0] - c[0]))
    return _arc(c, r, ang + w, ang - w)


# ================= 図 =================
def tri_svg():
    """△ABC。作図（Aから辺BCへの垂線）は .cons＝こたえだけ"""
    B_, C_, A_ = (20, 130), (260, 130), (100, 22)
    s = f'<polygon points="{A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]}" fill="none" stroke="#000" stroke-width="1.3"/>'
    s += T(A_[0], A_[1] - 6, "A") + T(B_[0] - 8, B_[1] + 12, "B") + T(C_[0] + 8, C_[1] + 12, "C")
    r = 124
    dx = math.sqrt(r * r - (B_[1] - A_[1]) ** 2)
    M, N = (A_[0] - dx, B_[1]), (A_[0] + dx, B_[1])
    r2 = 80
    Qp = (A_[0], B_[1] + math.sqrt(r2 * r2 - dx * dx))
    c = arc_at(A_, r, M) + arc_at(A_, r, N) + arc_at(M, r2, Qp, 14) + arc_at(N, r2, Qp, 14)
    c += L(A_, (Qp[0], Qp[1] + 6), 1.3) + right_mark((A_[0], B_[1]), (1, 0), (0, -1), 7)
    c += f'<circle cx="{A_[0]}" cy="{B_[1]}" r="2.4" fill="#c00"/>' + T(A_[0] + 10, B_[1] + 13, "P")
    return f'<svg width="285" height="{int(Qp[1]) + 14}" viewBox="0 0 285 {int(Qp[1]) + 14}">{s}<g class="cons">{c}</g></svg>'


def boxes_svg():
    def box(x0, balls, lab):
        s = (f'<path d="M{x0 + 22} 6 H{x0} V72 H{x0 + 116} V6 H{x0 + 94}" fill="none" stroke="#000" stroke-width="1.2"/>' + T(x0 + 58, 88, lab, "sm"))
        for i, b in enumerate(balls):
            x = x0 + 12 + (i % 6) * 18.5
            y = 62 - (i // 6) * 16
            s += f'<circle cx="{x:.1f}" cy="{y}" r="8" fill="{"#555" if b else "#fff"}" stroke="#000" stroke-width="1"/>'
        return s
    return f'<svg width="270" height="94" viewBox="0 0 270 94">{box(4, [0] * 6 + [1, 1], "箱A")}{box(146, [1] * 6 + [0, 1], "箱B")}</svg>'


def road_svg():
    s = (L((14, 40), (250, 40)) + '<path d="M14 36 Q132 4 250 36" fill="none" stroke="#000" stroke-width="0.8" stroke-dasharray="3,2"/>'
         + "".join(f'<circle cx="{x}" cy="40" r="2.3"/>' for x in (14, 170, 250))
         + T(132, 14, "1200m", "sm") + T(14, 56, "家", "sm") + T(170, 56, "公園", "sm") + T(250, 56, "駅", "sm"))
    return f'<svg width="266" height="62" viewBox="0 0 266 62">{s}</svg>'


def hyp_svg(with_l=False):
    sc = 10
    ox, oy = 9 * sc + 12, 10 * sc + 14
    X = lambda x: ox + x * sc
    Y = lambda y: oy - y * sc
    s = L((X(-9), Y(0)), (X(12), Y(0)), 1) + L((X(0), Y(-9)), (X(0), Y(10.5)), 1)
    s += T(X(12) + 6, Y(0) + 4, '<tspan class="ax">x</tspan>', "pl") + T(X(0) - 8, Y(10.5) + 2, '<tspan class="ax">y</tspan>', "pl") + T(X(0) + 7, Y(0) + 12, "O", "sm")
    for xs in ([-9 + i * 0.05 for i in range(160)], [1.15 + i * 0.05 for i in range(218)]):
        pts = " ".join(f"{X(x):.1f},{Y(12 / x):.1f}" for x in xs if -9 <= 12 / x <= 10.5)
        s += f'<polyline points="{pts}" fill="none" stroke="#000" stroke-width="1.2"/>'
    s += T(X(1.3) + 10, Y(10) + 2, "①", "sm") + T(X(-1.3) - 2, Y(-9) + 10, "①", "sm")
    s += f'<circle cx="{X(-6)}" cy="{Y(-2)}" r="2"/><circle cx="{X(4)}" cy="{Y(3)}" r="2"/>'
    s += T(X(-6), Y(-2) + 14, "A") + T(X(4) + 4, Y(3) - 6, "B")
    c = ""
    if with_l:
        s += L((X(-9), Y(-3.5)), (X(12), Y(7)), 1.1) + T(X(12) + 4, Y(7), '<tspan class="ax">ℓ</tspan>', "pl", "start")
        P, Qp = (X(0), Y(-5)), (X(10), Y(0))
        c = L((X(-6), Y(-2)), P, 1.3) + L(P, Qp, 1.3) + L(Qp, (X(4), Y(3)), 1.3)
        c += T(P[0] + 10, P[1] + 4, "P", "pl", "start") + T(Qp[0], Qp[1] + 14, "Q")
    return f'<svg width="{X(12) + 20}" height="{Y(-9) + 14}" viewBox="0 0 {X(12) + 20} {Y(-9) + 14}">{s}<g class="cons">{c}</g></svg>'


def iso_svg():
    k = 18
    S = lambda p: (14 + p[0] * k, 14 + (8 - p[1]) * k)
    B_, C_, A_ = S((0, 0)), S((12, 0)), S((6, 8))
    D_ = S((6 + 6 * 10 / 22, 8 - 8 * 10 / 22))
    t = (6 + 6 * 10 / 22) * 0.6 + (8 - 8 * 10 / 22) * 0.8
    E_ = S((0.6 * t, 0.8 * t))
    F_ = S((6 + 6 * 10 / 22, 0))
    s = f'<polygon points="{A_[0]:.1f},{A_[1]:.1f} {B_[0]:.1f},{B_[1]:.1f} {C_[0]:.1f},{C_[1]:.1f}" fill="none" stroke="#000" stroke-width="1.2"/>'
    s += L(B_, D_) + L(D_, E_) + L(D_, F_)
    s += right_mark(F_, (-1, 0), (0, -1), 6) + right_mark(E_, (0.6, 0.8), (0.8, -0.6), 6)
    s += T(A_[0], A_[1] - 5, "A") + T(B_[0] - 6, B_[1] + 12, "B") + T(C_[0] + 6, C_[1] + 12, "C") + T(D_[0] + 9, D_[1] + 2, "D") + T(E_[0] - 9, E_[1] - 2, "E") + T(F_[0], F_[1] + 13, "F")
    return f'<svg width="{C_[0] + 18:.0f}" height="{B_[1] + 18:.0f}" viewBox="0 0 {C_[0] + 18:.0f} {B_[1] + 18:.0f}">{s}</svg>'


def prism_svg(fig2=False):
    sc = 0.5
    P = lambda x, y: ((x - 1100) * sc, (y - 180) * sc)
    A_, C_, B_ = P(1140, 210), P(1450, 255), P(1300, 345)
    D_, F_, E_ = P(1140, 565), P(1450, 610), P(1300, 715)
    s = L(A_, C_) + L(A_, B_) + L(B_, C_) + L(A_, D_) + L(C_, F_) + L(B_, E_) + L(D_, E_) + L(E_, F_) + L(D_, F_, 1, True)
    s += right_mark(B_, (-0.88, -0.48), (0.86, -0.51), 6)
    lab = [("A", A_, -9, 2), ("C", C_, 9, 2), ("B", B_, 6, 14), ("D", D_, -9, 4), ("F", F_, 9, 6), ("E", E_, 0, 14)]
    if fig2:
        Pp = (C_[0], C_[1] + (F_[1] - C_[1]) * 0.4)
        s += L(A_, E_) + L(E_, Pp) + L(A_, Pp, 1, True) + L(D_, Pp, 1, True)
        lab.append(("P", Pp, 9, 4))
    s += "".join(T(p[0] + dx, p[1] + dy, n) for n, p, dx, dy in lab)
    return f'<svg width="205" height="285" viewBox="-12 -2 205 285">{s}</svg>'


# ================= 大問1 =================
def d1():
    c = [Q("(1)", r"$7-(-4)$ を計算しなさい。", W(r"$7+4$"), A("11"), 1),
         Q("(2)", r"$(-8)\div\dfrac45$ を計算しなさい。", W(r"$(-8)\times\dfrac54$"), A("$-10$"), 1),
         Q("(3)", r"$2(3a-b)+3(a+2b)$ を計算しなさい。", W(r"$6a-2b+3a+6b$"), A(r"$9a+4b$"), 1),
         Q("(4)", r"$(\sqrt7+\sqrt3)(\sqrt7-\sqrt3)$ を計算しなさい。", W(r"$(\sqrt7)^2-(\sqrt3)^2=7-3$"), A("4"), 1),
         Q("(5)", r"$x^2-10x+25$ を因数分解しなさい。", W(r"$x^2-2\times5\times x+5^2$"), A(r"$(x-5)^2$"), 1),
         Q("(6)", r"半径が8cmで、中心角が $135^\circ$ のおうぎ形の弧の長さを求めなさい。ただし、円周率は $\pi$ とする。",
           W(r"$2\pi\times8\times\dfrac{135}{360}$"), A(r"$6\pi$ cm"), 1)]
    rows = "".join(f"<tr><td>{10 + 5 * i}〜{15 + 5 * i}</td><td>{a}</td><td>{b}</td></tr>" for i, (a, b) in enumerate(zip(C1, C2)))
    tbl = ('<table class="tb"><tr><th rowspan="2">階級(m)</th><th colspan="2">度数(人)</th></tr><tr><th>1組</th><th>2組</th></tr>'
           f'{rows}<tr><td>計</td><td>25</td><td>25</td></tr></table><div style="font-size:7.5pt;text-align:center">（以上〜未満）</div>')
    c7 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(7)</span>右の表は、2年1組と2組の生徒各25人のハンドボール投げの記録を度数分布表に整理したものである。'
          'この表からいえることとして、<b>正しいとは限らないもの</b>を、次のア〜エから1つ選び、記号で答えなさい。</div>'
          '<div class="ch">ア　最頻値は、1組の方が2組より大きい。<br>イ　最大値は、2組の方が1組より大きい。<br>'
          'ウ　記録が25m以上の生徒の割合は、どちらの組も同じである。<br>エ　中央値のふくまれる階級は、どちらの組も同じである。</div>'
          + W("ア：最頻値は1組22.5m、2組17.5m（正しい）。ウ：25m以上はどちらも8人（正しい）。<br>"
              "エ：13番目はどちらも20〜25mの階級（正しい）。イ：最大値はどちらも35〜40mの階級にあり、どちらが大きいかはわからない。")
          + f'</div><div class="fig">{tbl}</div></div><div class="al">答　{A("イ", "w20")}</div></div>')
    c8 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(8)</span>右の図のような△ABCがある。辺BC上にあって、$\\angle\\mathrm{BPA}=90^\\circ$ となる点Pを、'
          'コンパスと定規を使って作図しなさい。作図に用いた線は消さずに、濃くはっきりと残しておくこと。</div>'
          + W("Pは、Aから辺BCにひいた垂線と辺BCの交点。<br>①Aを中心とする円をかき、辺BCとの2つの交点をつくる。<br>"
              "②その2点を中心に同じ半径の円をかき、交点とAを結ぶ。③その直線と辺BCの交点がP。")
          + f'</div><div class="fig">{tri_svg()}</div></div></div>')
    return f"""<section class="page tight">{header("大問1　小問集合")}
<div class="lead">次の(1)〜(8)の問いに答えなさい。</div>
<div class="grid2">{"".join(c)}</div>
{c7}{c8}
</section>"""


# ================= 大問2-1 確率 =================
def d2a():
    sousa = ('<div class="frame"><b>【操作】</b><div class="rb">① さいころを続けて2回投げる。<br>'
             r'② 1回目に出た目の数を $x$ として、箱Aから箱Bへ $x$ 個の白玉を移す。<br>'
             r'③ ②の操作で玉が移った状態から、2回目に出た目の数を $y$ として、箱Bから箱Aへ $y$ 個の黒玉を移す。</div></div>')
    q1 = Q("(1)", "①で、1回目に出た目の数が3、2回目に出た目の数が4のとき、③の操作を終えた後の箱Aには、白玉と黒玉あわせて何個の玉がはいっているか、求めなさい。",
           W(r"白玉 $6-3=3$（個）、黒玉 $2+4=6$（個）　$3+6=9$"), A("9個", "w20"), 12)
    q2 = Q("(2)", r"$x+y=4$ のとき、③の操作を終えた後の箱Aの白玉と黒玉の個数について、どのようなことがいえるか、簡潔に説明しなさい。",
           lines(r"箱Aの白玉は $(6-x)$ 個、黒玉は $(2+y)$ 個。その差は $(6-x)-(2+y)=4-(x+y)=0$<br>"
                 r"よって、<b>白玉と黒玉の個数は等しくなる</b>。", 22), "", 0)
    q3 = Q("(3)", "③の操作を終えた後の箱Bについて、黒玉の個数が白玉の個数より多くなっている確率を求めなさい。ただし、さいころは、1から6までのどの目が出ることも同様に確からしいとする。",
           W(r"箱Bの白玉は $(1+x)$ 個、黒玉は $(7-y)$ 個。$7-y>1+x$ より $x+y<6$（$x+y\leqq5$）<br>"
             r"$x+y=2$：1通り、3：2通り、4：3通り、5：4通りで 計10通り。全部で $6\times6=36$ 通り　$\dfrac{10}{36}=\dfrac{5}{18}$"),
           A(r"$\dfrac{5}{18}$", "w20"), 24)
    return f"""<section class="page">{header("大問2-1　確率")}
<div class="flex"><div class="grow"><div class="lead">右の図のように、白玉が6個と黒玉が2個はいっている箱Aと、白玉が1個と黒玉が7個はいっている箱Bがある。この状態から、1から6までの目が出るさいころを使って、次の①〜③の手順で【操作】を行う。<br>このとき、下の(1)〜(3)の問いに答えなさい。</div></div>
<div class="fig">{boxes_svg()}</div></div>
{sousa}{q1}{q2}{q3}
</section>"""


# ================= 大問2-2 連立方程式 =================
def d2b():
    q1 = Q("(1)", r"家から公園までの道のりを $x$ m、公園から駅までの道のりを $y$ m として、家から駅まで行くのにかかった時間を、$x,\ y$ を用いて表しなさい。",
           W(r"（時間）＝（道のり）÷（速さ）　歩いた時間 $\dfrac{x}{60}$ 分、走った時間 $\dfrac{y}{140}$ 分"),
           A(r"$\left(\dfrac{x}{60}+\dfrac{y}{140}\right)$ 分", "w30"), 20)
    q2 = Q("(2)", r"家から公園までの道のりと、公園から駅までの道のりを、方程式を使ってそれぞれ求めなさい。ただし、家から公園までの道のりを $x$ m、公園から駅までの道のりを $y$ m とし、答えを求める過程がわかるように、式と計算も書きなさい。",
           W(r"$\begin{cases}x+y=1200\\[2pt]\dfrac{x}{60}+\dfrac{y}{140}=16\end{cases}$　下の式を420倍して $7x+3y=6720$<br>"
             r"上の式を3倍した $3x+3y=3600$ をひいて　$4x=3120$　$x=780$　$y=1200-780=420$<br>（780÷60＝13分、420÷140＝3分、13＋3＝16分 で問題に合う）"),
           "家から公園：" + A("780m", "w20") + "　公園から駅：" + A("420m", "w20"), 60)
    return f"""<section class="page">{header("大問2-2　連立方程式の利用")}
<div class="flex"><div class="grow"><div class="lead">家を出発して、1200m離れた駅へ行く。途中にある公園までは分速60mで歩き、公園から駅までは分速140mで走ったところ、家から駅まで行くのに16分かかった。<br>このとき、次の(1)、(2)の問いに答えなさい。</div></div>
<div class="fig">{road_svg()}</div></div>
{q1}{q2}
</section>"""


# ================= 大問3 比例と反比例 =================
def d3():
    p1 = Q("(1)", r'$x$ の値が3倍になると、対応する $y$ の値は <span class="ul">3倍</span> になる。', W(r"反比例なので、$x$ が3倍になると $y$ は $\dfrac13$ 倍"), A(r"$\dfrac13$ 倍", "w20"), 4)
    p2 = Q("(2)", r'対応する $x$ と $y$ の値の積 $xy$ は、つねに <span class="ul">6</span> である。', W(r"$y=\dfrac{12}{x}$ だから $xy=12$"), A("12", "w20"), 4)
    p3 = Q("(3)", '変化の割合は <span class="ul">一定でない</span>。', W("反比例の変化の割合は一定ではない（正しい）"), A("○", "w20"), 4)
    s1 = Q("(1)", r"直線 $\ell$ の傾きを求めなさい。", W(r"A$(-6,\ -2)$、B$(4,\ 3)$（$y=\dfrac{12}{x}$ に代入）　傾き $\dfrac{3-(-2)}{4-(-6)}=\dfrac{5}{10}$"), A(r"$\dfrac12$", "w20"), 14)
    s2 = Q("(2)", r"$y$ 軸上に点P、$x$ 軸上に点Qをとって、平行四辺形APQBをかいた。このとき、直線PQの式を求めなさい。ただし、点Pの $y$ 座標は負の数とする。",
           W(r"平行四辺形だから AからPへの移動 ＝ BからQへの移動。Pの $x$ 座標は0なので、右へ6。<br>"
             r"Qは B$(4,\ 3)$ から右へ6 → $x=10$。Qは $x$ 軸上なので下へ3 → Q$(10,\ 0)$。Pは A から右へ6・下へ3 → P$(0,\ -5)$<br>"
             r"PQ∥AB なので傾き $\dfrac12$、切片 $-5$"), A(r"$y=\dfrac12x-5$", "w30"), 24)
    return f"""<section class="page">{header("大問3　比例と反比例")}
<div class="flex"><div class="grow"><div class="lead">図Ⅰのように、関数 $y=\\dfrac{{12}}{{x}}$ …①のグラフ上に2点A、Bがあり、点Aの $x$ 座標は $-6$、点Bの $x$ 座標は4である。このとき、次の1、2の問いに答えなさい。</div>
<div class="q"><div class="qt"><span class="no">1</span>次の(1)〜(3)は、関数①の特徴について述べたものである。それぞれの文中の下線部が正しければ○を書き、誤っていれば、下線部の誤りをなおして正しくしなさい。</div></div>
{p1}{p2}{p3}</div><div class="fig"><b>図Ⅰ</b><br>{hyp_svg()}</div></div>
<div class="flex"><div class="grow"><div class="q"><div class="qt"><span class="no">2</span>図Ⅱは、図Ⅰにおいて、2点A、Bを通る直線を $\\ell$ としたものである。このとき、次の(1)、(2)の問いに答えなさい。</div></div>
{s1}{s2}</div><div class="fig"><b>図Ⅱ</b><br>{hyp_svg(True)}</div></div>
</section>"""


# ================= 大問4 平面図形 =================
def d4():
    q1 = Q("1", r"$\angle\mathrm{BDF}=64^\circ$ のとき、$\angle\mathrm{EAD}$ の大きさを求めなさい。",
           W(r"△BDFで $\angle\mathrm{DBF}=180^\circ-90^\circ-64^\circ=26^\circ$。BDは二等分線なので $\angle\mathrm{ABC}=52^\circ$<br>"
             r"AB＝AC より $\angle\mathrm{ACB}=52^\circ$　$\angle\mathrm{EAD}=\angle\mathrm{BAC}=180^\circ-52^\circ\times2=76^\circ$"), A(r"$76^\circ$", "w20"), 14)
    q2 = Q("2", "△DBEと△DBFが合同であることを証明しなさい。",
           lines(r"△DBEと△DBFで、<br>仮定より　$\angle\mathrm{DEB}=\angle\mathrm{DFB}=90^\circ$　……①<br>共通な辺だから　DB＝DB　……②<br>"
                 r"BDは $\angle\mathrm{ABC}$ の二等分線だから　$\angle\mathrm{DBE}=\angle\mathrm{DBF}$　……③<br>"
                 r"①、②、③より、直角三角形の斜辺と1つの鋭角がそれぞれ等しいから、△DBE≡△DBF", 40), "", 0)
    q3 = Q("3", "AB＝10cm、BC＝12cmで、△ABCの面積が48cm²のとき、線分DEの長さを求めなさい。",
           W(r"2より DE＝DF。DE＝$x$ cm とすると、△ABC＝△ABD＋△DBC だから<br>"
             r"$\dfrac12\times10\times x+\dfrac12\times12\times x=48$　$11x=48$　$x=\dfrac{48}{11}$"), A(r"$\dfrac{48}{11}$ cm", "w20"), 26)
    return f"""<section class="page">{header("大問4　平面図形（合同・長さ）")}
<div class="flex"><div class="grow"><div class="lead">右の図で、△ABCはAB＝ACの二等辺三角形、点Dは∠ABCの二等分線と辺ACとの交点である。また、点E、Fは、それぞれ点Dから辺AB、BCにひいた垂線と辺AB、BCとの交点である。<br>このとき、次の1〜3の問いに答えなさい。</div></div>
<div class="fig">{iso_svg()}</div></div>
{q1}{q2}{q3}
</section>"""


# ================= 大問5 空間図形 =================
def d5():
    q1 = Q("1", "三角柱ABCDEFの体積を求めなさい。", W(r"底面 $\dfrac12\times12\times9=54$、高さ20　$54\times20$"), A("1080cm³", "w20"), 10)
    q2 = Q("2", "三角柱ABCDEFの表面積を求めなさい。", W(r"底面2つ $54\times2=108$、側面 $(12+9+15)\times20=720$　$108+720$"), A("828cm²", "w20"), 10)
    t1 = Q("(1)", "線分CPの長さを求めなさい。",
           W(r"四角錐の底面は台形BEPC（BE＝20、CP、高さBC＝9）。高さはAB＝12（ABは面BCFEに垂直）<br>"
             r"CP＝$x$ とすると　$\dfrac13\times\dfrac{(20+x)\times9}{2}\times12=504$　$18(20+x)=504$　$x=8$"), A("8cm", "w20"), 16)
    t2 = Q("(2)", "三角錐PDEFの表面積を求めなさい。",
           W(r"PF＝$20-8=12$。△DEF＝54、△PEF＝$\dfrac12\times9\times12=54$、△PDF＝$\dfrac12\times15\times12=90$<br>"
             r"DEは面BCFEに垂直なので $\angle\mathrm{DEP}=90^\circ$。PE＝15（3辺9・12・15の直角三角形）で △PDE＝$\dfrac12\times12\times15=90$<br>"
             r"$54+54+90+90=288$"), A("288cm²", "w20"), 22)
    return f"""<section class="page">{header("大問5　空間図形")}
<div class="flex"><div class="grow"><div class="lead">図Ⅰのような、底面が $\\angle\\mathrm{{ABC}}=\\angle\\mathrm{{DEF}}=90^\\circ$ の直角三角形である三角柱ABCDEFがあり、AB＝12cm、BC＝9cm、AC＝15cm、AD＝20cmである。このとき、次の1〜3の問いに答えなさい。</div>
{q1}{q2}</div><div class="fig"><b>図Ⅰ</b><br>{prism_svg()}</div></div>
<div class="flex"><div class="grow"><div class="q"><div class="qt"><span class="no">3</span>図Ⅱは、図Ⅰの三角柱の辺CF上に点Pをとったもので、四角錐ABEPCの体積は504cm³である。このとき、次の(1)、(2)の問いに答えなさい。</div></div>
{t1}{t2}</div><div class="fig"><b>図Ⅱ</b><br>{prism_svg(True)}</div></div>
</section>"""


JOBS = [("c3_jitsu_r409_d1", d1), ("c3_jitsu_r409_kakuritsu", d2a), ("c3_jitsu_r409_renritsu", d2b),
        ("c3_jitsu_r409_hirei", d3), ("c3_jitsu_r409_zukei", d4), ("c3_jitsu_r409_kuukan", d5)]

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
