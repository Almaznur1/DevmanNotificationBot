import requests
import os
from dotenv import load_dotenv
import logging
import time
import textwrap
from telegram import Bot


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        log_entry = log_entry[:4096]
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


logger = logging.getLogger(__file__)


def main():
    load_dotenv()
    devman_api_token = os.getenv('DEVMAN_API_TOKEN')
    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    tg_user_id = os.getenv('TG_USER_ID')

    bot = Bot(token=tg_bot_token)

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logging.info('Informational message')
    logger.addHandler(TelegramLogsHandler(bot, tg_user_id))

    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'authorization': f'Token {devman_api_token}'
    }
    timestamp = time.time()

    logger.info('Бот запущен!')
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

        except requests.exceptions.ConnectionError as error:
            logger.exception(error)
            time.sleep(10)
            continue

        except requests.exceptions.ReadTimeout as error:
            logger.exception(error)
            continue

        try:
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

                text = f'''
                Преподаватель проверил работу "{lesson_title}"
                {result_text}'''
                text = textwrap.dedent(text)

                bot.send_message(
                    chat_id=tg_user_id,
                    text=text
                )
        except Exception as error:
            logger.exception(error)


if __name__ == '__main__':
    main()
