import sys; sys.path.insert(0,'ujian/qullamx')
from tambahan import *
import warnings; warnings.filterwarnings('ignore')
fr,idx,asal=muat()

# Penapis QQQ (V3): SMA10>SMA20 dan kedua-duanya naik
q=idx['QQQ'].close; qm10=q.rolling(10).mean(); qm20=q.rolling(20).mean()
QOK=(qm10>qm20)&(qm10>qm10.shift())&(qm20>qm20.shift())

# Kira komponen indikator QULLAMX (kod awal) sekali bagi setiap saham
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
    BO=(C>H.rolling(10).max().shift())&(CLV>=0.5)
    SIAP=TOK&(SKOR.shift().rolling(5).max()>=14)&BO
    STOPW=(C-L)/C*100
    GAP=(O/C.shift()-1)*100; RVOL=V/V.rolling(50).mean().shift()
    ABAI=(C.shift()/C.shift(63))<1.2
    EP=(GAP>=10)&(RVOL>=3)&ABAI&(CLV>=0.5)
    g['_siap']=SIAP.fillna(False); g['_stopw']=STOPW; g['_adr']=ADR; g['_skor']=SKOR
    g['_ep']=EP.fillna(False); g['_e10']=E10; g['_m20']=M20
    g['_qok']=QOK.reindex(g.index).fillna(False).astype(bool)

def dedup(s,n):
    s=s.fillna(False).astype(bool); r=s.copy()
    for k in range(1,n+1): r&=~s.shift(k).fillna(False).astype(bool)
    return r

def sedia(bo=True,ep=True,qqq=False,trail='E10',stopx=1.0):
    for g in fr.values():
        for k in ['sig','stop','tgt','exitc','rank']:
            if k in g: del g[k]
        buy=g._siap&(g._stopw<=stopx*g._adr)
        b1=dedup(buy,3); e1=dedup(g._ep,1)
        s=(b1 if bo else False)|(e1 if ep else False)
        if not isinstance(s,pd.Series): s=pd.Series(False,index=g.index)
        if qqq: s=s&g._qok
        g['sig']=s; g['stop']=g.low; g['tgt']=np.nan
        g['exitc']=g.close<(g._e10 if trail=='E10' else g._m20)
        g['rank']=g._skor.fillna(0)

AND='Andaian saya: rank=skor 0-20 hari isyarat; SELL = close pertama bawah garis trail; masuk buka H+1'
VAR=[('V0 Indikator penuh (BO+EP, LOD, EMA10)',dict(),AND),
     ('V1 Breakout sahaja',dict(ep=False),AND),
     ('V2 EP sahaja',dict(bo=False),AND),
     ('V3 V0 + penapis QQQ MA10>MA20 naik',dict(qqq=True),AND+'; penapis QQQ SMA'),
     ('V4 V0 trail SMA20',dict(trail='M20'),AND),
     ('V5 V0 stop LOD <=0.5 ADR',dict(stopx=0.5),AND)]
rows=[]; TT={}
for nm,kw,cat in VAR:
    sedia(**kw); f=fr; T=trades(f); cv=portfolio(T,f); TT[nm]=(T,cv)
    rows.append(baris2('431','QULLAMX','Qullamaggie BO+EP (indikator QULLAMX)',nm,T,cv,f,idx,True,cat)); print(nm,rows[-1]['keputusan'],rows[-1]['cagr'],rows[-1]['mdd'],rows[-1]['n'],flush=True)
R=pd.DataFrame(rows,columns=LAJUR2)
ok=R[R.keputusan!='DITOLAK']
best=(ok.sort_values('skor',ascending=False) if len(ok) else R.sort_values('cagr',ascending=False)).varian.iloc[0]
pilih=[best]+[v for v in ok.varian if v!=best]
for nm,kw,cat in VAR:
    if nm not in pilih: continue
    sedia(**kw)
    for s in SETS:
        f=subset(fr,asal,s); T=trades(f); cv=portfolio(T,f)
        rows.append(baris2(s,'QULLAMX','Qullamaggie BO+EP (indikator QULLAMX)',nm,T,cv,f,idx,True,cat)); print(s,nm,rows[-1]['keputusan'],rows[-1]['cagr'],flush=True)
R=pd.DataFrame(rows,columns=LAJUR2); R.to_csv('ujian/qullamx/QULLAMX.csv',index=False)
import pickle; pickle.dump({k:v for k,v in TT.items()},open('ujian/qullamx/tt.pkl','wb'))
B=penanda(idx,fr); print({k:(round(v['cagr'],4),round(v['mdd'],4),round(v['h1'],4),round(v['h2'],4)) for k,v in B.items()})
print('BEST',best)
