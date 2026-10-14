# Chat: Minervini

- Pautan asal: https://claude.ai/chat/544926e9-250a-4935-a0cd-adcb1fb94c1e
- Kemas kini terakhir: 2026-10-13T02:58:11.448795+00:00
- Bilangan giliran: 2

---

## [0] 👤 Azim — Tue 2026-10-13 10:03

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

MMAVG:MM_MA10,COLORBLUE,LINETHICK2;  Saya Perlukan satu indicator lebih kurang macam SMRTMCDX. base on color coding. Yang penting saya nak tahu bila nak buy dan sell, macam smartmcdx. Anda selaku pakar dalam pembinaan indicators, fikirkan satu cara macamana nak represent data data penting dari minervini dalam bentuk lebih kurang macam SMRTMCDX ni. Yang penting user faham apa yang dia tgk. Gunakan color yang betul dan menarik. Kaji dahulu cara terbaik, dan bina.

## [1] 🤖 Claude

# MINERVINI SEPA — Indikator Moomoo (gaya SMRTMCDX)

## Konsep paparan

Skala menegak ialah 0 hingga 20, seperti SMRTMCDX. Bahagian **di atas garis 0 menunjukkan kekuatan**, disusun bertindan mengikut urutan SEPA. Bahagian **di bawah garis 0 menunjukkan amaran**.

| Warna | Lapisan | Mata | Maksud |
|---|---|---|---|
| Hijau terang | Trend (TT1–TT8) | 0–10 | Penuh 10 bermaksud Peringkat 2 sah, semua 7 syarat Trend Template lulus |
| Hijau pudar | Trend tidak lengkap | 0–10 | Belum Peringkat 2. Jangan beli |
| Emas | Setup VCP (VC1–VC4) | 0–6 | Muncul hanya jika Peringkat 2. Makin tinggi, makin ketat setup |
| Cyan | Tembusan (EN1–EN4) | 0–4 | Muncul pada hari harga tembus pangsi |
| Merah (bawah 0) | Pelanggaran (W1–W6) | 0 hingga −9 | Makin dalam, makin lemah |
| Garis biru MVAVG | Purata skor bersih 10 hari | — | Naik bermaksud kekuatan bertambah. Turun bermaksud kekuatan melemah |

| Penanda | Maksud |
|---|---|
| ▲ BUY (hijau, bawah) | Peringkat 2 + RS + VCP ketat semalam + tembus pangsi dengan volum ≥140% + belum terlanjur (≤5% atas pangsi) |
| ▼ SELL (merah, atas) | Tutup di bawah MA50, ATAU ≥3 pelanggaran serentak |
| ◆ TP (emas, atas) | Jual sebahagian ketika kuat: terlanjur ≥25% atas MA50 + hari naik/julat terbesar dalam 60 hari atau gap naik |
| ● (cyan, atas) | VCP siap, pantau pangsi (seperti SM dalam SMRTMCDX) |

## Kod

```
CC:=CLOSE; HH:=HIGH; LL:=LOW; VV:=VOLUME;
PIVN:=10; VDRY:=0.6; VBO:=1.4; CHASE:=1.05; RSMIN:=0.20; EXTN:=0.25;

MA20:=MA(CC,20); MA50:=MA(CC,50); MA150:=MA(CC,150); MA200:=MA(CC,200);
VMA50:=MA(VV,50);

TT1:=IF(CC>MA150 AND CC>MA200,1,0);
TT2:=IF(MA150>MA200,1,0);
TT3:=IF(MA200>REF(MA200,21),1,0);
TT4:=IF(MA50>MA150 AND MA50>MA200,1,0);
TT5:=IF(CC>MA50,1,0);
TT6:=IF(CC>=1.30*LLV(LL,252),1,0);
TT7:=IF(CC>=0.75*HHV(HH,252),1,0);
RSW:=0.4*(CC/REF(CC,63)-1)+0.2*(CC/REF(CC,126)-1)+0.2*(CC/REF(CC,189)-1)+0.2*(CC/REF(CC,252)-1);
TT8:=IF(RSW>=RSMIN,1,0);
TTN:=TT1+TT2+TT3+TT4+TT5+TT6+TT7;
STAGE2:=TTN=7;
TREND:=(TTN+TT8)*1.25;

R10:=HHV(HH,10)-LLV(LL,10);
R30:=HHV(HH,30)-LLV(LL,30);
VC1:=IF(R10<0.5*R30,1,0);
VC2:=IF((HHV(HH,5)-LLV(LL,5))/CC<=0.06,1,0);
VC3:=IF(MA(VV,5)<=VDRY*VMA50,1,0);
VC4:=IF(LLV(LL,10)>REF(LLV(LL,20),10),1,0);
VCN:=VC1+VC2+VC3+VC4;
SETUP:=IF(STAGE2,VCN*1.5,0);

PIVOT:=REF(HHV(HH,PIVN),1);
EN1:=IF(HH>PIVOT,1,0);
EN2:=IF(VV>=VBO*VMA50,1,0);
EN3:=IF(CC<=CHASE*PIVOT,1,0);
EN4:=IF(CC>(HH+LL)/2,1,0);
BRK:=IF(STAGE2,EN1*(1+EN2+EN3+EN4),0);

TOTAL:=TREND+SETUP+BRK;

W1:=IF(COUNT(LL<REF(LL,1),3)=3 AND VV>VMA50,1,0);
W2:=IF(CC<MA20 AND VV>VMA50,1,0);
W3:=IF(CC<MA50,1,0);
W4:=IF(COUNT(CC<REF(CC,1),10)>COUNT(CC>REF(CC,1),10),1,0);
W5:=IF(COUNT(CC<(HH+LL)/2,10)>=6,1,0);
W6:=IF(CC<REF(CC,1) AND VV>=HHV(VV,60),1,0);
WN:=W1+W2+W3+W4+W5+W6;
WBAR:=WN*1.5;

BUY:=STAGE2 AND TT8=1 AND REF(VCN,1)>=3 AND EN1=1 AND EN2=1 AND EN3=1;
BUY1:=BUY AND COUNT(BUY,10)=1;

SELLA:=CROSS(MA50,CC) AND COUNT(STAGE2,30)>0;
SELLB:=WN>=3 AND REF(WN,1)<3 AND COUNT(STAGE2,30)>0;
SELL:=SELLA OR SELLB;
SELL1:=SELL AND COUNT(SELL,5)=1;

UPD:=CC-REF(CC,1);
S1:=IF(UPD>0 AND UPD>=HHV(UPD,60),1,0);
S2:=IF(HH-LL>=HHV(HH-LL,60) AND CC>REF(CC,1),1,0);
S3:=IF(LL>REF(HH,1),1,0);
TP:=(CC-MA50)/MA50>=EXTN AND (S1+S2+S3)>=1;
TP1:=TP AND COUNT(TP,10)=1 AND SELL1=0;

READY:=STAGE2 AND TT8=1 AND VCN>=3 AND EN1=0;
READY1:=READY AND COUNT(READY,10)=1;

STICKLINE(1,0,20,1,0),COLOR1F2933;
STICKLINE(TOTAL>0,0,TOTAL,1,0),COLOR00E5FF;
STICKLINE(TREND+SETUP>0,0,TREND+SETUP,1,0),COLORFFC400;
STICKLINE(STAGE2,0,TREND,1,0),COLOR00C853;
STICKLINE(STAGE2=0 AND TREND>0,0,TREND,1,0),COLOR4E6E58;
STICKLINE(WN>0,0,-WBAR,1,0),COLORFF1744;

DRAWTEXT(BUY1,-11,'▲'),COLOR00FF00;
DRAWTEXT(BUY1,-13,'BUY'),COLOR00FF00;
DRAWTEXT(SELL1,22,'▼'),COLORFF1744;
DRAWTEXT(SELL1,24,'SELL'),COLORWHITE;
DRAWTEXT(TP1,22,'◆'),COLORFFC400;
DRAWTEXT(TP1,24,'TP'),COLORFFC400;
DRAWTEXT(READY1,21,'●'),COLOR00E5FF;

MVAVG:MA(TOTAL-WBAR,10),COLOR2979FF,LINETHICK2;
```

## Cara baca (urutan keputusan)

1. **Hijau pudar** bermaksud saham diabaikan.
2. **Hijau terang penuh** bermaksud saham masuk senarai pantau.
3. **Emas meninggi dan ● muncul** bermaksud setup sedia. Tetapkan *buy-stop* 1–2% di atas pangsi (paras tertinggi 10 hari).
4. **▲ BUY** bermaksud masuk. Henti rugi diletakkan di bawah paras rendah penguncupan terakhir, maksimum 8%. Henti rugi ini perlu dibuat secara manual kerana tidak dilukis oleh indikator.
5. **Merah mula muncul** bermaksud perlu berwaspada. **◆ TP** bermaksud jual sebahagian. **▼ SELL** bermaksud keluar.

## Perkara perlu disemak

- Jika Moomoo memaparkan ralat pada `VOLUME`, tukar kepada `VOL`.
- **TT8 ialah proksi** ⚪ (momentum berwajaran 12 bulan ≥20%), bukan RS Rating IBD. Tetapkan `RSMIN:=-9` untuk mematikannya.
- Parameter `PIVN`, `VDRY`, `VBO`, `CHASE`, `RSMIN` dan `EXTN` ialah pilihan saya ⚪, bukan angka Minervini. Nilai-nilai ini perlu disahkan melalui backtest.
- Ambang "≥3 pelanggaran untuk SELL" juga pilihan saya ⚪, kerana Minervini tiada angka tetap untuk ini.
- Saham dengan sejarah kurang 252 hari dagangan tidak akan lulus TT6, TT7 dan TT8.
