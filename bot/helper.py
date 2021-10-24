def help(update, context):
    update.message.reply_text(f'/div *ticket* - информация о дивидендах: /div aflt \n'
                              f'/trand *ticket* - тренд эмитента: /trand aflt \n'
                              f'/price *ticket*, *ticket - текущая цена бумаги эмитента: /price aflt \n'
                              f'/avg15 *ticket*, *ticket - скользящая средняя за 15 дней: /average15 aflt \n'
                              f'/avg50 *ticket*, *ticket - скользящая средняя за 50 дней: /average50 aflt \n'
                              f'/curr - текущая котировка валют: /curr \n'
                              f'/info - информация о торгуемых бумагах биржи: /info \n'
                              f'/info *ticket* - информация о конкретной бумаге: /info aflt'
                              f'/alert *ticket* *цена* — Добавить оповещение(SBER — тикер, 354.12 — цена, '
                              f'на которой придет уведомление): /alert SBER 354.12 \n'
                              f'/alert remove *ticket* — Все оповещения по указанному тикету будут удалены: '
                              f'/alert remove SBER \n'
                              f'/list - показать список всех оповещений: /list')


if __name__ == '__main__':
    pass
