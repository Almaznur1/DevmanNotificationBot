import requests
import os
from dotenv import load_dotenv
import logging
import time
from telegram import Bot


load_dotenv()
DEVMAN_API_TOKEN = os.getenv('DEVMAN_API_TOKEN')
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
USER_TG_ID = os.getenv('USER_TG_ID')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TG_BOT_TOKEN)

url = 'https://dvmn.org/api/long_polling/'
headers = {
    'authorization': f'Token {DEVMAN_API_TOKEN}'
}
timestamp = time.time()

while True:
    params = {
        'timestamp': timestamp
    }
    try:
        response = requests.get(
            url=url,
            headers=headers,
            params=params,
            timeout=100
        )
        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        print('Возникли проблемы с сетью! Проверьте ваше соединение. '
              'Повторный запрос будет отправлен через 10 сек')
        time.sleep(10)
        continue

    except requests.exceptions.ReadTimeout:
        print('Сервер не отвечает. Отправляю повторный запрос')
        continue

    response = response.json()

    if response['status'] == 'found':
        timestamp = response['last_attempt_timestamp']
        lesson_title = response['new_attempts'][0]['lesson_title']
        lesson_url = response['new_attempts'][0]['lesson_url']

        if response['new_attempts'][0]['is_negative']:
            lesson_url = response['new_attempts'][0]['lesson_url']
            result_text = 'К сожалению, в работе нашлись ошибки.\n'\
                          f'Ссылка на ваш урок:\n{lesson_url}'
        else:
            result_text = 'Преподавателю всё понравилось,'\
                          'можно приступать к следующему уроку!'

        bot.send_message(
            chat_id=USER_TG_ID,
            text=f'Преподаватель проверил работу "{lesson_title}"\n\n'
                 f'{result_text}'
        )
