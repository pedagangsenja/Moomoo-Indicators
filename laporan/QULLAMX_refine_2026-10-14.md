# QULLAMX v2 — Refine backtest dan paparan baru (14 Okt 2026)

Kod: `indikator/QULLAMX_harian.mai`. Skrip (jalankan dari akar repo): `ujian/qullamx/qullamx.py` (ulang V0–V5), `refine.py` (grid 51 varian), `sah_ep.py` (S1–S4 + kepekaan EP), `akhir.py` (konfigurasi akhir → registry), `semak_mai.py` (logik .mai lawan enjin). Enjin v1.2 tidak diubah; ulangan V0–V5 sama tepat dengan registry asal.

## Grid 51 varian (set 431)
Dimensi: trail EMA10/SMA10/SMA20 × ambang skor 14/16 × penapis QQQ × volume breakout ≥1.5× × EP diutamakan dalam ranking, + EP sahaja × 3 trail.
- **Semua 48 varian dengan breakout DITOLAK.** Yang terbaik gagal G5 (separuh 2020–22 negatif) atau G4 (MDD < −45%). Volume ≥1.5× dan ambang 16 kurangkan MDD ke −25%–−35% tetapi separuh pertama kekal rugi.
- **EP sahaja + trail SMA20** satu-satunya yang lulus semua gate: SIMPAN, CAGR 19.7%, MDD −19.5%.
- Penapis QQQ pada EP merosakkan (CAGR 8.7%).

## Kepekaan ambang EP (trail SMA20, set 431)
| Gap / RVOL | CAGR | MDD | Dagangan | Keputusan |
|---|---|---|---|---|
| 10% / 3× (asal) | 19.7% | −19.5% | 285 | SIMPAN |
| **8% / 3× (dipilih)** | **22.5%** | −24.5% | 383 | SIMPAN |
| 12% / 3× | 16.0% | −18.4% | 214 | SIMPAN |
| 10% / 2× | 16.7% | −18.5% | 394 | SIMPAN |
| 10% / 4× | 18.1% | −19.1% | 201 | SIMPAN |
| 8% / 2× | 22.2% | −21.3% | 572 | SIMPAN |

Semua jiran lulus, jadi keputusan tidak bergantung pada satu nilai ambang. Gap 8% dipilih kerana lebih banyak isyarat (slot lebih terisi).

## Konfigurasi akhir (V6) — 431 dan S1–S4
| Set | Keputusan | CAGR | MDD | Separuh 1/2 | Dagangan | Menang | Sama rata |
|---|---|---|---|---|---|---|---|
| 431 | SIMPAN (56.0) | 22.5% | −24.5% | 9.4% / 34.7% | 383 | 41% | 21.9% |
| S1 | DITOLAK | −3.2% | −23.2% | −6.9% / 0.0% | 90 | 30% | 18.9% |
| S2 | DITOLAK | 7.6% | −8.0% | 10.4% / 5.4% | 97 | 51% | 27.9% |
| S3 | DITOLAK | 14.4% | −11.5% | 8.3% / 19.9% | 109 | 42% | 21.8% |
| S4 | DITOLAK | 3.6% | −20.1% | 4.0% / 3.3% | 87 | 41% | 17.4% |

Subset gagal terutamanya kerana isyarat terlalu jarang (~13 setahun bagi ~108 saham; 8 slot jarang terisi, G2 < 100 dagangan). MDD kekal ≤ −23% di semua set. S1 rugi sebenar.

## Paparan baru (lampu isyarat)
Satu bar, tinggi = skor 0–20: hijau (trend OK, skor ≥14), kuning (trend OK, skor 8–13), merah (lain-lain). Latar kelabu gelap = skala 20. Simbol: ▲ BUY (EP), ▼ SELL putih (close < SMA20), ▼ STOP merah (Low sentuh Low hari BUY). Breakout BUY, SEDIA, LANGKAU, QAVG dan latar hijau/merah dibuang.

## Pengesahan logik .mai
`semak_mai.py`: 383/386 dagangan enjin sepadan tepat (tarikh dan jenis keluar); 3 baki masih terbuka di hujung data. Belum disahkan dalam Moomoo.

## Batasan
- Bias kemandirian (senarai Shariah hari ini); harga terlaras; daily sahaja.
- EP masuk buka H+1, bukan ORH hari gap; tiada data EPS/berita.
- Jika EP baru berlaku semasa masih pegang, indikator mula kiraan semula dari EP baru; enjin mengabaikannya (jarang).
- Bar warna = konteks kekuatan saham sahaja; tidak diuji sebagai isyarat.
