

def help(update, context):
    update.message.reply_text(f'/div *ticket* - информация о дивидендах: /div aflt \n'
                              f'/trand *ticket* - тренд эмитента: /trand aflt \n'
                              f'/price *ticket* - текущая цена бумаги эмитента: /price aflt \n'
                              f'/average15 *ticket* - скользящая средняя за 15 дней: /average15 aflt \n'
                              f'/average50 *ticket* - скользящая средняя за 50 дней: /average50 aflt \n'
                              f'/info - информация о торгуемых бумагах биржи: /info')

if __name__ == '__main__':
    pass