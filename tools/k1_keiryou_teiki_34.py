"""高1 数学Ⅰ 図形と計量 定期考査対策 第3回・第4回（A3 両面・1パターン2ページ）。
問題 pdf/k1_keiryou_teiki_{n}.pdf と、同じプリントに赤字で答え・途中式を書きこんだ pdf/k1_keiryou_teiki_{n}_ans.pdf を作る。
  cd tools && python3 k1_keiryou_teiki_34.py      （KaTeX は texlib と同じ探し方。見つからなければ npm install katex）
問題データと SymPy の検算は k1_keiryou_teiki_data.py（SETS に第5回…を足せば同じ形で作れる）。
レイアウト：No.1＝左［1］（答えのみ・解答表）、右［2］［3］／No.2＝左［4］［5］(1)(2)、右［5］(3)［6］。学校の 2学期期末考査（前段）と同じ並び・配点。"""
import math, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from texlib import tex, doc as texdoc
from k1_keiryou_teiki_data import SETS, check
OUT = Path(__file__).resolve().parent.parent / "pdf"
C="①②③④⑤⑥⑦⑧⑨"
CSS=r"""
@page{size:A3;margin:0}*{box-sizing:border-box}
body{margin:0;font-family:'Noto Sans CJK JP';font-size:13pt;line-height:1.45;color:#000;-webkit-print-color-adjust:exact}
.page{page-break-after:always;width:297mm;height:420mm;padding:12mm 14mm 8mm;display:flex;flex-direction:column;overflow:hidden}
.hd{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.8pt solid #000;padding-bottom:2mm}
.hd .t{white-space:nowrap;font-size:15pt;font-weight:600}.hd .n{font-size:12pt;white-space:nowrap}
.cols{flex:1;display:flex;min-height:0;margin-top:3mm}
.col{flex:1 1 0;min-width:0;display:flex;flex-direction:column}
.col.l{padding-right:6mm;border-right:.9pt solid #000}.col.r{padding-left:6mm}
.note{font-size:12pt;margin:0 0 3mm}
.big{display:flex;gap:2mm;align-items:flex-start;font-weight:500;margin-top:1mm}
.big .no{border:1.2pt solid #000;width:6.5mm;height:6.5mm;display:inline-flex;align-items:center;justify-content:center;font-size:10.5pt;flex:none;margin-top:.4mm}
.pt{font-size:11pt;font-weight:400;margin-left:auto;white-space:nowrap;padding-left:2mm}
.sub{margin:1.5mm 0 1mm 2mm}.subh{display:flex;align-items:baseline}
.box{border:1.1pt solid #000;flex:1 1 0;min-height:0;margin:0 0 3mm 2mm;position:relative;padding:2mm 3mm}
.gr{display:grid;grid-template-columns:1fr 1fr 1fr;margin:1.5mm 0 3mm 7mm;row-gap:2.5mm}.gr>div{white-space:nowrap}.gr.g2{grid-template-columns:1fr 1fr;row-gap:2mm}
.q5{margin:1.5mm 0 3mm 7mm}.q5>div{margin-bottom:2mm}
table.trig{border-collapse:collapse;margin:1mm auto 4mm;font-size:12pt}table.trig td{border:.9pt solid #000;padding:.6mm 5mm;text-align:center}
table.ans{border-collapse:collapse;width:100%;table-layout:fixed}
table.ans td{border:1pt solid #000;height:13.5mm;text-align:center;padding:0}
.pair{flex:1 1 0;min-height:0;display:flex;gap:3mm}.half{flex:1 1 0;min-width:0;display:flex;flex-direction:column}.foot{text-align:center;font-size:11pt;margin-top:2mm}.fig{position:absolute;right:3mm;top:3mm}
.red{color:#d40000}table.ans .red .katex{font-size:.9em}.red .katex{color:#d40000}
.sol{font-size:13.5pt;line-height:1.6}.sol>div{margin-bottom:1mm}.sol .katex{font-size:1em}
.box .fig~.sol{padding-right:40mm}
"""
ANS=False
def red(x): return f'<span class="red">{x}</span>' if ANS else ''
def big(n,txt,pt=""):
    return f'<div class="big"><span class="no">{n}</span><span>{txt}</span>'+(f'<span class="pt">&lt;{pt}&gt;</span>' if pt else '')+'</div>'
def boxed(label,txt,sol,pt="",extra="",grow=1):
    p=f'<span class="pt">&lt;{pt}&gt;</span>' if pt else ''
    body=('<div class="sol red">'+''.join(f'<div>{l}</div>' for l in sol)+'</div>') if ANS else ''
    return f'<div class="sub subh"><span>({label})&ensp;{txt}</span>{p}</div><div class="box" style="flex-grow:{grow}">{extra}{body}</div>'
def pair(a,b,grow=1):
    return f'<div class="pair" style="flex-grow:{grow}"><div class="half">{a}</div><div class="half">{b}</div></div>'
def gridq(items,cls="gr"): return f'<div class="{cls}">'+''.join(f'<div>{C[i]}&ensp;${q}$</div>' for i,q in enumerate(items))+'</div>'
def anstable():
    A=lambda key: [x[1] for x in S[key]]
    a1,a2,a3,a4,a5=A('q11'),[r"\theta="+x for x in A('q12')],A('q13'),A('q14'),[r"S="+x for x in A('q15')]
    cell=lambda v: f'<td>{red("$"+v+"$")}</td>'
    def rows(g,vals,n):
        out=''
        for i in range(n):
            out+='<tr>'+(f'<td rowspan="{n}">({g})</td>' if i==0 else '')+''.join(f'<td>{C[i*3+j]}</td>'+cell(vals[i*3+j]) for j in range(3))+'</tr>'
        return out
    cg='<colgroup><col style="width:9mm">'+'<col style="width:7mm"><col>'*3+'</colgroup>'
    t1='<table class="ans">'+cg+rows(1,a1,3)+rows(2,a2,2)+rows(3,a3,1)+rows(4,a4,1)+'</table>'
    t2=f'<table class="ans" style="margin-top:-1pt"><colgroup><col style="width:9mm"><col style="width:7mm"><col><col style="width:7mm"><col></colgroup><tr><td>(5)</td><td>①</td>{cell(a5[0])}<td>②</td>{cell(a5[1])}</tr></table>'
    return t1+t2
def tri_svg(a,b,c):
    x=(c*c+a*a-b*b)/(2*a); y=math.sqrt(c*c-x*x); k=150/max(a,x,a-x); h=y*k
    x0=18+max(0,-x*k); B=(x0,h+18);Cc=(x0+a*k,h+18);A=(x0+x*k,18); w=max(Cc[0],A[0])+20
    m=lambda p,q:((p[0]+q[0])/2,(p[1]+q[1])/2); ma,mb,mc=m(B,Cc),m(A,Cc),m(A,B)
    t=lambda x,y,s:f'<text x="{x:.1f}" y="{y:.1f}" font-size="16" text-anchor="middle" font-family="Noto Sans CJK JP">{s}</text>'
    return (f'<svg class="fig" width="{w:.0f}" height="{h+40:.0f}"><polygon points="{A[0]:.1f},{A[1]:.1f} {B[0]:.1f},{B[1]:.1f} {Cc[0]:.1f},{Cc[1]:.1f}" fill="none" stroke="#000" stroke-width="1.2"/>'
            +t(A[0],A[1]-5,"A")+t(B[0]-9,B[1]+6,"B")+t(Cc[0]+9,Cc[1]+6,"C")+t(ma[0],ma[1]+15,a)+t(mb[0]+9,mb[1],b)+t(mc[0]-9,mc[1],c)+'</svg>')
def page():
    TBL=S['table']
    tbl='<table class="trig"><tr><td>$\\theta$</td><td>$\\sin\\theta$</td><td>$\\cos\\theta$</td><td>$\\tan\\theta$</td></tr>'+''.join(f'<tr><td>${t}^\\circ$</td>'+''.join(f'<td>{v:.4f}</td>' for v in TBL[t])+'</tr>' for t in TBL)+'</table>'
    q2=lambda x:f'${x[0]}$ のとき，${x[1]}$ の値を求めよ。'
    L1=('<p class="note">「答えのみ」以外の問題は必ず途中式を書くこと。答案は必ず枠内に記入せよ。</p>'
       +big(1,'次の各問いに答え，解答欄に<u>答えのみ</u>記入せよ。','知・技 各2点×23問=46点')
       +'<div class="sub">(1)&ensp;次の三角比の値を求めよ。</div>'+gridq([x[0] for x in S['q11']])
       +'<div class="sub">(2)&ensp;$0^\\circ\\leqq\\theta\\leqq 180^\\circ$ のとき，次の等式を満たす $\\theta$ を求めよ。</div>'+gridq([x[0] for x in S['q12']],"gr g2")
       +'<div class="sub">(3)&ensp;次の三角比を $45^\\circ$ 以下の角の三角比で表せ。</div>'+gridq([x[0] for x in S['q13']])
       +'<div class="sub">(4)&ensp;次の値を，三角比の表を用いて求めよ。</div>'+gridq([x[0] for x in S['q14']])+tbl
       +'<div class="sub">(5)&ensp;次のような $\\triangle$ABC の面積 $S$ を求めよ。</div><div class="q5">'+''.join(f'<div>{C[i]}&ensp;${x[0]}$</div>' for i,x in enumerate(S['q15']))+'</div>'
       +'<div style="flex:1"></div>'+anstable())
    R1=(big(2,'$90^\\circ<\\theta<180^\\circ$ とする。$\\sin\\theta,\\ \\cos\\theta,\\ \\tan\\theta$ のうちの1つが次の値のとき，残り2つの値を求めよ。','思・判・表 各6点')
       +boxed(1,q2(S['q2'][0]),S['sol2'][0],grow=1.25)+boxed(2,q2(S['q2'][1]),S['sol2'][1],grow=1.25)
       +big(3,'$\\triangle$ABC の外接円の半径を $R$ とする。次のものを求めよ。','思・判・表 各5点')
       +boxed(1,S['q3'][0],S['sol3'][0])+boxed(2,S['q3'][1],S['sol3'][1]))
    a,b,c=S['tri']
    L2=(big(4,'$\\triangle$ABC において，次のものを求めよ。','思・判・表 6点')+boxed(1,S['q4'],S['sol4'])
       +big(5,'$\\triangle$ABC において，次のものを求めよ。','思・判・表 各6点')
       +boxed(1,S['q5'][0],S['sol5'][0])+boxed(2,S['q5'][1],S['sol5'][1]))
    R2=(boxed(3,S['q5'][2],S['sol5'][2],grow=1.1)
       +big(6,f'$\\triangle$ABC において，3辺の長さが $a={a},\\ b={b},\\ c={c}$ であるとき，次のものを求めよ。')
       +boxed(1,'$\\cos A$ の値',S['sol6'][0],'思・判・表 3点',tri_svg(a,b,c),grow=1)
       +boxed(2,'$\\sin A$ の値',S['sol6'][1],'思・判・表 3点',grow=1)
       +boxed(3,'面積 $S$',S['sol6'][2],'思・判・表 2点',grow=.9))
    t=lambda n:f'数学Ⅰ 図形と計量　定期考査対策 第{S["no"]}回 &lt;No.{n}&gt;'+('　<span class="red">【解答】</span>' if ANS else '')
    nm=lambda n:'1年(　　)組(　　)番 名前(　　　　　　　　)'+('　　　点' if n==1 else '')
    pg=lambda n,L,R:f'<div class="page"><div class="hd"><div class="t">{t(n)}</div><div class="n">{nm(n)}</div></div><div class="cols"><div class="col l">{L}</div><div class="col r">{R}</div></div><div class="foot">-{n}-</div></div>'
    return pg(1,L1,R1)+pg(2,L2,R2)
def doc(body):
    return texdoc(CSS, re.sub(r"\$(.+?)\$", lambda m: tex(m.group(1)), body))

if __name__ == "__main__":
    check()
    nos = [int(a) for a in sys.argv[1:]] or sorted(SETS)
    bad = 0
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page()
        for no in nos:
            S = SETS[no]
            for ANS, name in [(False, f"k1_keiryou_teiki_{no}"), (True, f"k1_keiryou_teiki_{no}_ans")]:
                pg.set_content(doc(page())); pg.wait_for_timeout(300); pg.evaluate("document.fonts.ready")
                over = pg.evaluate("""()=>[...document.querySelectorAll('.col,.box')].filter(e=>e.scrollHeight>e.clientHeight+1).length""")
                if over: bad += 1; print("!! はみ出し", name, over)
                pg.pdf(path=str(OUT / f"{name}.pdf"), prefer_css_page_size=True, print_background=True)
                print(name + ".pdf")
        br.close()
    if bad: raise SystemExit("はみ出しあり")
