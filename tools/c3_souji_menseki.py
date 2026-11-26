"""中3 相似比と面積比（4ページ）＋こたえ（問題に赤で書き込んだ形）

  cd tools && python3 c3_souji_menseki.py

- 1回で1つのことをじっくり（先生の希望・11/26）。体積比は別の回にする。
  その1＝相似比→面積比・面積比→相似比・面積を求める（比だけ）
  その2＝相似な図形の面積（図つき・円・正方形・面積比から長さ）
  その3＝図形の中の面積比（DE∥BC・ちょうちょ形・中点）
  その4＝練習・利用（☆＝チャレンジ）
- 1つの HTML から、赤字（.a）を消した問題と、赤字を出したこたえを作る。式は KaTeX。
- 出力：pdf/c3_souji_menseki_A.pdf と c3_souji_menseki_A_ans.pdf
"""
from fractions import Fraction as F
from math import gcd

from c3_souji_nagasa import tri
from c3_teiki_matome2 import Fig2, on
from texlib import doc, tex as T, write_pdfs

FILE = "c3_souji_menseki_A"
X_ = T("x")


def S(name):
    return T(r"\mathrm{%s}" % name)


def SIM(a, b):
    return T(r"\triangle\mathrm{%s}\backsim\triangle\mathrm{%s}" % (a, b))


def TR(a):
    return T(r"\triangle\mathrm{%s}" % a)


def A(s):
    return f"<span class=a>{s}</span>"


def st(*lines):
    return "".join(f"<span class=st>{A(l)}</span>" for l in lines)


def ln(body="", w=34, label="", unit=""):
    return f"<div class=ln style='width:{w}mm'>{label}{A(body)}{unit}</div>"


def ratio(a, b):
    return f"{a}：{b}"


def simp(a, b):
    g = gcd(a, b)
    return a // g, b // g


# ---------- 図 ----------
def fig_pair(ab, bc, ca, k, show1, show2, s1, flip=False):
    """相似な2つの三角形（ABC と DEF）。show＝{(p, q): 文字}"""
    f1 = Fig2(tri(ab, bc, ca, "ABC"), s1, pad=6).poly("ABC")
    t2 = tri(ab * k, bc * k, ca * k, "DEF")
    if flip:
        t2 = {n: (-x, y) for n, (x, y) in t2.items()}
    f2 = Fig2(t2, s1, pad=6).poly("DEF")
    for f, show in ((f1, show1), (f2, show2)):
        for (p, q), lab in show.items():
            f.side(p, q, lab, None)
    return f1, f2


def fig_par(ab, bc, ca, r, s, labels, mid=False):
    t = tri(ab, bc, ca)
    A_, B_, C_ = t["A"], t["B"], t["C"]
    f = Fig2({"A": A_, "B": B_, "C": C_, "D": on(A_, B_, r), "E": on(A_, C_, r)}, s, pad=9)
    f.poly("ABC").line("D", "E").label(D=(-3.4, -.8), E=(3.4, -.8))
    if not mid:
        f.par("D", "E").par("B", "C")
    for a, b, text, val, kw in labels:
        f.side(a, b, text, val, **kw)
    return f


def fig_bf(s):
    # O を中心に、上 B（左）・A（右）、下 D（左）・C（右）。OA＝4，OD＝6（A と D、B と C が O をはさむ）
    t = tri(4, 6, 5, "OAB")                     # OA＝4，AB＝6，BO＝5
    ox, oy = t["O"]
    a = (ox - t["A"][0], oy - t["A"][1])
    b = (ox - t["B"][0], oy - t["B"][1])
    k = 1.5
    pts = {"O": (0, 0), "A": a, "B": b, "D": (-a[0] * k, -a[1] * k), "C": (-b[0] * k, -b[1] * k)}
    f = Fig2(pts, s, pad=6).line("A", "B").line("D", "C").line("A", "D").line("B", "C").par("A", "B").par("D", "C")
    f.label(O=(4.2, .8)).side("O", "A", 4, 4, at=(3.2, 2.4)).side("O", "D", 6, 6, at=(-4, -2))
    return f


def fig_trap(s):
    # 台形 ABCD（AD∥BC，AD＝4，BC＝8）。対角線の交点 O
    pts = {"A": (2, 5), "D": (6, 5), "B": (0, 0), "C": (8, 0)}
    (ax, ay), (cx, cy) = pts["A"], pts["C"]
    pts["O"] = (ax + (cx - ax) / 3, ay + (cy - ay) / 3)    # AO：OC＝1：2
    f = Fig2(pts, 3.3, pad=6).poly("ABCD").line("A", "C").line("B", "D").par("A", "D").par("B", "C")
    f.label(O=(0, 4), A=(-1.5, -2.6), D=(1.5, -2.6)).side("A", "D", 4, 4).side("B", "C", 8, 8)
    return f


# ---------- チェック ----------
def check():
    for a, b in ((1, 2), (2, 5), (3, 4), (4, 3), (5, 6), (1, 3), (6, 9), (10, 4)):
        m, n = simp(a, b)
        assert (m * m, n * n) == P1_ANS[(a, b)]
    for (a, b), (m, n) in P1_REV.items():
        assert (m * m, n * n) == (a, b)
    for (m, n, known, big), ans in P1_AREA.items():
        assert (F(known) * n * n / (m * m) if not big else F(known) * m * m / (n * n)) == ans
    # その2
    assert F(8) * 9 / 4 == 18 and F(50) * 9 / 25 == 18 and F(6) * 5 / 3 == 10 and F(9) * 4 / 3 == 12
    # その3
    assert F(8) * 9 / 4 == 18 and 18 - 8 == 10
    assert F(50) * 9 / 25 == 18 and 50 - 18 == 32
    assert F(12) * 9 / 4 == 27 and F(48) / 4 == 12 and 48 - 12 == 36
    # その4
    assert F(27) * 16 / 9 == 48 and F(15) * 4 / 5 == 12 and 3 * 3 == 9 and 9 - 3 == 6
    assert F(6) * 4 == 24 and 6 * 2 == 12 and F(48) * 9 / 4 == 108 and 6 * 8 == 48
    print("確認OK")


P1_ANS = {(1, 2): (1, 4), (2, 5): (4, 25), (3, 4): (9, 16), (4, 3): (16, 9), (5, 6): (25, 36),
          (1, 3): (1, 9), (6, 9): (4, 9), (10, 4): (25, 4)}
P1_REV = {(9, 16): (3, 4), (1, 25): (1, 5), (4, 49): (2, 7), (36, 25): (6, 5)}
# (相似比 m:n, わかっている面積, わかっているのが大きい方か) → 答え
P1_AREA = {(2, 3, 12, False): 27, (3, 5, 75, True): 27, (1, 2, 8, False): 32, (5, 2, 50, False): 8}


# ---------- ページ ----------
CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans CJK JP', sans-serif; color: #111; font-size: 10.3pt; }
.page { width: 210mm; height: 297mm; padding: 10mm 13mm 9mm; page-break-after: always; display: flex; flex-direction: column; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.katex { font-size: 1.1em; }
.a, .a .katex { color: #c8102e; }
.hide .a { visibility: hidden; }
.head { display: flex; align-items: baseline; white-space: nowrap; border-bottom: 1.2pt solid #111; padding-bottom: 1.5mm; flex: none; }
.head b { font-size: 14pt; }
.head .sub { margin-left: 3mm; font-size: 10.5pt; }
.head .kai { color: #c8102e; font-weight: 700; margin-left: 2mm; }
.head .nm { margin-left: auto; font-size: 9.5pt; }
.head .u { display: inline-block; border-bottom: .7pt solid #111; width: 42mm; }
.tip { flex: none; margin-top: 2.5mm; border: .8pt solid #666; border-radius: 1.5mm; padding: 2mm 3.5mm; font-size: 10pt; line-height: 1.75; background: #f5f5f5; }
.tip b { color: #111; }
.big { flex: none; font-weight: 700; margin-top: 3mm; display: flex; align-items: center; gap: 1.8mm; line-height: 1.5; }
.big .box { flex: none; display: inline-flex; width: 5.4mm; height: 5.4mm; border: .9pt solid #111; align-items: center; justify-content: center; }
.grid { display: grid; column-gap: 4mm; margin-top: 1.5mm; flex: none; }
.c4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.c2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.cell { display: flex; flex-direction: column; min-height: 0; }
.cell .tx { display: flex; line-height: 1.65; }
.no { flex: none; width: 7mm; font-size: 9pt; padding-top: .5mm; }
.wk { flex: 1 0 auto; padding-left: 7mm; }
.st { display: block; font-size: 9.6pt; line-height: 1.55; }
.ln { border-bottom: .9pt solid #111; margin-left: auto; height: 7mm; flex: none; display: flex; align-items: flex-end; justify-content: center;
      padding-bottom: .5mm; white-space: nowrap; }
.lns { display: flex; justify-content: flex-end; gap: 3mm; flex: none; }
.lns .ln { margin-left: 0; }
.fill { flex: 1; min-height: 0; }
.row { display: flex; justify-content: space-between; align-items: flex-start; gap: 2mm; }
.figs { display: flex; justify-content: center; gap: 6mm; align-items: flex-end; margin: 1mm 0; }
.fig { flex: none; }
.fig text { fill: #111; }
.small { font-size: 8.5pt; }
"""


def head(no, title, ans):
    kai = "<span class=kai>【解答】</span>" if ans else ""
    return (f"<div class=head><b>中3数学 相似比と面積比 その{no}</b><span class=sub>{title}</span>{kai}"
            f"<span class=nm>名前 <span class=u></span></span></div>")


def big(n, text):
    return f"<div class=big><span class=box>{n}</span><span>{text}</span></div>"


def cell(no, text, body, style=""):
    num = f"({no})" if no != "" else ""
    return f"<div class=cell style='{style}'><div class=tx><span class=no>{num}</span><div>{text}</div></div>{body}</div>"


def page1(ans):
    c1 = ""
    for i, (a, b) in enumerate(P1_ANS):
        m, n = simp(a, b)
        pre = "" if (m, n) == (a, b) else st(f"{ratio(a, b)}＝{ratio(m, n)}")
        c1 += cell(i + 1, f"相似比 {ratio(a, b)}", f"<div class=wk>{pre}</div>" + ln(ratio(*P1_ANS[(a, b)]), 28, "面積比 "), "min-height:15mm")
    c2 = ""
    for i, ((a, b), (m, n)) in enumerate(P1_REV.items()):
        c2 += cell(i + 1, f"面積比 {ratio(a, b)}",
                   f"<div class=wk>{st(f'{a}＝{m}²，{b}＝{n}²')}</div>" + ln(ratio(m, n), 28, "相似比 "), "min-height:15mm")
    c3 = ""
    texts = [("相似比が 2：3 の2つの図形があります。小さい方の面積が 12cm² のとき，大きい方の面積を求めなさい。",
              ["面積比は 4：9", T("4:9=12:x"), T("4x=108"), T("x=27")], "27cm²"),
             ("相似比が 3：5 の2つの図形があります。大きい方の面積が 75cm² のとき，小さい方の面積を求めなさい。",
              ["面積比は 9：25", T("9:25=x:75"), T("25x=675"), T("x=27")], "27cm²"),
             ("相似比が 1：2 の2つの図形があります。小さい方の面積が 8cm² のとき，大きい方の面積を求めなさい。",
              ["面積比は 1：4", T("1:4=8:x"), T("x=32")], "32cm²"),
             (f"図形 P と図形 Q は相似で，相似比は 5：2 です。P の面積が 50cm² のとき，Q の面積を求めなさい。",
              ["面積比は 25：4", T("25:4=50:x"), T("25x=200"), T("x=8")], "8cm²")]
    for i, (t, w, r) in enumerate(texts):
        c3 += cell(i + 1, t, f"<div class=wk>{st(*w)}</div>" + ln(r, 30), "min-height:46mm")
    return f"""<div class="page{'' if ans else ' hide'}">{head(1, "相似比から面積比へ", ans)}
<div class=tip>相似な図形では，<b>相似比が {T('m:n')} のとき，面積比は {T('m^2:n^2')}</b>（相似比を2乗する）。<br>
例：相似比 2：3 → 面積比 {T('2^2:3^2=4:9')}　　<span class=small>※相似比は先にいちばん簡単な比にしてから2乗すると楽。</span></div>
{big(1, "次の相似比の2つの図形の，面積比を求めなさい。")}<div class="grid c4" style="row-gap:1mm">{c1}</div>
{big(2, "次の面積比の2つの図形の，相似比を求めなさい。（何を2乗した数かを考える）")}<div class="grid c4">{c2}</div>
{big(3, "次の問いに答えなさい。（面積比を出してから，比例式で求める）")}<div class="grid c2 fill" style="row-gap:2mm;grid-template-rows:1fr 1fr">{c3}</div>
</div>"""


def page2(ans):
    f1, f2 = fig_pair(4, 5, 3, F(3, 2), {("A", "B"): "4"}, {("D", "E"): "6"}, 4.0)
    g1, g2 = fig_pair(10, 10, 6, F(3, 5), {("B", "C"): "10"}, {("E", "F"): "6"}, 2.7, flip=True)
    q1 = cell(1, f"{SIM('ABC', 'DEF')}，{TR('ABC')} の面積は 8cm²",
              f"<div class=figs>{f1.svg()}{f2.svg()}</div><div class=wk>{st('相似比 AB：DE＝4：6＝2：3', '面積比 4：9', T('4:9=8:x') + '　' + T('x=18'))}</div>"
              f"<div class=lns>{ln('2：3', 22, '相似比 ')}{ln('4：9', 22, '面積比 ')}{ln('18cm²', 30, TR('DEF') + '＝')}</div>")
    q2 = cell(2, f"{SIM('ABC', 'DEF')}，{TR('ABC')} の面積は 50cm²",
              f"<div class=figs>{g1.svg()}{g2.svg()}</div><div class=wk>{st('相似比 BC：EF＝10：6＝5：3', '面積比 25：9', T('25:9=50:x') + '　' + T('x=18'))}</div>"
              f"<div class=lns>{ln('5：3', 22, '相似比 ')}{ln('25：9', 22, '面積比 ')}{ln('18cm²', 30, TR('DEF') + '＝')}</div>")
    r1 = cell(1, "1辺 3cm の正方形と，1辺 5cm の正方形の面積比",
              f"<div class=wk>{st('どんな正方形どうしも相似', '相似比 3：5 → 面積比 9：25')}</div>" + ln("9：25", 30))
    r2 = cell(2, "半径 2cm の円と，半径 6cm の円の面積比",
              f"<div class=wk>{st('どんな円どうしも相似', '相似比 2：6＝1：3 → 面積比 1：9')}</div>" + ln("1：9", 30))
    s1 = cell(1, f"{SIM('ABC', 'DEF')} で，面積比が 9：25，{T(r'\mathrm{AB}=6')}cm のとき，{S('DE')} の長さ",
              f"<div class=wk>{st('9＝3²，25＝5² → 相似比 3：5', T('6:x=3:5') + '　' + T('3x=30') + '　' + T('x=10'))}</div>" + ln("10cm", 30))
    s2 = cell(2, f"{SIM('ABC', 'DEF')} で，面積比が 16：9，{T(r'\mathrm{EF}=9')}cm のとき，{S('BC')} の長さ",
              f"<div class=wk>{st('16＝4²，9＝3² → 相似比 4：3', T('x:9=4:3') + '　' + T('3x=36') + '　' + T('x=12'))}</div>" + ln("12cm", 30))
    return f"""<div class="page{'' if ans else ' hide'}">{head(2, "図で考える", ans)}
<div class=tip>手順：① 対応する辺から<b>相似比</b>　→　② 2乗して<b>面積比</b>　→　③ 比例式で<b>面積</b>。<br>
逆に，面積比から長さを求めるときは　面積比 → （何の2乗か）→ 相似比 → 長さ。</div>
{big(1, "次の図で，相似比・面積比・△DEF の面積を求めなさい。（長さの単位は cm）")}
<div class="grid c2" style="flex:1 0 auto">{q1}{q2}</div>
{big(2, "次の面積比を求めなさい。")}<div class="grid c2" style="flex:1 0 auto">{r1}{r2}</div>
{big(3, "面積比から長さを求めなさい。")}<div class="grid c2" style="flex:1 0 auto">{s1}{s2}</div>
</div>"""


def page3(ans):
    fa = fig_par(6, 9, 8, 4 / 6, 3.2, [("A", "D", 4, 4, {}), ("D", "B", 2, 2, dict(at=(-7, .2)))])
    fb = fig_par(5, 8, 7, 3 / 5, 3.0, [("A", "D", 3, 3, {}), ("D", "B", 2, 2, dict(at=(-7, .2)))])
    fc = fig_bf(3.0)
    fd = fig_par(8, 10, 9, .5, 2.6, [], mid=True)
    qa = (f"<div class=row><div style='flex:1'>"
          + cell(1, f"{TR('ADE')} と {TR('ABC')} の相似比", f"<div class=wk>{st(SIM('ADE', 'ABC'), 'AD：AB＝4：6＝2：3')}</div>" + ln("2：3", 26))
          + cell(2, f"{TR('ADE')} と {TR('ABC')} の面積比", "<div class=wk></div>" + ln("4：9", 26))
          + cell(3, f"{TR('ADE')} の面積が 8cm² のとき，{TR('ABC')} の面積", f"<div class=wk>{st(T('4:9=8:x') + '　' + T('x=18'))}</div>" + ln("18cm²", 26))
          + cell(4, f"台形 {S('DBCE')} の面積", f"<div class=wk>{st('△ABC－△ADE＝18－8')}</div>" + ln("10cm²", 26))
          + f"</div>{fa.svg()}</div>")
    qb = (f"<div class=row><div style='flex:1'>"
          + cell(1, f"{TR('ADE')} の面積", f"<div class=wk>{st('AD：AB＝3：(3＋2)＝3：5', '面積比 9：25', T('9:25=x:50') + '　' + T('x=18'))}</div>" + ln("18cm²", 26))
          + cell(2, f"台形 {S('DBCE')} の面積", f"<div class=wk>{st('50－18')}</div>" + ln("32cm²", 26))
          + f"</div>{fb.svg()}</div>")
    qc = (f"<div class=row><div style='flex:1'>"
          + cell("", f"{TR('OAB')} の面積が 12cm² のとき，{TR('ODC')} の面積を求めなさい。",
                 f"<div class=wk>{st(SIM('OAB', 'ODC') + '（錯角・対頂角）', '相似比 OA：OD＝4：6＝2：3', '面積比 4：9　' + T('4:9=12:x') + '　' + T('x=27'))}</div>" + ln("27cm²", 26))
          + f"</div>{fc.svg()}</div>")
    qd = (f"<div class=row><div style='flex:1'>"
          + cell("", f"点 {S('D')}，{S('E')} はそれぞれ辺 {S('AB')}，{S('AC')} の中点です。{TR('ABC')} の面積が 48cm² のとき，{TR('ADE')} と台形 {S('DBCE')} の面積を求めなさい。",
                 f"<div class=wk>{st('中点連結定理より DE∥BC，DE＝½BC', SIM('ADE', 'ABC') + '　相似比 1：2 → 面積比 1：4', '△ADE＝48÷4＝12，台形＝48－12＝36')}</div>"
                 + f"<div class=lns>{ln('12cm²', 22, TR('ADE') + '＝')}{ln('36cm²', 22, '台形＝')}</div>")
          + f"</div>{fd.svg()}</div>")
    return f"""<div class="page{'' if ans else ' hide'}">{head(3, "図形の中の面積比", ans)}
<div class=tip>重なった図形では，まず<b>相似な三角形を見つける</b>（{T(r'\mathrm{DE}\parallel\mathrm{BC}')} なら {SIM('ADE', 'ABC')}）。<br>
相似比は <b>AD：AB</b>（AD：DB ではない！）。台形の面積は「大きい三角形 － 小さい三角形」。</div>
{big(1, f"右の図で {S('DE')} ∥ {S('BC')} です。（単位は cm）")}{qa}
{big(2, f"右の図で {S('DE')} ∥ {S('BC')}，{TR('ABC')} の面積は 50cm² です。")}{qb}
{big(3, f"右の図で {S('AB')} ∥ {S('DC')}，{S('O')} は {S('AD')} と {S('BC')} の交点です。")}{qc}
{big(4, "中点と面積")}{qd}
</div>"""


def page4(ans):
    ft = fig_trap(3.3)
    q = [
        cell(1, f"{SIM('ABC', 'DEF')} で，相似比は 3：4，{TR('ABC')} の面積は 27cm² です。{TR('DEF')} の面積を求めなさい。",
             f"<div class=wk>{st('面積比 9：16', T('9:16=27:x') + '　' + T('9x=432') + '　' + T('x=48'))}</div>" + ln("48cm²", 30)),
        cell(2, "相似な2つの図形の面積比は 25：16 です。大きい方の図形の辺 15cm に対応する，小さい方の図形の辺の長さを求めなさい。",
             f"<div class=wk>{st('25＝5²，16＝4² → 相似比 5：4', T('5:4=15:x') + '　' + T('5x=60') + '　' + T('x=12'))}</div>" + ln("12cm", 30)),
        cell(3, f"{S('DE')} ∥ {S('BC')}（D は AB 上，E は AC 上）で，{TR('ADE')} の面積は 4cm²，{TR('ABC')} の面積は 36cm² です。{T(r'\mathrm{AD}=3')}cm のとき，{S('AB')} と {S('DB')} の長さを求めなさい。",
             f"<div class=wk>{st('面積比 4：36＝1：9 → 相似比 1：3', 'AB＝3×3＝9，DB＝9－3＝6')}</div>"
             + f"<div class=lns>{ln('9cm', 22, 'AB＝')}{ln('6cm', 22, 'DB＝')}</div>"),
        cell(4, "縦 6cm，横 8cm の写真を，縦も横も 1.5倍に拡大しました。拡大した写真の面積を求めなさい。",
             f"<div class=wk>{st('もとの面積 6×8＝48', '相似比 1：1.5＝2：3 → 面積比 4：9', T('4:9=48:x') + '　' + T('x=108'))}</div>" + ln("108cm²", 30)),
    ]
    trap = (f"<div class=row><div style='flex:1'>"
            + cell(1, f"{TR('OAD')} と {TR('OCB')} の面積比を求めなさい。",
                   f"<div class=wk>{st(SIM('OAD', 'OCB') + '（錯角）', '相似比 AD：CB＝4：8＝1：2')}</div>" + ln("1：4", 26))
            + cell(2, f"{TR('OAD')} の面積が 6cm² のとき，{TR('OCB')} の面積を求めなさい。",
                   f"<div class=wk>{st('6×4')}</div>" + ln("24cm²", 26))
            + cell("☆", f"{TR('OAB')} の面積を求めなさい。（ヒント：OA：OC と高さ）",
                   f"<div class=wk>{st('AO：OC＝1：2，△OAB と △OCB は高さが同じ', '→ 面積の比も 1：2　△OAB＝24÷2＝12')}</div>" + ln("12cm²", 26))
            + f"</div>{ft.svg()}</div>")
    return f"""<div class="page{'' if ans else ' hide'}">{head(4, "練習・利用", ans)}
{big(1, "次の問いに答えなさい。")}
<div class="grid c2" style="flex:1 0 auto;row-gap:2mm;grid-template-rows:1fr 1fr">{''.join(q)}</div>
{big(2, f"右の図の台形 {S('ABCD')} で {S('AD')} ∥ {S('BC')}，{T(r'\mathrm{AD}=4')}cm，{T(r'\mathrm{BC}=8')}cm，{S('O')} は対角線の交点です。")}
{trap}
</div>"""


if __name__ == "__main__":
    check()
    pages = lambda ans: page1(ans) + page2(ans) + page3(ans) + page4(ans)
    write_pdfs([(doc(CSS, pages(False)), f"{FILE}.pdf"), (doc(CSS, pages(True)), f"{FILE}_ans.pdf")])
