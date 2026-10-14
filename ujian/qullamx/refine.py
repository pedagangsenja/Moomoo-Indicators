# QULLAMX refine: grid atas enjin v1.2 (logik teras tidak diubah). Jalankan dari akar repo.
import sys; sys.path.insert(0,'ujian/qullamx')
from tambahan import *
import warnings, itertools, pickle; warnings.filterwarnings('ignore')
from multiprocessing import Pool
fr,idx,asal=muat()
q=idx['QQQ'].close; qm10=q.rolling(10).mean(); qm20=q.rolling(20).mean()
QOK=(qm10>qm20)&(qm10>qm10.shift())&(qm20>qm20.shift())

TR={}
for t,g in fr.items():
    C,H,L,O,V=g.close,g.high,g.low,g.open,g.volume.astype(float)
    E10=C.ewm(span=10,adjust=False).mean(); M10=C.rolling(10).mean(); M20=C.rolling(20).mean()
    ADR=100*((H/L).rolling(20).mean()-1); CLV=(C-L)/(H-L+0.0001)
    TOK=(M10>M20)&(M10>M10.shift())&(M20>M20.shift())
    G3=C/C.rolling(63).min()
    MOM=np.where(G3>=1.30,4,np.where(G3>=1.15,2,0))
    SURF=np.where((C>E10)&TOK,4,np.where((C>M20)&(M20>M20.shift()),2,0))
    RK=((H.rolling(6).max()-L.rolling(6).min())/C*100)/ADR
    KETAT=np.where(RK<=1.5,4,np.where(RK<=2.5,2,0))
    VK=V.rolling(5).mean()/V.rolling(50).mean()
    KERING=np.where(VK<=0.7,4,np.where(VK<=0.9,2,0))
    ADRS=np.where(ADR>=5,4,np.where(ADR>=3.5,2,0))
    SKOR=pd.Series(MOM+SURF+KETAT+KERING+ADRS,index=g.index).astype(float)
    RVOL=V/V.rolling(50).mean().shift()
    g['_bo']=((C>H.rolling(10).max().shift())&(CLV>=0.5)&TOK).fillna(False)
    g['_pskor']=SKOR.shift().rolling(5).max()
    g['_stopw']=(C-L)/C*100; g['_adr']=ADR; g['_skor']=SKOR; g['_rvol']=RVOL
    GAP=(O/C.shift()-1)*100; ABAI=(C.shift()/C.shift(63))<1.2
    g['_ep']=((GAP>=10)&(RVOL>=3)&ABAI&(CLV>=0.5)).fillna(False)
    TR[t]={'E10':E10,'M10':M10,'M20':M20}
    g['_qok']=QOK.reindex(g.index).fillna(False).astype(bool)

def dedup(s,n):
    s=s.fillna(False).astype(bool); r=s.copy()
    for k in range(1,n+1): r&=~s.shift(k).fillna(False).astype(bool)
    return r

def bina(f,bo=True,ep=True,qqq=False,trail='E10',amb=14,bovol=0.0,eprank=False,adrmin=0.0):
    out={}
    for t,g0 in f.items():
        g=g0[['open','high','low','close']].copy()
        buy=g0._bo&(g0._pskor>=amb)&(g0._stopw<=g0._adr)&(g0._rvol>=bovol)&(g0._adr>=adrmin)
        b1=dedup(buy,3); e1=dedup(g0._ep,1)
        s=pd.Series(False,index=g.index)
        if bo: s|=b1
        if ep: s|=e1
        if qqq: s&=g0._qok
        g['sig']=s; g['stop']=g0.low; g['tgt']=np.nan
        g['exitc']=g0.close<TR[t][trail]
        g['rank']=g0._skor.fillna(0)+(100*e1 if eprank else 0)
        out[t]=g
    return out


def nama(kw): return ' '.join(f'{k}={v}' for k,v in kw.items())
def jalan(arg):
    set_,kw=arg
    f=subset(fr,asal,set_); s=bina(f,**kw); T=trades(s); cv=portfolio(T,s)
    return baris2(set_,'QULLAMX-R','Qullamaggie BO+EP refine',nama(kw),T,cv,f,idx,True,'grid refine; masuk buka H+1; stop LOD; SELL close bawah trail')

GRID=[dict(trail=tr,amb=a,qqq=qq,bovol=bv,eprank=er) for tr,a,qq,bv,er in
      itertools.product(['E10','M10','M20'],[14,16],[False,True],[0.0,1.5],[False,True])]
GRID+=[dict(bo=False,trail=tr) for tr in ['E10','M10','M20']]
if __name__=='__main__':
    with Pool(4) as p: rows=p.map(jalan,[('431',kw) for kw in GRID],chunksize=1)
    R=pd.DataFrame(rows,columns=LAJUR2); R.to_csv('ujian/qullamx/grid431.csv',index=False)
    print(R[['varian','keputusan','skor','cagr','mdd','mar','h1','h2','n','win','gate_gagal']].sort_values('mar',ascending=False).to_string())
