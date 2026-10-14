# Semak logik QULLAMX_harian.mai (BUY/STOP/SELL) lawan enjin trades() untuk EP gap>=8, trail SMA20
import sys; sys.path.insert(0,'ujian/qullamx')
from sah_ep import *
def mai(g):
    C,O,H,L,V=g.close,g.open,g.high,g.low,g.volume.astype(float); M20=C.rolling(20).mean()
    GAP=(O/C.shift()-1)*100; RV=V/V.rolling(50).mean().shift(); CLV=(C-L)/(H-L+0.0001); AB=(C.shift()/C.shift(63))<1.2
    E=((GAP>=8)&(RV>=3)&AB&(CLV>=0.5)).fillna(False).values; BUY=E&~np.r_[False,E[:-1]]
    l,c,m=L.values,C.values,M20.values; ent=[];ex=[];last_b=None;stop=np.nan;last_k=None
    for t in range(len(c)):
        if BUY[t]: last_b=t; stop=l[t]; ent.append(g.index[t]); continue
        if last_b is None or t-last_b<1: continue
        kel=(l[t]<=stop) or (c[t]<m[t])
        if kel and (last_k is None or last_k<last_b): ex.append((g.index[t],'STOP' if l[t]<=stop else 'SELL'))
        if kel: last_k=t
    return ent,ex
f=ep_bina(fr,gap=8); T=trades(f); n_ok=n=0; beza=[]
for t,g in fr.items():
    ent,ex=mai(g); Tt=T[T.ticker==t]
    for r in Tt.itertuples():
        n+=1; e=[x for x in ex if x[0]>=r.sig]
        if e and ((r.why=='henti' and e[0][0]==r.ex and e[0][1]=='STOP') or (r.why=='isyarat keluar' and g.index[g.index.get_loc(e[0][0])+1]==r.ex and e[0][1]=='SELL')): n_ok+=1
        elif r.why!='hujung': beza.append((t,r.sig.date(),r.why,r.ex.date(),e[0] if e else None))
print('dagangan enjin',n,'sepadan',n_ok,'beza',len(beza)); print(beza[:8])
