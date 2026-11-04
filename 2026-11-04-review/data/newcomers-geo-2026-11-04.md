# Топ-10 стран и новички, W43 (19–25.10) vs W44 (26.10–01.11)

Amplitude 717020, окна по UTC-полуночи: W43 1792368000–1792972799, W44 1792972800–1793577599. Выгрузка 04.11.

## Топ-10 стран по выручке W44 (user property country)
data_table: PROPSUM($revenue) Payment Succeeded, TOTALS/UNIQUES Payment Succeeded, UNIQUES Payment Started,
TOTALS и PROPSUM($revenue) Payment Succeeded c isFirstPayment=True, UNIQUES Registration Completed.
Overall: выручка 684 317,52 / 731 720,11 — совпадает с недельным тоталом отчёта.
Конверсия: funnel Payment Started → Payment Succeeded, 1800 с, group by country.
Сырьё: geo-top10-w43-w44.json (rev43, rev44, pay43, pay44, payers43, payers44, starts43, starts44,
first43, first44, firstrev43, firstrev44, reg43, reg44, conv43, conv44).
(none) по выручке: 26 397,66 / 34 798,94.

## Новички, окно 24 ч (funnel Registration Completed → Payment Started → Payment Succeeded)
| | W43 | W44 |
|---|---|---|
| Регистрации | 40 790 | 39 272 |
| Дошли до оплаты за 24 ч | 1 900 | 1 762 |
| Заплатили за 24 ч | 822 | 902 |
| Медиана старт → оплата, с | 127 | 76 |
| Сделали генерацию за 24 ч (Reg → Task Created) | 887 | 1 079 |
| Первых оплат (isFirstPayment=True), по дате оплаты | 1 507 | 1 741 |
| Выручка с первых оплат, $ | 46 007,80 | 51 092,42 |
platformType регистраций: zencreator 40 596 / 39 097, openmov 172 / 163, прочие 22 / 12.

## Новички по странам, 24 ч: регистрации, заплатили
W43: (none) 21410/337, US 4506/176, IN 1723/3, ID 852/2, UK 801/48, BR 793/7, MX 740/6, DE 612/22, CA 606/32, ES 472/13, AR 396/0, AU 372/25
W44: (none) 21339/413, US 3972/180, IN 1433/5, ID 869/0, BR 833/6, MX 808/7, UK 778/52, DE 578/29, CA 520/30, AR 482/1, ES 438/4, AU 356/25
