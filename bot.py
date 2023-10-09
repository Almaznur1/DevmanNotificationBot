import requests
import os
from dotenv import load_dotenv
import logging
import time
from telegram import Bot


def main():
    load_dotenv()
    devman_api_token = os.getenv('DEVMAN_API_TOKEN')
    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    tg_user_id = os.getenv('TG_USER_ID')

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    logger = logging.getLogger(__name__)

    bot = Bot(token=tg_bot_token)

    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'authorization': f'Token {devman_api_token}'
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

        reviews = response.json()

        if reviews['status'] == 'timeout':
            timestamp = reviews['timestamp_to_request']

        elif reviews['status'] == 'found':
            timestamp = reviews['last_attempt_timestamp']
            lesson_title = reviews['new_attempts'][0]['lesson_title']

            if reviews['new_attempts'][0]['is_negative']:
                lesson_url = reviews['new_attempts'][0]['lesson_url']
                result_text = f'''
К сожалению, в работе нашлись ошибки.
Ссылка на ваш урок:
{lesson_url}'''
            else:
                result_text = 'Преподавателю всё понравилось,'\
                              'можно приступать к следующему уроку!'

            bot.send_message(
                chat_id=tg_user_id,
                text=f'''
Преподаватель проверил работу "{lesson_title}"

{result_text}'''
            )


if __name__ == '__main__':
    main()
