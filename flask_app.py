# -*- coding: utf-8 -*-
from flask import Flask, request
import vk_api
from vk_api.utils import get_random_id

"""
Пример бота для группы ВКонтакте использующего
callback-api для получения сообщений.
Подробнее: https://vk.com/dev/callback_api
Перед запуском необходимо установить flask (pip install flask)
Запуск:
$ FLASK_APP=callback_bot.py flask run
При развертывании запускать с помощью gunicorn (pip install gunicorn):
$ gunicorn callback_bot:app
"""

app = Flask(__name__)
vk_session = vk_api.VkApi(token='')
vk = vk_session.get_api()

confirmation_code = '81d3d835'


@app.route('/my_bot', methods=['POST'])
def bot():
    data = request.get_json(force=True, silent=True)



    if not data or 'type' not in data:
        return 'not ok'

    if data['type'] == 'confirmation':
        return confirmation_code
    elif data['type'] == 'message_new':
        text = data['object']["text"]
        if text.lower() == "/хочусосать":
            from_id = data['object']['peer_id']
            vk.messages.send(
                message='Ну пососи!',
                random_id=get_random_id(),
                peer_id=from_id
            )
            return 'ok'

    return 'ok'
