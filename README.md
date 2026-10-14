# Moomoo Indicators

Arkib Project claude.ai **"Moomoo Indicators"** — indikator tersuai Moomoo (Mai Language) gaya SMRTMCDX berdasarkan kaedah Minervini, Oliver Kell, Weinstein dan Qullamaggie, beserta data dan keputusan backtest.

## Struktur

| Folder | Isi |
|---|---|
| `chats/` | Transkrip penuh setiap chat (Markdown) |
| `data/` | `dataset_S1`–`S4.csv` (431 saham Shariah, harian, Jan 2019 – Okt 2026) + `index_benchmark.csv` (SPY, QQQ) |
| `registry/` | `QULLAMX.csv` — keputusan backtest enjin v1.2 |
| `notes/` | Nota memori Project |
| `indikator/` | Kod Mai Language terkini (`WSTAGE_harian.mai`) |
| `laporan/` | Laporan ujian (`WSTAGE_ujian_2026-10-14.md`) |
| `ujian/` | Skrip simulasi Python; jalankan dari akar repo |

## Chat

| Fail | Indikator | Status |
|---|---|---|
| `chats/01-minervini.md` | MINERVINI SEPA | Kod awal, belum diuji |
| `chats/02-oliver.md` | KELLCYCLE (Oliver Kell) | Kod awal, belum diuji |
| `chats/03-weinstein.md` | WSTAGE (Weinstein) | Kod akhir: `indikator/WSTAGE_harian.mai` (CERUN 40, GAGAL dibetulkan 14 Okt 2026); penapis trend sahaja |
| `chats/04-qullamaggie.md` | QULLAMX (Qullamaggie) | Backtest: semua varian DITOLAK; EP sahaja berpotensi |

## Nota transkrip
- Mesej yang hanya mengandungi tangkapan skrin ditanda _(tangkapan skrin / lampiran sahaja)_ — imej tidak dieksport.
- Panggilan alat Claude (kod Python, carian) dilipat dalam blok `🔧 Alat`. Output alat tidak termasuk dalam transkrip sumber.
