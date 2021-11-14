# FinanceBot
## Tool Setup

### Install Python dependencies

Run the following line in the terminal: `pip install -r requirements.txt`.

### Create user configuration

Create a configs/settings.py file named `settings.py` based off `settings.py.example`, 
then add your API keys and current coin.

**The configuration file consists of the following fields:**

-   **MOEX_AUTH_URL** - URL MOEX API.
-   **EMAIL** - Login to MOEX API.
-   **PASSWORD** - Password to MOEX API.
-   **BOT_API_KEY** - Telegram Bot API KEY. Go to BotFather
-   **URL_DB** - 'URL to SQLITE database file.
-   **IMAGE_PATH** - Full path to image folders.

#### Environment Variables

All of the options provided in `configs/settings.py` can also be configured using environment variables.

```
MOEX_AUTH_URL = 'https://passport.moex.com/authenticate'
EMAIL = 'example@email.com'
PASSWORD = 'PASSWORD'
BOT_API_KEY = '19423577671:AAHuqpWsIBsadasdq9QW_DtBzhcb5zBD296SbTI'
URL_DB = '/var/www/Finance_Bot'
IMAGE_PATH = '/var/www/Finance_Bot/images'
```
### Pre-requisite
```shell
python db_models.py # create sqlite database
python get_calendar.py # add to table calendar working days
```
### Run

```shell
python bot.py # run telegram bot 
python scheduler.py # run scheduler
```
