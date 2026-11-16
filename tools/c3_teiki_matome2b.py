"""中3 定期テスト対策「学習のまとめ(2)」の類題②（2ページ＝A3 2枚）＋こたえ（問題に赤で書き込んだ形）

  cd tools && python3 c3_teiki_matome2b.py

- c3_teiki_matome2.py（類題①）と同じ並び・同じ形で、数字・図・証明の形を変えたもの。部品は類題①から借りる。
  1ページ目：［1］〜［6］／2ページ目：［7］〜［10］
- 出力：pdf/c3_teiki_matome2b.pdf と c3_teiki_matome2b_ans.pdf
"""
import math
from fractions import Fraction as F

import sympy as sp

from c3_souji_nagasa import tri
from c3_teiki_matome2 import (A, CSS, S, SIM, X_, Y_, Fig2, ln, on, parabola_fig, q, st, sub, table,
                              tri_angles)
from texlib import doc, tex as T, write_pdfs

FILE = "c3_teiki_matome2b"


def head(page, ans):
    kai = "<span class=kai>【解答】</span>" if ans else ""
    return (f"<div class=head><b>中3数学 定期テスト対策　学習のまとめ(2) 類題②（{page}/2）{kai}</b>"
            f"<span class=cl>（　）組（　）番　名前 <span class=u></span></span></div>")


# ---------- 図 ----------
def fig8():
    f1 = tri_angles(65, 70, 12, "ABC", 2.6)
    f1.side("A", "B", "12", None).side("B", "C", "x", None)
    f1.angle("B", "A", "C").angle("A", "C", "B")
    f1.text("A", -0.4, 7.2, "65°", 3).text("C", -6, -1.5, "70°", 3)
    f2 = tri_angles(65, 70, 8, "DEF", 2.6)
    f2.side("D", "E", "8", None).side("E", "F", "10", None)
    f2.angle("D", "F", "E")
    f2.text("F", -6, -1.5, "70°", 3)
    return f1.svg() + f2.svg()


def fig9():
    t = tri(10, 12, 11)
    A_, B_, C_ = t["A"], t["B"], t["C"]
    f = Fig2({"A": A_, "B": B_, "C": C_, "D": on(A_, B_, .45), "E": on(A_, C_, .45)}, 2.6, pad=6)
    f.poly("ABC").line("D", "E").par("D", "E").par("B", "C").label(D=(-3.4, -.6), E=(3.4, -.6))
    return f.svg()


def fig10_1():
    t = tri(9, 13, 12)
    A_, B_, C_ = t["A"], t["B"], t["C"]
    f = Fig2({"A": A_, "B": B_, "C": C_, "D": on(A_, B_, 6 / 9), "E": on(A_, C_, 6 / 9)}, 2.4)
    f.poly("ABC").line("D", "E").par("D", "E").par("B", "C").label(D=(-3.4, -.6), E=(3.4, -.6))
    f.label(D=(-3.4, -2)).side("A", "D", 6, 6).side("D", "B", 3, 3, at=(-6, 1.2)).side("A", "E", 8, 8).side("E", "C", "x", 4, at=(4.2, -.5))
    return f.svg()


def fig10_2():
    # A＝交点、上に B（左）・C（右）、下に E（左）・D（右）。AC＝6，BC＝8，AE＝9，ED＝12
    t = tri(6, 8, 7, "OCB")
    ox, oy = t["O"]
    c = (ox - t["C"][0], oy - t["C"][1])
    b = (ox - t["B"][0], oy - t["B"][1])
    k = 1.5
    pts = {"A": (0, 0), "C": c, "B": b, "E": (-c[0] * k, -c[1] * k), "D": (-b[0] * k, -b[1] * k)}
    f = Fig2(pts, 2.4).line("B", "C").line("E", "D").line("B", "D").line("C", "E").par("B", "C").par("E", "D")
    f.label(A=(4.2, .8))
    f.side("B", "C", 8, 8).side("E", "D", 12, 12).side("A", "C", 6, 6, at=(3.2, 2.2)).side("A", "E", "x", 9, at=(-3.6, -2.2))
    return f.svg()


def fig10_3():
    sa, sb = .9, .6                              # 左の線：4 と 6，右の線：6 と x（9）
    ca, cb = math.sqrt(1 - sa * sa), math.sqrt(1 - sb * sb)
    p = {"l0": (-1.5, 9), "l1": (19.5, 9), "m0": (-1.5, 5.4), "m1": (19.5, 5.4), "n0": (-1.5, 0), "n1": (19.5, 0)}
    p["a1"] = (1, 9)
    p["a2"] = (1 + ca * 4, 5.4)
    p["a3"] = (p["a2"][0] + ca * 6, 0)
    p["a0"] = (1 - ca * 1.3, 9 + sa * 1.3)
    p["a4"] = (p["a3"][0] + ca * 1.3, -sa * 1.3)
    p["b1"] = (6.5, 9)
    p["b2"] = (6.5 + cb * 6, 5.4)
    p["b3"] = (p["b2"][0] + cb * 9, 0)
    p["b0"] = (6.5 - cb * 1.3, 9 + sb * 1.3)
    p["b4"] = (p["b3"][0] + cb * 1.3, -sb * 1.3)
    f = Fig2(p, 1.85, hide=p.keys(), pad=4)
    f.line("l0", "l1").line("m0", "m1").line("n0", "n1").line("a0", "a4").line("b0", "b4")
    f.side("a1", "a2", 4, 4, at=(-4.8, 0)).side("a2", "a3", 6, 6, at=(-4.8, 0))
    f.side("b1", "b2", 6, 6, at=(5, -.5)).side("b2", "b3", "x", 9, at=(5.5, -.5))
    it = 'font-family="KaTeX_Math" font-style="italic"'
    for nm, lab in (("l0", "ℓ"), ("m0", "m"), ("n0", "n")):
        f.text(nm, -2.5, .2, lab, 3.6, it)
    return f.svg()


# ---------- チェック ----------
def check():
    x, a = sp.symbols("x a")
    assert sp.solve(9 - 3 * a + 15, a) == [8] and set(sp.solve(x**2 - 8 * x + 15, x)) == {3, 5}
    assert set(sp.solve(x**2 - 4 * x - 21, x)) == {-3, 7}
    assert set(sp.solve(x * (x - 5) - 84, x)) == {12, -7} and 12 - 7 == 5 and 12 * 7 == 84
    assert F(10, 4) == F(5, 2) and F(5, 2) * 16 == 40
    # ［5］ y＝3x²，y＝−½x²
    assert (0, 3 * 4) == (0, 12) and (3 * 1, 3 * 9) == (3, 27)
    h = lambda v: F(-1, 2) * v * v
    assert (h(4) - h(2)) / (4 - 2) == -3 and (h(2) - h(-6)) / (2 - (-6)) == 2
    assert (h(2), h(4), h(-6)) == (-2, -8, -18)
    # ［7］ y＝x²，A(−1,1)，B(2,4)
    m = F(1 - 4, 1 - (-2))
    n = 1 - m * 1
    assert (m, n) == (-1, 2) and F(1, 2) * n * (2 + 1) == 3
    # ［8］
    assert F(12, 8) == F(3, 2) and 10 * F(3, 2) == 15 and 180 - 65 - 70 == 45
    # ［10］
    assert F(8 * 3, 6) == 4 and F(6 * 12, 8) == 9 and F(6 * 6, 4) == 9
    print("確認OK")


# ---------- ページ ----------
def page1(ans):
    q1 = q(1, f"二次方程式 {T('x^2-ax+15=0')} の解の1つが3であるとき，{T('a')} の値を求めなさい。また，もう1つの解を求めなさい。",
           "<div class=wk>" + st(f"{T('x=3')} を代入すると", T("9-3a+15=0"), T("-3a=-24") + "　" + T("a=8"),
                                  T("x^2-8x+15=0"), T("(x-3)(x-5)=0") + "　" + T("x=3,\\ 5")) + "</div>"
           + f"<div class=lns>{ln(T('8'), 26, T('a') + '＝')}{ln(T('x=5'), 38, 'もう1つの解 ')}</div>", "1.15 1 0")
    q2 = q(2, f"ある数 {X_} を，2乗しなければならないところを，まちがえて4倍したため，計算の結果は21だけ小さくなりました。この数 {X_} を求めなさい。",
           "<div class=wk>" + st("（式）" + T("x^2-4x=21"), T("x^2-4x-21=0"), T("(x+3)(x-7)=0"),
                                  T("x=-3,\\ 7") + "　（どちらも問題に合っている）") + "</div>"
           + ln("−3，7", 40, f"ある数 {X_} は "), "1 1 0")
    q3 = q(3, "大小2つの自然数があります。その差は5で，積は84です。この2つの数を求めなさい。",
           "<div class=wk>" + st(f"大きい方を {X_}，小さい方を {T('x-5')} とおくと", "（式）" + T("x(x-5)=84"), T("x^2-5x-84=0"),
                                  T("(x+7)(x-12)=0") + "　" + T("x=-7,\\ 12"), f"{T('x>0')} より {T('x=12')}（これがないとダメ）") + "</div>"
           + ln("12，7", 32), "1.15 1 0")
    q4 = q(4, f"{Y_} は {X_} の2乗に比例し，{T('x=-2')} のとき {T('y=10')} です。",
           sub(1, f"{Y_} を {X_} の式で表しなさい。") + "<div class=wk>" + st(T("y=ax^2") + " に代入　" + T("10=4a") + "　" + T("a=\\dfrac{5}{2}")) + "</div>"
           + ln(T("y=\\dfrac{5}{2}x^2"), 36)
           + sub(2, f"{T('x=4')} のときの {Y_} の値を求めなさい。") + "<div class=wk>" + st(T("y=\\dfrac{5}{2}\\times4^2=\\dfrac{5}{2}\\times16")) + "</div>"
           + ln(T("y=40"), 36), "1.25 1 0")
    q5 = q(5, "次の各問いに答えなさい。",
           sub(1, f"関数 {T('y=3x^2')} について，{X_} の変域が次のとき，{Y_} の変域を求めなさい。")
           + sub("", f"① {T('-2\\leqq x\\leqq 1')}") + "<div class=wk>" + st(f"{T('x=0')} をふくむので，最小は {T('y=0')}", f"0 から遠い {T('x=-2')} のとき 最大 {T('y=12')}") + "</div>"
           + ln(T("0\\leqq y\\leqq 12"), 42)
           + sub("", f"② {T('1\\leqq x\\leqq 3')}") + "<div class=wk>" + st(f"{T('x=1')} のとき {T('y=3')}，{T('x=3')} のとき {T('y=27')}") + "</div>"
           + ln(T("3\\leqq y\\leqq 27"), 42)
           + sub(2, f"{T('y=-\\dfrac{1}{2}x^2')} について，{X_} の値が次のように増加するときの変化の割合を求めなさい。")
           + sub("", "① 2から4まで") + table((2, 4), (-2, -8), ans) + "<div class=wk>" + st(T("\\dfrac{-8-(-2)}{4-2}=\\dfrac{-6}{2}")) + "</div>"
           + ln(T("-3"), 30)
           + sub("", "② −6から2まで") + table((-6, 2), (-18, -2), ans) + "<div class=wk>" + st(T("\\dfrac{-2-(-18)}{2-(-6)}=\\dfrac{16}{8}")) + "</div>"
           + ln(T("2"), 30), "3 1 0")
    q6 = q(6, "三角形の相似条件を3つ書きなさい。",
           "<div class=cond>" + "".join(ln(t, 80, "○ ") for t in
                                        ("3組の辺の比が，すべて等しい。", "2組の辺の比とその間の角が，それぞれ等しい。", "2組の角が，それぞれ等しい。")) + "</div>",
           "0 0 auto")
    return (f"<div class='page{'' if ans else ' hide'}'>{head(1, ans)}<div class=cols>"
            f"<div class=col>{q1}{q2}{q3}{q4}</div><div class=col>{q5}{q6}</div></div></div>")


def page2(ans):
    q7 = q(7, f"右の図のように，関数 {T('y=x^2')} のグラフ上に，2点 {S('A')}，{S('B')} があります。"
              f"{S('A')}，{S('B')} の {X_} 座標が，それぞれ {T('-2')}，1 であるとき，",
           f"<div class=row><div style='flex:1'>{sub(1, f'2点 {S(chr(65))}，{S(chr(66))} の座標を求めなさい。')}"
           + "<div class=wk>" + st(T("y=(-2)^2=4"), T("y=1^2=1")) + "</div>"
           + f"</div>{parabola_fig(F(1), -2, 1, ans)}</div>"
           + f"<div class=lns>{ln(T('\\mathrm{A}(-2,\\ 4)'), 30)}{ln(T('\\mathrm{B}(1,\\ 1)'), 30)}</div>"
           + sub(2, f"2点 {S('A')}，{S('B')} を通る直線の式を求めなさい。")
           + "<div class=wk>" + st(T("y=ax+b") + "　" + T("a=\\dfrac{1-4}{1-(-2)}=\\dfrac{-3}{3}=-1"),
                                    T("y=-x+b") + " に B(1, 1) を代入", T("1=-1+b") + "　" + T("b=2")) + "</div>"
           + ln(T("y=-x+2"), 40)
           + sub(3, f"{T('\\triangle\\mathrm{AOB}')} の面積を求めなさい。")
           + "<div class=wk>" + st("直線と " + Y_ + " 軸の交点 (0, 2) で左右に分ける",
                                    "左側…" + T("2\\times2\\times\\dfrac{1}{2}=2") + "　右側…" + T("2\\times1\\times\\dfrac{1}{2}=1"),
                                    T("2+1=3")) + "</div>"
           + ln(T("3"), 30), "1.35 1 0")
    q8 = q(8, f"下の図で，{SIM('ABC', 'DEF')} のとき，次の各問いに答えなさい。（単位は cm）",
           f"<div class=row style='justify-content:space-around;align-items:flex-end;margin-top:1mm'>{fig8()}</div>"
           + sub(1, f"{T('\\triangle\\mathrm{ABC}')} と {T('\\triangle\\mathrm{DEF}')} の相似比をいいなさい。")
           + "<div class=wk>" + st(T("\\mathrm{AB}:\\mathrm{DE}=12:8=3:2")) + "</div>" + ln("3：2", 32)
           + sub(2, f"{S('BC')} の長さを求めなさい。")
           + "<div class=wk>" + st(f"{T('\\mathrm{BC}=x')} cm とすると", T("x:10=3:2"), T("2x=30") + "　" + T("x=15")) + "</div>"
           + ln(T("\\mathrm{BC}=15") + "（cm）", 40)
           + sub(3, f"{T('\\angle\\mathrm{C}')}，{T('\\angle\\mathrm{E}')} の大きさをそれぞれ求めなさい。")
           + "<div class=wk>" + st(T("\\angle\\mathrm{C}=\\angle\\mathrm{F}") + "，" + T("\\angle\\mathrm{E}=\\angle\\mathrm{B}=180^\\circ-65^\\circ-70^\\circ")) + "</div>"
           + f"<div class=lns>{ln(T('\\angle\\mathrm{C}=70^\\circ'), 30)}{ln(T('\\angle\\mathrm{E}=45^\\circ'), 30)}</div>", "1.25 1 0")
    proof = st(f"{T('\\triangle\\mathrm{ADE}')} と {T('\\triangle\\mathrm{ABC}')} において",
               f"{T('\\mathrm{DE}')} ∥ {T('\\mathrm{BC}')} より",
               "　" + T("\\angle\\mathrm{ADE}=\\angle\\mathrm{ABC}") + "（同位角）……①",
               "　" + T("\\angle\\mathrm{AED}=\\angle\\mathrm{ACB}") + "（同位角）……②",
               "①，②より",
               "　2組の角がそれぞれ等しいので",
               "　　" + SIM("ADE", "ABC"),
               "（②のかわりに " + T("\\angle\\mathrm{DAE}=\\angle\\mathrm{BAC}") + "（共通）を使ってもよい）")
    q9 = (f"<div class=q style='flex:1 1 0'><div class=row><div class=qt><span class=box>9</span><div>右の図で，"
          f"{S('D')}，{S('E')} はそれぞれ辺 {S('AB')}，{S('AC')} 上の点で，{S('DE')} ∥ {S('BC')} です。"
          f"{SIM('ADE', 'ABC')} であることを証明しなさい。</div></div>{fig9()}</div>"
          f"<div class=pf>{proof}</div></div>")
    q10 = q(10, f"下の図で，{S('DE')} ∥ {S('BC')} のとき，{X_} の値を求めなさい。（(3)は ℓ ∥ m ∥ n，単位は cm）",
            sub(1, "") + f"<div class=row><div class=wk>{st(T('\\mathrm{AD}:\\mathrm{DB}=\\mathrm{AE}:\\mathrm{EC}'), T('6:3=8:x'), T('6x=24'))}</div>{fig10_1()}</div>"
            + ln(T("x=4"), 30)
            + sub(2, f"（{S('BC')} ∥ {S('ED')}）") + f"<div class=row><div class=wk>{st(SIM('ABC', 'ADE'), T('\\mathrm{BC}:\\mathrm{DE}=8:12=2:3'), T('6:x=2:3'), T('2x=18'))}</div>{fig10_2()}</div>"
            + ln(T("x=9"), 30)
            + sub(3, "") + f"<div class=row><div class=wk>{st(T('4:6=6:x'), T('4x=36'))}</div>{fig10_3()}</div>"
            + ln(T("x=9"), 30), "0 0 auto")
    return (f"<div class='page{'' if ans else ' hide'}'>{head(2, ans)}<div class=cols>"
            f"<div class=col>{q7}{q8}</div><div class=col>{q9}{q10}</div></div></div>")


if __name__ == "__main__":
    check()
    write_pdfs([
        (doc(CSS, page1(False) + page2(False)), f"{FILE}.pdf"),
        (doc(CSS, page1(True) + page2(True)), f"{FILE}_ans.pdf"),
    ])
