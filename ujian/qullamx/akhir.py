# Konfigurasi akhir QULLAMX v2 (EP gap>=8, RVOL>=3, stop LOD, SELL close<SMA20): 431 + S1-S4, tambah ke registry
import sys; sys.path.insert(0,'ujian/qullamx')
from sah_ep import *
def j(s):
    f=subset(fr,asal,s); x=ep_bina(f,gap=8); T=trades(x); cv=portfolio(T,x)
    return baris2(s,'QULLAMX','Qullamaggie BO+EP (indikator QULLAMX)','V6 EP sahaja gap>=8 RVOL>=3 trail SMA20 (QULLAMX v2)',T,cv,f,idx,True,
                  'Kod indikator/QULLAMX_harian.mai; masuk buka H+1; stop LOD; SELL close bawah SMA20; pilih daripada grid 51 varian')
if __name__=='__main__':
    with Pool(4) as p: rows=p.map(j,['431','S1','S2','S3','S4'])
    R=pd.DataFrame(rows,columns=LAJUR2); print(R[['set','keputusan','skor','cagr','mdd','h1','h2','n','win','ret10','ew_cagr','gate_gagal','bulan_untung','pegang']].to_string())
    old=pd.read_csv('registry/QULLAMX.csv'); pd.concat([old,R]).to_csv('registry/QULLAMX.csv',index=False)
