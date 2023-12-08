# Отправляем уведомления о проверке работ на Devman.org

Скрипт предназначен для отправки уведомлений о проверенных работах на курсах [Devman](https://devman.org/) через телеграм бота.

### Как установить

Python3 должен быть уже установлен.

Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
* Зарегистрируйтесь на сайте [Devman](https://devman.org/) и [получите токен](https://dvmn.org/api/docs/)
* Зарегистрируйте бота в Telegram через [BotFather](https://t.me/BotFather)
* Узнайте ваш телеграм id [@userinfobot](https://t.me/userinfobot)

Перед запуском переименуйте файл *.env.example* в *.env* и запишите в него следующие данные:

```
DEVMAN_API_TOKEN=<токен API Девмана>
TG_BOT_TOKEN=<токен вашего телеграм бота>
TG_USER_ID=<ваш телеграм id>

```

Запустите скрипт через терминал

```
python bot.py
```

### Запуск в Docker-контейнере

Для того чтобы развернуть приложение в контейнере:

* установите [Docker](https://docs.docker.com/desktop/install/linux-install/) на вашем сервере (данная сборка предназначена для unix-подобных систем)
* соберите образ контейнера:
```sh
docker build . -t dvmn_notification_bot
```
* запустите контейнер:
```sh
docker run -d --env-file ./.env dvmn_notification_bot
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).