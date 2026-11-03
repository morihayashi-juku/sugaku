"""中2 合同の証明（木曜用・6ページ24問＋こたえ3ページ）

  cd tools && python3 c2_goudou_shoumei_L12_thu.py

- 前半3ページ（問1〜12）＝レベル1：文章中に合同条件の仮定を3つ書く。
- 後半3ページ（問13〜24）＝レベル2：文章中の仮定は2つだけ。あと1つは図から自分で見つける
  （共通な辺・対頂角）。
- 図に等しい印（ー・弧）は書かない。証明を書く欄の罫線もない（白い余白）。
- 1ページ＝左右2列×2問。出力：pdf/c2_goudou_shoumei_L12_thu.pdf と _ans.pdf
- 図は三角形を移動・回転・裏返し（共通な辺は線対称・点対称、対頂角は点対称）にして作り、
  ぴったり合同になること、合同条件の形（間の角・両端の角）になっていることをスクリプトで確かめる。
"""
import math
import random

from mathlib import CSS, answer_doc, head, write_pdfs
from c2_goudou_shoumei_L1 import (COND, EXTRA, H, MX, MY, SHAPES, W, angle_at, build, conds, figure,
                                  refl, rot, sub, tri, unit, verify, rad)

LEAD = {"given": "仮定より", "side": "共通な辺だから", "vert": "対頂角は等しいから"}
CONDLINE = "合同条件：<b>3組の辺</b>／<b>2組の辺とその間の角</b>／<b>1組の辺とその両端の角</b>　がそれぞれ等しい"


# ---------- レベル1（仮定3つ・印なし） ----------
def specs1(rnd):
    pool = SHAPES[:]
    rnd.shuffle(pool)

    def shape(f=False):
        for s in pool:
            if not f or s[2] <= 62:
                pool.remove(s)
                return s

    names = [("ABC", "DEF"), ("ABC", "PQR"), ("DEF", "GHJ"), ("ABC", "XYZ"),
             ("KLM", "PQR"), ("ABC", "DEF"), ("ABC", None), ("PQR", "STU"),
             ("ABC", "XYZ"), ("KLM", None), ("ABC", "PQR"), ("DEF", None)]
    plan = [("SSS", 0, "S", (0, 0, False)), ("SAS", 1, "S", (0, 0, True)),
            ("ASA", 0, "S", (0, 180, True)), ("SSS", 0, "S", (0, 180, False)),
            ("SAS", 2, "S", (14, -10, False)), ("ASA", 1, "S", (-12, 16, True)),
            ("SAS", 0, "F", ("rot", 40, -6, 1)), ("SSS", 0, "S", (8, 90, False)),
            ("ASA", 2, "S", (-8, 160, True)), ("SAS", 0, "F", ("mir", 38, 8, 1)),
            ("SSS", 0, "S", (16, -16, False)), ("ASA", 0, "F", ("rot", 42, 0, -1))]
    out = []
    for (typ, i, kind, o), (a, b) in zip(plan, names):
        sp = {"typ": typ, "i": i, "kind": kind, "l1": a}
        if kind == "S":
            sp["shape"], sp["o"], sp["l2"] = shape(), o, b
        else:
            sp["shape"] = shape(True)
            sp["f"] = {"var": o[0], "g": o[1], "jit": o[2], "dir": o[3]}
            sp["l2"] = a[0] + {"A": "DE", "K": "NP", "P": "ST", "D": "GH"}[a[0]]
        P1, P2 = build(sp)
        verify(sp, P1, P2)
        out.append(sp)
    return out


# ---------- レベル2（仮定2つ・1つは自分で見つける） ----------
def build2(sp):
    """（点の名前→座標）と、線分、1つめ・2つめの三角形の座標を返す（数学の座標・y が上）"""
    T = tri(sp["shape"])
    a, b, c, d = sp["letters"]
    if sp["fig"] in ("K", "P"):
        A, B, C = T
        if sp["fig"] == "K":                # 共通な辺 AC をはさんで線対称
            D = refl(B, math.atan2(C[1], C[0]))
            P2 = [A, D, C]
            sp["l1"], sp["l2"] = a + b + c, a + d + c
        else:                               # AC の真ん中について点対称（平行四辺形）
            D = (A[0] + C[0] - B[0], A[1] + C[1] - B[1])
            P2 = [C, D, A]
            sp["l1"], sp["l2"] = a + b + c, c + d + a
        pts = {a: A, b: B, c: C, d: D}
        segs = [(a, b), (b, c), (c, d), (d, a), (a, c)]
        return pts, segs, [A, B, C], P2
    O, A, B = T                              # 対頂角：O について点対称
    D, C = (-A[0], -A[1]), (-B[0], -B[1])
    pts = {"O": O, a: A, b: B, c: C, d: D}
    segs = [("O", a), ("O", b), ("O", c), ("O", d), (a, b), (d, c)]
    sp["l1"], sp["l2"] = "O" + a + b, "O" + d + c
    return pts, segs, [O, A, B], [O, D, C]


def found_index(sp, items):
    f = [k for k, (kind, idx, _) in enumerate(items)
         if (sp["fig"] != "B" and kind == "side" and set(idx) == {2, 0}) or (sp["fig"] == "B" and kind == "angle" and idx == 0)]
    assert len(f) == 1, (sp, items)
    return f[0]


def verify2(sp, P1, P2):
    d = lambda P, x, y: math.dist(P[x], P[y])  # noqa: E731
    for i in range(3):
        assert abs(d(P1, i, (i + 1) % 3) - d(P2, i, (i + 1) % 3)) < 1e-6, ("辺", sp)
        assert abs(angle_at(P1, i) - angle_at(P2, i)) < 1e-6, ("角", sp)
    items, text = conds(sp)
    kinds = [k for k, _, _ in items]
    if sp["typ"] == "SSS":
        assert kinds == ["side"] * 3
    elif sp["typ"] == "SAS":
        (_, s1, _), (_, s2, _), (_, v, _) = items
        assert set(s1) & set(s2) == {v}
    else:
        (_, v1, _), (_, s, _), (_, v2, _) = items
        assert {v1, v2} == set(s)
    f = found_index(sp, items)
    l, r = text[f]
    if sp["fig"] != "B":
        assert set(l) == set(r), "共通な辺になっていない"
    else:
        l, r = l[1:], r[1:]                                   # 「∠」をとる
        assert l[1] == r[1] == "O" and {l[0], l[2]} == {sp["letters"][0], sp["letters"][1]}
    return f


def figure2(sp):
    pts, segs, P1, P2 = build2(sp)
    f = verify2(sp, P1, P2)
    allp = list(pts.values())
    best = None
    for rr in (sp["jit"], sp["jit"] + 90):
        Q = [rot(p, rad(rr)) for p in allp]
        xs, ys = [q[0] for q in Q], [q[1] for q in Q]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        s = min(1.4, (W - 2 * MX) / w, (H - 2 * MY) / h)
        if best is None or s > best[0]:
            best = (s, rr, (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
    s, rr, cx, cy = best
    tr = {k: (lambda q: ((q[0] - cx) * s + W / 2, H / 2 - (q[1] - cy) * s))(rot(v, rad(rr))) for k, v in pts.items()}
    out = []
    for x, y in segs:
        out.append(f'<line x1="{tr[x][0]:.2f}" y1="{tr[x][1]:.2f}" x2="{tr[y][0]:.2f}" y2="{tr[y][1]:.2f}" stroke-width=".45"/>')
    cen = (sum(p[0] for p in tr.values()) / len(tr), sum(p[1] for p in tr.values()) / len(tr))
    for k, q in tr.items():
        if k == "O" and sp["fig"] == "B":                    # O は、三角形のない側のすきまに書く
            a, b, c, d = sp["letters"]
            u1, u2 = unit(sub(tr[b], q)), unit(sub(tr[d], q))
            dd = unit((u1[0] + u2[0], u1[1] + u2[1]))
            # すきま（B–D）と（A–C）のうち広いほう
            v1, v2 = unit(sub(tr[a], q)), unit(sub(tr[c], q))
            ee = unit((v1[0] + v2[0], v1[1] + v2[1]))
            ang1 = math.degrees(math.acos(max(-1, min(1, u1[0] * u2[0] + u1[1] * u2[1]))))
            ang2 = math.degrees(math.acos(max(-1, min(1, v1[0] * v2[0] + v1[1] * v2[1]))))
            dd = dd if ang1 >= ang2 else ee
            x, y = q[0] + dd[0] * 3.6, q[1] + dd[1] * 3.6
        else:
            ref = tr["O"] if sp["fig"] == "B" else cen
            dd = unit(sub(q, ref))
            x, y = q[0] + dd[0] * 3.8, q[1] + dd[1] * 3.8
        out.append(f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle" dominant-baseline="central" stroke="none" fill="#111">{k}</text>')
    svg = (f'<svg class=fig viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="#111" '
           f'stroke-linecap="round" font-family="\'Noto Serif CJK JP\', serif" font-size="4.3">' + "".join(out) + "</svg>")
    return svg, f


def specs2(rnd):
    pool = [s for s in SHAPES if s[2] <= 70]
    rnd.shuffle(pool)
    sets = ["ABCD", "PQRS", "KLMN", "EFGH", "WXYZ"]
    plan = [("K", "SSS", 0), ("P", "SAS", 0), ("B", "SAS", 0), ("K", "ASA", 2),
            ("P", "SSS", 0), ("B", "ASA", 0), ("K", "SAS", 2), ("P", "ASA", 2),
            ("B", "SAS", 0), ("K", "SSS", 0), ("P", "ASA", 2), ("B", "ASA", 2)]
    out = []
    for k, (fig, typ, i) in enumerate(plan):
        if fig == "K":      # 線対称の図が凹まないように、A・C の角が90°より小さい三角形にする
            sh = next(x for x in reversed(pool) if angle_at(tri(x), 2) < 85)
            pool.remove(sh)
        else:
            sh = pool.pop()
        sp = {"fig": fig, "typ": typ, "i": i, "shape": sh, "letters": sets[(k * 2 + k // 5) % 5],
              "jit": rnd.choice([-12, -6, 0, 6, 12])}
        build2(sp)
        out.append(sp)
    return out


# ---------- ページ ----------
def stmt(items):
    ka = "".join(f"<span class=nb>{l}＝{r}{'、' if k < len(items) - 1 else ''}</span>" for k, (l, r) in enumerate(items))
    return ka


def cell(no, svg, given, concl):
    """問題文は文章（例：下の図で、AB＝DE、BC＝EF、CA＝FD です。このとき、△ABC≡△DEF であることを証明しなさい。）"""
    return (f"<div class=q><div class=txt><span class=nobox>問{no}</span>下の図で、{stmt(given)} です。"
            f"このとき、<span class=nb>{concl}</span> であることを証明しなさい。</div>{svg}</div>")


def proof_rows(sp, lead_of, no):
    items, text = conds(sp)
    t1, t2 = f"△{sp['l1']}", f"△{sp['l2']}"
    eq = "".join(f"<div class='ln eq'><span class=lead>{lead_of(k)}</span><span>{l}＝{r}　…{'①②③'[k]}</span></div>"
                 for k, (l, r) in enumerate(text))
    return (f"<div class=a><div class=ano>問{no}</div><div class=pf2>"
            f"<div class=ln>{t1} と {t2} において、</div>{eq}<div class=ln>①、②、③より、</div>"
            f"<div class=ln><b>{COND[sp['typ']]}</b>から、</div><div class=ln>{t1}≡{t2}</div></div></div>")


def make():
    rnd = random.Random(2026)
    s1, s2 = specs1(rnd), specs2(rnd)
    tips = [
        "ポイント：<b>仮定</b>は問題文に書いてある。「仮定より」のあとにそのまま写して①②③と番号をつける。",
        "ポイント：仮定を3つ写したら、「①、②、③より、（合同条件）から、」。最後の行は<b>結論</b>。",
        "ポイント：「△　と△　において」→「仮定より」①②③→「①、②、③より」合同条件→結論。自分で書こう。",
        "ポイント：仮定は<b>2つだけ</b>。あと1つは<b>図から自分で見つける</b>（共通な辺・対頂角）。",
        "ポイント：見つけた1つには「共通な辺だから」「対頂角は等しいから」と理由を書く。",
        "ポイント：3つがどの合同条件になるかを考えて、自分で書こう。",
    ]
    subs = ["レベル1　仮定が3つ"] * 3 + ["レベル2　仮定が2つ（1つは自分で見つける）"] * 3
    pages, asec = [], []
    ans1 = [proof_rows(sp, lambda k: "仮定より" if k == 0 else "", n + 1) for n, sp in enumerate(s1)]
    ans2 = []
    for n, sp in enumerate(s2):
        svg, f = figure2(sp)
        sp["svg"], sp["f"] = svg, f
        lead = lambda k, f=f, fig=sp["fig"]: LEAD["given"] if k != f else (LEAD["vert"] if fig == "B" else LEAD["side"])  # noqa: E731
        ans2.append(proof_rows(sp, lead, 13 + n).replace("class=a>", "class='a l2'>", 1))
    for p in range(6):
        cs = []
        for j in range(4):
            n = p * 4 + j
            if p < 3:
                sp = s1[n]
                _, text = conds(sp)
                cs.append(cell(n + 1, figure(sp, marks=False), text, f"△{sp['l1']}≡△{sp['l2']}"))
            else:
                sp = s2[n - 12]
                items, text = conds(sp)
                cs.append(cell(n + 1, sp["svg"], [t for k, t in enumerate(text) if k != sp["f"]], f"△{sp['l1']}≡△{sp['l2']}"))
        pages.append(f"<div class=page>{head('合同の証明 その' + str(p + 1), subs[p], score=4)}"
                     f"<div class=tip>{tips[p]}<br>{CONDLINE}</div>"
                     f"<div class=grid><div class=col>{cs[0]}{cs[1]}</div><div class=col>{cs[2]}{cs[3]}</div></div></div>")
        rows = (ans1 + ans2)[p * 4:(p + 1) * 4]
        asec.append({"label": f"その{p + 1}　{subs[p]}", "rows": rows})
    prob = f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
    ans = answer_doc("合同の証明（木曜）", asec, pages=[2, 4])
    return [(prob, "c2_goudou_shoumei_L12_thu.pdf"), (ans, "c2_goudou_shoumei_L12_thu_ans.pdf")]


EXTRA2 = EXTRA + """
.txt { font-size: 10.4pt; line-height: 1.7; min-height: 18mm; }
.nobox { display: inline-block; background: #222; color: #fff; font-weight: 700; font-size: 10pt; border-radius: 1mm;
         padding: 0 1.8mm; margin-right: 1.6mm; line-height: 1.45; }
.nb { font-family: 'Noto Serif CJK JP', serif; }
.fig { margin-top: 0 !important; }
.l2 .lead { width: 37mm; }
"""

if __name__ == "__main__":
    write_pdfs(make(), EXTRA2)
