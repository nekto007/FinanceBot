import requests, auth

def get_stock(update, context):
    auth.is_cookie_expired(auth.validation_cookie) #Проверка текущего куки на валидность
    ticket = update.message.text.split()[1]
    response = requests.get(f'https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticket}.json?iss.meta=off')
    moex_answer = response.json()
    #moex_indexes = list(moex_answer['marketdata'].values())[0]
    #moex_values = list(moex_answer['marketdata'].values())[1:]
    #for x in moex_values[0]:
    #   update.message.reply_text(f'Наименование тикета: {x[0]}, Режим торговой сессии: {x[1]}, Цена открытия: {x[9]}, Цена закрытия: {x[23]}')
    
    for x in moex_answer["marketdata"]["data"]:
        str_for_sending = (
        f'''{moex_answer["marketdata"]["columns"][0]} : {x[0]}; ''' \
        f'''{moex_answer["marketdata"]["columns"][1]} : {x[1]}; ''' \
        f'''{moex_answer["marketdata"]["columns"][9]} : {x[9]}; ''' \
        f'''{moex_answer["marketdata"]["columns"][10]} : {x[10]}; ''' \
        f'''{moex_answer["marketdata"]["columns"][11]} : {x[11]}; ''' \
        f'''{moex_answer["marketdata"]["columns"][12]} : {x[12]}. ''' \
        )

        update.message.reply_text(str_for_sending)
        

if __name__ == '__main__':
    pass