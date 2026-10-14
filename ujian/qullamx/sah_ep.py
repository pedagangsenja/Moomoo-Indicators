# Pengesahan EP + trail SMA20: S1-S4 dan kepekaan ambang gap/RVOL (set 431)
import sys; sys.path.insert(0,'ujian/qullamx')
from refine import *
def ep_bina(f,gap=10,rv=3,trail='M20',qqq=False):
    out={}
    for t,g0 in f.items():
        C,O,H,L=g0.close,g0.open,g0.high,g0.low
        GAP=(O/C.shift()-1)*100; CLV=(C-L)/(H-L+0.0001); ABAI=(C.shift()/C.shift(63))<1.2
        e=((GAP>=gap)&(g0._rvol>=rv)&ABAI&(CLV>=0.5)).fillna(False); e1=dedup(e,1)
        if qqq: e1&=g0._qok
        g=g0[['open','high','low','close']].copy(); g['sig']=e1; g['stop']=L; g['tgt']=np.nan
        g['exitc']=C<TR[t][trail]; g['rank']=g0._skor.fillna(0); out[t]=g
    return out
def jalan2(arg):
    set_,kw=arg; f=subset(fr,asal,set_); s=ep_bina(f,**kw); T=trades(s); cv=portfolio(T,s)
    return baris2(set_,'QULLAMX-EP','Qullamaggie EP sahaja',nama(kw),T,cv,f,idx,True,'EP; masuk buka H+1; stop LOD; SELL close bawah SMA20')
J=[(s,dict()) for s in ['S1','S2','S3','S4']]+[('431',dict(gap=g,rv=r)) for g,r in [(8,3),(12,3),(10,2),(10,4),(8,2)]]+[('431',dict(qqq=True))]
if __name__=='__main__':
    with Pool(4) as p: rows=p.map(jalan2,J,chunksize=1)
    R=pd.DataFrame(rows,columns=LAJUR2); R.to_csv('ujian/qullamx/sah_ep.csv',index=False)
    print(R[['set','varian','keputusan','skor','cagr','mdd','h1','h2','n','win','ret10','ew_cagr','gate_gagal']].to_string())
