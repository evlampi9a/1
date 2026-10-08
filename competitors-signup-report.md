# Регистрация у конкурентов ZenCreator — сводный отчёт

_Дата проверки: 08.10.2026. Формы открывались headless-браузером Chromium (Playwright), дополнительно — справки и обзоры._
_Пометки: ✅ — видно на странице при проверке; 📄 — из официальной справки; ⚠️ — из сторонних обзоров, проверить вручную._

## 1. Сводная таблица

| Платформа | Тип | Способы входа | Поля email-формы | 18+ / возраст | Бонус на форме | Бесплатно вообще |
|---|---|---|---|---|---|---|
| **ZenCreator** | AI / NSFW | Google ✅ | email + пароль + чекбокс ✅ | строка «confirm that you are 18+» ✅ | ❌ нет ✅ | 0 кредитов 📄 |
| **Higgsfield** | AI | Google, Apple, Microsoft ✅ | только email → 6-значный код ✅📄 | 18+ в ToS 📄 | **«Sign in with work email & Get 50 credits»** + баннер «Sign up — 30% OFF» ✅ | 50 кредитов (рабочий email) ✅ |
| **PixAI** | AI / NSFW-toggle | Google (Recommended), Discord, X, Apple, email ✅ | email отдельной кнопкой ✅ | toggle NSFW в настройках ⚠️ | **«free daily credits», «10,000 Free Credits Daily — No credit card needed»** ✅ | 10 000/день ✅ |
| **Promptchan** | NSFW | Google, Apple, email ✅ | только email ✅ | «you confirm that you are at least 18» ✅ | **«Starter credits included», «No credit card required», список «что откроется»** ✅ | стартовые Gems 📄 |
| **OpenArt** | AI | Google, Apple, Discord, X ✅ | email + пароль + повтор пароля ✅ | — | ❌ ✅ | 40 кредитов / 7 дней 📄 |
| **Krea** | AI | Google, Apple, SSO, email ✅ | только email ✅ | — | ❌ ✅ | ~100 CU/день ⚠️ |
| **Foxy AI** | AI-инфлюенсеры | Google, Facebook, Apple, X ✅ | только email ✅ | только ToS ✅ | ❌ ✅ | оплата за изображение ⚠️ |
| **Civitai** | AI / NSFW-toggle | Discord, Google, GitHub, Reddit, email ✅ | только email (magic link) ✅ | 18+ в ToS; **ушёл из UK** вместо age verification 📄 | ❌ ✅ | Buzz за активность ⚠️ |
| **SeaArt** | AI | Google, Apple, Discord, Microsoft, email ⚠️ | — (модалка не открылась) | — | — | генератор открыт **без входа** ✅; ~130–150 Stamina/день ⚠️ |
| **Leonardo** | AI | Google, Apple, Microsoft, email ⚠️ | — (бот-защита) | — | — | 150 токенов/день ⚠️; онбординг-анкета ⚠️ |
| **Candy.ai** | NSFW | email, Google, Apple, Discord ⚠️ | — (модалка не открылась) | самоподтверждение 18+ ⚠️ | на главной: «Create Free Account», «-70%», free trial ✅ | free trial + токены ✅ |
| **SoulGen** | NSFW | email, Google ⚠️ | — | — | — | ~1 кредит/день ⚠️ |
| **Glambase** | AI-инфлюенсеры | — | — | 18+ только в ToS ⚠️ | ❌ на главной ✅ | — |
| **Pornhub** | adult (ориентир) | Google ✅ | email + пароль ✅ | **полноэкранный гейт «I am 18 or older — Enter / I am under 18 — Exit»** + ссылка на Parental Controls ✅ | «Sign up for free» ✅ | бесплатный аккаунт |
| **OnlyFans** | adult (ориентир) | X, Google ✅ | email + пароль ✅ | «confirm that you are at least 18» ✅; креаторы — ID + селфи (Ondato) 📄 | ❌ ✅ | — |
| **Fanvue** | AI-креаторы (монетизация) | email, Google ⚠️ | — (бот-защита) | креаторы — ID + live-селфи (Ondato) 📄 | — | — |

Не удалось открыть: Tensor.art, Leonardo, Pornify, Fanvue (Cloudflare/Vercel bot-защита), PornPen (недоступен из сети).

## 2. Ключевые паттерны

1. **Способы входа: стандарт — Google + Apple + email.** Discord — для AI/NSFW-аудитории (Civitai, PixAI, OpenArt), X — у NSFW/adult (PixAI, OpenArt, OnlyFans, Foxy). Microsoft — у «про»-инструментов (Higgsfield, Leonardo). Вход по телефону/SMS не нашёлся ни у кого.
2. **Беспарольный email.** Higgsfield, Krea, Promptchan, Civitai, Foxy, PixAI просят только email и шлют код или ссылку. Пароль требуют ZenCreator, OpenArt, Pornhub, OnlyFans.
3. **Бонус на форме — у 3 из ~10 открывшихся форм** (Higgsfield, PixAI, Promptchan), три формата:
   - конкретная цифра кредитов («Get 50 credits»);
   - ежедневный бесплатный лимит («10,000 Free Credits Daily»);
   - список «что сразу откроется» + «Starter credits included».
   «No credit card required» — у двух из трёх.
4. **Возраст: везде самоподтверждение.** У AI-генераторов — строка под кнопкой. У Pornhub — отдельный полноэкранный гейт до входа на сайт + Parental Controls. Строгая проверка (ID + селфи) — только для креаторов с выплатами (OnlyFans, Fanvue).
5. **Регуляторика ужесточается.** UK Online Safety Act (с 25.07.2025) не принимает клик «мне 18+» для порно-контента, в т.ч. GenAI; ~27 штатов США требуют age verification (Верховный суд в 2025 оставил в силе закон Техаса). Pornhub и Civitai в ответ блокируют регионы. Гейт Pornhub из таблицы — версия для региона без таких требований (как видит его наш браузер).
6. **Регистрация обязательна до генерации** почти везде; исключение — SeaArt (генератор открыт без входа). Promptchan закрывает регистрацией даже просмотр галереи.

## 3. Рекомендации для ZenCreator

1. **Бонус на форме:** «Create account & get N free credits · No credit card required». Сейчас 0 бесплатных кредитов — это и отличие от всего рынка, и частая жалоба в отзывах (Trustpilot). Запустить как A/B-тест конверсии регистрации.
2. **Больше способов входа:** добавить Apple, Discord и X к Google.
3. **Email без пароля:** код или magic link вместо «придумайте пароль».
4. **Продающая форма в стиле Promptchan:** 2–3 пункта «что откроется» (No filter, 4K, AI-инфлюенсеры, видео) рядом с кнопками.
5. **Возраст и NSFW:**
   - отдельный гейт 18+ до показа NSFW-контента (по образцу Pornhub), а не только строка под формой;
   - NSFW — явный переключатель после подтверждения;
   - гео-зависимая строгая проверка возраста (оценка по лицу / ID) для UK и штатов США с законами об age verification;
   - если появятся выплаты креаторам — KYC (ID + селфи), как у Fanvue/OnlyFans.
