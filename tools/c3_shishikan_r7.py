"""尚志館高等学校 入学試験問題（令和7年度 本試験）数学を、大問ごとの PDF にする。
問題（pdf/c3_shishikan_r7_*.pdf）と、問題に赤字で答え・解説を書き込んだ「解答・解説」（_ans.pdf）を同じレイアウトで出す。
サイトでは「尚志館入試過去問」のタブ（common.json の nyushi[] の id＝shishikan）。test の id は shi-r7。

  大問1  計算                          c3_shishikan_r7_d1      → 小問集合（大問1・大問2）
  大問2  小問集合（8問）                c3_shishikan_r7_d2      → 小問集合（大問1・大問2）
  大問3  関数（直線と放物線・回転体）    c3_shishikan_r7_kansu   → 関数 y＝ax²
  大問4  正方形と直角二等辺三角形      c3_shishikan_r7_zukei   → 平面図形
  大問5  四角すい                      c3_shishikan_r7_kuukan  → 空間図形
         ※問題文に高さ（または辺OAの長さ）の条件がなく、(2)〜(4)は数値が決まらない。
           先生に確認中のため、こたえは (1) と考え方だけ。条件がわかったら KUUKAN_H を入れて作り直す。

実行：cd tools && python3 c3_shishikan_r7.py
"""
from fractions import Fraction as F
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from c3_jitsu_test import A, W, BX, Q, lines, OUT  # noqa: E402
from c3_jitsu2_test import build, _arc  # noqa: E402
from c3_jitsu3_test import T, L, right_mark  # noqa: E402
from c3_shishikan_r8 import header as _header, svg, dot  # noqa: E402

KUUKAN_H = None          # 大問5 の四角すいの高さ（cm）。条件がわかったら入れる

# ================= 答えの確認 =================
assert 45 ** 2 - 7 * 127 == 1136 and F(1, 4) - F(1, 12) == F(1, 6)
for a in range(1, 4):
    for b in range(1, 4):
        assert F(3 * a + b, 2) - F(a + 2 * b, 4) == F(5 * a, 4)
        assert F((2 * a * b * b) ** 2, -a ** 3 * b) / (F(1, 2) * a * b ** 3) == F(-8, a * a)
assert 9 - 2 + 3 == 10                                          # 9√3−2√3＋3√3
assert all((x - 1) * (x + 3) - (x + 1) ** 2 == -4 for x in range(-3, 4))
xs5 = math.sqrt(5) - 2
assert abs(xs5 ** 2 + 4 * xs5 + 4 - 5) < 1e-9
assert 2 * 1 * 3 - (-1) * (-1) == 5 and 1 * 3 - 4 * (-1) * (-1) == -1   # a＝1、b＝−1
assert F(3 * -4, F(1, 2)) == -24
sq = {1, 4, 9, 16, 25, 36}
assert F(sum(a * b in sq for a in range(1, 7) for b in range(1, 7)), 36) == F(2, 9)
gold = [40, 40, 20, 18, 16, 15, 14, 13, 12, 12]
silver = sorted([44, 27, 12, 19, 26, 7, 22, 9, 13, 13])
assert sum(gold) / 10 == 20 and silver[7] - silver[2] == 14
assert 180 - 90 + 42 - 80 == 52                                 # ∠ECB＝90−42、∠ABC＝180−80−48
assert 7 ** 2 == 9 + 11 + 29
assert 200 * F(30 - 12, 12) == 300
s3 = math.sqrt(3)
Ap, Bp = (-1, s3), (2, 2 * s3)
assert abs(abs(Ap[0] * Bp[1] - Bp[0] * Ap[1]) / 2 - 2 * s3) < 1e-9
assert abs(-Ap[0] * (Bp[0] - Ap[0]) - Ap[1] * (Bp[1] - Ap[1])) < 1e-9    # ∠OAB＝90°
assert abs(math.dist(Ap, Bp) - 2 * s3) < 1e-9 and abs(math.dist((0, 0), Bp) - 4) < 1e-9
assert abs(F(1, 3) * 12 * 2 - 8) == 0                           # 体積 8π


def sq_fig():
    B_, C_, A_ = (0.0, 0.0), (5.0, 0.0), (0.9, 3.9)
    def outward(p, q, other):
        d = (q[0] - p[0], q[1] - p[1])
        n = (-d[1], d[0])
        c = ((other[0] - p[0]) * n[0] + (other[1] - p[1]) * n[1])
        return (n[0], n[1]) if c < 0 else (-n[0], -n[1])
    n1 = outward(A_, B_, C_)
    D_, E_ = (A_[0] + n1[0], A_[1] + n1[1]), (B_[0] + n1[0], B_[1] + n1[1])
    n2 = outward(A_, C_, B_)
    G_, F_ = (A_[0] + n2[0], A_[1] + n2[1]), (C_[0] + n2[0], C_[1] + n2[1])
    mid = lambda p, q: ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    return dict(A=A_, B=B_, C=C_, D=D_, E=E_, F=F_, G=G_, P=mid(D_, B_), Q=mid(C_, G_), M=mid(B_, C_))


Z = sq_fig()
vPM = (Z["P"][0] - Z["M"][0], Z["P"][1] - Z["M"][1])
vQM = (Z["Q"][0] - Z["M"][0], Z["Q"][1] - Z["M"][1])
assert abs(vPM[0] * vQM[0] + vPM[1] * vQM[1]) < 1e-9 and abs(math.hypot(*vPM) - math.hypot(*vQM)) < 1e-9
assert abs(math.dist(Z["D"], Z["C"]) - math.dist(Z["B"], Z["G"])) < 1e-9

TAG = "尚志館　令和7年度　本試験"


def header(title, page=None):
    return _header(title, page).replace("令和8年度", "令和7年度")


def ch(*ws):
    return '<div class="ch" style="border:1px solid #444;display:inline-block;padding:0.6mm 4mm;margin:0.6mm 0 0.6mm 2mm">' + "　".join(ws) + "</div>"


def dl(who, t):
    return f'<p class="dl"><b>{who}</b>「{t}」</p>'


# ================= 図 =================
def circ_svg():
    k = 64
    O_ = (80, 76)
    P = lambda deg: (O_[0] + k * math.cos(math.radians(deg)), O_[1] - k * math.sin(math.radians(deg)))
    A_, B_, C_, D_ = P(180), P(0), P(76), P(264)
    t = (O_[1] - C_[1]) / (D_[1] - C_[1])
    E_ = (C_[0] + (D_[0] - C_[0]) * t, O_[1])
    s = f'<circle cx="{O_[0]}" cy="{O_[1]}" r="{k}" fill="none" stroke="#000" stroke-width="1"/>'
    s += L(A_, B_) + L(A_, C_) + L(A_, D_) + L(C_, D_) + dot(O_, 1.8)
    s += T(A_[0] - 8, A_[1] + 4, "A") + T(B_[0] + 8, B_[1] + 4, "B") + T(C_[0] + 4, C_[1] - 4, "C") + T(D_[0], D_[1] + 13, "D") + T(O_[0], O_[1] + 13, "O")
    s += T(C_[0] - 6, C_[1] + 26, "42°", "sm") + T(E_[0] + 14, E_[1] - 6, "80°", "sm") + T(D_[0] - 8, D_[1] - 18, '<tspan class="ax">x</tspan>°', "sm")
    c = L(C_, B_, 0.9, True, "#c00")
    return svg(170, 160, s + f'<g class="cons">{c}</g>', 0, -2)


def graph_svg():
    k = 30
    ox, oy = 20 + 4.3 * k, 14 + 4.2 * k
    X = lambda x: ox + x * k
    Y = lambda y: oy - y * k
    s = L((X(-4.3), Y(0)), (X(2.8), Y(0)), 1) + L((X(0), Y(-1.2)), (X(0), Y(4.3)), 1)
    s += T(X(2.8) + 7, Y(0) + 4, '<tspan class="ax">x</tspan>', "pl") + T(X(0) + 3, Y(4.3) + 2, '<tspan class="ax">y</tspan>', "pl", "start") + T(X(0) + 7, Y(0) + 13, "O", "sm")
    s += L((X(0), Y(0)), (X(-2.45), Y(2.45 * s3)), 1.2)
    xs = [i / 40 for i in range(0, 95)]
    s += '<polyline points="' + " ".join(f"{X(x):.1f},{Y(s3 / 2 * x * x):.1f}" for x in xs if s3 / 2 * x * x <= 4.2) + '" fill="none" stroke="#000" stroke-width="1.2"/>'
    s += L((X(-1), Y(s3)), (X(-1), Y(0)), 0.7, True) + L((X(2), Y(2 * s3)), (X(2), Y(0)), 0.7, True)
    s += dot((X(-1), Y(s3))) + dot((X(2), Y(2 * s3))) + T(X(-1) - 8, Y(s3) - 4, "A") + T(X(2) + 9, Y(2 * s3) - 2, "B")
    s += T(X(-1), Y(0) + 13, "−1", "sm") + T(X(2), Y(0) + 13, "2", "sm")
    c = f'<polygon points="{X(0)},{Y(0)} {X(-1)},{Y(s3)} {X(2)},{Y(2 * s3)}" fill="rgba(204,0,0,0.12)" stroke="#c00" stroke-width="1.1"/>'
    a_, o_, b_ = (X(-1), Y(s3)), (X(0), Y(0)), (X(2), Y(2 * s3))
    un = lambda p, q: ((q[0] - p[0]) / math.dist(p, q), (q[1] - p[1]) / math.dist(p, q))
    c += right_mark(a_, un(a_, o_), un(a_, b_), 7)
    c += L((X(-1), Y(s3)), (X(-4), Y(0)), 0.9, True, "#c00") + dot((X(-4), Y(0)), 2, "#c00") + T(X(-4), Y(0) + 13, "B′", "sm")
    return svg(X(2.8) + 18, Y(-1.2) + 4, s + f'<g class="cons">{c}</g>')


def squares_svg():
    k = 30
    xs = [p[0] for p in Z.values()]
    ys = [p[1] for p in Z.values()]
    x0, y1 = min(xs), max(ys)
    P = lambda p: (16 + (p[0] - x0) * k, 14 + (y1 - p[1]) * k)
    z = {n: P(p) for n, p in Z.items()}
    s = "".join(L(z[a], z[b], 1.1) for a, b in ["AB", "BC", "CA", "AD", "DE", "EB", "AG", "GF", "FC", "PM", "QM", "PQ"])
    s += L((z["B"][0] - 18, z["B"][1]), (z["C"][0] + 20, z["C"][1]), 0.8)
    off = {"A": (-4, -6), "B": (0, 14), "C": (4, 14), "D": (-6, -5), "E": (-9, 5), "F": (9, 3), "G": (0, -5), "P": (-9, 3), "Q": (9, 0), "M": (0, 14)}
    s += "".join(T(z[n][0] + dx, z[n][1] + dy, n, "sm") for n, (dx, dy) in off.items())
    c = L(z["D"], z["C"], 0.9, True, "#c00") + L(z["B"], z["G"], 0.9, True, "#c00")
    W_ = max(q[0] for q in z.values()) + 24
    H_ = max(q[1] for q in z.values()) + 20
    return svg(W_, H_, s + f'<g class="cons">{c}</g>')


def pyr_svg():
    O_, A_, B_, C_, D_ = (100, 12), (14, 150), (150, 182), (232, 112), (100, 84)
    s = L(O_, A_) + L(O_, B_) + L(O_, C_) + L(A_, B_) + L(B_, C_) + L(O_, D_, 0.8, True) + L(A_, D_, 0.8, True) + L(D_, C_, 0.8, True)
    s += T(O_[0], O_[1] - 4, "O") + T(A_[0] - 8, A_[1] + 4, "A") + T(B_[0] + 2, B_[1] + 13, "B") + T(C_[0] + 9, C_[1] + 4, "C") + T(D_[0] + 2, D_[1] - 6, "D")
    return svg(250, 196, s, 0, -4)


# ================= 大問1 =================
def d1():
    c = [Q("(1)", r"$45^2-7\times127$", W(r"$2025-889$"), A("1136"), 10),
         Q("(2)", r"$\dfrac14-\dfrac1{12}$", W(r"$\dfrac3{12}-\dfrac1{12}=\dfrac2{12}$"), A(r"$\dfrac16$"), 10),
         Q("(3)", r"$\dfrac{3a+b}2-\dfrac{a+2b}4$", W(r"$\dfrac{2(3a+b)-(a+2b)}{4}=\dfrac{6a+2b-a-2b}{4}$"), A(r"$\dfrac{5a}{4}$"), 10),
         Q("(4)", r"$(2ab^2)^2\div(-a^3b)\div\dfrac12ab^3$",
           W(r"$4a^2b^4\times\left(-\dfrac1{a^3b}\right)\times\dfrac2{ab^3}=-\dfrac{8a^2b^4}{a^4b^4}$<br>（わる数は逆数にしてかける）"), A(r"$-\dfrac{8}{a^2}$"), 10),
         Q("(5)", r"$\sqrt{243}-2\sqrt3+\dfrac9{\sqrt3}$", W(r"$\sqrt{243}=9\sqrt3$、$\dfrac9{\sqrt3}=\dfrac{9\sqrt3}3=3\sqrt3$<br>$9\sqrt3-2\sqrt3+3\sqrt3$"), A(r"$10\sqrt3$"), 10),
         Q("(6)", r"$(x-1)(x+3)-(x+1)^2$", W(r"$(x^2+2x-3)-(x^2+2x+1)$<br>$=-3-1$"), A("$-4$"), 10)]
    return f"""<section class="page">{header("大問1　計算")}
<div class="lead">次の(1)〜(6)の計算をしなさい。</div>
<div class="grid2">{"".join(c)}</div>
</section>"""


# ================= 大問2 =================
def d2():
    q = [Q("(1)", r"$x=\sqrt5-2$ のとき、$x^2+4x+4$ の値を求めなさい。",
           W(r"$x^2+4x+4=(x+2)^2$、$x+2=\sqrt5$ なので $(\sqrt5)^2$"), A("5"), 8),
         Q("(2)", r"$x$ と $y$ についての連立方程式 $\begin{cases}2ax-by=5\\ax-4by=-1\end{cases}$ の解が $\begin{cases}x=3\\y=-1\end{cases}$ であるとき、定数 $a$、$b$ の値を求めなさい。",
           W(r"解を代入すると $\begin{cases}6a+b=5\\3a+4b=-1\end{cases}$　上の式を4倍してひく：$24a-3a=20+1$　$21a=21$　$a=1$、$b=5-6=-1$"),
           A(r"$a=1,\ b=-1$"), 12),
         Q("(3)", r"$y$ は $x$ に反比例し、$x=3$ のとき $y=-4$ である。$y=\dfrac12$ のとき $x$ の値を求めなさい。",
           W(r"$xy=3\times(-4)=-12$　$x=-12\div\dfrac12$"), A(r"$x=-24$"), 8),
         Q("(4)", r"大小2つのさいころを同時に投げ、大きいさいころの出た目の数を $a$、小さいさいころの出た目の数を $b$ とする。$n=a\times b$ とするとき、$\sqrt n$ の値が整数になる確率を求めなさい。",
           W(r"$ab$ が平方数（1、4、9、16、25、36）になればよい。全部で36通り<br>"
             r"1：(1,1)　4：(1,4)(4,1)(2,2)　9：(3,3)　16：(4,4)　25：(5,5)　36：(6,6) の8通り　$\dfrac8{36}$"),
           A(r"$\dfrac29$"), 12)]
    names = ["アメリカ", "中国", "日本", "オースト<br>ラリア", "フランス", "オランダ", "イギリス", "韓国", "イタリア", "ドイツ"]
    gs = [40, 40, 20, 18, 16, 15, 14, 13, 12, 12]
    ss = [44, 27, 12, 19, 26, 7, 22, 9, 13, 13]
    tb = ('<table class="tb" style="font-size:7.8pt;margin:1mm 0;white-space:nowrap"><tr><th>国名</th>' + "".join(f"<td>{n}</td>" for n in names) + "</tr>"
          + '<tr><th>金メダル</th>' + "".join(f"<td>{v}</td>" for v in gs) + "</tr><tr><th>銀メダル</th>" + "".join(f"<td>{v}</td>" for v in ss) + "</tr></table>")
    q2 = [Q("(5)", "以下の表は、2024年のパリ五輪で金メダルを多く獲得した上位10ヶ国のメダルの個数である。" + tb
            + "①　金メダルの個数について、10ヶ国の平均値を求めなさい。<br>②　銀メダルの個数について、四分位範囲を求めなさい。",
            W(r"①　合計は $40+40+20+18+16+15+14+13+12+12=200$　$200\div10=20$<br>"
              r"②　小さい順に 7、9、12、13、13 ｜ 19、22、26、27、44。第1四分位数は前半5個の中央値12、第3四分位数は後半5個の中央値26　$26-12$"),
            "①" + A("20個", "w20") + "　②" + A("14個", "w20"), 10),
          '<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(6)</span>右図で、線分ABは円Oの直径であり、2点C、Dは円O上の点である。このとき <span class="ax">x</span> の値を求めなさい。</div>'
          + W(r"CBを結ぶ。ABは直径なので ∠ACB＝90°、∠DCB＝90°−42°＝48°<br>"
              r"CDとABの交点をEとすると、△CEBで ∠CBE＝180°−80°−48°＝52°<br>"
              r"∠ADC と ∠ABC は弧ACに対する円周角なので等しい")
          + f'<div class="al">答　{A(r"$x=52$")}</div></div><div class="fig">{circ_svg()}</div></div></div>',
          Q("(7)", "連続する3つの正の奇数がある。最も小さい奇数の2乗が、残りの2つの奇数の和より29大きいとき、この連続する3つの奇数を求めなさい。",
            W(r"最も小さい奇数を $n$ とすると、3つは $n$、$n+2$、$n+4$<br>"
              r"$n^2=(n+2)+(n+4)+29$　$n^2-2n-35=0$　$(n-7)(n+5)=0$　$n$ は正なので $n=7$"),
            A("7、9、11"), 10),
          Q("(8)", "箱の中に大量の白球が入っている。この箱に、白球と同じ大きさの赤球を200個入れる。よく混ぜた後、この箱から30個の球を取り出すと、12個の赤球が含まれていた。箱の中に入っていた白球の個数は何個であったと推定できるか答えなさい。",
            W(r"取り出した球は 白18個：赤12個＝3：2。箱の中でも同じ比と考えて、白球を $x$ 個とすると　$x:200=3:2$　$2x=600$"),
            A("およそ300個"), 10)]
    return f"""<section class="page">{header("大問2　小問集合", "1")}
<div class="lead">次の(1)〜(8)の各問いに答えなさい。</div>
{"".join(q)}
</section>
<section class="page">{header("大問2　小問集合", "2")}
{"".join(q2)}
</section>"""


# ================= 大問3 =================
def d3():
    q = [Q("(1)", r"$a$、$b$ の値を求めなさい。",
           W(r"$a=-\sqrt3\times(-1)=\sqrt3$　$b=\dfrac{\sqrt3}2\times2^2=2\sqrt3$"), A(r"$a=\sqrt3,\ b=2\sqrt3$", "w30"), 6),
         Q("(2)", "△OABの面積を求めなさい。",
           W(r"A$(-1,\ \sqrt3)$、B$(2,\ 2\sqrt3)$。直線ABの式は傾き $\dfrac{2\sqrt3-\sqrt3}{2-(-1)}=\dfrac{\sqrt3}3$、切片 $\sqrt3+\dfrac{\sqrt3}3=\dfrac{4\sqrt3}3$<br>"
             r"$y$ 軸で2つに分けて　$\dfrac12\times\dfrac{4\sqrt3}3\times\{2-(-1)\}=2\sqrt3$"), A(r"$2\sqrt3$", "w20"), 10),
         Q("(3)", "点Aから直線OBに垂線AHを下ろす。AHの長さを求めなさい。",
           W(r"OB＝$\sqrt{2^2+(2\sqrt3)^2}=\sqrt{16}=4$。△OAB＝$\dfrac12\times\mathrm{OB}\times\mathrm{AH}$ なので　$2\sqrt3=\dfrac12\times4\times\mathrm{AH}$"),
           A(r"$\sqrt3$", "w20"), 8),
         Q("(4)", r"△OABを直線 $y=-\sqrt3x$ のまわりに1回転させてできる立体の体積を求めなさい。",
           W(r"OA＝$\sqrt{1+3}=2$、AB＝$\sqrt{3^2+(\sqrt3)^2}=2\sqrt3$、OB＝4 で $\mathrm{OA}^2+\mathrm{AB}^2=4+12=16=\mathrm{OB}^2$ → ∠OAB＝90°（三平方の定理の逆）<br>"
             r"回転の軸は直線OAなので、できる立体は 底面の半径AB＝$2\sqrt3$、高さOA＝2 の円すい<br>"
             r"$\dfrac13\times\pi\times(2\sqrt3)^2\times2=\dfrac13\times12\pi\times2$"),
           A(r"$8\pi$", "w20"), 14)]
    return f"""<section class="page">{header("大問3　関数")}
<div class="flex"><div class="grow"><div class="lead">右のグラフは、直線 $y=-\\sqrt3x$ の $x\\lt0$ の部分と、放物線 $y=\\dfrac{{\\sqrt3}}2x^2$ の $x\\geqq0$ の部分を表している。<br>
直線 $y=-\\sqrt3x$ の $x\\lt0$ の部分に点A$(-1,\\ a)$、放物線 $y=\\dfrac{{\\sqrt3}}2x^2$ の $x\\geqq0$ の部分に点B$(2,\\ b)$ をとる。次の(1)〜(4)の各問いに答えなさい。</div>{q[0]}</div>
<div class="fig">{graph_svg()}</div></div>
{q[1]}{q[2]}{q[3]}
</section>"""


# ================= 大問4 =================
def d4():
    talk = ('<div style="line-height:1.9;font-size:9.5pt">'
            + dl("志郎", "PM＝QMを直接示すのは難しそうだね。")
            + dl("尚子", "そうね。PはDBの中点で、MはBCの中点だから。")
            + dl("志郎", "そうか！ということは " + BX("ア", "中点連結の定理") + " から、PMとDCは " + BX("イ", "平行") + " でPMの長さはDCの " + BX("ウ", r"$\dfrac12$") + " 倍ということになるのか。")
            + dl("尚子", "ということは、同様に考えると、QMも…")
            + dl("志郎", "わかった！△ADCと△" + BX("エ", "ABG") + " が合同であることを示せばいいということか。")
            + dl("尚子", "これで、いえたのはPM＝QMだから、あと∠PMQ＝90°を示さなければならないのね。")
            + dl("志郎", "そうだね。△ADC≡△" + BX("エ", "ABG") + " ということは…")
            + dl("尚子", "△ADCと△" + BX("エ", "ABG") + " は重なるということよね。")
            + dl("志郎", "だったら、Aのまわりに…") + dl("尚子", "できたわね。") + "</div>")
    q1 = Q("(1)", "ア 〜 エ に入るものを、ア はⅠ、イ はⅡ、エ はⅢから選びなさい。また、ウ には正しい数値を入れなさい。<br>"
           + "Ⅰ" + ch("ピタゴラスの定理", "平行線の定理", "中点連結の定理", "三角形の定理") + "<br>Ⅱ" + ch("垂直", "平行", "同位", "一致") + "<br>Ⅲ" + ch("ABG", "AEC", "ABF", "ADG"),
           W(r"△BDCで、PはDBの中点、MはBCの中点なので、中点連結の定理より PM∥DC、PM＝$\dfrac12$DC<br>"
             r"同じように△CGBで QM∥GB、QM＝$\dfrac12$GB。だから DC＝GB（△ADC≡△ABG）がいえれば PM＝QM"),
           "ア" + A("中点連結の定理", "w30") + "　イ" + A("平行", "w20") + "　ウ" + A(r"$\dfrac12$", "w20") + "　エ" + A("ABG", "w20"), 4)
    q2 = Q("(2)", "△ADC≡△ エ であることを証明しなさい。",
           lines(r"△ADCと△ABGで、<br>四角形ADEBは正方形なので　AD＝AB……①<br>四角形ACFGは正方形なので　AC＝AG……②<br>"
                 r"∠DAC＝∠DAB＋∠BAC＝90°＋∠BAC、∠BAG＝∠BAC＋∠CAG＝∠BAC＋90° なので　∠DAC＝∠BAG……③<br>"
                 r"①、②、③より、2組の辺とその間の角がそれぞれ等しいから　△ADC≡△ABG", 32), "", 0)
    q3 = Q("(3)", "∠PMQ＝90°であることを説明しなさい。",
           lines(r"△ABGは、△ADCを点Aのまわりに90°回転させたもの（D→B、C→G）なので、DC⊥BG になる。<br>"
                 r"（くわしく：DCとAB、BGの交点をそれぞれY、Xとすると、合同より ∠ADY＝∠XBY、対頂角で ∠AYD＝∠XYB なので ∠BXY＝∠DAY＝90°）<br>"
                 r"(1)より PM∥DC、QM∥BG なので　PM⊥QM　つまり ∠PMQ＝90°<br>"
                 r"また PM＝$\dfrac12$DC＝$\dfrac12$BG＝QM なので、△MQPは∠PMQ＝90°の直角二等辺三角形である。", 32), "", 0)
    return f"""<section class="page">{header("大問4　平面図形", "1")}
<div class="lead">△ABCの辺AB、辺AC上に正方形を図のようにつくる。正方形ADEBの中心（対角線の交点）をP、正方形ACFGの中心をQとする。また、辺BCの中点をMとすると、△MQPは∠PMQ＝90°である直角二等辺三角形となることを示しなさい。<br>この問題を考えている志郎君と尚子さんの会話を読んで、(1)〜(3)の各問いに答えなさい。</div>
{talk}
<div style="text-align:center">{squares_svg()}</div>
</section>
<section class="page">{header("大問4　平面図形", "2")}
{q1}{q2}{q3}
</section>"""


# ================= 大問5 =================
def d5():
    note = "<b>※</b>問題文には高さ（または辺OAの長さ）の条件が書かれていないため、(2)〜(4)の数値は決まりません（先生に確認中）。下は考え方です。"
    if KUUKAN_H is None:
        h_txt = "高さを $h$ cm とすると"
    else:
        h_txt = f"高さ {KUUKAN_H} cm より"
    q = [Q("(1)", "辺ABとねじれの位置にある辺を、次の（ア）〜（キ）からすべて選んで答えなさい。"
           '<div class="ch">（ア）OA　（イ）OB　（ウ）OC　（エ）OD　（オ）BC　（カ）CD　（キ）DA</div>',
           W("OA・OB・BC・DAはABと交わる。CDはABと平行。残りのOC・ODは、ABと交わらず平行でもない"), A("（ウ）、（エ）", "w30"), 4),
         Q("(2)", "辺OAの長さを求めなさい。",
           W(f"<span style='color:#c00'>{note}</span><br>" + r"底面の対角線 AC＝$6\sqrt2$、中心をHとすると AH＝$3\sqrt2$。" + h_txt + r"　OA＝$\sqrt{(3\sqrt2)^2+h^2}=\sqrt{18+h^2}$"),
           A("（条件を確認中）", "w30"), 10),
         Q("(3)", "辺OA、OB、OC、ODの中点をそれぞれ点P、Q、R、Sとする。四角すいO−ABCDを4点P、Q、R、Sを通る平面で分けたときにできる2つの立体のうち、点Oを含まない立体の体積を求めなさい。",
           W(r"四角すいO−PQRSは、もとの四角すいの $\dfrac12$ の縮図なので、体積は $\left(\dfrac12\right)^3=\dfrac18$<br>"
             r"点Oを含まない立体は　もとの体積 $\times\dfrac78$。もとの体積は $\dfrac13\times36\times h=12h$ なので $12h\times\dfrac78=\dfrac{21}{2}h$"),
           A("（条件を確認中）", "w30"), 12),
         Q("(4)", "辺OC上に、OT：TC＝1：2を満たす点をTとする。点T、A、Bを通るように、この立体を切断したとき、切断面の面積を求めなさい。",
           W(r"AB∥DC なので、切り口はODとも交わる。その点をUとすると TU∥CD、OU：UD＝1：2 で TU＝$6\times\dfrac13=2$<br>"
             r"切り口は AB＝6、TU＝2 の等脚台形ABTU。高さは、ABの中点と TUの中点を結ぶ線分の長さ（$h$ によって決まる）<br>"
             r"面積＝$\dfrac12\times(6+2)\times$（台形の高さ）"),
           A("（条件を確認中）", "w30"), 12)]
    return f"""<section class="page">{header("大問5　空間図形")}
<div class="flex"><div class="grow"><div class="lead">1辺の長さ6cmの正方形ABCDを底面とし、OA＝OB＝OC＝ODである四角すいO−ABCDについて、次の(1)〜(4)の各問いに答えなさい。</div>{q[0]}</div>
<div class="fig">{pyr_svg()}</div></div>
{q[1]}{q[2]}{q[3]}
</section>"""


JOBS = [("c3_shishikan_r7_d1", d1), ("c3_shishikan_r7_d2", d2), ("c3_shishikan_r7_kansu", d3),
        ("c3_shishikan_r7_zukei", d4), ("c3_shishikan_r7_kuukan", d5)]

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
