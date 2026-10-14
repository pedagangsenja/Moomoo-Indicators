---
name: weinstein-moomoo-indicator
description: Azim's Moomoo custom indicator styled like SMRTMCDX, based on Stan Weinstein Stage Analysis (BUY/SELL by color coding)
sources: [chat]
aliases: [Weinstein indicator, Stage Analysis indicator, Weinstein SMRTMCDX]
---
- [stated] Building a Moomoo indicator like SMRTMCDX based on Weinstein Stage Analysis (Oct 2026); research summary in Weinstein_Stage_Analysis_Ringkasan.md; main goal is clear BUY/SELL timing via color coding
- [stated] Chose: usable on both weekly and daily (adjustable parameters), Mansfield RS via INDEXC with no-index fallback, SELL sensitivity per the book (close below non-rising 30WMA)
- [stated] 14 Oct 2026: GAGAL bug fixed (VALUEWHEN breakout level), MA50>MA150 removed (no out-of-sample effect); median trade −5% vs market, edge from few outliers; use as trend filter only. Code in indikator/WSTAGE_harian.mai, report in laporan/WSTAGE_ujian_2026-10-14.md
