import pickle,pandas as pd,numpy as np
pd.set_option('display.width',250)
T,V=pickle.load(open('ujian/wstage/T.pkl','rb')); N=[v[0] for v in V]
T['yr']=pd.to_datetime(T.ent).dt.year
T['P1']=np.where(T.ent<'2023-01-01','P1','P2'); T['Q']=np.where(T.ent<'2024-01-01','Q1','Q2'); T['sp']=np.where(T.set.isin(['S1','S2']),'S12','S34')
def m(g):
    w=g.ret>0
    return pd.Series(dict(n=len(g),ret=g.ret.mean(),exc=g.exc.mean(),win=w.mean(),pf=g.ret[w].sum()/-g.ret[~w].sum(),
        avgloss=g.ret[~w].mean(),worst=g.ret.min(),hari=g.days.mean(),gagal=(g.why=='GAGAL').mean()))
A=T.groupby('vi').apply(m); A.index=N; print(A.round(3).to_string())
for k in ['P1','Q','sp','yr']:
    X=T.groupby(['vi',k]).exc.agg(['mean','count']).unstack(); X.index=N; print(X.round(3).to_string())
rng=np.random.default_rng(1); tick=T.ticker.unique(); pos={t:i for i,t in enumerate(tick)}
IDX=[np.array([pos[t] for t in rng.choice(tick,len(tick))]) for _ in range(2000)]
def bs(sub):
    s=sub.groupby('ticker').exc.agg(['sum','count']).reindex(tick).fillna(0); S=s['sum'].values; C=s['count'].values
    return np.array([S[i].sum()/max(1,C[i].sum()) for i in IDX])
def ci(a): return f'{a.mean()*100:5.1f}% [{np.percentile(a,2.5)*100:5.1f}, {np.percentile(a,97.5)*100:5.1f}] P>0={np.mean(a>0):.2f}'
for lab,f in [('SEMUA',lambda x:x),('P1 2020-22',lambda x:x[x.P1=='P1']),('P2 2023-26',lambda x:x[x.P1=='P2']),
              ('Q1 2020-23',lambda x:x[x.Q=='Q1']),('Q2 2024-26',lambda x:x[x.Q=='Q2']),('S1+S2',lambda x:x[x.sp=='S12']),('S3+S4',lambda x:x[x.sp=='S34'])]:
    R={vi:bs(f(T[T.vi==vi])) for vi in range(4)}
    print(lab); [print('  ',N[vi].ljust(24),ci(R[vi])) for vi in range(4)]
    print('   K4-asas (GAGAL baharu)'.ljust(27),ci(R[3]-R[1])); print('   baharu-lama (asas)'.ljust(27),ci(R[1]-R[0]))
