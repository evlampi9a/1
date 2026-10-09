Собери статистику продукта Lounge за ПРОШЛЫЙ день (сутки по часовому поясу проекта Amplitude) и отправь одно сообщение в Slack-канал #thelounge (channel_id C0C0ZEMEN1J). Больше ничего не делай.

1. Amplitude (организация zencreator, проект Production, projectId 717020). Вызови query_amplitude_data с chart:
{"kind":"data_table","name":"Lounge · ежедневная сводка","date_range":{"relative":"Last 0 Days Offset 1"},"columns":[
 {"metric_type":"PROPSUM","event":{"event":"Lounge Credits Spent","where":[],"group_by":[]},"aggregation_property":"credits"},
 {"metric_type":"UNIQUES","event":{"event":"Lounge Credits Spent","where":[],"group_by":[]}},
 {"metric_type":"UNIQUES","event":{"event":"ce:Lounge: написал персонажу","where":[],"group_by":[]}},
 {"metric_type":"UNIQUES","event":{"event":"ce:Lounge: 5-е сообщение в разговоре","where":[],"group_by":[]}}
]}
Колонки: A = кредитов потрачено, B = людей потратили кредиты, C = людей писали персонажам, D = людей с диалогами 5+ сообщений.

2. Slack: slack_send_message, channel_id C0C0ZEMEN1J, текст (дата вчерашняя ДД.ММ.ГГГГ):

**Lounge · статистика за <дата>**
• Кредитов потрачено: <A> (потратили <B> чел.)
• Писали сообщения персонажам: <C> чел.
• Диалоги 5+ сообщений: <D> чел.
<https://app.amplitude.com/analytics/zencreator/dashboard/z09za0qn|Дашборд Lounge>

3. Если Amplitude вернул ошибку или пустые данные — не выдумывай цифры, отправь «Lounge · статистика за <дата>: не удалось получить данные из Amplitude (<причина>)». Ровно одно сообщение.
