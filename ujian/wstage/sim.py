import pandas as pd, numpy as np, pickle
from multiprocessing import Pool
COST=0.001
def MA(x,n): return pd.Series(x).rolling(n,min_periods=n).mean().values
def HHV(x,n): return pd.Series(x).rolling(n,min_periods=1).max().values
def REF(x,n):
    x=np.asarray(x,dtype=float); o=np.full_like(x,np.nan); o[n:]=x[:-n]; return o
def SUM(b,n):
    c=np.cumsum(np.nan_to_num(np.asarray(b,dtype=float))); o=c.copy(); o[n:]=c[n:]-c[:-n]; return o
# vi: (nama, wajib K4, GAGAL baharu)
V=[('C40 asas, GAGAL lama',False,False),('C40 asas, GAGAL baharu',False,True),
   ('C40 +K4, GAGAL lama',True,False),('C40 +K4, GAGAL baharu',True,True)]
def run(a):
    t,g=a
    o,h,l,c,v=[g[k].values.astype(float) for k in ['open','high','low','close','volume']]
    d=g.index.values; n=len(c)
    with np.errstate(invalid='ignore'):
        MAPJ=MA(c,150); MAPD=MA(c,50); KRS=(c/MA(c,250)-1)*100; KRSA=MA(KRS,20)
        VOLB=v>=3*REF(MA(v,50),1); HB=HHV(h,100); LVL=REF(HB,1); PECAH=c>LVL
        r=REF(MAPJ,40); NAIK=MAPJ>r*1.01; TURUN=MAPJ<r*0.99; ST2=(c>MAPJ)&NAIK
        K=[c>MAPJ,NAIK,c>MAPD,MAPD>MAPJ,KRS>0,KRSA>REF(KRSA,1),SUM(VOLB,20)>=1,SUM(PECAH,20)>=1,c>=HHV(h,250)*0.85,c>REF(c,65)]
        SK=sum(k.astype(int) for k in K)
        RSOK=(KRS>0)|(KRS>REF(KRS,1))
        B0=PECAH&VOLB&(~TURUN)&(c>MAPJ)&RSOK&(SK>=7)&(REF(SUM(ST2,40),1)<40)
        JUALA=(c<MAPJ)&(~NAIK)
        GL=(c<REF(HB,21))
    out=[]
    for vi,(nm,k4,baru) in enumerate(V):
        BELIC=B0&(MAPD>MAPJ) if k4 else B0
        BELI=BELIC&(REF(SUM(BELIC,40),1)==0)
        nxt=0
        for i in np.flatnonzero(BELI):
            if i<nxt or i>=n-1: continue
            e=o[i+1]; x=None; why='hujung'; j=i+1
            while j<n:
                gagal=(j-i<=20) and (not BELI[j]) and ((c[j]<LVL[i]) if baru else GL[j])
                if JUALA[j] or gagal:
                    if j+1<n: x=o[j+1]; why='GAGAL' if (gagal and not JUALA[j]) else 'SELL'; j+=1
                    break
                j+=1
            if x is None: j=n-1; x=c[j]
            out.append((vi,t,d[i+1],d[j],j-(i+1),x/e*(1-COST)/(1+COST)-1,why))
            nxt=j
    return out
if __name__=='__main__':
    fr=[]; asal={}
    for s in ['S1','S2','S3','S4']:
        dd=pd.read_csv(f'data/dataset_{s}.csv'); dd['date']=pd.to_datetime(dd.date.astype(str))
        for t,g in dd.groupby('ticker'): fr.append((t,g.sort_values('date').set_index('date'))); asal[t]=s
    with Pool() as p: res=p.map(run,fr,chunksize=4)
    T=pd.DataFrame([x for r in res for x in r],columns=['vi','ticker','ent','ex','days','ret','why'])
    T['set']=T.ticker.map(asal)
    cl=pd.DataFrame({t:g.close for t,g in fr}).sort_index()
    EWI=(1+cl.pct_change(fill_method=None).mean(axis=1).fillna(0)).cumprod()
    T['exc']=T.ret-(EWI.reindex(T.ex).values/EWI.reindex(T.ent).values-1)
    print('saham',len(fr),'tarikh',cl.index.min().date(),cl.index.max().date())
    pickle.dump((T,V),open('ujian/wstage/T.pkl','wb')); print(T.groupby('vi').size())
