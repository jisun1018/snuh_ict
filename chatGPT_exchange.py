import requests
import telegram
from telegram.ext import Updater, CommandHandler

# 환율 정보 API 주소
API_URL = "https://api.manana.kr/exchange/rate.json"

# 텔레그램 봇 토큰
BOT_TOKEN = "your_bot_token_here"

# 환율 정보 가져오는 함수
def get_exchange_rate(currency):
    response = requests.get(API_URL, params={"base": currency})
    data = response.json()
    exchange_rate = data["rates"]["KRW"]
    return exchange_rate

# /usd 명령어 핸들러
def usd_handler(update, context):
    exchange_rate = get_exchange_rate("USD")
    message = f"USD 환율: {exchange_rate}"
    update.message.reply_text(message)

# /eur 명령어 핸들러
def eur_handler(update, context):
    exchange_rate = get_exchange_rate("EUR")
    message = f"EUR 환율: {exchange_rate}"
    update.message.reply_text(message)

# 텔레그램 봇 생성 및 핸들러 등록
updater = Updater(BOT_TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler("usd", usd_handler))
updater.dispatcher.add_handler(CommandHandler("eur", eur_handler))

# 봇 시작
updater.start_polling()
updater.idle()