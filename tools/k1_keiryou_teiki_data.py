"""高1 数学Ⅰ 図形と計量 定期考査対策（第3回〜）の問題データと答え。python3 k1_keiryou_teiki_data.py で SymPy 検算"""
import math
from sympy import *
d=lambda x: x*pi/180
S2,S3=sqrt(2),sqrt(3)
def tbl(*ts): return {t:tuple(round(f(math.radians(t)),4) for f in (math.sin,math.cos,math.tan)) for t in ts}
TBL=tbl(18,39,76)
P3=dict(no=3,table=TBL,
 q11=[(r"\sin 30^\circ",r"\dfrac{1}{2}",sin(d(30)),Rational(1,2)),(r"\tan 45^\circ",r"1",tan(d(45)),1),(r"\cos 60^\circ",r"\dfrac{1}{2}",cos(d(60)),Rational(1,2)),
      (r"\cos 150^\circ",r"-\dfrac{\sqrt{3}}{2}",cos(d(150)),-S3/2),(r"\tan 120^\circ",r"-\sqrt{3}",tan(d(120)),-S3),(r"\sin 135^\circ",r"\dfrac{1}{\sqrt{2}}",sin(d(135)),1/S2),
      (r"\tan 0^\circ",r"0",tan(0),0),(r"\sin 90^\circ",r"1",sin(d(90)),1),(r"\cos 90^\circ",r"0",cos(d(90)),0)],
 q12=[(r"\sin\theta=\dfrac{\sqrt{3}}{2}",r"60^\circ,\ 120^\circ",sin,S3/2,[60,120]),(r"\cos\theta=\dfrac{\sqrt{3}}{2}",r"30^\circ",cos,S3/2,[30]),(r"\tan\theta=-\dfrac{1}{\sqrt{3}}",r"150^\circ",tan,-1/S3,[150]),
      (r"\cos\theta=0",r"90^\circ",cos,0,[90]),(r"\tan\theta=-\sqrt{3}",r"120^\circ",tan,-S3,[120]),(r"\cos\theta=-\dfrac{1}{\sqrt{2}}",r"135^\circ",cos,-1/S2,[135])],
 q13=[(r"\sin 68^\circ",r"\cos 22^\circ"),(r"\cos 77^\circ",r"\sin 13^\circ"),(r"\tan 54^\circ",r"\dfrac{1}{\tan 36^\circ}")],
 q14=[(r"\sin 162^\circ",f"{TBL[18][0]:.4f}"),(r"\cos 141^\circ",f"-{TBL[39][1]:.4f}"),(r"\tan 104^\circ",f"-{TBL[76][2]:.4f}")],
 q15=[(r"b=6,\ c=7,\ A=150^\circ",r"\dfrac{21}{2}"),(r"1\,\text{辺の長さが}\,10\,\text{の正三角形}\,\text{ABC}",r"25\sqrt{3}")],
 q2=[(r"\cos\theta=-\dfrac{1}{3}",r"\sin\theta,\ \tan\theta"),(r"\tan\theta=-\dfrac{\sqrt{5}}{2}",r"\cos\theta,\ \sin\theta")],
 q3=[r"$c=4,\ C=30^\circ$ のとき $R$",r"$a=3\sqrt{3},\ R=3$ のとき $A$"],
 q4=r"$a=4,\ A=30^\circ,\ B=135^\circ$ のとき，辺 CA の長さ $b$",
 q5=[r"$a=2\sqrt{3},\ c=4,\ B=30^\circ$ のとき，辺 CA の長さ $b$",r"$b=2,\ c=2\sqrt{3},\ A=150^\circ$ のとき，辺 BC の長さ $a$",r"$a=5,\ b=7,\ c=8$ のとき，$\cos B$ の値と $B$"],
 tri=(4,3,2),
 sol2=[[r"$\sin^2\theta=1-\cos^2\theta=1-\dfrac{1}{9}=\dfrac{8}{9}$",r"$\sin\theta>0$ より $\sin\theta=\boldsymbol{\dfrac{2\sqrt{2}}{3}}$",r"$\tan\theta=\dfrac{2\sqrt{2}}{3}\div\left(-\dfrac{1}{3}\right)=\boldsymbol{-2\sqrt{2}}$"],
       [r"$\dfrac{1}{\cos^2\theta}=1+\tan^2\theta=1+\dfrac{5}{4}=\dfrac{9}{4}$",r"$\cos\theta<0$ より $\cos\theta=\boldsymbol{-\dfrac{2}{3}}$",r"$\sin\theta=\tan\theta\cos\theta=\left(-\dfrac{\sqrt{5}}{2}\right)\times\left(-\dfrac{2}{3}\right)=\boldsymbol{\dfrac{\sqrt{5}}{3}}$"]],
 sol3=[[r"正弦定理より $\dfrac{4}{\sin 30^\circ}=2R$",r"$2R=4\div\dfrac{1}{2}=8$　　$R=\boldsymbol{4}$"],
       [r"正弦定理より $\dfrac{3\sqrt{3}}{\sin A}=2\times 3$",r"$\sin A=\dfrac{3\sqrt{3}}{6}=\dfrac{\sqrt{3}}{2}$",r"$0^\circ\lt A\lt 180^\circ$ より $A=\boldsymbol{60^\circ,\ 120^\circ}$"]],
 sol4=[r"正弦定理より $\dfrac{4}{\sin 30^\circ}=\dfrac{b}{\sin 135^\circ}$",r"$b=4\div\dfrac{1}{2}\times\dfrac{1}{\sqrt{2}}=8\times\dfrac{1}{\sqrt{2}}=\boldsymbol{4\sqrt{2}}$"],
 sol5=[[r"余弦定理より",r"$b^2=(2\sqrt{3})^2+4^2-2\cdot 2\sqrt{3}\cdot 4\cdot\cos 30^\circ$",r"$=12+16-24=4$",r"$b>0$ より $b=\boldsymbol{2}$"],
       [r"余弦定理より",r"$a^2=2^2+(2\sqrt{3})^2-2\cdot 2\cdot 2\sqrt{3}\cdot\cos 150^\circ$",r"$=4+12+12=28$",r"$a>0$ より $a=\boldsymbol{2\sqrt{7}}$"],
       [r"余弦定理より",r"$\cos B=\dfrac{5^2+8^2-7^2}{2\cdot 5\cdot 8}=\dfrac{40}{80}=\boldsymbol{\dfrac{1}{2}}$",r"$0^\circ\lt B\lt 180^\circ$ より $B=\boldsymbol{60^\circ}$"]],
 sol6=[[r"$\cos A=\dfrac{3^2+2^2-4^2}{2\cdot 3\cdot 2}=\dfrac{-3}{12}=\boldsymbol{-\dfrac{1}{4}}$"],
       [r"$\sin A>0$ より",r"$\sin A=\sqrt{1-\left(-\dfrac{1}{4}\right)^2}$",r"$=\boldsymbol{\dfrac{\sqrt{15}}{4}}$"],
       [r"$S=\dfrac{1}{2}bc\sin A$",r"$=\dfrac{1}{2}\cdot 3\cdot 2\cdot\dfrac{\sqrt{15}}{4}$",r"$=\boldsymbol{\dfrac{3\sqrt{15}}{4}}$"]],
)

TBL4=tbl(26,47,68)
P4=dict(no=4,table=TBL4,
 q11=[(r"\cos 30^\circ",r"\dfrac{\sqrt{3}}{2}",cos(d(30)),S3/2),(r"\tan 60^\circ",r"\sqrt{3}",tan(d(60)),S3),(r"\sin 45^\circ",r"\dfrac{1}{\sqrt{2}}",sin(d(45)),1/S2),
      (r"\tan 150^\circ",r"-\dfrac{1}{\sqrt{3}}",tan(d(150)),-1/S3),(r"\sin 120^\circ",r"\dfrac{\sqrt{3}}{2}",sin(d(120)),S3/2),(r"\cos 135^\circ",r"-\dfrac{1}{\sqrt{2}}",cos(d(135)),-1/S2),
      (r"\cos 180^\circ",r"-1",cos(pi),-1),(r"\sin 0^\circ",r"0",sin(0),0),(r"\cos 0^\circ",r"1",cos(0),1)],
 q12=[(r"\sin\theta=\dfrac{1}{2}",r"30^\circ,\ 150^\circ",sin,Rational(1,2),[30,150]),(r"\cos\theta=-\dfrac{\sqrt{3}}{2}",r"150^\circ",cos,-S3/2,[150]),(r"\tan\theta=1",r"45^\circ",tan,1,[45]),
      (r"\sin\theta=0",r"0^\circ,\ 180^\circ",sin,0,[0,180]),(r"\cos\theta=\dfrac{1}{2}",r"60^\circ",cos,Rational(1,2),[60]),(r"\tan\theta\,\text{が定義されない}",r"90^\circ",None,None,[90])],
 q13=[(r"\sin 74^\circ",r"\cos 16^\circ"),(r"\cos 59^\circ",r"\sin 31^\circ"),(r"\tan 81^\circ",r"\dfrac{1}{\tan 9^\circ}")],
 q14=[(r"\sin 154^\circ",f"{TBL4[26][0]:.4f}"),(r"\cos 133^\circ",f"-{TBL4[47][1]:.4f}"),(r"\tan 112^\circ",f"-{TBL4[68][2]:.4f}")],
 q15=[(r"a=4,\ b=9,\ C=45^\circ",r"9\sqrt{2}"),(r"1\,\text{辺の長さが}\,12\,\text{の正三角形}\,\text{ABC}",r"36\sqrt{3}")],
 q2=[(r"\sin\theta=\dfrac{3}{4}",r"\cos\theta,\ \tan\theta"),(r"\tan\theta=-\dfrac{3}{4}",r"\cos\theta,\ \sin\theta")],
 q3=[r"$a=6\sqrt{2},\ A=135^\circ$ のとき $R$",r"$c=2\sqrt{3},\ R=2$ のとき $C$"],
 q4=r"$b=2\sqrt{6},\ B=60^\circ,\ C=45^\circ$ のとき，辺 AB の長さ $c$",
 q5=[r"$a=4,\ c=3\sqrt{2},\ B=45^\circ$ のとき，辺 CA の長さ $b$",r"$b=3,\ c=\sqrt{2},\ A=135^\circ$ のとき，辺 BC の長さ $a$",r"$a=\sqrt{7},\ b=2,\ c=3$ のとき，$\cos A$ の値と $A$"],
 tri=(5,3,7),
 sol2=[[r"$\cos^2\theta=1-\sin^2\theta=1-\dfrac{9}{16}=\dfrac{7}{16}$",r"$\cos\theta<0$ より $\cos\theta=\boldsymbol{-\dfrac{\sqrt{7}}{4}}$",r"$\tan\theta=\dfrac{3}{4}\div\left(-\dfrac{\sqrt{7}}{4}\right)=\boldsymbol{-\dfrac{3}{\sqrt{7}}}$　$\left(=-\dfrac{3\sqrt{7}}{7}\right)$"],
       [r"$\dfrac{1}{\cos^2\theta}=1+\tan^2\theta=1+\dfrac{9}{16}=\dfrac{25}{16}$",r"$\cos\theta<0$ より $\cos\theta=\boldsymbol{-\dfrac{4}{5}}$",r"$\sin\theta=\tan\theta\cos\theta=\left(-\dfrac{3}{4}\right)\times\left(-\dfrac{4}{5}\right)=\boldsymbol{\dfrac{3}{5}}$"]],
 sol3=[[r"正弦定理より $\dfrac{6\sqrt{2}}{\sin 135^\circ}=2R$",r"$2R=6\sqrt{2}\div\dfrac{1}{\sqrt{2}}=12$　　$R=\boldsymbol{6}$"],
       [r"正弦定理より $\dfrac{2\sqrt{3}}{\sin C}=2\times 2$",r"$\sin C=\dfrac{2\sqrt{3}}{4}=\dfrac{\sqrt{3}}{2}$",r"$0^\circ\lt C\lt 180^\circ$ より $C=\boldsymbol{60^\circ,\ 120^\circ}$"]],
 sol4=[r"正弦定理より $\dfrac{2\sqrt{6}}{\sin 60^\circ}=\dfrac{c}{\sin 45^\circ}$",r"$c=2\sqrt{6}\div\dfrac{\sqrt{3}}{2}\times\dfrac{1}{\sqrt{2}}=4\sqrt{2}\times\dfrac{1}{\sqrt{2}}=\boldsymbol{4}$"],
 sol5=[[r"余弦定理より",r"$b^2=4^2+(3\sqrt{2})^2-2\cdot 4\cdot 3\sqrt{2}\cdot\cos 45^\circ$",r"$=16+18-24=10$",r"$b>0$ より $b=\boldsymbol{\sqrt{10}}$"],
       [r"余弦定理より",r"$a^2=3^2+(\sqrt{2})^2-2\cdot 3\cdot\sqrt{2}\cdot\cos 135^\circ$",r"$=9+2+6=17$",r"$a>0$ より $a=\boldsymbol{\sqrt{17}}$"],
       [r"余弦定理より",r"$\cos A=\dfrac{2^2+3^2-(\sqrt{7})^2}{2\cdot 2\cdot 3}=\dfrac{6}{12}=\boldsymbol{\dfrac{1}{2}}$",r"$0^\circ\lt A\lt 180^\circ$ より $A=\boldsymbol{60^\circ}$"]],
 sol6=[[r"$\cos A=\dfrac{3^2+7^2-5^2}{2\cdot 3\cdot 7}=\dfrac{33}{42}=\boldsymbol{\dfrac{11}{14}}$"],
       [r"$\sin A>0$ より",r"$\sin A=\sqrt{1-\left(\dfrac{11}{14}\right)^2}=\sqrt{\dfrac{75}{196}}$",r"$=\boldsymbol{\dfrac{5\sqrt{3}}{14}}$"],
       [r"$S=\dfrac{1}{2}bc\sin A$",r"$=\dfrac{1}{2}\cdot 3\cdot 7\cdot\dfrac{5\sqrt{3}}{14}$",r"$=\boldsymbol{\dfrac{15\sqrt{3}}{4}}$"]],
)
SETS={3:P3,4:P4}

def check():
    ok=lambda a,b: simplify(a-b)==0
    law=lambda p,q,a: sqrt(p**2+q**2-2*p*q*cos(d(a)))
    for P in SETS.values():
        for *_,v,e in P['q11']: assert ok(v,e),(P['no'],v,e)
        for r in P['q12']:
            if r[2] is None: continue
            sol=[t for t in range(0,181,15) if not(r[2] is tan and t==90) and ok(r[2](d(t)),r[3])]; assert sol==r[4],(r[0],sol)
        a,b,c=P['tri']; assert a<b+c and b<a+c and c<a+b
    # 第3回
    assert ok(sin(d(68)),cos(d(22))) and ok(cos(d(77)),sin(d(13))) and ok(tan(d(54)),1/tan(d(36)))
    assert ok(6*7*sin(d(150))/2,Rational(21,2)) and ok(S3/4*100,25*S3)
    s_=sqrt(1-Rational(1,9)); assert ok(s_,2*S2/3) and ok(s_/(-Rational(1,3)),-2*S2)
    c=-1/sqrt(1+Rational(5,4)); assert ok(c,-Rational(2,3)) and ok(-sqrt(5)/2*c,sqrt(5)/3)
    assert ok(4/sin(d(30))/2,4) and ok(3*S3/6,S3/2) and ok(4/sin(d(30))*sin(d(135)),4*S2)
    assert ok(law(2*S3,4,30),2) and ok(law(2,2*S3,150),2*sqrt(7)) and Rational(25+64-49,80)==Rational(1,2)
    C=Rational(9+4-16,12); assert C==Rational(-1,4) and ok(sqrt(1-C**2),sqrt(15)/4) and ok(3*2*sqrt(1-C**2)/2,3*sqrt(15)/4)
    # 第4回
    assert ok(sin(d(74)),cos(d(16))) and ok(cos(d(59)),sin(d(31))) and ok(tan(d(81)),1/tan(d(9)))
    assert ok(4*9*sin(d(45))/2,9*S2) and ok(S3/4*144,36*S3)
    c=-sqrt(1-Rational(9,16)); assert ok(c,-sqrt(7)/4) and ok(Rational(3,4)/c,-3/sqrt(7))
    c=-1/sqrt(1+Rational(9,16)); assert ok(c,-Rational(4,5)) and ok(-Rational(3,4)*c,Rational(3,5))
    assert ok(6*S2/sin(d(135))/2,6) and ok(2*S3/4,S3/2) and ok(2*sqrt(6)/sin(d(60))*sin(d(45)),4)
    assert ok(law(4,3*S2,45),sqrt(10)) and ok(law(3,S2,135),sqrt(17)) and Rational(4+9-7,12)==Rational(1,2)
    C=Rational(9+49-25,42); assert C==Rational(11,14) and ok(sqrt(1-C**2),5*S3/14) and ok(3*7*sqrt(1-C**2)/2,15*S3/4)
    for P in SETS.values():   # 表の値（4けた）
        for t,(a,b,c) in P['table'].items():
            assert abs(math.sin(math.radians(t))-a)<6e-5 and abs(math.cos(math.radians(t))-b)<6e-5 and abs(math.tan(math.radians(t))-c)<6e-5
    print("全問OK", P4['q14'])

if __name__=="__main__":
    check()
