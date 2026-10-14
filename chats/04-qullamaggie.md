# Chat: Qullamaggie

- Pautan asal: https://claude.ai/chat/443a45f8-7409-40e6-a47a-196a81792cc9
- Kemas kini terakhir: 2026-10-13T05:52:47.666403+00:00
- Bilangan giliran: 14

---

## [0] 👤 Azim — Tue 2026-10-13 10:05

MM_BASE:=50;
MM_PERIOD:=50;
MM_SENS:=1.5;

HOT_BASE:=30;
HOT_PERIOD:=40;
HOT_SENS:=0.7;
LC:=REF(CLOSE,1);
TEMP1:=MAX(CLOSE-LC,0);
TEMP2:=ABS(CLOSE-LC);
RSI1:=SMA(TEMP1,MM_PERIOD,1)/SMA(TEMP2,MM_PERIOD,1)*100;
RSI_B:=MM_SENS*(RSI1-MM_BASE);
MM_RSI:=IF(RSI_B>20,20, IF(RSI_B<0,0,RSI_B));
RSI2:=SMA(TEMP1,HOT_PERIOD,1)/SMA(TEMP2,HOT_PERIOD,1)*100;
RSI_M:=HOT_SENS*(RSI2-HOT_BASE);
HOT_RSI:=IF(RSI_M>20,20,IF(RSI_M<0,0,RSI_M));
MM_MA10:=MA(MM_RSI,10);
SMART:=MM_RSI>0 AND SUM(REF(MM_RSI,1),20)=0;
BUY:=CROSS(MM_RSI,5) AND MM_RSI>MM_MA10 AND SMART=0;
BUY1:=BUY=1 AND REF(BUY,1)=0 AND REF(BUY,2)=0 AND REF(BUY,3)=0
SELL:=CROSS(15,MM_RSI);
SELL1:=SELL=1 AND REF(SELL,1)=0 AND REF(SELL,2)=0 AND REF(SELL,3)=0

HOT_RSI2:=HOT_RSI-MM_RSI
HOT_MA10:=MA(HOT_RSI2,10);
GC:=CROSS(MM_MA10,HOT_MA10)
GC1:=GC=1 AND SELL1=0
DC:=CROSS(HOT_MA10,MM_MA10)
JERUNG:=CROSS(HOT_RSI,10) AND HOT_RSI>HOT_MA10;
JERUNG1:=JERUNG=1 AND REF(JERUNG,1)=0 AND REF(JERUNG,2)=0

STICKLINE(1,0,20,1,0),COLORGREEN;
STICKLINE(1,0,HOT_RSI,1,0),COLORD8C200;
STICKLINE(1,0,MM_RSI,1,0),COLORRED;

DRAWTEXT(BUY1,-2,'▲'),COLOR00FF00;
DRAWTEXT(BUY1,3,'BUY'),COLOR00FF00;

DRAWTEXT(SELL1,22,'▼'),COLORRED;
DRAWTEXT(SELL1,17,'SELL'),COLORWHITE;

DRAWTEXT(SMART,-2,'▲'),COLOR00FFFF;
DRAWTEXT(SMART,2,'SM'),COLORBLACK;

DRAWTEXT(JERUNG1,-2,'֍'),COLORORANGE;
DRAWTEXT(GC1,2,'◊'),COLOR800000;
DRAWTEXT(DC,18,'◊'),COLOR90EE90;

MMAVG:MM_MA10,COLORBLUE,LINETHICK2;  Saya Perlukan satu indicator lebih kurang macam SMRTMCDX. base on color coding. Yang penting saya nak tahu bila nak buy dan sell, macam smartmcdx. Anda selaku pakar dalam pembinaan indicators, fikirkan satu cara macamana nak represent data data penting dari Qullamaggie dalam bentuk lebih kurang macam SMRTMCDX ni. Yang penting user faham apa yang dia tgk. Gunakan color yang betul dan menarik. Kaji dahulu cara terbaik, dan bina.

## [1] 🤖 Claude

<details><summary>🔧 Alat: mcp__memory__memory_read</summary>

````
<parameter name="path">['/areas/kell-moomoo-indicator.md', '/areas/backtest-strategi.md']</parameter>
````
</details>


<details><summary>🔧 Alat: AskUserQuestion</summary>

````
<parameter name="questions">[{'question': 'Setup Qullamaggie mana yang indikator perlu tandakan?', 'header': 'Setup', 'multiSelect': False, 'options': [{'label': 'Breakout + EP (Disyorkan)', 'description': 'BUY breakout (▲) dan penanda EP berasingan (♦)'}, {'label': 'Breakout sahaja', 'description': 'Lebih ringkas, satu jenis isyarat BUY'}, {'label': 'Breakout + EP + Momentum Burst', 'description': 'Tiga jenis isyarat, lebih banyak penanda'}]}, {'question': 'Garis trail untuk isyarat SELL (close pertama di bawah garis)?', 'header': 'Trail SELL', 'multiSelect': False, 'options': [{'label': 'EMA10 (Disyorkan)', 'description': 'Lalai jadual penyelarasan; keluar lebih awal'}, {'label': 'SMA10', 'description': 'Versi blog asal'}, {'label': 'SMA20', 'description': 'Lebih perlahan, pegang lebih lama'}]}, {'question': 'Penapis pasaran (MA10>MA20 indeks) — formula Moomoo mungkin tidak boleh baca data indeks dari carta saham (belum disahkan). Bagaimana?', 'header': 'Penapis', 'multiSelect': False, 'options': [{'label': 'Proksi saham sendiri (Disyorkan)', 'description': 'Guna MA10>MA20 & naik pada saham itu; lampu pasaran disemak manual di carta QQQ'}, {'label': 'Indikator yang sama pada QQQ', 'description': 'Pasang indikator di carta QQQ untuk baca lampu pasaran'}, {'label': 'Tiada penapis', 'description': 'Abaikan rejim pasaran'}]}, {'question': 'Bentuk output?', 'header': 'Output', 'multiSelect': False, 'options': [{'label': 'Formula dalam chat sahaja', 'description': 'Kod + panduan baca, tiada fail'}, {'label': 'Chat + fail PDF', 'description': 'Kod dan panduan juga sebagai PDF'}]}]</parameter>
````
</details>

Nama dicadangkan: **QULLAMX**. Salin terus ke Moomoo (Indicator → Custom).

```
{=== QULLAMX : Qullamaggie Breakout + EP ===}
AMBANG:=14;
EMA10:=EMA(C,10);
MA10:=MA(C,10);
MA20:=MA(C,20);
ADR:=100*(MA(H/L,20)-1);
CLV:=(C-L)/(H-L+0.0001);

{--- Lampu trend (proksi penapis pasaran) ---}
TREND_OK:=MA10>MA20 AND MA10>REF(MA10,1) AND MA20>REF(MA20,1);

{--- Skor 0-20 ---}
G3:=C/LLV(C,63);
MOM:=IF(G3>=1.30,4,IF(G3>=1.15,2,0));
SURF:=IF(C>EMA10 AND TREND_OK,4,IF(C>MA20 AND MA20>REF(MA20,1),2,0));
RK:=((HHV(H,6)-LLV(L,6))/C*100)/ADR;
KETAT:=IF(RK<=1.5,4,IF(RK<=2.5,2,0));
VK:=MA(V,5)/MA(V,50);
KERING:=IF(VK<=0.7,4,IF(VK<=0.9,2,0));
ADRS:=IF(ADR>=5,4,IF(ADR>=3.5,2,0));
T:=MOM+SURF;
B:=KETAT+KERING;
SKOR:=T+B+ADRS;

{--- BUY Breakout ---}
BO:=C>REF(HHV(H,10),1) AND CLV>=0.5;
STOP_OK:=(C-L)/C*100<=ADR;
SIAP:=TREND_OK AND HHV(REF(SKOR,1),5)>=AMBANG AND BO;
BUY:=SIAP AND STOP_OK;
BUY1:=BUY AND REF(BUY,1)=0 AND REF(BUY,2)=0 AND REF(BUY,3)=0;
LANGKAU:=SIAP AND STOP_OK=0;
LANGKAU1:=LANGKAU AND REF(LANGKAU,1)=0 AND REF(LANGKAU,2)=0;

{--- EP (Episodic Pivot) ---}
GAP:=(O/REF(C,1)-1)*100;
RVOL:=V/REF(MA(V,50),1);
ABAI:=REF(C,1)/REF(C,63)<1.2;
EP:=GAP>=10 AND RVOL>=3 AND ABAI AND CLV>=0.5;
EP1:=EP AND REF(EP,1)=0;

{--- SEDIA (masuk watchlist) ---}
SEDIA:=TREND_OK AND SKOR>=AMBANG AND REF(SKOR,1)<AMBANG;

{--- SELL: close pertama bawah EMA10 selepas BUY/EP ---}
MASUK:=BUY1 OR EP1;
XR:=CROSS(EMA10,C);
SELL1:=XR AND BARSLAST(MASUK)<REF(BARSLAST(XR),1)+1;

{--- Lukisan ---}
STICKLINE(TREND_OK,0,20,1,0),COLOR1B5E20;
STICKLINE(TREND_OK=0,0,20,1,0),COLOR4A1C1C;
STICKLINE(1,0,T,1,0),COLOR29B6F6;
STICKLINE(1,T,T+B,1,0),COLORFFC107;
STICKLINE(1,T+B,SKOR,1,0),COLORD500F9;

DRAWTEXT(BUY1,-2,'▲'),COLOR00E676;
DRAWTEXT(BUY1,3,'BUY'),COLOR00E676;
DRAWTEXT(EP1,-2,'♦'),COLORFF4081;
DRAWTEXT(EP1,3,'EP'),COLORFF4081;
DRAWTEXT(LANGKAU1,-2,'×'),COLOR9E9E9E;
DRAWTEXT(SELL1,22,'▼'),COLORFF1744;
DRAWTEXT(SELL1,17,'SELL'),COLORFFFFFF;
DRAWTEXT(SEDIA,21,'●'),COLORFFC107;

QAVG:MA(SKOR,5),COLORFFFFFF,LINETHICK2;
```

**Cara membaca**

| Warna / Simbol | Maksud |
|---|---|
| Latar **hijau gelap** | Trend sihat (MA10 > MA20, kedua-duanya naik). Boleh cari BUY |
| Latar **merah gelap** | Tiada trend. Jangan buka breakout |
| Bar **biru** (0–8) | Momentum: naik ≥30% dalam 63 hari + harga "surf" EMA10/MA20 |
| Bar **kuning** (0–8) | Base ketat: julat 6 hari kecil berbanding ADR + volume mengering |
| Bar **ungu** (0–4) | ADR: saham cukup bergerak (≥5% penuh) |
| Garis **putih** QAVG | Purata skor 5 hari. Naik ke ≥14 = setup matang |
| ● kuning (atas) | SEDIA: skor baru capai 14. Masukkan watchlist |
| ▲ BUY hijau | Breakout pecah high 10 hari, tutup kuat, stop LOD ≤ 1 ADR |
| × kelabu | Breakout sah tetapi stop LOD terlalu lebar. **Langkau** |
| ♦ EP merah jambu | Gap ≥10%, volume ≥3× purata, saham diabaikan 3 bulan, tutup kuat |
| ▼ SELL | Close pertama di bawah EMA10 selepas BUY/EP. Keluar baki |

**Logik ringkas:** bar penuh setinggi 20 dan latar hijau = saham kuat, ketat, volatil, dalam trend → tunggu ▲. Ruang kosong di atas bar menunjukkan latar (hijau/merah) seperti SMRTMCDX.

**Penggunaan**
1. Pasang juga pada carta **QQQ**. Latar QQQ hijau = lampu pasaran Qullamaggie (MA10>MA20 naik). Latar QQQ merah → abaikan semua BUY/EP.
2. Stop awal = Low hari BUY/EP (letak manual). Indikator hanya tanda trail EMA10.
3. EP dikesan pada close; edge sebenar pada **open/ORH hari gap** (21:30 MYT). Penanda ♦ = semakan selepas tutup / hari kedua.

**Perkara belum disahkan ⚠️**
- `BARSLAST` mungkin tiada dalam Moomoo. Jika ralat, ganti baris SELL1 dengan: `SELL1:=XR AND HHV(MASUK,30)>0;` (SELL boleh muncul lebih sekali).
- Ambang (14, 30%, 1.5/2.5 ADR, 0.7/0.9 volume, gap 10%, 3×) ialah cadangan awal 💡, belum di-backtest. Sesuai dijalankan melalui STEP-2 sebelum guna wang sebenar.

## [2] 👤 Azim — Tue 2026-10-13 11:04

ada error. Boleh recheck balik semuanya

## [3] 🤖 Claude

<details><summary>🔧 Alat: WebSearch</summary>

````
<parameter name="query">moomoo custom indicator formula functions BARSLAST</parameter>
<parameter name="mode">standard</parameter>
````
</details>

Punca utama: Moomoo tidak menerima komen `{ }`. Semua komen dibuang, nama pemboleh ubah yang mungkin bertembung dengan nama fungsi ditukar, dan `BARSLAST` (belum disahkan wujud di Moomoo) diganti.

```
AMBANG:=14;
E10:=EMA(CLOSE,10);
M10:=MA(CLOSE,10);
M20:=MA(CLOSE,20);
ADR:=100*(MA(HIGH/LOW,20)-1);
CLV:=(CLOSE-LOW)/(HIGH-LOW+0.0001);
TRENDOK:=M10>M20 AND M10>REF(M10,1) AND M20>REF(M20,1);

G3:=CLOSE/LLV(CLOSE,63);
MOM:=IF(G3>=1.3,4,IF(G3>=1.15,2,0));
SURF:=IF(CLOSE>E10 AND TRENDOK,4,IF(CLOSE>M20 AND M20>REF(M20,1),2,0));
RK:=((HHV(HIGH,6)-LLV(LOW,6))/CLOSE*100)/ADR;
KETAT:=IF(RK<=1.5,4,IF(RK<=2.5,2,0));
VK:=MA(VOL,5)/MA(VOL,50);
KERING:=IF(VK<=0.7,4,IF(VK<=0.9,2,0));
ADRS:=IF(ADR>=5,4,IF(ADR>=3.5,2,0));
TRD:=MOM+SURF;
BASE:=KETAT+KERING;
SKOR:=TRD+BASE+ADRS;

BO:=CLOSE>REF(HHV(HIGH,10),1) AND CLV>=0.5;
STOPOK:=(CLOSE-LOW)/CLOSE*100<=ADR;
SIAP:=TRENDOK AND HHV(REF(SKOR,1),5)>=AMBANG AND BO;
BUY:=SIAP AND STOPOK;
BUY1:=BUY=1 AND REF(BUY,1)=0 AND REF(BUY,2)=0 AND REF(BUY,3)=0;
LANGKAU:=SIAP AND STOPOK=0;
LANGKAU1:=LANGKAU=1 AND REF(LANGKAU,1)=0 AND REF(LANGKAU,2)=0;

GAP:=(OPEN/REF(CLOSE,1)-1)*100;
RVOL:=VOL/REF(MA(VOL,50),1);
ABAI:=REF(CLOSE,1)/REF(CLOSE,63)<1.2;
EPX:=GAP>=10 AND RVOL>=3 AND ABAI AND CLV>=0.5;
EP1:=EPX=1 AND REF(EPX,1)=0;

SEDIA:=TRENDOK AND SKOR>=AMBANG AND REF(SKOR,1)<AMBANG;

MASUK:=BUY1 OR EP1;
XR:=CROSS(E10,CLOSE);
SELL1:=XR AND HHV(MASUK,30)>0 AND SUM(REF(XR,1),3)=0;

STICKLINE(TRENDOK,0,20,1,0),COLOR1B5E20;
STICKLINE(TRENDOK=0,0,20,1,0),COLOR4A1C1C;
STICKLINE(1,0,TRD,1,0),COLOR29B6F6;
STICKLINE(1,TRD,TRD+BASE,1,0),COLORFFC107;
STICKLINE(1,TRD+BASE,SKOR,1,0),COLORD500F9;

DRAWTEXT(BUY1,-2,'▲'),COLOR00E676;
DRAWTEXT(BUY1,3,'BUY'),COLOR00E676;
DRAWTEXT(EP1,-2,'֍'),COLORFF4081;
DRAWTEXT(EP1,3,'EP'),COLORFF4081;
DRAWTEXT(LANGKAU1,-2,'X'),COLOR9E9E9E;
DRAWTEXT(SELL1,22,'▼'),COLORFF1744;
DRAWTEXT(SELL1,17,'SELL'),COLORFFFFFF;
DRAWTEXT(SEDIA,21,'◊'),COLORFFC107;

QAVG:MA(SKOR,5),COLORFFFFFF,LINETHICK2;
```

**Perubahan**

| Perkara | Asal | Baharu |
|---|---|---|
| Komen `{ }` | Ada | Dibuang (punca ralat) |
| Nama | EMA10, MA10, MA20, T, B, EP | E10, M10, M20, TRD, BASE, EPX (elak bertembung nama fungsi/sistem) |
| Data | C, H, L, O, V | CLOSE, HIGH, LOW, OPEN, VOL (ejaan penuh, lebih selamat) |
| SELL | Guna `BARSLAST` | Guna `HHV` + `SUM` sahaja (fungsi yang sama seperti SMRTMCDX) |
| Simbol | ♦ × ● | ֍ X ◊ (simbol yang sudah terbukti berfungsi dalam SMRTMCDX) |

**Kesan pertukaran SELL:** ▼ kini muncul untuk setiap close bawah EMA10 dalam 30 hari selepas BUY/EP. **Hanya ▼ pertama selepas ▲/֍ dikira** sebagai isyarat keluar.

Simbol baharu: ֍ merah jambu = EP, X kelabu = LANGKAU, ◊ kuning atas = SEDIA. Warna lain kekal.

Jika masih ada ralat, hantar tangkapan skrin mesej ralat atau baris yang bergaris merah.

## [4] 👤 Azim — Tue 2026-10-13 11:06

error lagi

## [5] 🤖 Claude

Baris pemalar `AMBANG` dibuang; nilai 14 ditulis terus.

**Padam baris pertama:**
```
AMBANG:=14;
```

**Ganti dua baris ini:**
```
SIAP:=TRENDOK AND HHV(REF(SKOR,1),5)>=14 AND BO;
```
```
SEDIA:=TRENDOK AND SKOR>=14 AND REF(SKOR,1)<14;
```

Jika garis merah berpindah ke baris lain, hantar tangkapan skrin **mesej ralat penuh** (biasanya di bahagian bawah editor Moomoo) supaya punca sebenar dapat dikenal pasti, bukan diteka.

## [6] 👤 Azim — Tue 2026-10-13 11:07

bagi saya final

## [7] 🤖 Claude

```
E10:=EMA(CLOSE,10);
M10:=MA(CLOSE,10);
M20:=MA(CLOSE,20);
ADR:=100*(MA(HIGH/LOW,20)-1);
CLV:=(CLOSE-LOW)/(HIGH-LOW+0.0001);
TRENDOK:=M10>M20 AND M10>REF(M10,1) AND M20>REF(M20,1);

G3:=CLOSE/LLV(CLOSE,63);
MOM:=IF(G3>=1.3,4,IF(G3>=1.15,2,0));
SURF:=IF(CLOSE>E10 AND TRENDOK,4,IF(CLOSE>M20 AND M20>REF(M20,1),2,0));
RK:=((HHV(HIGH,6)-LLV(LOW,6))/CLOSE*100)/ADR;
KETAT:=IF(RK<=1.5,4,IF(RK<=2.5,2,0));
VK:=MA(VOL,5)/MA(VOL,50);
KERING:=IF(VK<=0.7,4,IF(VK<=0.9,2,0));
ADRS:=IF(ADR>=5,4,IF(ADR>=3.5,2,0));
TRD:=MOM+SURF;
BASE:=KETAT+KERING;
SKOR:=TRD+BASE+ADRS;

BO:=CLOSE>REF(HHV(HIGH,10),1) AND CLV>=0.5;
STOPOK:=(CLOSE-LOW)/CLOSE*100<=ADR;
SIAP:=TRENDOK AND HHV(REF(SKOR,1),5)>=14 AND BO;
BUY:=SIAP AND STOPOK;
BUY1:=BUY=1 AND REF(BUY,1)=0 AND REF(BUY,2)=0 AND REF(BUY,3)=0;
LANGKAU:=SIAP AND STOPOK=0;
LANGKAU1:=LANGKAU=1 AND REF(LANGKAU,1)=0 AND REF(LANGKAU,2)=0;

GAP:=(OPEN/REF(CLOSE,1)-1)*100;
RVOL:=VOL/REF(MA(VOL,50),1);
ABAI:=REF(CLOSE,1)/REF(CLOSE,63)<1.2;
EPX:=GAP>=10 AND RVOL>=3 AND ABAI AND CLV>=0.5;
EP1:=EPX=1 AND REF(EPX,1)=0;

SEDIA:=TRENDOK AND SKOR>=14 AND REF(SKOR,1)<14;

MASUK:=BUY1 OR EP1;
XR:=CROSS(E10,CLOSE);
SELL1:=XR AND HHV(MASUK,30)>0 AND SUM(REF(XR,1),3)=0;

STICKLINE(TRENDOK,0,20,1,0),COLOR1B5E20;
STICKLINE(TRENDOK=0,0,20,1,0),COLOR4A1C1C;
STICKLINE(1,0,TRD,1,0),COLOR29B6F6;
STICKLINE(1,TRD,TRD+BASE,1,0),COLORFFC107;
STICKLINE(1,TRD+BASE,SKOR,1,0),COLORD500F9;

DRAWTEXT(BUY1,-2,'▲'),COLOR00E676;
DRAWTEXT(BUY1,3,'BUY'),COLOR00E676;
DRAWTEXT(EP1,-2,'֍'),COLORFF4081;
DRAWTEXT(EP1,3,'EP'),COLORFF4081;
DRAWTEXT(LANGKAU1,-2,'X'),COLOR9E9E9E;
DRAWTEXT(SELL1,22,'▼'),COLORFF1744;
DRAWTEXT(SELL1,17,'SELL'),COLORFFFFFF;
DRAWTEXT(SEDIA,21,'◊'),COLORFFC107;

QAVG:MA(SKOR,5),COLORFFFFFF,LINETHICK2;
```

## [8] 👤 Azim — Tue 2026-10-13 11:07

error lagi

## [9] 🤖 Claude

Garis merah sentiasa di baris pertama, walaupun baris itu sudah ditukar. Ini bermaksud editor Moomoo menanda baris 1 untuk ralat **di mana-mana** dalam kod, jadi punca sebenar belum dapat dilihat. Saya tidak mahu meneka lagi.

Sila buat ujian ringkas ini (padam semua kod dahulu):

**Ujian 1** (sahkan tampal berfungsi):
```
E10:=EMA(CLOSE,10);
QAVG:E10,COLORFFFFFF;
```

**Ujian 2** (sahkan nama volume, calon punca utama):
```
VK:=MA(VOL,5);
QAVG:VK,COLORFFFFFF;
```

| Keputusan | Maksud |
|---|---|
| Ujian 1 ralat | Ada aksara tersembunyi semasa salin. Taip baris pertama secara manual |
| Ujian 1 OK, Ujian 2 ralat | `VOL` tidak dikenali. Saya tukar kepada `VOLUME` atau `V` |
| Kedua-dua OK | Punca di bahagian lain. Hantar tangkapan skrin **mesej ralat** (tekan/sentuh garis merah atau lihat panel bawah editor) |

Beritahu keputusan, saya beri kod final yang betul terus.

## [10] 👤 Azim — Tue 2026-10-13 13:47

saya pakai code awal, saya tersilap, paste dekat phyton. Boleh backtest? ada 431 saham kan

## [11] 🤖 Claude

<details><summary>🔧 Alat: Skill</summary>

````
<parameter name="skill">step2</parameter>
<parameter name="args">QULLAMX (Qullamaggie Breakout + EP, kod awal dengan BARSLAST, trail EMA10)</parameter>
````
</details>


<details><summary>🔧 Alat: Projects</summary>

````
<parameter name="method">project_info</parameter>
````
</details>


<details><summary>🔧 Alat: Glob</summary>

````
<parameter name="pattern">**/*.csv</parameter>
<parameter name="path">/mnt</parameter>
````
</details>


<details><summary>🔧 Alat: Bash</summary>

````
<parameter name="command">ls -la /root/.claude/uploads/*/ 2>/dev/null; find / -name "index_benchmark*" 2>/dev/null | head</parameter>
<parameter name="description">List uploaded files and look for benchmark file</parameter>
````
</details>


<details><summary>🔧 Alat: Bash</summary>

````
<parameter name="command">cd /root/.claude/uploads/*/ && python3 -c "
import pandas as pd,glob
t=set();d0=[];d1=[]
for f in glob.glob('*dataset_S*.csv'):
    d=pd.read_csv(f,usecols=['ticker','date']);t|=set(d.ticker);d0.append(d.date.min());d1.append(d.date.max())
print(len(t),min(d0),max(d1),[x for x in ['SPY','QQQ'] if x in t])"</parameter>
<parameter name="description">Count tickers, date range, check for SPY/QQQ</parameter>
````
</details>

Boleh, dan ya: 4 fail dataset ini mengandungi **431 saham** (2 Jan 2019 – 2 Okt 2026).

Tetapi backtest belum boleh dijalankan sekarang kerana satu fail wajib tiada.

| Perkara | Status |
|---|---|
| dataset_S1–S4.csv (431 saham) | ✅ Ada |
| **index_benchmark.csv** (SPY, QQQ) | ❌ Tiada dalam Project ini |
| SPY/QQQ dalam dataset | ❌ Tiada |

**Kenapa wajib:** gate G3 (kalahkan SPY), skor S1 (banding QQQ), lajur "tahun kalah SPY" dan verdict LAYAK semuanya dikira terhadap SPY/QQQ. Tanpanya keputusan tidak boleh dibanding dengan kaedah lain dalam registry.

**Tindakan:** muat naik `index_benchmark.csv` (fail yang sama digunakan dalam Project backtest sebelum ini, format: ticker, date, open, high, low, close, volume) ke Project Files ini.

Selepas fail ada, saya jalankan terus:

| Perkara | Tetapan |
|---|---|
| Kod | Kod **awal** QULLAMX (yang berfungsi di Moomoo) |
| ID registry | `registry/QULLAMX.csv` |
| Masuk | Buka hari selepas ▲ BUY atau ֍ EP |
| Henti rugi | Low hari isyarat (LOD) |
| Keluar | Buka hari selepas close pertama di bawah EMA10 |
| Penapis pasaran | Proksi saham sendiri (seperti indikator) |
| Set | 431, kemudian S1–S4 |

## [12] 👤 Azim — Tue 2026-10-13 13:50

saya dah muat naik

## [13] 🤖 Claude

<details><summary>🔧 Alat: Bash</summary>

````
<parameter name="command">ls /root/.claude/uploads/*/ ; find / -name "*index_benchmark*" -not -path "/proc/*" 2>/dev/null | head</parameter>
<parameter name="description">Look for the newly uploaded benchmark file</parameter>
````
</details>


<details><summary>🔧 Alat: Projects</summary>

````
<parameter name="method">project_info</parameter>
````
</details>


<details><summary>🔧 Alat: Projects</summary>

````
<parameter name="method">project_read</parameter>
<parameter name="path">index_benchmark.csv</parameter>
````
</details>


<details><summary>🔧 Alat: Bash</summary>

````
<parameter name="command">mkdir -p /home/claude/bt/data && cd /home/claude/bt/data && for s in S1 S2 S3 S4; do cp /root/.claude/uploads/*/*dataset_$s.csv dataset_$s.csv; done && cp /root/.claude/projects/-home-claude/3d685035-efd9-58c9-bb6a-79ce56a95be9/tool-results/project-file-*-index_benchmark.csv index_benchmark.csv && head -3 index_benchmark.csv && python3 -c "import pandas as pd;d=pd.read_csv('index_benchmark.csv');print(d.ticker.unique(),d.date.min(),d.date.max())"</parameter>
<parameter name="description">Stage datasets and benchmark into working folder</parameter>
````
</details>


<details><summary>🔧 Alat: Write</summary>

````
<parameter name="content"># ENJIN BACKTEST STANDARD v1.2 — jangan ubah logik teras
import pandas as pd, numpy as np, glob
COST=0.001; START='2019-11-01'; H1_END='2022-12-31'; ENJIN='v1.2'

def cari(nama):
    for pat in [f'/root/.claude/uploads/**/*{nama}', f'/mnt/user-data/uploads/**/*{nama}', f'/mnt/project/{nama}', f'/home/claude/**/{nama}']:
        f=glob.glob(pat,recursive=True)
        if f: return sorted(f)[-1]
    raise FileNotFoundError(nama+' tiada — minta pengguna muat naik ke Project Files')

def rsi(c,n=14):
    dl=c.diff(); au=dl.clip(lower=0).ewm(alpha=1/n,adjust=False).mean()
    ad=(-dl.clip(upper=0)).ewm(alpha=1/n,adjust=False).mean(); return 100-100/(1+au/ad)
def atr(g,n=14):
    c=g.close; tr=pd.concat([g.high-g.low,(g.high-c.shift()).abs(),(g.low-c.shift()).abs()],axis=1).max(axis=1)
    return tr.rolling(n).mean()

def siap(g):
    for k,v in [('sig',False),('stop',np.nan),('tgt',np.nan),('exitc',False),('rank',0.0)]:
        if k not in g: g[k]=v
    return g

def trades(fr, tmax=None, warm=200):
    out=[]
    for t,g in fr.items():
        g=siap(g); o,h,l,c=g.open.values,g.high.values,g.low.values,g.close.values
        sig=g.sig.fillna(False).astype(bool).values; st=g.stop.astype(float).values; tg=g.tgt.astype(float).values
        ex=g.exitc.fillna(False).astype(bool).values; rk=g['rank'].astype(float).values; ix=g.index; n=len(g); i=warm
        while i<n-1:
            if not sig[i]: i+=1; continue
            e=o[i+1]; sp=st[i] if not np.isnan(st[i]) else -np.inf
            j=i+1; x=None; why='hujung'
            while j<n:
                tgt=tg[j-1] if j>i+1 else np.nan
                if j>i+1 and o[j]<=sp: x,why=o[j],'henti'; break
                if l[j]<=sp: x,why=sp,'henti'; break
                if not np.isnan(tgt):
                    if j>i+1 and o[j]>=tgt: x,why=o[j],'sasaran'; break
                    if h[j]>=tgt: x,why=tgt,'sasaran'; break
                if ex[j] and j+1<n: j+=1; x,why=o[j],'isyarat keluar'; break
                if tmax and (j-i)>=tmax: x,why=c[j],'masa'; break
                j+=1
            if x is None: j=n-1; x=c[j]
            out.append(dict(ticker=t,sig=ix[i],ent=ix[i+1],ex=ix[j],ret=x/e*(1-COST)/(1+COST)-1,days=j-i,
                            why=why,rank=rk[i],mfe=h[i+1:j+1].max()/e-1))
            i=j+1
    return pd.DataFrame(out)

def portfolio(T, fr, slots=8, w=0.125):
    dates=sorted(set().union(*[g.index for g in fr.values()])); dates=[x for x in dates if x>=pd.Timestamp(START)]
    T=T[T.ent>=pd.Timestamp(START)].sort_values(['ent','rank'],ascending=[True,False])
    byent={k:v for k,v in T.groupby('ent')}; cl={t:g.close for t,g in fr.items()}
    eq=cash=1.0; pos=[]; curve=[]
    for dt in dates:
        keep=[]
        for p in pos:
            if p['ex']==dt: cash+=p['a']*(1+p['ret'])
            else: keep.append(p)
        pos=keep
        if dt in byent:
            for _,r in byent[dt].iterrows():
                if len(pos)>=slots: break
                if any(p['t']==r.ticker for p in pos): continue
                a=min(cash,eq*w)
                if a<=0: break
                cash-=a; pos.append(dict(t=r.ticker,ex=r.ex,ret=r.ret,a=a,ent=dt))
        keep=[]
        for p in pos:                      # v1.2: tutup posisi yang keluar pada hari masuk
            if p['ex']==dt and p['ent']==dt: cash+=p['a']*(1+p['ret'])
            else: keep.append(p)
        pos=keep
        mv=sum(p['a']*cl[p['t']].asof(dt)/cl[p['t']].asof(p['ent']) if p['ent']!=dt else p['a'] for p in pos)
        eq=cash+mv; curve.append((dt,eq))
    return pd.Series(dict(curve))

def _cagr(s):
    y=(s.index[-1]-s.index[0]).days/365.25; return (s.iloc[-1]/s.iloc[0])**(1/y)-1
def _mdd(s): return (s/s.cummax()-1).min()

def penanda(idx, fr):
    out={}
    ew=pd.concat([g.close[g.index>=START]/g.close[g.index>=START].iloc[0] for g in fr.values()],axis=1).ffill().mean(axis=1)
    for k,s in [('QQQ',idx['QQQ'].close),('SPY',idx['SPY'].close),('Sama rata 100',ew)]:
        s=s[s.index>=START]
        out[k]=dict(cagr=_cagr(s),mdd=_mdd(s),h1=_cagr(s[:H1_END]),h2=_cagr(s[H1_END:]),
                    tahunan=s.resample('YE').last().pct_change().dropna())
    return out

def metrik(T, cv, B, ada_henti, long_only=True, mekanikal=True):
    T=T[T.ent>=pd.Timestamp(START)]; w=T.ret>0
    yrs=(cv.index[-1]-cv.index[0]).days/365.25
    th=cv.resample('YE').last().pct_change().dropna(); sp=B['SPY']['tahunan']
    th=th[th.index.isin(sp.index)][:-1]  # tahun kalendar penuh sahaja
    m=dict(n=len(T),dagangan_setahun=len(T)/yrs,win=w.mean(),avg=T.ret.mean(),avgwin=T.ret[w].mean(),
           avgloss=T.ret[~w].mean(),pf=T.ret[w].sum()/-T.ret[~w].sum(),days=T.days.mean(),
           hit10=(T.mfe>=0.10).mean(),ret10=(T.ret>=0.10).mean(),
           cagr=_cagr(cv),mdd=_mdd(cv),h1=_cagr(cv[:H1_END]),h2=_cagr(cv[H1_END:]),
           thn_kalah_spy=(th>sp.reindex(th.index)).mean(),terburuk=T.ret.min(),
           ada_henti=ada_henti,long_only=long_only,mekanikal=mekanikal)
    m['mar']=m['cagr']/abs(m['mdd']) if m['mdd']<0 else np.nan
    return m

def gate(m,B):
    return {'G1':m['ada_henti'] and m['avgloss']>=-0.12,'G2':m['n']>=100,'G3':m['cagr']>B['SPY']['cagr'],
            'G4':m['mdd']>=-0.45,'G5':m['h1']>0 and m['h2']>0,'G6':m['long_only'] and m['mekanikal']}

def skor(m,B):
    c=lambda x:max(0.0,min(1.0,x)); spy,qqq=B['SPY']['cagr'],B['QQQ']['cagr']
    s={'S1':25*c((m['cagr']-spy)/((qqq+0.10)-spy)),'S2':20*c(m['mar']/1.5),'S3':15*c(m['thn_kalah_spy']),
       'S4':10*c(min(m['h1'],m['h2'])/max(m['h1'],m['h2'])) if max(m['h1'],m['h2'])>0 else 0.0,
       'S5':15*c(m['ret10']/0.40),'S6':(5 if 20<=m['dagangan_setahun']<=150 else 0)+(5 if 5<=m['days']<=60 else 0),
       'S7':5*c(m['avg']/0.05)}
    s['JUMLAH']=sum(s.values()); return s

def keputusan(m,B):
    g=gate(m,B)
    if not all(g.values()): return 'DITOLAK', g, None
    s=skor(m,B); q=B['QQQ']
    if s['JUMLAH']>=75 and m['h1']>q['h1'] and m['h2']>q['h2']: k='GUNA'
    elif s['JUMLAH']>=60: k='UJI KERTAS'
    else: k='SIMPAN'
    return k, g, s

LAJUR=['id','kaedah','varian','enjin','tarikh','keputusan','skor','cagr','mdd','mar','h1','h2','thn_kalah_spy',
       'n','dagangan_setahun','win','avg','avgwin','avgloss','pf','days','hit10','ret10','terburuk',
       'ada_henti','gate_gagal','catatan']
def baris(id_,kaedah,varian,m,B,catatan=''):
    k,g,s=keputusan(m,B)
    r={'id':id_,'kaedah':kaedah,'varian':varian,'enjin':ENJIN,'tarikh':pd.Timestamp.today().strftime('%Y-%m-%d'),
       'keputusan':k,'skor':round(s['JUMLAH'],1) if s else '','gate_gagal':' '.join(x for x,v in g.items() if not v),'catatan':catatan}
    for x in LAJUR:
        if x not in r: r[x]=round(m[x],4) if isinstance(m[x],float) else m[x]
    return r
</parameter>
<parameter name="file_path">/home/claude/bt/enjin.py</parameter>
````
</details>


<details><summary>🔧 Alat: Write</summary>

````
<parameter name="content"># TAMBAHAN SHARIAH v1.0 — lapisan atas enjin v1.2; TIDAK mengubah trades/portfolio/metrik/gate/skor
from enjin import *
SETS=['S1','S2','S3','S4']; HARI=[5,10,15,20,30,40,60]
def muat():
    fr={}; asal={}
    for s in SETS:
        d=pd.read_csv(cari(f'dataset_{s}.csv')); d['date']=pd.to_datetime(d.date.astype(str))
        for t,g in d.groupby('ticker'): fr[t]=g.sort_values('date').set_index('date').copy(); asal[t]=s
    ix=pd.read_csv(cari('index_benchmark.csv')); ix['date']=pd.to_datetime(ix.date.astype(str))
    idx={t:g.sort_values('date').set_index('date').copy() for t,g in ix.groupby('ticker')}
    return fr, idx, asal
def subset(fr,asal,s): return fr if s=='431' else {t:g for t,g in fr.items() if asal[t]==s}
def tambah(T,cv,fr,B):
    T=T[T.ent>=pd.Timestamp(START)]; bl=cv.resample('ME').last().pct_change().dropna()
    x={'ew_cagr':round(B['Sama rata 100']['cagr'],4),'bulan_untung':round((bl>0).mean(),4),'bulan10':round((bl>=0.10).mean(),4)}
    R={k:[] for k in HARI}
    for r in T.itertuples():
        g=fr[r.ticker]; i=g.index.get_loc(r.ent); e=g.open.values[i]; c=g.close.values
        for k in HARI:
            if i+k-1<len(c): R[k].append(c[i+k-1]/e-1)
    x['pegang']='|'.join(f'{k}:{np.mean(v)*100:.1f}' for k,v in R.items() if v)
    return x
LAJUR2=['set']+LAJUR+['ew_cagr','menang_ew','bulan_untung','bulan10','pegang']
def baris2(set_,id_,kaedah,varian,T,cv,frs,idx,ada_henti,catatan=''):
    B=penanda(idx,frs); m=metrik(T,cv,B,ada_henti=ada_henti); r=baris(id_,kaedah,varian,m,B,catatan)
    r.update(tambah(T,cv,frs,B)); r['set']=set_; r['menang_ew']=bool(m['cagr']>B['Sama rata 100']['cagr']); return r
</parameter>
<parameter name="file_path">/home/claude/bt/tambahan.py</parameter>
````
</details>


<details><summary>🔧 Alat: Write</summary>

````
<parameter name="content">import sys; sys.path.insert(0,'/home/claude/bt')
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
R=pd.DataFrame(rows,columns=LAJUR2); R.to_csv('/home/claude/bt/QULLAMX.csv',index=False)
import pickle; pickle.dump({k:v for k,v in TT.items()},open('/home/claude/bt/tt.pkl','wb'))
B=penanda(idx,fr); print({k:(round(v['cagr'],4),round(v['mdd'],4),round(v['h1'],4),round(v['h2'],4)) for k,v in B.items()})
print('BEST',best)
</parameter>
<parameter name="file_path">/home/claude/bt/qullamx.py</parameter>
````
</details>


<details><summary>🔧 Alat: Bash</summary>

````
<parameter name="command">cd /home/claude/bt && timeout 590 python3 qullamx.py 2>&1 | tail -30</parameter>
<parameter name="description">Run QULLAMX backtest across 431 stocks and subsets</parameter>
<parameter name="timeout">600000</parameter>
````
</details>


<details><summary>🔧 Alat: Bash</summary>

````
<parameter name="command">python3 -c "
import pandas as pd,pickle
R=pd.read_csv('QULLAMX.csv')
print(R[['set','varian','keputusan','skor','cagr','mdd','h1','h2','n','dagangan_setahun','win','avg','avgwin','avgloss','days','ret10','thn_kalah_spy','gate_gagal','ew_cagr','menang_ew','bulan_untung','bulan10','pegang']].to_string())
TT=pickle.load(open('tt.pkl','rb'))
for k in ['V0 Indikator penuh (BO+EP, LOD, EMA10)','V4 V0 trail SMA20','V2 EP sahaja']:
    T,cv=TT[k];T=T[T.ent>='2019-11-01']
    print('==',k); print(T.why.value_counts(normalize=True).round(3).to_dict())
    print(T.groupby(T.ent.dt.year).ret.agg(['count','mean']).round(3).T.to_string())
    print(cv.resample('YE').last().pct_change().round(3).to_dict())
    print(T.nlargest(3,'ret')[['ticker','ent','ret','days']].to_string()); print(T.nsmallest(3,'ret')[['ticker','ent','ret','days','why']].to_string())
"</parameter>
<parameter name="description">Sanity checks: results table, exit reasons, yearly breakdown, extremes</parameter>
````
</details>


<details><summary>🔧 Alat: Projects</summary>

````
<parameter name="local_path">/home/claude/bt/QULLAMX.csv</parameter>
<parameter name="method">project_write</parameter>
<parameter name="path">registry/QULLAMX.csv</parameter>
````
</details>

# QULLAMX — Keputusan Backtest Shariah: Qullamaggie Breakout + EP (enjin v1.2)

**1. Cara ujian**

| Perkara | Tetapan |
|---|---|
| Isyarat | ▲ BUY (breakout) dan ֍ EP, logik kod awal QULLAMX |
| Masuk | Buka hari selepas isyarat |
| Henti rugi | Low hari isyarat (LOD) |
| Keluar | Buka hari selepas close pertama di bawah EMA10 (V4: SMA20) |
| Had masa | Tiada |
| Ranking | Skor 0–20 hari isyarat (Andaian saya) |
| Portfolio | 8 slot × 12.5%, 1 Nov 2019 – Okt 2026 |

**2. Semua varian, set 431**

| Varian | Keputusan | CAGR | MDD | Separuh 1/2 | Dagangan | Menang | ≥+10% | Gate gagal |
|---|---|---|---|---|---|---|---|---|
| V0 Indikator penuh | DITOLAK | 10.0% | −61.5% | −5.8% / 26.1% | 4,145 | 26% | 9.1% | G3 G4 G5 |
| V1 Breakout sahaja | DITOLAK | 3.6% | −59.2% | −6.5% / 13.5% | 3,931 | 25% | 8.5% | G3 G4 G5 |
| V2 EP sahaja | DITOLAK | 12.2% | **−12.8%** | 7.4% / 16.4% | 285 | 43% | 19.7% | G3 |
| V3 V0 + penapis QQQ | DITOLAK | 7.8% | −49.4% | −0.7% / 15.6% | 2,966 | 26% | 9.2% | G3 G4 G5 |
| **V4 V0 trail SMA20** | DITOLAK | **17.4%** | −57.1% | 6.9% / 27.8% | 3,928 | 23% | 10.4% | G4 |
| V5 Stop ≤ 0.5 ADR | DITOLAK | 5.2% | −45.6% | −10.7% / 21.0% | 1,504 | 25% | 8.2% | G3 G4 G5 |
| QQQ | — | 21.7% | −35.1% | 10.4% / 32.4% | — | — | — | — |
| SPY | — | 15.9% | −33.7% | 9.1% / 22.1% | — | — | — | — |
| Sama rata 431 | — | 21.9% | −40.3% | 16.4% / 27.4% | — | — | — | — |

Tiada varian menang lawan beli semua 431 sama rata.

**3. Ujian konsisten S1–S4 (V4)**

| Set | Keputusan | CAGR | MDD | Sama rata set | Gate gagal |
|---|---|---|---|---|---|
| S1 | DITOLAK | 1.0% | −46.8% | 18.9% | G3 G4 G5 |
| S2 | DITOLAK | 7.9% | −45.8% | 27.9% | G3 G4 |
| S3 | DITOLAK | 10.6% | −26.4% | 21.8% | G3 |
| S4 | DITOLAK | 4.0% | −49.2% | 17.4% | G3 G4 G5 |
| **Lulus** | **0/4** | | | | |

**4. Berapa lama pegang (pulangan purata jika dipegang tepat N hari)**

| Hari | 5 | 10 | 15 | 20 | 30 | 40 | 60 |
|---|---|---|---|---|---|---|---|
| V4 | 0.5% | 1.3% | 2.0% | 2.8% | 4.5% | 6.4% | 9.5% |
| V2 EP | 0.3% | 2.5% | 2.9% | 4.3% | 5.7% | 8.9% | **18.4%** |

Pegangan sebenar V4 purata 9 hari; 74% keluar kena henti LOD. Isyarat BUY tidak pernah mencapai purata +10%; EP mencapai +10% hanya sekitar hari ke-60.

**5. Sasaran bulanan (V4):** bulan untung 45%, bulan ≥ +10% 16%.

**6. Gate V4**

| Gate | Syarat | Nilai | |
|---|---|---|---|
| G1 | Ada henti, rugi purata ≥ −12% | −4.0% | ✅ |
| G2 | ≥ 100 dagangan | 3,928 | ✅ |
| G3 | CAGR > SPY (15.9%) | 17.4% | ✅ |
| G4 | MDD ≥ −45% | −57.1% | ❌ |
| G5 | Kedua separuh positif | 6.9% / 27.8% | ✅ |
| G6 | Long, mekanikal | Ya | ✅ |

**7. Penemuan penting**
- BUY breakout terlalu kerap: ~570 isyarat setahun, 74–66% kena henti LOD. Penapis skor ≥14 tidak cukup memilih.
- 2022 meranapkan V0 (−38%). Penapis QQQ hanya kurangkan MDD ke −49%, sambil menurunkan CAGR.
- **EP ialah bahagian terbaik:** MDD −12.8%, menang 43%, 20% dagangan tutup ≥+10%, untung tiap tahun kecuali 2022 (−7%). Gagal G3 semata-mata kerana terlalu jarang (~41 setahun, anggaran hanya ~2 daripada 8 slot terisi).
- Stop ketat ≤0.5 ADR (bukti vishnuv) **tidak** membantu di sini: CAGR jatuh ke 5.2%.
- Trail SMA20 lebih baik daripada EMA10 (17.4% vs 10.0%): pemenang perlu ruang.

**8. Verdict**

**TIDAK LAYAK: semua 6 varian DITOLAK di set 431, tiada yang mengalahkan beli-semua sama rata, dan varian terbaik (V4) lulus 0/4 subset. Isyarat BUY QULLAMX jangan digunakan untuk wang sebenar; isyarat ֍ EP sahaja yang berpotensi.**

**9. Batasan**
- Senarai Shariah ialah senarai hari ini: bias kemandirian (hasil sebenar mungkin lebih buruk).
- Harga terlaras; data daily sahaja. EP sebenar Qullamaggie masuk ORH hari gap; di sini masuk buka H+1 (edge hari pertama terlepas).
- Andaian saya: ranking ikut skor; SELL = close pertama bawah garis trail (bukan CROSS); penapis QQQ guna SMA; V1–V5 ialah varian yang saya bina daripada jadual percanggahan §12, bukan senarai rasmi.
- Tiada data EPS/berita, jadi syarat pemangkin EP tidak diuji.

registry/QULLAMX.csv disimpan (10 baris). Jalankan /step1 untuk kaedah seterusnya atau /step3 untuk papan kedudukan.
