# Агенты по флагам Unleash и экспериментам

Два сценария для Claude Code:

| Команда | Что делает |
|---|---|
| `/flags-audit` | Берёт все флаги Unleash, включённые на проде, и находит по каждому контекст в Asana и Slack: зачем флаг, кто владелец, какой статус, есть ли противоречия и можно ли его удалить. |
| `/experiments-daily` | Ежедневная сводка: для каждого запущенного эксперимента (флаг с вариантами на проде) считает основные метрики в Amplitude по вариантам и добавляет контекст из Asana и Slack. Может отправлять сводку в Slack. |

## Из чего состоит

- `scripts/unleash_prod_flags.py` — выгрузка флагов через Unleash Admin API (только stdlib): раскатка, варианты, сравнение со вчерашним снимком.
- `.claude/agents/flag-context-researcher.md` — субагент, который ищет контекст по флагам в Asana и Slack (только чтение).
- `.claude/agents/experiment-metrics-analyst.md` — субагент, который считает метрики экспериментов в Amplitude (только чтение).
- `.claude/skills/flags-audit`, `.claude/skills/experiments-daily` — оркестраторы: запускают субагентов параллельно пачками и собирают отчёт в `reports/`.
- `config/agents.json` — настройки.

## Настройка

1. Добавьте в секреты окружения `UNLEASH_URL` (без `/api`) и `UNLEASH_TOKEN` (Admin API token) и разрешите хост Unleash в сетевой политике. Облачный прокси пропускает только HTTPS, поэтому Unleash должен быть доступен по `https://` (сейчас он на `http://unleash.htz.zncr.pro:4242`). Запускайте в окружении **EU**: там открыта сеть.
2. Заполните `config/agents.json`:
   - `unleash.production_environment` — имя прод-окружения; в `projects` можно перечислить проекты (если пусто, берутся все), в `ignore_flags` — флаги, которые не нужно проверять;
   - `asana.workspace_gid` / `project_gids` — где искать задачи;
   - `slack.search_channels` — ID каналов, где обсуждают фичи; `report_channel` — канал для отчётов;
   - `amplitude.project_id`, `variant_property` (как вариант попадает в Amplitude, `{flag}` заменяется на ключ флага), `exposure_event`, `key_metrics` / `guardrail_metrics` (ID метрик или имена событий).
3. Проверьте вручную: `/flags-audit`, затем `/experiments-daily`.
4. Ежедневный запуск — плановой задачей Claude Code с промптом `/experiments-daily` (например, по будням в 10:00).

Изменения со вчерашнего дня считаются по `state/flags_snapshot.json`. В облачной сессии, которая каждый раз создаётся заново, снимка не будет, и блок «изменения» появится только со второго запуска внутри одной сессии.
