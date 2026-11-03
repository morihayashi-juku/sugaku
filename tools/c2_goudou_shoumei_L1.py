"""中2 合同の証明 レベル1（A4・問題4ページ16問＋こたえ2ページ）

  cd tools && python3 c2_goudou_shoumei_L1.py        # A・B 両方
  cd tools && python3 c2_goudou_shoumei_L1.py A      # Aだけ

レベル1＝問題文の「仮定」がそのまま合同条件になっている問題（自分で合同条件を見つけなくてよい）。
ねらいは、合同条件（3つ）と「仮定は問題文に書いてある」ことを覚えて、証明の型を身につけること。
- 1ページ＝左右2列×2問＝4問。図の中の同じ印（ー・＝・弧）は、問題文の仮定と同じもの。
- 足場を少しずつ減らす：その1＝穴うめ／その2＝ワク（型だけ）／その3・その4＝罫線だけ（自分で書く）
- その4には、△の名前の順（対応する頂点の順）がちがう問題がある（結論を写せばよい）。
- 図は三角形を移動・回転・裏返しただけにして、ぴったり合同になるように作る（スクリプトで確かめる）。
  共通な辺・対頂角・平行線など「仮定に書いていないのに図から言えること」は使わない（それはレベル2）。
- パターン A＝月曜の授業、B＝木曜の授業（同じ形・別の図）。
- 出力：pdf/c2_goudou_shoumei_L1_{A,B}.pdf と _ans.pdf
"""
import math
import random
import sys

from mathlib import CSS, answer_doc, head, write_pdfs

W, H = 84.0, 35.0          # 図の大きさ（mm）
MX, MY = 5.5, 6.2          # 図の余白（頂点の名前の分）
COND = {"SSS": "3組の辺がそれぞれ等しい",
        "SAS": "2組の辺とその間の角がそれぞれ等しい",
        "ASA": "1組の辺とその両端の角がそれぞれ等しい"}


# ---------- 幾何の部品 ----------
def rad(d):
    return d * math.pi / 180


def rot(p, a):
    c, s = math.cos(a), math.sin(a)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def mir(p):
    return (p[0], -p[1])


def refl(p, beta):
    """原点を通り角 beta の直線についての対称移動"""
    x, y = rot(p, -beta)
    return rot((x, -y), beta)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def unit(v):
    n = math.hypot(*v)
    return (v[0] / n, v[1] / n)


def angle_at(P, v):
    """三角形 P の頂点 v の角（度）"""
    u, w = sub(P[(v + 2) % 3], P[v]), sub(P[(v + 1) % 3], P[v])
    return math.degrees(math.acos((u[0] * w[0] + u[1] * w[1]) / (math.hypot(*u) * math.hypot(*w))))


def tri(shape):
    c, b, al = shape
    return [(0.0, 0.0), (float(c), 0.0), (b * math.cos(rad(al)), b * math.sin(rad(al)))]


def shape_ok(shape):
    P = tri(shape)
    sides = sorted(math.dist(P[i], P[(i + 1) % 3]) for i in range(3))
    angs = sorted(angle_at(P, v) for v in range(3))
    return (all(sides[i + 1] / sides[i] >= 1.12 for i in range(2))
            and all(angs[i + 1] - angs[i] >= 10 for i in range(2))
            and angs[0] >= 30 and angs[2] <= 108 and not any(86 <= a <= 94 for a in angs))


SHAPES = [(c, b, a) for c in range(20, 28) for b in range(12, 21) for a in range(34, 76, 3)
          if c != b and shape_ok((c, b, a))]


# ---------- 問題のデータ ----------
def conds(sp):
    """仮定の3つ。items＝図の印（種類, 場所, 印の数）、text＝問題文の（左, 右）"""
    typ, i = sp["typ"], sp.get("i", 0)
    n = (sp["l1"], sp["l2"])

    def S(t, a, b):
        return n[t][a] + n[t][b]

    def A(t, v):
        return "∠" + n[t][(v + 2) % 3] + n[t][v] + n[t][(v + 1) % 3]

    if typ == "SSS":
        items = [("side", (0, 1), 1), ("side", (1, 2), 2), ("side", (2, 0), 3)]
    elif typ == "SAS":      # 角 i をはさむ2辺
        items = [("side", ((i + 2) % 3, i), 1), ("side", (i, (i + 1) % 3), 2), ("angle", i, 1)]
    else:                   # ASA：辺 (i, i+1) とその両端の角
        j = (i + 1) % 3
        items = [("angle", i, 1), ("side", (i, j), 1), ("angle", j, 2)]
    text = [((S(0, *x), S(1, *x)) if k == "side" else (A(0, x), A(1, x))) for k, x, _ in items]
    return items, text


def build(sp):
    """点の座標（作図用・確認用）を作る"""
    T = tri(sp["shape"])
    if sp["kind"] == "S":
        r1, r2, m2 = sp["o"]
        P1 = [rot(p, rad(r1)) for p in T]
        P2 = [rot(mir(p) if m2 else p, rad(r2)) for p in T]
    else:                                   # F：点 A（0番目）を共有する2つの三角形（ひらいた扇）
        al = angle_at(T, 0)
        g = sp["f"]["g"]
        if sp["f"]["var"] == "rot":
            P2 = [rot(p, rad(al + g)) for p in T]
        else:
            P2 = [refl(p, rad(al + g / 2)) for p in T]
        # 扇の向き：ひらいた角（0〜2α+g）の真ん中が真上（dir=1）か真下（dir=-1）になるようにする
        R = rad(sp["f"]["dir"] * 90 - (2 * al + g) / 2 + sp["f"]["jit"])
        P1, P2 = [rot(p, R) for p in T], [rot(p, R) for p in P2]
    return P1, P2


def verify(sp, P1, P2):
    """図が本当に合同か、印をつけた辺・角が本当に等しいか、合同条件の形になっているかを確かめる"""
    d = lambda P, a, b: math.dist(P[a], P[b])  # noqa: E731
    for i in range(3):
        assert abs(d(P1, i, (i + 1) % 3) - d(P2, i, (i + 1) % 3)) < 1e-6, ("辺", sp)
        assert abs(angle_at(P1, i) - angle_at(P2, i)) < 1e-6, ("角", sp)
    items, _ = conds(sp)
    kinds = [k for k, _, _ in items]
    typ = sp["typ"]
    if typ == "SSS":
        assert kinds == ["side"] * 3 and len({frozenset(x) for _, x, _ in items}) == 3
    elif typ == "SAS":                       # 2辺と「その間の角」：角の頂点が2辺の共通の頂点
        (_, s1, _), (_, s2, _), (_, v, _) = items
        assert kinds == ["side", "side", "angle"] and set(s1) & set(s2) == {v} and v in s1 and v in s2
    else:                                    # 辺と「その両端の角」：角の頂点が辺の両端
        (_, v1, _), (_, s, _), (_, v2, _) = items
        assert kinds == ["angle", "side", "angle"] and {v1, v2} == set(s)
    assert len(set(sp["l1"]) | set(sp["l2"])) == (5 if sp["kind"] == "F" else 6), sp
    if sp["kind"] == "F":
        assert sp["l1"][0] == sp["l2"][0] and sp["f"]["g"] >= 36, "内がわの頂点の名前がぶつかる"
        al = angle_at(P1, 0)
        assert 2 * al + sp["f"]["g"] <= 172, "ひらいた扇が広すぎる"


# ---------- 図（SVG） ----------
def figure(sp, marks=True):
    P1, P2 = build(sp)
    verify(sp, P1, P2)

    def bb(P):
        xs, ys = [p[0] for p in P], [p[1] for p in P]
        return max(xs) - min(xs), max(ys) - min(ys), (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2

    if sp["kind"] == "S":
        w1, h1, x1, y1 = bb(P1)
        w2, h2, x2, y2 = bb(P2)
        s = min(1.4, (W / 2 - 2 * MX - 3) / max(w1, w2), (H - 2 * MY) / max(h1, h2))   # -3：2つの三角形の間をあける
        Q1 = [((p[0] - x1) * s + W / 4, H / 2 - (p[1] - y1) * s) for p in P1]
        Q2 = [((p[0] - x2) * s + 3 * W / 4, H / 2 - (p[1] - y2) * s) for p in P2]
    else:
        w, h, x0, y0 = bb(P1 + P2)
        s = min(1.4, (W - 2 * MX) / w, (H - 2 * MY) / h)
        Q1 = [((p[0] - x0) * s + W / 2, H / 2 - (p[1] - y0) * s) for p in P1]
        Q2 = [((p[0] - x0) * s + W / 2, H / 2 - (p[1] - y0) * s) for p in P2]

    items = conds(sp)[0] if marks else []     # marks=False：等しい印（ー・弧）を書かない
    out = []

    def line(a, b, w=.4):
        out.append(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke-width="{w}"/>')

    for Q, names in ((Q1, sp["l1"]), (Q2, sp["l2"])):
        out.append('<polygon points="' + " ".join(f"{x:.2f},{y:.2f}" for x, y in Q) + '" stroke-width=".45"/>')
        for kind, idx, k in items:
            if kind == "side":                                  # 辺の印（ー）
                P, R = Q[idx[0]], Q[idx[1]]
                m = ((P[0] + R[0]) / 2, (P[1] + R[1]) / 2)
                u = unit(sub(R, P))
                nv = (-u[1], u[0])
                for t in range(k):
                    off = (t - (k - 1) / 2) * 1.3
                    c = (m[0] + u[0] * off, m[1] + u[1] * off)
                    line((c[0] - nv[0] * 1.6, c[1] - nv[1] * 1.6), (c[0] + nv[0] * 1.6, c[1] + nv[1] * 1.6), .4)
            else:                                               # 角の印（弧）
                v = idx
                V, U, R = Q[v], Q[(v + 2) % 3], Q[(v + 1) % 3]
                du, dw = unit(sub(U, V)), unit(sub(R, V))
                r0 = min(5.2, .33 * min(math.dist(V, U), math.dist(V, R)))
                sweep = 1 if du[0] * dw[1] - du[1] * dw[0] > 0 else 0
                for t in range(k):
                    r = r0 + t * 1.25
                    a = (V[0] + du[0] * r, V[1] + du[1] * r)
                    b = (V[0] + dw[0] * r, V[1] + dw[1] * r)
                    out.append(f'<path d="M{a[0]:.2f},{a[1]:.2f} A{r:.2f},{r:.2f} 0 0 {sweep} {b[0]:.2f},{b[1]:.2f}" stroke-width=".4"/>')
    # 頂点の名前：角の外がわ（外角の二等分線の向き）。共有する頂点は1回だけ・扇の外がわ
    for t, (Q, names) in enumerate(((Q1, sp["l1"]), (Q2, sp["l2"]))):
        for v in range(3):
            if sp["kind"] == "F" and v == 0:
                if t == 1:
                    continue
                ref = [p for q in (Q1, Q2) for p in q[1:]]
                d = unit(sub(Q[0], (sum(p[0] for p in ref) / 4, sum(p[1] for p in ref) / 4)))
            else:
                a, b = unit(sub(Q[v], Q[(v + 1) % 3])), unit(sub(Q[v], Q[(v + 2) % 3]))
                d = unit((a[0] + b[0], a[1] + b[1]))
            x, y = Q[v][0] + d[0] * 3.8, Q[v][1] + d[1] * 3.8
            out.append(f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle" dominant-baseline="central" '
                       f'stroke="none" fill="#111">{names[v]}</text>')
    return (f'<svg class=fig viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="#111" '
            f'stroke-linecap="round" font-family="\'Noto Serif CJK JP\', serif" font-size="4.3">' + "".join(out) + "</svg>")


# ---------- 証明の文章 ----------
def tris(sp):
    return f"△{sp['l1']}", f"△{sp['l2']}"


def proof_lines(sp):
    """（こたえ）証明の全文。[('t', 文)] ／ [('eq', [3つの式])] の形"""
    _, text = conds(sp)
    a, b = tris(sp)
    return [f"{a} と {b} において、"], [f"{l}＝{r}" for l, r in text], f"<b>{COND[sp['typ']]}</b>から、", f"{a}≡{b}"


def blank(mm):
    return f'<span class=bl style="width:{mm}mm"></span>'


def proof_frame(sp, lv):
    """問題用紙の証明の欄。lv a＝穴うめ／b＝ワク／c＝罫線だけ"""
    _, text = conds(sp)
    a, b = tris(sp)
    if lv == "c":
        return "<div class=pf>" + "<div class=rl></div>" * 7 + "</div>"
    rows = []
    if lv == "a":
        rows.append(f"<div class=ln>{a} と {b} において、</div>")
        for k, (l, r) in enumerate(text):
            rows.append(f"<div class='ln eq'><span class=lead>{'仮定より' if k == 0 else ''}</span>"
                        f"<span>{l}＝{blank(21)}　…{'①②③'[k]}</span></div>")
        rows.append("<div class=ln>①、②、③より、</div>")
        rows.append(f"<div class=ln>{blank(64)}から、</div>")
        rows.append(f"<div class=ln>{a}≡△{blank(15)}</div>")
    else:
        rows.append(f"<div class=ln>△{blank(15)} と △{blank(15)} において、</div>")
        for k in range(3):
            rows.append(f"<div class='ln eq'><span class=lead>{'仮定より' if k == 0 else ''}</span>"
                        f"<span>{blank(44)}　…{'①②③'[k]}</span></div>")
        rows.append("<div class=ln>①、②、③より、</div>")
        rows.append(f"<div class=ln>{blank(64)}から、</div>")
        rows.append(f"<div class=ln>△{blank(15)}≡△{blank(15)}</div>")
    return "<div class=pf>" + "".join(rows) + "</div>"


def cell(sp, no, lv):
    _, text = conds(sp)
    a, b = tris(sp)
    ka = "".join(f"<span class=nb>{l}＝{r}{'、' if k < 2 else ''}</span>" for k, (l, r) in enumerate(text))
    return (f"<div class=q><div class=qno>問{no}</div>{figure(sp)}"
            f"<div class=stmt><div class=sr><span class=lb>仮定</span><span class=sx>{ka}</span></div>"
            f"<div class=sr><span class=lb>結論</span><span class=sx>{a}≡{b}</span></div></div>"
            f"{proof_frame(sp, lv)}</div>")


def answer_row(sp, no):
    head_, eqs, why, last = proof_lines(sp)
    eq_html = "".join(f"<div class='ln eq'><span class=lead>{'仮定より' if k == 0 else ''}</span>"
                      f"<span>{e}　…{'①②③'[k]}</span></div>" for k, e in enumerate(eqs))
    return (f"<div class=a><div class=ano>問{no}</div><div class=pf2>"
            f"<div class=ln>{head_[0]}</div>{eq_html}<div class=ln>①、②、③より、</div>"
            f"<div class=ln>{why}</div><div class=ln>{last}</div></div></div>")


# ---------- 16問の設計 ----------
PAGES = [
    ("その1", "穴うめ", "a",
     "ポイント：<b>仮定</b>は問題文に書いてある。「仮定より」のあとに<b>そのまま写して</b>①②③と番号をつける。"
     "<br>合同条件：<b>3組の辺</b>／<b>2組の辺とその間の角</b>／<b>1組の辺とその両端の角</b>　がそれぞれ等しい"),
    ("その2", "ワク（型だけ）", "b",
     "ポイント：証明の型は同じ。「仮定より」のあとに、問題文の仮定を3つ写そう。最後の行は<b>結論</b>。"
     "<br>合同条件：<b>3組の辺</b>／<b>2組の辺とその間の角</b>／<b>1組の辺とその両端の角</b>　がそれぞれ等しい"),
    ("その3", "自分で書く", "c",
     "ポイント：型を思い出して書こう。「△と△において」→「仮定より」①②③→「①、②、③より」→結論。"
     "<br>合同条件：<b>3組の辺</b>／<b>2組の辺とその間の角</b>／<b>1組の辺とその両端の角</b>　がそれぞれ等しい"),
    ("その4", "自分で書く（△の順に注意）", "c",
     "ポイント：△ABC≡△QRP のように、<b>対応する頂点は同じ順番</b>に書く。問題の結論を写せばよい。"
     "<br>合同条件：<b>3組の辺</b>／<b>2組の辺とその間の角</b>／<b>1組の辺とその両端の角</b>　がそれぞれ等しい"),
]


def specs(key):
    """key＝A（月曜）／B（木曜）。型の並びは同じで、図・文字・向きを変える"""
    rnd = random.Random({"A": 11, "B": 23}[key])
    pool = SHAPES[:]
    rnd.shuffle(pool)

    def shape(f=False):
        for s in pool:
            if not f or s[2] <= 62:
                pool.remove(s)
                return s

    # △の名前（1つめ, 2つめ）。扇の図（F）は 2つめを None にする（共有する頂点＋あとの2文字で作る）
    names = {"A": [("ABC", "DEF"), ("ABC", "PQR"), ("DEF", "GHJ"), ("ABC", "XYZ"),
                   ("KLM", "PQR"), ("ABC", "DEF"), ("ABC", None), ("DEF", "GHJ"),
                   ("ABC", "XYZ"), ("KLM", None), ("ABC", "PQR"), ("PQR", None),
                   ("DEF", "GHJ"), ("ABC", None), ("KLM", "PQR"), ("DEF", None)],
             "B": [("ABC", "PQR"), ("ABC", "DEF"), ("PQR", "STU"), ("KLM", "XYZ"),
                   ("DEF", "GHJ"), ("ABC", "XYZ"), ("KLM", None), ("ABC", "PQR"),
                   ("PQR", "STU"), ("ABC", None), ("KLM", "PQR"), ("PQR", None),
                   ("ABC", "XYZ"), ("KLM", None), ("DEF", "GHJ"), ("ABC", None)]}[key]

    # （型, 起点 i, 図の種類, 向き(r1,r2,裏返し) or 扇(形,ひらき,ゆらぎ,上下), 名前の順 or None）
    plan = [
        # その1：ならべただけ・名前も順どおり
        ("SSS", 0, "S", (0, 0, False), None), ("SAS", 1, "S", (0, 0, True), None),
        ("ASA", 0, "S", (0, 180, True), None), ("SSS", 0, "S", (0, 180, False), None),
        # その2：向きをかえる・扇の形が1つ
        ("SAS", 2, "S", (14, -10, False), None), ("ASA", 1, "S", (-12, 16, True), None),
        ("SAS", 0, "F", ("rot", 40, -6, 1), None), ("SSS", 0, "S", (8, 90, False), None),
        # その3：扇の形が2つ
        ("ASA", 2, "S", (-8, 160, True), None), ("SAS", 0, "F", ("mir", 38, 8, 1), None),
        ("SSS", 0, "S", (16, -16, False), None), ("ASA", 0, "F", ("rot", 42, 0, -1), None),
        # その4：△の順がちがう
        ("SAS", 1, "S", (0, 180, False), (2, 0, 1)), ("SSS", 0, "F", ("mir", 44, 5, 1), (0, 2, 1)),
        ("ASA", 1, "S", (10, -170, True), (1, 2, 0)), ("SAS", 0, "F", ("rot", 38, -8, 1), None),
    ]
    out = []
    for k, (typ, i, kind, o, perm) in enumerate(plan):
        a, b = names[k]
        sp = {"typ": typ, "i": i, "kind": kind, "l1": a}
        if kind == "S":
            sp["shape"] = shape()
            sp["o"] = o
            l2 = list(b)
        else:
            sp["shape"] = shape(True)
            sp["f"] = {"var": o[0], "g": o[1], "jit": o[2], "dir": o[3]}
            l2 = [a[0]] + list({"A": "DE", "K": "NP", "P": "ST", "D": "GH"}[a[0]])   # 共有する頂点＋あとの2つ
        if perm:
            l2 = [l2[p] for p in perm]
        sp["l2"] = "".join(l2)
        if kind == "F":
            assert sp["l1"][0] == sp["l2"][0] or perm, sp
        out.append(sp)
    return out


def make(key):
    sp = specs(key)
    for s in sp:
        P1, P2 = build(s)
        verify(s, P1, P2)
    secs, asecs = [], []
    for p, (lab, sub_, lv, tip) in enumerate(PAGES):
        cs = [cell(sp[p * 4 + j], p * 4 + j + 1, lv) for j in range(4)]
        secs.append(f"<div class=page>{head('合同の証明 レベル1 ' + lab, sub_, score=4)}"
                    f"<div class=tip>{tip}</div>"
                    f"<div class=grid><div class=col>{cs[0]}{cs[1]}</div><div class=col>{cs[2]}{cs[3]}</div></div></div>")
        asecs.append({"label": f"{lab}　{sub_}", "rows": [answer_row(sp[p * 4 + j], p * 4 + j + 1) for j in range(4)]})
    prob = f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{''.join(secs)}</body></html>"
    ans = answer_doc(f"合同の証明 レベル1 {key}", asecs, pages=[2])
    return [(prob, f"c2_goudou_shoumei_L1_{key}.pdf"), (ans, f"c2_goudou_shoumei_L1_{key}_ans.pdf")]


EXTRA = """
.col { grid-template-rows: repeat(2, 1fr); }
.col:first-child { padding-right: 5mm; } .col:last-child { padding-left: 5mm; }
.q { padding-top: 1.5mm; }
.tip { font-size: 9.6pt; line-height: 1.55; padding: 1.6mm 3.6mm; }
.qno { font-weight: 700; font-size: 12pt; line-height: 1; }
.fig { display: block; width: 100%; height: auto; margin-top: -1.2mm; overflow: visible; }
.stmt { font-family: 'Noto Serif CJK JP', serif; font-size: 11pt; line-height: 1.7; margin-top: .5mm; }
.sr { display: flex; align-items: flex-start; } .sx { flex: 1; } .nb { display: inline-block; white-space: nowrap; margin-right: 1.2mm; }
.lb { display: inline-block; font-family: 'Noto Sans CJK JP', sans-serif; font-size: 8.6pt; font-weight: 700;
      background: #222; color: #fff; border-radius: 1mm; padding: 0 1.6mm; margin-right: 2mm; line-height: 1.5; vertical-align: 1pt; }
.pf, .pf2 { font-family: 'Noto Serif CJK JP', serif; font-size: 10.6pt; margin-top: 1.5mm; }
.pf .ln { height: 7.4mm; line-height: 7.4mm; white-space: nowrap; }
.pf .rl { height: 7.4mm; border-bottom: .6pt solid #bbb; }
.eq { display: flex; } .lead { width: 17mm; flex: none; }
.bl { display: inline-block; border-bottom: .7pt solid #111; height: 1em; margin: 0 .8mm; }
/* こたえ */
.ano { font-family: 'Noto Sans CJK JP', sans-serif; font-weight: 700; font-size: 10pt; margin-bottom: .5mm; }
.pf2 { margin-top: 0; font-size: 10.4pt; }
.pf2 .ln { line-height: 1.62; white-space: nowrap; }
.pf2 b { font-weight: 700; }
"""

if __name__ == "__main__":
    docs = []
    for k in sys.argv[1:] or ["A", "B"]:
        docs += make(k)
    write_pdfs(docs, EXTRA)
