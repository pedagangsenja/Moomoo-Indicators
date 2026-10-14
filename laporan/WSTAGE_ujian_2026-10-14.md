# WSTAGE — Semakan kod dan ujian semula (14 Okt 2026)

Kod akhir: `indikator/WSTAGE_harian.mai`. Skrip: `ujian/wstage/sim.py` (simulasi) dan `ujian/wstage/an.py` (analisis); jalankan dari akar repo.

## Perubahan kod berbanding kod akhir chat 03 (mesej [31])
| Baris | Lama | Baru | Sebab |
|---|---|---|---|
| `GAGAL` | `CLOSE<REF(HHV(HIGH,BASELEN),VOLWIN+1)` | `CLOSE<VALUEWHEN(BELI,REF(HHV(HIGH,BASELEN),1))` | Pepijat: rujukan tetap 21 bar hanya sama dengan paras breakout jika BUY tepat 20 bar lalu |
| `BELIC` | `... AND MAPD>MAPJ AND ...` | dibuang | Ujian 2: tiada kesan konsisten |

Disahkan dalam Moomoo (14 Okt 2026): kod diterima, `VALUEWHEN` berfungsi, BUY/SELL muncul pada MGNI, DV, ALAB.

## Kaedah
431 saham (S1–S4), Feb 2020 – 2 Okt 2026, CERUN 40, SELL buku, kos 0.1% setiap belah. Masuk buka hari selepas BUY; keluar buka hari selepas SELL/GAGAL. Lebihan = pulangan dagangan − pulangan indeks sama rata 431 saham bagi tempoh sama. Selang 95% = bootstrap 2,000 kali, sampel semula ikut saham.

## Ujian 1 — pembetulan GAGAL
| Varian | Dagangan | Lebihan | Kerugian purata | Hari pegangan | Keluar GAGAL |
|---|---|---|---|---|---|
| Asas, GAGAL lama | 439 | 12.9% | −10.0% | 135 | 47% |
| Asas, GAGAL baharu | 440 | 11.8% | −8.6% | 123 | 50% |
| +MA50>MA150, GAGAL lama | 371 | 13.8% | −10.7% | 142 | 44% |
| +MA50>MA150, GAGAL baharu | 372 | 11.8% | −9.0% | 124 | 50% |

Beza baharu − lama (asas): −1.1% [−3.5, 0.8], tidak signifikan. Pembetulan dikekalkan kerana logik betul.

## Ujian 2 — MA50>MA150 luar sampel (GAGAL baharu)
| Pecahan | Beza lebihan (dengan − tanpa) |
|---|---|
| Semua | 0.0% [−3.3, 3.2] |
| 2020–22 / 2023–26 | −0.6% / +0.7% |
| 2020–23 / 2024–26 | −1.5% / +2.1% |
| S1+S2 / S3+S4 | +0.5% / −0.3% |

Tiada kesan konsisten; negatif bila data awal menjadi set uji. Syarat dibuang.

## Penemuan: kelebihan bergantung pada beberapa dagangan
| Varian (GAGAL baharu) | Median lebihan | Purata pangkas 5% | Purata tanpa 5 teratas | Pulangan ≥ +10% |
|---|---|---|---|---|
| Asas | −4.9% | −5.0% | +0.3% | 24% |
| +MA50>MA150 | −5.6% | −5.2% | −0.5% | 25% |

Pemenang utama: AXTI (+2,000%), BE (+1,200%), SMCI (+1,000%). Tanpa 5 dagangan teratas, 2020–22 = −7% hingga −10%. Lebihan 2020–22 keseluruhan: 2.8% [−7.8, 19.1].

## Percanggahan dengan chat 03
Varian MA50>MA150 sepadan (13.8% vs 13.9%, P1 2.0% vs 2.1%, P2 20.4% vs 20.4%), tetapi asas 12.9% di sini vs 9.4% dalam chat. Punca belum dikenal pasti (kemungkinan data berbeza daripada muat naik asal). Dakwaan "9.4% → 13.9% kerana MA50>MA150" tidak dapat diulang.

## Verdict
**Guna WSTAGE sebagai penapis trend sahaja: dagangan biasa rugi ~5% berbanding pasaran, dan keuntungan purata datang daripada segelintir pemenang luar biasa.**

## Description Moomoo (ganti bahagian ISYARAT dan HAD)
```
ISYARAT
BUY (segi tiga hijau): breakout dari base + volume >= 3x purata 50 hari + MA150 tidak turun + kekuatan harga positif/naik. Hanya pada peralihan ke Stage 2.
SELL (segi tiga merah): tutup bawah MA150 yang tidak lagi naik, ATAU tutup bawah paras breakout dalam 20 hari selepas BUY. Hanya selepas BUY.
Berlian cyan (bawah): entry B - pullback ke MA50 dengan volume kecil selepas BUY.
Berlian oren (atas): amaran - MA150 mendatar, kekuatan harga jatuh bawah 0, atau tutup bawah MA50 dalam Stage 2. Amaran sahaja, bukan isyarat jual.
HENTI RUGI (manual): low terendah 20 hari sebelum BUY.

HAD
- Diuji atas 431 saham Shariah (2020-2026): median dagangan -5% berbanding pasaran; keuntungan purata datang daripada beberapa pemenang besar.
- Tiada kelebihan 2020-2022.
- Guna sebagai penapis trend, bukan sistem berdiri sendiri.
- Purata pegangan ~4 bulan.
- Kekuatan harga = harga vs purata 250 hari sendiri, bukan Mansfield RS.
- Versi mingguan belum diuji.
```

## Belum diuji
Tanda aras SPY; peringkat portfolio; versi mingguan; bias kemandirian (senarai Shariah hari ini).
