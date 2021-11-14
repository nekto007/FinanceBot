def help(update, context):
    update.message.reply_text(
        f'/div *ticket* - информация о дивидендах: /div aflt \n'
        f'/trand *ticket* - тренд эмитента: /trand aflt \n'
        f'/price *ticket*, *ticket - текущая цена бумаги эмитента: /price aflt \n'
        f'/avg15 *ticket*, *ticket - скользящая средняя за 15 дней: /avg15 aflt \n'
        f'/avg50 *ticket*, *ticket - скользящая средняя за 50 дней: /avg50 aflt \n'
        f'/curr - текущая котировка валют: /curr \n'
        f'/rub, /usd, /eur - конвертер: /rub 5500 \n'
        f'/hist *usd/rub (eur/rub)* *days*: график валютной пары: /hist usd/rub 15 \n'
        f'/info - информация о торгуемых бумагах биржи: /info \n'
        f'/info *ticket* - информация о конкретной бумаге: /info aflt \n'
        f'/alert *ticket* *цена* — Добавить оповещение(SBER — тикер, 354.12 — цена, '
        f'на которой придет уведомление): /alert SBER 354.12 \n'
        f'/alert remove *ticket* — Все оповещения по указанному тикету будут удалены: /alert remove SBER \n'
        f'/list_alert - показать список всех оповещений: /list_alert \n'
        f'/subs *ticket* — Добавить подписку(SBER — тикер)'
        f'на тикер и тогда по рабочим дням в 09:00(мск) я отправлю сообщение): /subs SBER \n'
        f'/subs remove *ticket* — Подписка по указанному тикету будут удалена: /subs remove SBER \n'
        f'/list_subs - показать список всех подписок: /list_subs')


if __name__ == '__main__':
    pass
